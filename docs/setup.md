# Setup Instructions

This page walks through setup from scratch.

## 1) Prerequisites

- Python `>=3.9,<4.0` (3.12 recommended)
- HarpRegulator CLI installed
- USB access to your Harp devices
- `uv` package manager

## 2) Install uv

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 3) Install project dependencies

```bash
cd harp-updater-gui
uv sync
```

## 4) Configure HarpRegulator executable path

Open `src/harp_updater_gui/main.py` and verify the executable path passed to:

- `DeviceManager(...)`
- `FirmwareService(...)`

The repository currently includes a machine-specific Windows path by default.

## 5) Start the application

```bash
uv run harp-updater-gui
```

Alternative launcher:

```bash
uv run python run.py
```

## 6) Confirm startup

You should see:

- Header with app title
- Device table panel
- Activity log panel
- Footer links

If startup fails, check [Issue Reporting](issue-reporting.md) and [FAQs](faq.md).
