# HARP Firmware Updater GUI - Current Implementation

## Overview

This document reflects the repository as it exists today. The app is a NiceGUI-based native desktop UI that wraps HarpRegulator CLI operations for device discovery and firmware deployment.

## Architecture

### Entry and Runtime

- `run.py` starts `harp_updater_gui.main:start_app`
- `main.py` configures theme, static CSS injection, and `ui.run(...)`
- Runtime settings currently use:
  - `native=True`
  - `port=4277`
  - `reload=False`
- Module boot guard uses `if __name__ == "__main__":` (not `__mp_main__`) to avoid Windows multiprocessing worker reinitialization.

### UI Composition

`HarpFirmwareUpdaterApp.render()` builds:

1. `Header` (title, host label, dark-mode toggle)
2. Main splitter layout:
   - Left pane: `DeviceTable`
   - Right pane: `UpdateWorkflow` activity log
3. Footer with documentation link

### Core Components

#### `components/device_table.py`

- Search + filter controls
- Refresh button and modal refresh dialog (`Refreshing devices...`)
- Optional `Connect all` behavior for refresh
- Quasar table with single-row selection
- Firmware upload section:
  - file browse
  - batch-update-by-name checkbox
  - force upload checkbox
  - deploy button
- Asynchronous refresh via `run.io_bound(...)`

#### `components/update_workflow.py`

- Log panel using `ui.log`
- Log levels: info/success/warning/error/debug
- Error dialogs for failed uploads and force-upload guidance

#### `components/header.py`

- App icon/title
- Host machine label
- Dark mode toggle button with icon state updates

## Services and Models

### `services/cli_wrapper.py`

Subprocess wrapper around HarpRegulator CLI:
- `list_devices()`
- `inspect_firmware()`
- `upload_firmware()`
- `install_drivers()`

### `services/device_manager.py`

- Device list refresh/parsing
- In-memory device selection/filtering
- Upload helper that maps Pico bootloader uploads to `PICOBOOT`

### `services/firmware_service.py`

- Firmware inspection with cache
- Extension/type detection
- Device-kind compatibility checks
- Placeholder methods for remote firmware catalog/download

### Models

- `models/device.py`: Pydantic model with HarpRegulator field aliases and health/display helpers
- `models/firmware.py`: firmware metadata model

## Firmware Deploy Flow (Implemented)

`on_firmware_deploy(...)` in `main.py`:

1. Opens deploy loading dialog
2. Logs workflow start
3. Validates firmware file
4. Refreshes devices once with `allow_connect=False` to release handles
5. Uploads firmware (single or batch)
6. Logs success/fail per device
7. Refreshes device table (shows refresh dialog)
8. Closes loading dialog

## Tests

- `tests/test_device_manager.py`
- `tests/test_firmware_service.py`

These cover service/model behavior; UI interaction tests are not present.

## Known Constraints

1. `main.py` currently uses a machine-specific Windows path to `HarpRegulator.exe`
2. Firmware repository download methods are placeholders
3. UI is desktop-native by default; browser-first workflow is not the primary target

## Directory Snapshot

```
src/harp_updater_gui/
├── main.py
├── components/
│   ├── header.py
│   ├── device_table.py
│   └── update_workflow.py
├── models/
│   ├── device.py
│   └── firmware.py
├── services/
│   ├── cli_wrapper.py
│   ├── device_manager.py
│   └── firmware_service.py
├── static/
│   └── styles.css
└── utils/
    └── constants.py
```
