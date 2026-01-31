from nicegui import ui
from typing import Optional, Callable
from pathlib import Path
from harp_regulator_gui.models.device import Device
from harp_regulator_gui.services.firmware_service import FirmwareService


class FirmwareBrowser:
    """Firmware browser panel component"""
    
    def __init__(self, firmware_service: FirmwareService, on_deploy: Optional[Callable] = None):
        """
        Initialize firmware browser
        
        Args:
            firmware_service: FirmwareService instance
            on_deploy: Callback when firmware deployment is initiated
        """
        self.firmware_service = firmware_service
        self.on_deploy = on_deploy
        self.selected_device: Optional[Device] = None
        self.firmware_file_path: Optional[str] = None
        self.firmware_info: Optional[dict] = None
        
        self.device_name_label = None
        self.firmware_info_container = None
        self.firmware_select = None
        self.deploy_button = None
    
    def render(self):
        """Render the firmware browser panel"""
        with ui.element('div').classes('firmware-browser-container'):
            # Device summary section
            with ui.column().classes('firmware-section'):
                with ui.row().classes('section-header'):
                    ui.label('Selected Device').classes('section-title')
                
                with ui.card().classes('summary-card'):
                    with ui.column().classes('gap-2'):
                        self.device_name_label = ui.label('No device selected').classes('device-name')
                        self.hardware_label = ui.label('Hardware: -').classes('device-metadata')
                        self.current_firmware_label = ui.label('Current firmware: -').classes('device-metadata')
                        self.device_type_label = ui.label('Device type: -').classes('device-metadata')
            
            # Firmware selection section
            with ui.column().classes('firmware-section'):
                with ui.row().classes('section-header'):
                    ui.label('Select Firmware').classes('section-title')
                
                with ui.column().classes('gap-3'):
                    # File picker for local firmware
                    with ui.row().classes('gap-2 items-center'):
                        ui.button('📁 Browse local firmware', on_click=self.browse_firmware).classes('btn btn-secondary')
                        self.file_path_label = ui.label('No file selected').classes('text-sm text-secondary')
                    
                    # Or select from available versions
                    self.firmware_select = ui.select(
                        options=[],
                        label='Or select from repository',
                        with_input=False
                    ).classes('select-field')
                    self.firmware_select.on('change', lambda e: self.on_firmware_version_select(e.value))
                
                # Firmware info
                self.firmware_info_container = ui.column().classes('gap-2 mt-3')
            
            # Actions
            with ui.row().classes('firmware-actions gap-2 mt-4'):
                ui.button('⬇️ Download firmware', on_click=self.download_firmware).classes('btn btn-secondary')
                self.deploy_button = ui.button('🚀 Deploy firmware', on_click=self.deploy_firmware).classes('btn btn-primary')
                self.deploy_button.set_enabled(False)
    
    def update_device(self, device: Optional[Device]):
        """
        Update the displayed device information
        
        Args:
            device: Selected device
        """
        self.selected_device = device
        
        if device:
            self.device_name_label.set_text(device.display_name)
            self.hardware_label.set_text(f'Hardware: v{device.hardware_version or "Unknown"}')
            self.current_firmware_label.set_text(f'Current firmware: v{device.firmware_version or "Unknown"}')
            self.device_type_label.set_text(f'Device type: {device.kind}')
            
            # Load available firmware versions (placeholder)
            available_versions = self.firmware_service.get_available_firmware_versions(device.display_name)
            self.firmware_select.set_options(available_versions)
        else:
            self.device_name_label.set_text('No device selected')
            self.hardware_label.set_text('Hardware: -')
            self.current_firmware_label.set_text('Current firmware: -')
            self.device_type_label.set_text('Device type: -')
            self.firmware_select.set_options([])
    
    async def browse_firmware(self):
        """Open file picker to browse for firmware file"""
        # NiceGUI file upload
        result = await ui.run_javascript('''
            new Promise((resolve) => {
                const input = document.createElement('input');
                input.type = 'file';
                input.accept = '.uf2,.hex';
                input.onchange = (e) => {
                    const file = e.target.files[0];
                    if (file) {
                        resolve(file.name);
                    } else {
                        resolve(null);
                    }
                };
                input.click();
            })
        ''')
        
        if result:
            self.file_path_label.set_text(result)
            # In a real implementation, you'd handle the actual file upload here
            ui.notify(f'Selected: {result}', type='info')
    
    def on_firmware_version_select(self, version: str):
        """Handle firmware version selection"""
        if version:
            ui.notify(f'Selected firmware version: {version}', type='info')
            # Would load firmware info here
            self.deploy_button.set_enabled(True)
    
    def download_firmware(self):
        """Download firmware from repository"""
        if not self.selected_device:
            ui.notify('Please select a device first', type='warning')
            return
        
        ui.notify('Firmware download not yet implemented', type='info')
    
    def deploy_firmware(self):
        """Deploy firmware to device"""
        if not self.selected_device:
            ui.notify('Please select a device first', type='warning')
            return
        
        if not self.firmware_file_path and not self.firmware_select.value:
            ui.notify('Please select a firmware file or version', type='warning')
            return
        
        if self.on_deploy:
            self.on_deploy(self.selected_device, self.firmware_file_path or self.firmware_select.value)
        
        ui.notify(f'Deploying firmware to {self.selected_device.display_name}...', type='positive')