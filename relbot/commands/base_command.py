from enum import Enum
from abc import ABC, abstractmethod
from relbot.database.database_manager import DatabaseManager
from relbot.app_config import GlobalCommandConfig, GlobalAppConfig, GlobalLanguageConfig


class BaseCommand(ABC):
    def __init__(self):
        return
