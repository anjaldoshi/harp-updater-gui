# FAQs

## Why does firmware file validation fail?

Common causes:

- File does not exist
- Unsupported extension (must be `.uf2` or `.hex`)
- Device/file mismatch:
  - Pico requires `.uf2`
  - ATxmega requires `.hex`

## Why are no devices shown after refresh?

- Check USB cable/power
- Reconnect device and retry
- Enable **Connect all** and refresh again
- On Windows, install drivers with:

```bash
HarpRegulator install-drivers
```

## Why does upload fail on a device in use?

Ports can be held by another process. Close tools that may be using the device serial port, then retry.

## When should I use Force upload?

Only when normal upload fails due to compatibility/safety checks and you understand the risk.

## Where can I get more help?

- [Issue Reporting](issue-reporting.md)
- GitHub repository: https://github.com/yourusername/harp-updater-gui
