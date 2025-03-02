from typing import Dict
from tabaka_core.config import (
    BaseLanguageConfig,
    PythonLanguageConfig,
    JavaScriptLanguageConfig,
    RustLanguageConfig,
    GoLanguageConfig,
    JavaLanguageConfig,
)
from docker.models.containers import Container
from typing import Set, Dict, Optional


class LanguageRegistry:
    def __init__(self):
        self.languages: Dict[str, BaseLanguageConfig] = {
            "python": PythonLanguageConfig(),
            "javascript": JavaScriptLanguageConfig(),
            # "rust": RustLanguageConfig(),
            # "go": GoLanguageConfig(),
            # "java": JavaLanguageConfig(),
        }

    def register_language(self, language: BaseLanguageConfig):
        self.languages[language.name] = language

    def get_language(self, name: str) -> BaseLanguageConfig:
        return self.languages.get(name)


class ContainerRegistry:
    def __init__(self):
        self.containers: Dict[str, Container] = {}
        self.available_containers: Set[str] = set()
        self.container_packages: Dict[str, Set[str]] = {}
        self.container_languages: Dict[str, str] = {}
