# Tutorials

This section covers the core workflows in the app.

## Tutorial 1: Refresh and inspect devices

1. Connect your Harp device(s) over USB.
2. Click **Refresh** in the device table toolbar.
3. Wait for the refresh dialog to finish.
4. Use search/filter controls to locate your device.
5. Select a row to target a device for deployment.

## Tutorial 2: Deploy firmware to one device

1. Select a device row in the table.
2. Click **Browse** and select a firmware file (`.uf2` or `.hex`).
3. Optional: enable **Force upload** only when needed.
4. Click **Deploy Firmware**.
5. Follow progress in:
   - Upload dialog
   - Activity log panel
6. After completion, wait for automatic table refresh.

## Tutorial 3: Batch update by device name

1. Select one device from the target group.
2. Enable **Update all devices with same name**.
3. Select firmware file.
4. Click **Deploy Firmware**.
5. Watch per-device results in the activity log.

## Tutorial 4: Use activity logs for troubleshooting

- `ℹ` info entries show workflow steps.
- `✓` success entries confirm completed steps.
- `⚠` warning entries indicate caution or partial issues.
- `✗` error entries indicate failure and usually require action.

When reporting issues, include the relevant log excerpt and device details.
