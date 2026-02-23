# Setup Instructions

This page walks through setup from scratch.

## Option A: Use pre-built binaries (Windows)

This is the fastest path if you only need to run the app.

1. Go to the app's GitHub [releases](https://github.com/AllenNeuralDynamics/harp-updater-gui/releases) page
2. Download the latest release zip (for example `harp_updater_gui-vX.Y.Z.zip`)
3. After downloading, right-click the zip file → Properties → Unblock before extracting
4. Extract to a local folder (for example `C:\Apps\harp_updater_gui`)
5. Double-click `harp_updater_gui.exe`

Important:

- Keep the extracted folder structure intact (`harp_updater_gui.exe` + `_internal`)
- Install [Microsoft .NET 8.0 Desktop Runtime (x64)](https://dotnet.microsoft.com/en-us/download/dotnet/8.0/runtime/desktop)
- If SmartScreen appears, verify source and allow execution
- If a browser opens on `localhost` but no native window appears, install WebView2 Runtime and .NET Desktop Runtime (x64)

## Option B: Run from source

Use this option if you are developing or testing changes.

## 1) Prerequisites

- Python `>=3.11,<4.0` (3.12 recommended)
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
