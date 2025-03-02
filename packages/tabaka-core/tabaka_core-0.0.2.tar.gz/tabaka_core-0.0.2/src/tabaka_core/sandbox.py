import os
import sys
from typing import Optional, Set, Dict, List
import docker
from docker.types import Mount
from docker.models.containers import Container
import threading
import time
from pathlib import Path
import logging
from contextlib import contextmanager
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from tabaka_core.pathutil import secure_path
from tabaka_core import models
from tabaka_core.config import TabakaConfig, BaseLanguageConfig
from tabaka_core.registry import LanguageRegistry, ContainerRegistry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tabaka-core")


class Tabaka:
    def __init__(
        self,
        config: Optional[TabakaConfig] = None,
        **kwargs,
    ):
        self.config = config or TabakaConfig(**kwargs)

        self.docker_client = docker.from_env()
        self.startup_commands = []
        self.startup_commands.extend(self.config.custom_startup_commands)

        self._lock = threading.Lock()
        self.logger = logger
        self.language_registry: LanguageRegistry = LanguageRegistry()
        self.container_registry: ContainerRegistry = ContainerRegistry()

        if self.check_if_running():
            self.build_registry_from_running_containers()
        else:
            self.ensure_vfs()
            self._initialize_pool()

    def check_if_running(self) -> bool:
        # find docker container with name prefix
        for container in self.docker_client.containers.list(all=True):
            if container.name.startswith(self.config.container_name_prefix):
                return True
        return False

    def build_registry_from_running_containers(self) -> None:
        for container in self.docker_client.containers.list(all=True):
            if container.name.startswith(self.config.container_name_prefix):
                language_id = container.name.split("-")[2]
                self.container_registry.container_languages[container.id] = language_id
                self.container_registry.containers[container.id] = container
                self.container_registry.available_containers.add(container.id)
                self.container_registry.container_packages[container.id] = set()

    def _initialize_pool(self) -> None:
        try:
            self.logger.debug("Initializing container pool")
            self._cleanup_old_containers()
            for i in range(self.config.pool_size):
                for (
                    language_id,
                    language_config,
                ) in self.language_registry.languages.items():
                    if language_id not in self.config.allowed_languages:
                        continue
                    container = self._create_container(
                        f"{self.config.container_name_prefix}-{language_id}-{i}",
                        language_config,
                    )
                    self.container_registry.containers[container.id] = container
                    self.container_registry.available_containers.add(container.id)
                    self.container_registry.container_packages[container.id] = set()
                    self.container_registry.container_languages[container.id] = (
                        language_id
                    )
        except Exception as e:
            self.logger.error(f"Failed to initialize container pool: {e}")
            raise

    def _cleanup_old_containers(self) -> None:
        """Remove any existing sandbox containers"""
        for container in self.docker_client.containers.list(all=True):
            if container.name.startswith(self.config.container_name_prefix):
                try:
                    container.remove(force=True)
                except Exception as e:
                    self.logger.warning(
                        f"Failed to remove container {container.id}: {e}"
                    )

    def _create_container(
        self, name: str, language_config: BaseLanguageConfig
    ) -> Container:
        """Create a new sandbox container"""
        volumes = {}
        mounts = []  # For volume mounts
        working_dir = "/sandbox"

        if self.config.filesystem.mode != "disabled":
            fs_mode = self.config.filesystem.mode

            if fs_mode == "host":
                # Map host directory to container - this WILL create a path on your computer
                host_path = os.path.abspath(self.config.filesystem.host_mount_path)
                os.makedirs(host_path, exist_ok=True)  # Ensure it exists
                volumes[host_path] = {
                    "bind": "/sandbox",
                    "mode": "rw",
                }

            elif fs_mode == "shared":
                # Use a shared Docker volume for all containers - NO path on your computer
                volume_name = (
                    f"{self.config.filesystem.vfs_container_name_prefix}-shared"
                )
                self._ensure_volume_exists(volume_name)

                # Use the mount parameter for Docker volumes
                mounts.append(
                    Mount(
                        target="/sandbox",
                        source=volume_name,
                        type="volume",
                        read_only=False,
                    )
                )

            elif fs_mode == "container":
                # Each container gets its own Docker volume - NO path on your computer
                container_id = name.replace(self.config.container_name_prefix, "")
                volume_name = f"{self.config.filesystem.vfs_container_name_prefix}-container-{container_id}"
                self._ensure_volume_exists(volume_name)

                # Use the mount parameter for Docker volumes
                mounts.append(
                    Mount(
                        target="/sandbox",
                        source=volume_name,
                        type="volume",
                        read_only=False,
                    )
                )

            elif fs_mode == "session":
                # Session mode - not implemented yet
                raise NotImplementedError(
                    "Session filesystem mode is not yet implemented"
                )
        else:
            # Filesystem disabled
            working_dir = "/tmp"

        # Add custom allowed paths
        for path in self.config.filesystem.allowed_paths:
            abs_path = os.path.abspath(path)
            if os.path.exists(abs_path):
                volumes[abs_path] = {
                    "bind": f"/mnt/{os.path.basename(path)}",
                    "mode": "ro",
                }

        container_args = {
            "image": language_config.base_image,
            "name": name,
            "command": "tail -f /dev/null",
            "detach": True,
            "mem_limit": language_config.resources.memory_limit,
            "nano_cpus": int(language_config.resources.cpu_limit * 1e9),
            "working_dir": working_dir,
            "remove": True,
            "network_mode": self.config.network_mode,
            "security_opt": self.config.security.security_opts,
            "cap_drop": self.config.security.drop_capabilities,
            "read_only": self.config.security.read_only_root,
        }

        if mounts:
            container_args["mounts"] = mounts
        if volumes:
            container_args["volumes"] = volumes

        container = self.docker_client.containers.run(**container_args)

        if self.startup_commands:
            for command in self.startup_commands:
                try:
                    self.logger.debug(
                        f"Running startup command: {command} in container {container.id}"
                    )
                    exit_code, output = container.exec_run(command, demux=True)
                    if exit_code != 0:
                        self.logger.warning(
                            f"Startup command '{command}' failed with exit code {exit_code} in container {container.id}: {output}"
                        )
                    else:
                        self.logger.debug(
                            f"Startup command '{command}' succeeded in container {container.id}"
                        )
                except Exception as e:
                    self.logger.error(
                        f"Failed to run startup command '{command}' in container {container.id}: {e}"
                    )

        return container

    @contextmanager
    def get_sandbox(
        self, language_id: str, required_packages: Optional[Set[str]] = None
    ) -> Container:  # type: ignore
        """Get a sandbox container with required packages installed"""
        self.logger.debug(
            f"Acquiring sandbox container with required packages: {required_packages}"
        )
        container_id = None
        try:
            container_id = self._acquire_container(
                language_id, required_packages or set()
            )
            yield self.container_registry.containers[container_id]
        finally:
            if container_id:
                for container in self.container_registry.containers.values():
                    if container.id == container_id:
                        if (
                            container_id
                            not in self.container_registry.available_containers
                        ):
                            self._release_container(container_id)

    def ensure_vfs(self) -> None:
        fs_mode = self.config.filesystem.mode
        self.logger.debug(f"Setting up VFS in {fs_mode} mode")

        try:
            if fs_mode == "disabled":
                ...

            elif fs_mode == "host":
                host_path = os.path.abspath(self.config.filesystem.host_mount_path)
                if not os.path.exists(host_path):
                    self.logger.debug(
                        f"Creating host filesystem directory: {host_path}"
                    )
                    os.makedirs(host_path, exist_ok=True)

            elif fs_mode == "shared":
                volume_name = (
                    f"{self.config.filesystem.vfs_container_name_prefix}-shared"
                )
                self._ensure_volume_exists(volume_name)
                self.logger.debug(f"Using shared Docker volume: {volume_name}")

            elif fs_mode == "container":
                ...

            elif fs_mode == "session":
                raise NotImplementedError(
                    "Session filesystem mode is scheduled for a future release"
                )

            else:
                raise ValueError(f"Invalid filesystem mode: {fs_mode}")

        except Exception as e:
            self.logger.error(f"Failed to set up VFS: {e}")
            raise

    def _ensure_volume_exists(self, volume_name: str) -> None:
        """Helper method to ensure a Docker volume exists"""
        try:
            try:
                self.docker_client.volumes.get(volume_name)
                self.logger.debug(f"Docker volume already exists: {volume_name}")
            except docker.errors.NotFound:
                self.docker_client.volumes.create(volume_name)
                self.logger.debug(f"Created Docker volume: {volume_name}")
        except Exception as e:
            self.logger.error(f"Failed to ensure volume {volume_name}: {e}")
            raise

    def _acquire_container(
        self,
        language_id: str,
        required_packages: Set[str],
    ) -> str:
        """Acquire a container with required packages"""
        # Convert required_packages to set if it's a list
        if isinstance(required_packages, list):
            required_packages = set(required_packages)

        with self._lock:
            # Find container with most matching packages
            best_container_id = None
            min_missing_packages = float("inf")

            for container_id in self.container_registry.available_containers:
                if (
                    self.container_registry.container_languages[container_id]
                    != language_id
                ):
                    continue
                installed_packages = self.container_registry.container_packages[
                    container_id
                ]
                missing_packages = len(required_packages - installed_packages)
                if missing_packages < min_missing_packages:
                    best_container_id = container_id
                    min_missing_packages = missing_packages

            if not best_container_id:
                # Wait for a container to be available
                self.logger.error("No available containers, waiting for 3 seconds")
                time.sleep(3)
                return self._acquire_container(language_id, required_packages)

            # Install missing packages
            missing_packages = (
                required_packages
                - self.container_registry.container_packages[best_container_id]
            )

            if missing_packages:
                self._install_packages(best_container_id, missing_packages)

            self.logger.debug(
                f"Acquired container {best_container_id} with missing packages: {missing_packages}"
            )

            return best_container_id

    def _release_container(self, container_id: str) -> None:
        """Release container back to pool"""
        with self._lock:
            self.container_registry.available_containers.add(container_id)

    def _install_packages(self, container_id: str, packages: Set[str]) -> None:
        """Install packages in container"""
        container = self.container_registry.containers[container_id]
        for package in packages:
            if package in sys.stdlib_module_names:
                self.logger.debug(f"Skipping standard library package: {package}")
                continue
            try:
                exit_code, output = container.exec_run(
                    f"pip install --no-cache-dir '{package}'", demux=True
                )
                if exit_code != 0:
                    raise RuntimeError(f"Failed to install {package}: {output}")
                self.container_registry.container_packages[container_id].add(package)
            except Exception as e:
                self.logger.error(f"Package installation failed: {e}")
                raise

    def _kill_and_recreate_container(self, container_id: str) -> None:
        """Kill a container and recreate it with the same ID"""
        with self._lock:
            try:
                # Get the container name before removing it
                container = self.container_registry.containers[container_id]
                container_name = container.name

                # Remove from available containers if it's there
                if container_id in self.container_registry.available_containers:
                    self.container_registry.available_containers.remove(container_id)

                # Kill and remove the container
                self.logger.warning(f"Killing container {container_id} due to timeout")
                container.remove(force=True)

                # Create a new container with the same name
                new_container = self._create_container(container_name)

                # Update our records
                self.container_registry.available_containers[new_container.id] = (
                    new_container
                )
                self.container_registry.available_containers.add(new_container.id)
                self.container_registry.container_packages[new_container.id] = set()
                self.container_registry.container_languages[new_container.id] = (
                    self.container_registry.container_languages[container_id]
                )

                # Clean up old container records
                if container_id != new_container.id:
                    if container_id in self.container_registry.containers:
                        del self.container_registry.containers[container_id]
                    if container_id in self.container_registry.container_packages:
                        del self.container_registry.container_packages[container_id]
                    if container_id in self.container_registry.container_languages:
                        del self.container_registry.container_languages[container_id]

                self.logger.debug(
                    f"Recreated container {container_id} as {new_container.id}"
                )

            except Exception as e:
                self.logger.error(
                    f"Failed to kill and recreate container {container_id}: {e}"
                )
                # Try to ensure the container is in the available pool even if recreation failed
                if (
                    container_id in self.container_registry.containers
                    and container_id not in self.container_registry.available_containers
                ):
                    self.container_registry.available_containers.add(container_id)

    def execute_code(
        self,
        code: str,
        language_id: str,
        required_packages: Optional[Set[str]] = None,
        timeout: Optional[int] = 180,
    ) -> models.CodeExecutionResult:
        """Execute code in a sandbox container

        Args:
            code: The Python code to execute
            required_packages: Packages to install before execution
            timeout: Maximum execution time in seconds

        Returns:
            The output of the code execution

        Raises:
            RuntimeError: If execution fails or times out
        """
        self.logger.debug(f"Executing code in sandbox with timeout {timeout}s")
        container_id = None
        start_time = time.time()
        duration = 0
        with self.get_sandbox(language_id, required_packages) as container:
            container_id = container.id

            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(
                    container.exec_run,
                    [
                        self.language_registry.get_language(
                            language_id
                        ).execution.entrypoint,
                        *self.language_registry.get_language(
                            language_id
                        ).execution.args,
                        code,
                    ],
                    demux=True,
                    stderr=True,
                )

                try:
                    exit_code, output = future.result(timeout=timeout)
                    stdout, stderr = output
                    err = ""
                    if stderr:
                        err = stderr.decode()
                    if exit_code != 0:
                        self.logger.error(f"Execution failed: {err}")

                    duration = time.time() - start_time

                    return models.CodeExecutionResult(
                        stdout=stdout.decode() if stdout else "",
                        stderr=err,
                        exit_code=exit_code,
                        duration=duration,
                        memory_usage=0,
                    )
                except concurrent.futures.TimeoutError:
                    self.logger.error(f"Execution timed out after {timeout}s")
                    # Cancel the future (this won't stop the container process)
                    future.cancel()

                    # We need to kill and recreate the container since the process is stuck
                    if container_id:
                        # Call _kill_and_recreate_container synchronously
                        self._kill_and_recreate_container(container_id)

                    return models.CodeExecutionResult(
                        stdout="",
                        stderr=f"Execution timed out after {timeout}s",
                        exit_code=1,
                        duration=timeout,
                        memory_usage=0,
                    )

    def cleanup(self) -> None:
        """Stop all containers"""
        for container in self.container_registry.containers.values():
            try:
                container.remove(force=True)
            except Exception as e:
                self.logger.warning(f"Failed to remove container {container.id}: {e}")


if __name__ == "__main__":
    container_name_prefix = "tabaka-sandbox-test-"
    sandbox = Tabaka()  # Example startup command
    #     result = sandbox.execute_code(
    #         """
    # import time
    # print("Hello, World!")
    # print("Hello, World!")
    #         """,
    #         timeout=5,
    #     )
    # print(result)
    vfs_test_code = """
#write to a file
with open("test.txt", "w") as f:
    f.write("Hello, World!")
"""
    vfs_result = sandbox.execute_code(
        vfs_test_code,
        language_id="python",
        timeout=10,
    )
    print("\nVFS Test Result:\n", vfs_result)

    vfs_test_code_2 = """
#read the file test.txt
print(open("test.txt").read())
    """
    vfs_result_2 = sandbox.execute_code(
        vfs_test_code_2,
        language_id="python",
        timeout=10,
    )
    print("\nVFS Test Result 2:\n", vfs_result_2)

    result = sandbox.execute_code(
        """
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(np.random.randint(1, 100))
print(np.__version__)
print(pd.__version__)
    """,
        language_id="python",
        timeout=10,
        required_packages=["pandas", "numpy", "matplotlib"],
    )
    print("\nResult:\n", result)
    # import os
    sandbox.cleanup()
