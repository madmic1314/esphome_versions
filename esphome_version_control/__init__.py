import logging
import os
import shutil
from datetime import datetime

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

DOMAIN = "esphome_version_control"

# Path to ESPHome YAML files
ESPHOME_FOLDER = "/config/esphome"

# Path to store backups
VERSION_FOLDER = "/config/esphome_versions"

# Maximum number of versions per device
MAX_VERSIONS = 10


class ESPHomeFileHandler(FileSystemEventHandler):
    """Handle file events for ESPHome YAML files."""

    def on_modified(self, event):
        self._handle_event(event)

    def on_created(self, event):
        self._handle_event(event)

    def on_moved(self, event):
        if not event.is_directory and event.dest_path.endswith(".yaml"):
            self._backup_file(event.dest_path)

    def _handle_event(self, event):
        if not event.is_directory and event.src_path.endswith(".yaml"):
            self._backup_file(event.src_path)

    def _backup_file(self, filepath):
        """Copy YAML file to timestamped folder and prune old versions."""
        try:
            if not os.path.exists(filepath):
                return

            filename = os.path.basename(filepath)
            device_name = os.path.splitext(filename)[0]

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            target_dir = os.path.join(VERSION_FOLDER, device_name, timestamp)
            os.makedirs(target_dir, exist_ok=True)

            shutil.copy2(filepath, os.path.join(target_dir, filename))

            _LOGGER.info(
                "ESPHome VC: Backed up %s to %s", filename, target_dir
            )

            # --- Prune old versions ---
            device_dir = os.path.join(VERSION_FOLDER, device_name)
            versions = sorted(
                [d for d in os.listdir(device_dir) if os.path.isdir(os.path.join(device_dir, d))]
            )

            while len(versions) > MAX_VERSIONS:
                oldest = versions.pop(0)
                shutil.rmtree(os.path.join(device_dir, oldest))
                _LOGGER.info(
                    "ESPHome VC: Removed old version %s for device %s",
                    oldest,
                    device_name,
                )

        except Exception as e:
            _LOGGER.error("ESPHome VC backup failed: %s", e)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up ESPHome Version Control."""

    _LOGGER.info("Starting ESPHome Version Control")

    os.makedirs(VERSION_FOLDER, exist_ok=True)

    event_handler = ESPHomeFileHandler()
    observer = Observer()
    observer.schedule(event_handler, ESPHOME_FOLDER, recursive=False)
    observer.start()

    # Stop observer when Home Assistant stops
    def stop_observer(event):
        _LOGGER.info("Stopping ESPHome Version Control")
        observer.stop()
        observer.join()

    hass.bus.async_listen_once("homeassistant_stop", stop_observer)

    return True

