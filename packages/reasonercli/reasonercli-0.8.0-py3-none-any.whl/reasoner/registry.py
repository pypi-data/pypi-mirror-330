from typing import Any, List, Optional
from weakref import WeakSet

_INSTALLED_SDK_VERSION = None

_REASONER_CLIENT_INSTANCES = WeakSet()

_LAST_CHECKED_FOR_UPDATES = None

def get_installed_sdk_version() -> str:
    global _INSTALLED_SDK_VERSION
    return _INSTALLED_SDK_VERSION

def set_installed_sdk_version(version: str):
    global _INSTALLED_SDK_VERSION

    if not _INSTALLED_SDK_VERSION:
        _INSTALLED_SDK_VERSION = version

def register_reasoner_instance(instance):
    global _REASONER_CLIENT_INSTANCES
    _REASONER_CLIENT_INSTANCES.add(instance)

def get_reasoner_instances() -> List[Any]:
    global _REASONER_CLIENT_INSTANCES
    return list(_REASONER_CLIENT_INSTANCES)

def get_last_checked_for_updates() -> Optional[float]:
    global _LAST_CHECKED_FOR_UPDATES
    return _LAST_CHECKED_FOR_UPDATES

def set_last_checked_for_updates(timestamp: float):
    global _LAST_CHECKED_FOR_UPDATES
    _LAST_CHECKED_FOR_UPDATES = timestamp