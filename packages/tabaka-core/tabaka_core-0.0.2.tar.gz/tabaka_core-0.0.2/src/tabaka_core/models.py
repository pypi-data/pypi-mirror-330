from pydantic import BaseModel

ALLOWED_BASE_DIR = ".tabaka/vfs"


class SandboxConfig(BaseModel):
    pool_size: int = 1
    max_memory: str = "4g"
    cpu_limit: float = 1.0


class CodeExecutionResult(BaseModel):
    stdout: str
    stderr: str
    exit_code: int
    duration: float
    memory_usage: float
