#!/usr/bin/env python3
"""
HARP Firmware Updater GUI

A graphical user interface for managing Harp devices and updating firmware.
Built with NiceGUI and integrating with the HarpRegulator CLI tool.
"""

import os
import sys
from pathlib import Path
from nicegui import ui, app
from harp_regulator_gui.components.header import Header
from harp_regulator_gui.components.device_list import DeviceList
from harp_regulator_gui.components.firmware_browser import FirmwareBrowser
from harp_regulator_gui.components.update_workflow import UpdateWorkflow
from harp_regulator_gui.services.device_manager import DeviceManager
from harp_regulator_gui.services.firmware_service import FirmwareService
from harp_regulator_gui.models.device import Device

# Get the path to the static directory
STATIC_DIR = Path(__file__).parent / 'static'


class HarpFirmwareUpdaterApp:
    """Main application class"""
    
    def __init__(self):
        """Initialize the application"""
        # Initialize services
        self.device_manager = DeviceManager("C:\\Users\\anjal\\Projects\\aind\\harp-regulator\\artifacts\\bin\\HarpRegulator\\debug\\HarpRegulator.exe")
        self.firmware_service = FirmwareService("C:\\Users\\anjal\\Projects\\aind\\harp-regulator\\artifacts\\bin\\HarpRegulator\\debug\\HarpRegulator.exe")
        
        # Initialize components (will be set in render)
        self.header = None
        self.device_list = None
        self.firmware_browser = None
        self.update_workflow = None
    
    def on_device_select(self, device: Device):
        """
        Handle device selection
        
        Args:
            device: Selected device
        """
        self.firmware_browser.update_device(device)
    
    def on_firmware_deploy(self, device: Device, firmware_path: str):
        """
        Handle firmware deployment
        
        Args:
            device: Target device
            firmware_path: Path to firmware file or version string
        """
        # Start update workflow
        self.update_workflow.start_update(device.display_name, firmware_path)
        
        # Simulate update progress (in real implementation, this would monitor the actual upload)
        self.update_workflow.update_step('validate', 'running', 'In progress')
        self.update_workflow.add_log(f'Validating firmware for {device.display_name}...')
        self.update_workflow.set_progress(25)
        
        # Here you would actually call the device_manager to upload firmware
        # success, output = self.device_manager.upload_firmware_to_device(device, firmware_path)
        
        # For now, just show an info message
        ui.notify(f'Firmware deployment to {device.display_name} would happen here', type='info')
    
    def render(self):
        """Render the main application UI"""
        # Configure NiceGUI color theme
        ui.colors(
            primary='#2563eb',      # Blue for primary actions
            secondary='#6b7280',    # Gray for secondary elements
            accent='#7c3aed',       # Purple accent
            positive='#10b981',     # Green for success states
            negative='#ef4444',     # Red for errors
            info='#06b6d4',         # Cyan for info
            warning='#f59e0b',      # Orange for warnings
        )
        
        # Create dark mode toggle
        dark_mode = ui.dark_mode()
        
        # Create header with dark mode toggle
        self.header = Header(dark_mode_toggle=dark_mode)
        
        # Main content area with 3-column layout
        with ui.row().classes('app-container w-full flex-1'):
            # Left: Device List
            self.device_list = DeviceList(
                device_manager=self.device_manager,
                on_device_select=self.on_device_select
            )
            self.device_list.render()
            
            # Center: Firmware Browser (flexible width)
            self.firmware_browser = FirmwareBrowser(
                firmware_service=self.firmware_service,
                on_deploy=self.on_firmware_deploy
            )
            self.firmware_browser.render()
            
            # Right: Update Workflow
            self.update_workflow = UpdateWorkflow()
            self.update_workflow.render()
        
        # Footer
        with ui.footer().classes('footer-container'):
            with ui.row().classes('w-full items-center justify-between'):
                ui.label('© 2025 Allen Institute').classes('text-sm')
                ui.link('Help and Documentation', 'https://github.com/harp-tech/protocol', new_tab=True).classes('footer-link')


def start_app():
    """Initialize and start the application."""
    # Ensure NiceGUI error pages can locate the running script when launched via entrypoints
    sys.argv[0] = str(Path(__file__).resolve())

    # Add static files directory
    app.add_static_files('/static', str(STATIC_DIR))
    
    # Load custom CSS
    css_path = STATIC_DIR / 'styles.css'
    if css_path.exists():
        with open(css_path, 'r', encoding='utf-8') as f:
            ui.add_head_html(f'<style>{f.read()}</style>')

    # Create app instance and render UI
    app_instance = HarpFirmwareUpdaterApp()
    app_instance.render()

    # Run the application
    ui.run(
        title='HARP Regulator GUI',
        favicon='🔧',
        host="0.0.0.0",
        port=4277,
        dark=None,  # Start in auto mode (respects system preference)
        reload=False,
        show=True
    )


# Start the app if running as a module
if __name__ in {"__main__", "__mp_main__"}:
    start_app()
