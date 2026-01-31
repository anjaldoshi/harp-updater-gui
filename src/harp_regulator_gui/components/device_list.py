from nicegui import ui
from typing import List, Callable, Optional
from harp_regulator_gui.services.device_manager import DeviceManager
from harp_regulator_gui.models.device import Device


class DeviceList:
    """Device list sidebar component"""
    
    def __init__(self, device_manager: DeviceManager, on_device_select: Optional[Callable] = None):
        """
        Initialize device list component
        
        Args:
            device_manager: DeviceManager instance
            on_device_select: Callback when device is selected
        """
        self.device_manager = device_manager
        self.on_device_select = on_device_select
        self.search_query = ""
        self.filter_type = "All types"
        self.selected_devices = set()
        self.device_cards = []
        
    def render(self):
        """Render the device list sidebar"""
        with ui.column().classes('sidebar-left'):
            # Search
            with ui.column().classes('device-search-container'):
                search_input = ui.input(placeholder='Search devices...').classes('input-field')
                search_input.on_value_change(lambda e: self.on_search_change(e.value))
            
            # Filter
            with ui.column().classes('device-filter-container'):
                filter_select = ui.select(
                    options=['All types', 'Pico', 'ATxmega', 'Healthy', 'Needs update', 'Error'],
                    value='All types',
                    on_change=lambda e: self.on_filter_change(e.value)
                ).classes('select-field')
                
                ui.button('🔄 Check for updates', on_click=self.refresh_devices).classes('btn btn-primary btn-full mt-2')
            
            # Device list (scrollable)
            self.device_list_container = ui.column().classes('device-list-container overflow-y-auto')
            
        # Initial load
        self.refresh_devices()
    
    def refresh_devices(self):
        """Refresh device list from device manager"""
        ui.notify('Checking for devices...', type='info')
        try:
            devices = self.device_manager.refresh_devices()
            self.update_device_list()
            ui.notify(f'Found {len(devices)} device(s)', type='positive')
        except Exception as e:
            ui.notify(f'Error: {str(e)}', type='negative')
    
    def update_device_list(self):
        """Update the displayed device list"""
        # Clear existing cards
        self.device_list_container.clear()
        
        # Get filtered devices
        devices = self.device_manager.filter_devices(
            search_query=self.search_query,
            device_type=self.filter_type
        )
        
        # Render device cards
        with self.device_list_container:
            for device in devices:
                self.render_device_card(device)
    
    def render_device_card(self, device: Device):
        """Render a single device card"""
        # Determine status badge class
        status_class = 'healthy'
        if device.health_color == 'yellow':
            status_class = 'warning'
        elif device.health_color == 'red':
            status_class = 'error'
        
        is_selected = device.port_name in self.selected_devices
        card_class = 'device-card selected' if is_selected else 'device-card'
        
        with ui.card().classes(card_class).on('click', lambda d=device: self.select_device(d)):
            with ui.row().classes('device-card-header'):
                ui.label(device.display_name).classes('device-name')
                ui.label(device.health_status).classes(f'device-status-badge {status_class}')
            
            ui.label(device.metadata_line).classes('device-metadata')
    
    def select_device(self, device: Device):
        """Handle device selection"""
        # Update selected devices set
        self.selected_devices.clear()
        self.selected_devices.add(device.port_name)
        
        # Re-render the device list to update visual selection
        self.update_device_list()
        
        # Call the selection callback
        self.device_manager.select_device(device)
        if self.on_device_select:
            self.on_device_select(device)
        ui.notify(f'Selected: {device.display_name}', type='info')
    
    def toggle_device_selection(self, device: Device, selected: bool):
        """Toggle device in multi-select"""
        if selected:
            self.selected_devices.add(device.port_name)
        else:
            self.selected_devices.discard(device.port_name)
    
    def on_search_change(self, query: str):
        """Handle search query change"""
        self.search_query = query
        self.update_device_list()
    
    def on_filter_change(self, filter_type: str):
        """Handle filter type change"""
        self.filter_type = filter_type
        self.update_device_list()