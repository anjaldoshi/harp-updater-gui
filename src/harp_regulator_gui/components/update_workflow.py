from nicegui import ui
from typing import List, Dict
from datetime import datetime


class UpdateWorkflow:
    """Update workflow panel component"""
    
    def __init__(self):
        """Initialize update workflow component"""
        self.steps = [
            {'id': 'validate', 'state': 'pending', 'text': 'Validating', 'meta': 'Pending'},
            {'id': 'flash', 'state': 'pending', 'text': 'Flashing', 'meta': 'Pending'},
            {'id': 'verify', 'state': 'pending', 'text': 'Verifying', 'meta': 'Pending'},
        ]
        self.log_messages: List[str] = []
        self.current_progress = 0
        self.is_running = False
        self.has_error = False
        self.error_message = ""
        
        # UI elements
        self.step_elements = {}
        self.log_container = None
        self.progress_bar = None
        self.progress_label = None
        self.alert_container = None
    
    def render(self):
        """Render the update workflow panel"""
        with ui.column().classes('sidebar-right workflow-container'):
            # Workflow title
            ui.label('Update Workflow').classes('workflow-title')
            
            # Progress section
            with ui.column().classes('workflow-section'):
                ui.label('Status').classes('workflow-title text-sm')
                
                # Steps
                with ui.column().classes('progress-container'):
                    for step in self.steps:
                        self.render_step(step)
                
                # Progress bar
                with ui.column().classes('gap-2 mt-3'):
                    self.progress_label = ui.label('Progress: 0%').classes('text-sm font-semibold')
                    self.progress_bar = ui.linear_progress(value=0).classes('w-full')
            
            # Log section
            with ui.column().classes('workflow-section'):
                ui.label('Activity Log').classes('workflow-title text-sm')
                self.log_container = ui.column().classes('activity-log')
                self.add_log('Waiting for update to start...')
            
            # Alert container (initially hidden)
            self.alert_container = ui.column().classes('hidden')
    
    def render_step(self, step: Dict):
        """Render a single workflow step"""
        state_class_map = {
            'pending': 'pending',
            'running': 'active',
            'completed': 'completed',
            'error': 'pending',
        }
        step_class = state_class_map.get(step['state'], 'pending')
        
        with ui.row().classes(f'progress-step {step_class}'):
            # State icon (bullet point)
            icon_class = f'progress-step-icon {step_class}'
            state_icon = ui.label('•').classes(icon_class)
            
            # Step text
            with ui.column().classes(''):
                text_label = ui.label(step['text']).classes('progress-step-text font-medium')
                meta_label = ui.label(step['meta']).classes('progress-step-text text-secondary text-xs')
            
            # Store references for updates
            self.step_elements[step['id']] = {
                'icon': state_icon,
                'meta': meta_label,
                'text': text_label
            }
    
    def start_update(self, device_name: str, firmware_version: str):
        """
        Start an update workflow
        
        Args:
            device_name: Name of device being updated
            firmware_version: Firmware version being installed
        """
        self.is_running = True
        self.has_error = False
        self.current_progress = 0
        self.log_messages = []
        
        self.add_log(f'Starting firmware update for {device_name}')
        self.add_log(f'Target firmware version: {firmware_version}')
        
        # Reset steps
        for step in self.steps:
            step['state'] = 'pending'
            step['meta'] = 'Pending'
        
        self.update_step('validate', 'running', 'In progress')
        self.set_progress(10)
    
    def update_step(self, step_id: str, state: str, meta: str):
        """
        Update a workflow step
        
        Args:
            step_id: Step identifier
            state: New state (pending, running, completed, error)
            meta: Status text
        """
        # Find and update step
        for step in self.steps:
            if step['id'] == step_id:
                step['state'] = state
                step['meta'] = meta
                break
        
        # Update UI (would need to re-render in actual implementation)
        # For now, just log it
        self.add_log(f'Step {step_id}: {meta}')
    
    def add_log(self, message: str):
        """
        Add a log message
        
        Args:
            message: Log message text
        """
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = f'[{timestamp}] {message}'
        self.log_messages.append(log_entry)
        
        # Update UI
        if self.log_container:
            with self.log_container:
                ui.label(log_entry).classes('text-xs')
    
    def set_progress(self, percentage: int):
        """
        Set progress percentage
        
        Args:
            percentage: Progress percentage (0-100)
        """
        self.current_progress = percentage
        if self.progress_bar:
            self.progress_bar.set_value(percentage / 100)
        if self.progress_label:
            self.progress_label.set_text(f'Progress: {percentage}%')
    
    def show_error(self, error_message: str):
        """
        Show an error alert
        
        Args:
            error_message: Error message text
        """
        self.has_error = True
        self.error_message = error_message
        
        # Show alert
        if self.alert_container:
            self.alert_container.clear()
            self.alert_container.classes(remove='hidden')
            
            with self.alert_container:
                with ui.card().classes('p-3 bg-red-50 border border-red-200'):
                    ui.label(error_message).classes('text-red-900 text-sm')
                    with ui.row().classes('gap-2 mt-2'):
                        ui.button('Retry', on_click=self.on_retry).classes(
                            'bg-white border hover:bg-gray-50'
                        )
                        ui.button('Rollback', on_click=self.on_rollback).classes(
                            'bg-white border hover:bg-gray-50'
                        )
    
    def hide_error(self):
        """Hide error alert"""
        self.has_error = False
        if self.alert_container:
            self.alert_container.classes(add='hidden')
    
    def on_retry(self):
        """Handle retry button click"""
        self.hide_error()
        self.add_log('Retrying update...')
        ui.notify('Retrying update', type='info')
    
    def on_rollback(self):
        """Handle rollback button click"""
        self.hide_error()
        self.add_log('Rolling back to previous firmware...')
        ui.notify('Rolling back firmware', type='warning')
    
    def complete_update(self, success: bool):
        """
        Complete the update workflow
        
        Args:
            success: Whether update completed successfully
        """
        self.is_running = False
        
        if success:
            self.update_step('verify', 'completed', 'Completed')
            self.set_progress(100)
            self.add_log('✓ Firmware update completed successfully!')
            ui.notify('Firmware update completed!', type='positive')
        else:
            self.show_error('Firmware update failed. Please check the logs and try again.')