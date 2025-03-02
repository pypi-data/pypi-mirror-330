from typing import Dict, Optional, List, Any, Literal
from pydantic import BaseModel, field_validator, Field


class FilesystemConfig(BaseModel):
    """Configuration for filesystem handling"""

    mode: Literal["disabled", "container", "session", "shared", "host"] = Field(
        default="shared",
        description="How filesystem is managed: disabled (no fs), container (per container), session (per session), shared (across all), host (on host)",
    )

    persistence: bool = Field(
        default=False,
        description="Whether filesystem changes persist between executions",
    )

    # For external_vfs mode
    vfs_container_name_prefix: Optional[str] = Field(
        default="tabaka-vfs",
        description="Name of the external VFS container",
    )

    host_mount_path: str = Field(
        default="./.tabaka/vfs",
        description="Path where host is mounted in the container",
    )

    allowed_paths: List[str] = Field(
        default_factory=list,
        description="Additional paths to make available in the container",
    )


class SecurityConfig(BaseModel):
    """Security configuration for a language runtime"""

    allowed_capabilities: List[str] = Field(default_factory=list)
    drop_capabilities: List[str] = Field(
        default=["ALL"], description="Capabilities to drop"
    )
    read_only_root: bool = Field(
        default=False, description="Whether to mount the root filesystem as read-only"
    )
    network_enabled: bool = Field(
        default=True, description="Whether to enable network access"
    )
    allow_privilege_escalation: bool = Field(
        default=False, description="Whether to allow privilege escalation"
    )
    security_opts: List[str] = Field(
        default=[
            "no-new-privileges",
            "apparmor=docker-default",
        ],
        description="Security options for the container",
    )


class TabakaConfig(BaseModel):
    filesystem: FilesystemConfig = Field(default_factory=FilesystemConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)

    pool_size: int = Field(
        default=1, description="Number of containers to maintain in the pool"
    )

    # Security Features
    security_profile: str = Field(
        default="default", description="Security profile (default, strict, permissive)"
    )

    allow_network_access: bool = Field(
        default=True, description="Allow containers to access the network"
    )

    # Experimental Features (marked with comments)
    enable_gpu: bool = Field(
        default=False,
        description="Enable GPU access in containers (experimental)",  # Experimental feature
    )

    enable_persistent_sessions: bool = Field(
        default=False,
        description="Allow sessions to persist between executions (experimental)",  # Experimental feature
    )

    enable_container_commit: bool = Field(
        default=False,
        description="Allow committing container state for future reuse (experimental)",  # Experimental feature
    )

    enable_multi_tenancy: bool = Field(
        default=False,
        description="Enable multi-tenant mode with stricter isolation (experimental)",  # Experimental feature
    )

    multi_language_support: bool = Field(
        default=False,
        description="Enable support for multiple programming languages (experimental)",  # Experimental feature
    )

    allowed_languages: List[str] = Field(
        default=["python"],
        # Experimental
        # when multi_language_support is enabled,
        # allowed_languages will be used to determine which languages to load
        # if not set, no languages will be loaded
        description="List of allowed languages (experimental)",
    )

    advanced_networking: Dict[str, Any] = Field(
        default_factory=dict,
        description="Advanced networking configuration (experimental)",  # Experimental feature
    )

    resource_monitoring: bool = Field(
        default=False,
        description="Enable detailed resource monitoring (experimental)",  # Experimental feature
    )

    custom_startup_commands: List[str] = Field(
        default_factory=list,
        description="Custom commands to run when initializing containers",
    )

    network_mode: str = Field(
        default="host",
        description="Network mode for containers",
    )

    container_name_prefix: str = Field(
        default="tabaka-sandbox",
        description="Prefix for container names",
    )

    auto_remove: bool = Field(
        default=True,
        description="Automatically remove containers when they exit",
    )

    ipc_mode: str = Field(
        default="host",
        description="IPC mode for containers",
        examples=[
            "host",
            "private",
            "shareable",
        ],
    )

    pid_mode: str = Field(
        default="host",
        description="PID mode for containers",
        examples=[
            "host",
        ],
    )

    labels: Dict[str, str] = Field(
        default_factory=dict,
        description="Labels for containers",
    )

    idle_timeout: int = Field(
        default=300,
        description="Idle timeout for containers in seconds, after which the container will be stopped",
    )


class EnvironmentConfig(BaseModel):
    """Environment configuration for a language runtime"""

    env_vars: Dict[str, str] = Field(default_factory=dict)
    working_dir: str = "/workspace"
    user: Optional[str] = None


class ResourceLimits(BaseModel):
    """Resource limits for container execution"""

    memory_limit: str = Field(default="4g", description="Memory limit for containers")
    cpu_limit: float = Field(default=2.0, description="CPU limit for containers")
    max_file_size: int = Field(
        default=10 * 1024 * 1024, description="Maximum file size for containers"
    )
    max_processes: Optional[int] = Field(
        default=None, description="Maximum number of processes for containers"
    )


class ExecutionConfig(BaseModel):
    """Execution configuration for a language runtime"""

    entrypoint: str = Field(default=..., description="Entrypoint for the language")
    args: List[str] = Field(
        default_factory=list, description="Arguments for the entrypoint"
    )
    timeout_default: int = Field(
        default=300, description="Default timeout for code execution in seconds"
    )
    require_file_saving: bool = Field(
        default=False, description="Whether to save files to the filesystem"
    )


class BaseLanguageConfig(BaseModel):
    id: str
    name: str
    version: str
    base_image: str
    description: Optional[str] = None
    custom_startup_commands: List[str] = Field(default_factory=list)

    environment: EnvironmentConfig = Field(default_factory=EnvironmentConfig)
    resources: ResourceLimits = Field(default_factory=ResourceLimits)
    execution: ExecutionConfig = Field(default_factory=ExecutionConfig)


class PythonLanguageConfig(BaseLanguageConfig):
    """Python language configuration"""

    id: str = "python"
    name: str = "Python"
    version: str = "3.11"
    base_image: str = "python:3.11-slim"
    description: str = "Python programming language runtime"
    custom_startup_commands: List[str] = Field(default_factory=list)

    resources: ResourceLimits = Field(default_factory=ResourceLimits)
    environment: EnvironmentConfig = Field(default_factory=EnvironmentConfig)
    execution: ExecutionConfig = ExecutionConfig(
        entrypoint="python",
        args=[
            "-c",
        ],
    )


class JavaScriptLanguageConfig(BaseLanguageConfig):
    """JavaScript language configuration"""

    id: str = "javascript"
    name: str = "JavaScript"
    version: str = "18"
    base_image: str = "node:18-slim"
    description: str = "JavaScript programming language runtime"
    custom_startup_commands: List[str] = Field(default_factory=list)

    resources: ResourceLimits = Field(default_factory=ResourceLimits)
    environment: EnvironmentConfig = Field(default_factory=EnvironmentConfig)
    execution: ExecutionConfig = ExecutionConfig(
        entrypoint="node",
        args=[
            "-e",
        ],
    )


class RustLanguageConfig(BaseLanguageConfig):
    """Rust language configuration"""

    id: str = "rust"
    name: str = "Rust"
    version: str = "1.79.0"
    base_image: str = "rust:1.79.0-slim"
    description: str = "Rust programming language runtime"
    custom_startup_commands: List[str] = Field(default_factory=list)

    resources: ResourceLimits = Field(default_factory=ResourceLimits)
    environment: EnvironmentConfig = Field(default_factory=EnvironmentConfig)
    execution: ExecutionConfig = ExecutionConfig(
        entrypoint="rustc",
        args=["-c", "$TABAKA_CODE"],
    )


class GoLanguageConfig(BaseLanguageConfig):
    """Go language configuration"""

    id: str = "go"
    name: str = "Go"
    version: str = "1.22.3"
    base_image: str = "golang:1.22.3-slim"
    description: str = "Go programming language runtime"
    custom_startup_commands: List[str] = Field(default_factory=list)

    resources: ResourceLimits = Field(default_factory=ResourceLimits)
    environment: EnvironmentConfig = Field(default_factory=EnvironmentConfig)
    execution: ExecutionConfig = Field(default_factory=ExecutionConfig)


class JavaLanguageConfig(BaseLanguageConfig):
    """Java language configuration"""

    id: str = "java"
    name: str = "Java"
    version: str = "17"
    base_image: str = "openjdk:17-slim"
    description: str = "Java programming language runtime"
    custom_startup_commands: List[str] = Field(default_factory=list)

    resources: ResourceLimits = Field(default_factory=ResourceLimits)
    environment: EnvironmentConfig = Field(default_factory=EnvironmentConfig)
    execution: ExecutionConfig = Field(default_factory=ExecutionConfig)
