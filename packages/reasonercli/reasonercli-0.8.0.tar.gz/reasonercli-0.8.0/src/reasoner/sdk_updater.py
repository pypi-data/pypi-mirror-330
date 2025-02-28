import httpx
import platform
import socket
import re
import sysconfig
import tarfile
import tempfile
import time
import uuid
import sys
import os
import io
import subprocess
import logging
import importlib
import importlib.metadata
import importlib.util
from types import ModuleType
from typing import Any, List, Optional, TypedDict, Set, Union
import zipfile

logger = logging.getLogger(__name__)

DIST_INFO_PATTERN = re.compile(r"reasonercli-([\d\.]+)\.dist-info")
WHEEL_PATTERN = re.compile(r"reasonercli-([\d\.]+)-py3-none-any\.whl$")

class SystemInfo(TypedDict):
    is_pip_installed: bool
    is_disk_writable: bool
    has_exec: bool
    platform_name: str
    platform_release: str
    platform_version: str
    architecture: str
    hostname: str
    ip_address: str
    mac_address: str
    processor: str
    language: str
    language_version: str
    reasoner_sdk_version: str

class SDKUpdateRequest(TypedDict):
    system_info: SystemInfo

class SDKUpdateResponse(TypedDict):
    latest_version: str
    target_version: str
    package_url: str
    should_update: bool
    package_manager_target_location: Optional[str]


class SDKUpdater:
    def __init__(self, client, base_url, reasoner_instance):
        self.client = client
        self.base_url = base_url
        self.reasoner_instance = reasoner_instance

    def get_latest_version(self, system_info: SystemInfo) -> SDKUpdateResponse:
        request_data = SDKUpdateRequest(system_info=system_info)
        response = self.client.post(f"{self.base_url}/public/v1/version/sdk", json=request_data)
        response.raise_for_status()
        return SDKUpdateResponse(**response.json())

    def check_for_updates(self) -> None:
        now = time.time()
        from .registry import get_installed_sdk_version
      
        try:
            system_info = collect_system_info()
            system_info["reasoner_installed_sdk_version"] = get_installed_sdk_version()
            sdk_update_response = self.get_latest_version(system_info)
            _try_sdk_version_update(system_info, sdk_update_response)
        except Exception as e:
            logger.error(f"Error checking for updates: {e}")
        finally:
            self.reasoner_instance.update_last_checked_for_updates(now)


class SDKUpdaterAsync:
    def __init__(self, client, base_url, async_reasoner_instance):
        self.client = client
        self.base_url = base_url
        self.reasoner_instance = async_reasoner_instance

    async def get_latest_version(self, system_info: SystemInfo) -> SDKUpdateResponse:
        request_data = SDKUpdateRequest(system_info=system_info)
        response = await self.client.post(f"{self.base_url}/public/v1/version/sdk", json=request_data)
        response.raise_for_status()
        return SDKUpdateResponse(**response.json())

    async def check_for_updates(self) -> None:
        now = time.time()
        from .registry import get_installed_sdk_version

        try:
            system_info = collect_system_info()
            system_info["reasoner_installed_sdk_version"] = get_installed_sdk_version()
            sdk_update_response = await self.get_latest_version(system_info)
            _try_sdk_version_update(system_info, sdk_update_response)
        except Exception as e:
            logger.error(f"Error checking for updates: {e}")
        finally:
            self.reasoner_instance.update_last_checked_for_updates(now)


def _try_sdk_version_update(system_info: SystemInfo, sdk_update_response: SDKUpdateResponse) -> bool:    
    from .registry import get_reasoner_instances
    instances = get_reasoner_instances()
    
    latest_available_version = sdk_update_response["latest_version"]
    current_runtime_version = system_info["reasoner_runtime_sdk_version"]
    
    if latest_available_version and latest_available_version != current_runtime_version:
        logger.info(
            f"Detected SDK version {current_runtime_version}. Latest SDK version is {latest_available_version}. Please update to the latest version by running `pip install --upgrade reasonercli`."
        )

    if not sdk_update_response["should_update"]:
        logger.debug("No auto update is available. Skipping SDK version update.")
        return False

    if system_info["is_pip_installed"] and system_info["is_site_packages_writable"] and sdk_update_response["package_manager_target_location"]:
        logger.debug("Detected pip is installed and disk is writable. Attempting to install the latest version of the Reasoner SDK via pip.")
        try:
            reinstall_from_pip(sdk_update_response["package_manager_target_location"], instances or [])
            return True
        except Exception as e:
            logger.debug(f"Failed to install the latest version of the Reasoner SDK via pip. Reason: {e}")
    else:
        logger.debug("Skipping SDK version update via pip because the disk is not writable or pip is not installed.")
    
    if system_info["is_site_packages_writable"]:
        try:
            logger.debug("Detected site packages is writable. Attempting to patch files from the latest version of the Reasoner SDK.")
            patch_files_from_remote(sdk_update_response["package_url"], instances or [])
            return True
        except Exception as e:
            logger.debug(f"Failed to install the latest version of the Reasoner SDK via disk patching. Reason: {e}")
    else:
        logger.debug("Skipping SDK version update via disk patching because the disk is not writable.")
    
    if system_info["is_temp_dir_writable"]:
        try:
            logger.debug("Detected temp dir is writable. Attempting to install the latest version of the Reasoner SDK via via disk patching.")
            patch_files_from_temp(sdk_update_response["package_url"], instances or [])
            return True
        except Exception as e:
            logger.debug(f"Failed to install the latest version of the Reasoner SDK via disk patching. Reason: {e}")
    else:
        logger.debug("Skipping SDK version update via disk patching because the temp dir is not writable.")
    
    if system_info["has_exec"]:
        try:
            logger.debug("Detected exec is available. Attempting to install the latest version of the Reasoner SDK via via module patching.")
            patch_module_from_memory(sdk_update_response["package_url"], instances or [])
            return True
        except Exception as e:
            logger.debug(f"Failed to install the latest version of the Reasoner SDK via module patching. Reason: {e}")
    else:
        logger.debug("Skipping SDK version update via module patching because exec is not available.")

    return False


def collect_system_info():
    is_pip_installed = importlib.util.find_spec("pip") is not None
    is_site_packages_writable = os.access(sysconfig.get_paths()["purelib"], os.W_OK) 
    is_temp_dir_writable = os.access(tempfile.gettempdir(), os.W_OK)
    has_exec = __builtins__.get("exec") and callable(__builtins__.get("exec"))
    
    language = "python"
    python_version = sys.version_info
    python_major_version = python_version.major
    python_minor_version = python_version.minor
    python_micro_version = python_version.micro
    language_version = f"{python_major_version}.{python_minor_version}.{python_micro_version}"
    
    platform_name = platform.system()
    platform_release = platform.release()
    platform_version = platform.version()
    architecture = platform.machine()
    hostname = socket.gethostname()
    ip_address = None
    mac_address = mac_address =':'.join(re.findall('..', '%012x' % uuid.getnode()))
    processor = platform.processor()

    errors = []

    try:
        hostname = socket.gethostname()
    except Exception as e:
        errors.append(f"Failed to get hostname. Reason {e}.")

    try:
        ip_address = socket.gethostbyname(socket.gethostname())
    except Exception as e:
        errors.append(f"Failed to get ip_address. Reason {e}.")

    try:
        reasoner_runtime_sdk_version = importlib.metadata.version("reasonercli")
    except Exception as e:
        errors.append(f"Failed to get installed runtime sdk version: {e}")

    if errors:
        logger.warning("Could not collect the following system information: " + ", ".join(errors))

    return SystemInfo(
        is_pip_installed=is_pip_installed,
        is_site_packages_writable=is_site_packages_writable,
        is_temp_dir_writable=is_temp_dir_writable,
        has_exec=has_exec,
        platform_name=platform_name,
        platform_release=platform_release,
        platform_version=platform_version,
        architecture=architecture,
        hostname=hostname,
        ip_address=ip_address,
        mac_address=mac_address,
        processor=processor,
        language=language,
        language_version=language_version,
        reasoner_runtime_sdk_version=reasoner_runtime_sdk_version,
        # installed sdk version is inferred based on the version of the first reasoner client at startup 
        reasoner_installed_sdk_version=None,
    )

def reinstall_from_pip(target_version: str, instances):
    # Reinstalls a target version of the Reasoner SDK via pip.
    # This method make type hinting available to IDEs.
    install_target_version(target_version)
    hot_reload("reasoner")

    for instance in list(instances):
        update_class(instance)

def patch_files_from_temp(package_url: str, instances):
    # Adds a new sys path so that module files are loaded from the latest version.
    # This is primarily a runtime patching operation and does not make type hinting available to IDEs.
    file_suffix = package_url.replace('/', '_')
    
    temp_dir_path = tempfile.gettempdir()

    # attempt to clean up old temp files
    try:
        for f in os.listdir(temp_dir_path):
            if f.endswith(file_suffix):
                os.remove(os.path.join(temp_dir_path, f))
    except:
        logger.debug(f"Failed to clean up old temp files in {temp_dir_path} with file suffix {file_suffix}")

    r = httpx.get(package_url, timeout=20)

    temp_file_name = None
    
    with tempfile.NamedTemporaryFile(delete=False, mode="w+b", suffix=f"-{file_suffix}") as temp_file:
        temp_file.write(r.content)
        temp_file_name = temp_file.name # can't reference name in windows while file is open

    for sys_path in reversed(sys.path):
        if WHEEL_PATTERN.search(sys_path):
            sys.path.remove(sys_path)
    
    if temp_file_name:
        sys.path.insert(0, temp_file_name)

    if sys.modules.get("reasoner"):
        hot_reload("reasoner")

        # overwrite modules that are already cached - this is danger mode, best to only use in ephemeral contexts
        _overwrite_cached_sys_modules("reasoner")
    

    for instance in list(instances):
        update_class(instance)

def patch_files_from_remote(package_url: str, instances):
    # Patches files from remote can to site-packages. This method can result in partial updates,
    # so it is important that the patched individual files do not have hard dependencies on other patched files 
    # This method make type hinting available to IDEs.
    patch_path = os.path.abspath(os.path.join(os.path.dirname(__file__ ), '..'))
    
    archive = None
    
    if package_url.startswith("http"):
        r = httpx.get(package_url, timeout=20)
        archive = retrieve_archive(r.content, package_url)
    else:
        with io.open(package_url, mode="rb") as f:
            archive = retrieve_archive(f.read(), package_url)

    if not archive:
        logger.error(f"Failed to retrieve archive from {package_url}")
        return

    for relative_file_path in archive.namelist():
        # don't patch the dist-info folder, not sure of the implications
        if DIST_INFO_PATTERN.search(relative_file_path):
            continue
        
        # guard against matching arbitrary files outside of reasoner namespace
        if not relative_file_path.startswith("reasoner"):
            continue

        overwrite_path = os.path.join(patch_path, relative_file_path)
        with io.open(overwrite_path, "rb") as f:
            old_contents = f.read()

            try:
                with io.open(overwrite_path, "wb") as f:
                    f.write(archive.open(relative_file_path).read())
            except Exception as e:
                logger.error(f"Error writing to {overwrite_path}: {e}")
                with io.open(overwrite_path, "wb") as f:
                    f.write(old_contents)

    hot_reload("reasoner")

    for instance in list(instances):
        update_class(instance)

def patch_module_from_memory(package_url: str, instances):
    # Adds a new meta_path so that reasoner files are loaded from a remote source, entirely in memory.
    # This is primarily a runtime patching operation and does not make type hinting available to IDEs.

    import httpimport

    httpimport.add_remote_repo(package_url)
    # current behavior is that httpimport adds to the sys.meta_path at the end of the list
    # the problem is that the built-in loader will resolve the `reasoner` module first, so we 
    # need to remove the httpimport importer and insert it at the front of the list so that it is used instead
    if sys.meta_path[-1].__class__.__name__ == "HttpImporter":
        sys.meta_path.insert(0, sys.meta_path.pop())

    # overwrite modules that are already cached - this is danger mode, best to only use in ephemeral contexts
    if sys.modules.get("reasoner"):
        _overwrite_cached_sys_modules("reasoner")

    for instance in list(instances):
        update_class(instance)
        
def install_target_version(version: str):
    subprocess.run(["pip", "install", "--upgrade", "-q", "-q", "-q", version])
    
def hot_reload(mod: str):
    reload_recursive(sys.modules[mod], reload_external_modules=False, exclude_modules=["reasoner.registry"])

def reload_recursive(module: ModuleType, reload_external_modules: bool = False, exclude_modules: List[str] = []):
    """
    Recursively reload a module (in order of dependence).

    Parameters
    ----------
    module : ModuleType or str
        The module to reload.

    reload_external_modules : bool, optional

        Whether to reload all referenced modules, including external ones which
        aren't submodules of ``module``.

    exclude_modules : List[str], optional
        A list of modules to exclude from reloading.
    """
    _reload(module, reload_external_modules, set(), exclude_modules)

def _reload(module: Union[ModuleType, str], reload_all: bool, reloaded: Set[str], exclude_modules: List[str]):
    if isinstance(module, ModuleType):
        module_name = module.__name__
    elif isinstance(module, str):
        module_name, module = module, importlib.import_module(module)

    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        check = (
            # is it a module?
            isinstance(attr, ModuleType)

            # has it already been reloaded?
            and attr.__name__ not in reloaded

            and attr.__name__ not in exclude_modules

            # is it a proper submodule? (or just reload all)
            and (reload_all or attr.__name__.startswith(module_name))
        )
        if check:
            _reload(attr, reload_all, reloaded, exclude_modules)

    logger.debug(f"reloading module: {module.__name__}")
    importlib.reload(module)
    reloaded.add(module_name)

def update_class(inst: Any):
    cls=getattr(inst, '__class__')
    mod_name = getattr(inst, '__module__')
    mod = importlib.import_module(mod_name, cls.__name__)
    setattr(inst, '__class__', getattr(mod, cls.__name__))
    return inst

def retrieve_archive(content, url):
    """ Returns an ZipFile or tarfile Archive object if available

    Args:
        content (bytes): Bytes (typically HTTP Response body) to be parsed as archive

    Returns:
        object: zipfile.ZipFile, tarfile.TarFile or None (if `contents` could not be parsed)

    Adapted from httpimporter.py
    """
    content_io = io.BytesIO(content)
    try:
        tar = tarfile.open(fileobj=content_io, mode='r:*')
        return tar
    except tarfile.ReadError:
        logger.debug("[*] URL: '%s' is not a (compressed) tarball" % url)
        pass
    try:
        zip_ = zipfile.ZipFile(content_io)
        logger.debug("[+] URL: '%s' is a ZIP file" % url)
        return zip_
    except zipfile.BadZipfile:
        logger.debug("[*] Response of '%s' is not a ZIP file" % url)
        pass

    return None

def _overwrite_cached_sys_modules(module_name: str):
    # This should only be called for the reasoner module in order to force the loading a submodules
    # from a new destination after they have already been cached from an old destination and they are different.
    # Note: it requires that the packaged module is flat and does not have submodules of submodules.
    for attr_name in dir(sys.modules[module_name]):
        attr = getattr(sys.modules[module_name], attr_name)
        if isinstance(attr, ModuleType) and attr.__name__.startswith(module_name):
            del sys.modules[attr.__name__]
            sys.modules[attr.__name__] = importlib.import_module(attr.__name__)
