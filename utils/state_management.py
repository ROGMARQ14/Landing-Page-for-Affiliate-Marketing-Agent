import streamlit as st
from datetime import datetime
import json
from typing import Dict, Any, Optional

class StateManager:
    """Manages application state across workflow steps"""

    def __init__(self):
        self.default_workflow_data = {
            'project_name': '',
            'selected_model': 'gpt-4-turbo-preview',
            'current_step': 1,
            'created_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),

            # Step completion status
            'step_1_completed': False,
            'step_2_completed': False,
            'step_3_completed': False,
            'step_4_completed': False,
            'step_5_completed': False,
            'step_6_completed': False,
            'step_7_completed': False,
            'step_8_completed': False,

            # Step data storage
            'step_1_data': {},  # Product research
            'step_2_data': {},  # Landing page outline
            'step_3_data': {},  # Hero section copy
            'step_4_data': {},  # Problem-Agitate-Solution copy
            'step_5_data': {},  # Social proof & comparisons
            'step_6_data': {},  # Final CTA & roadmap
            'step_7_data': {},  # Assembly & consistency
            'step_8_data': {},  # Design & technical specs

            # Configuration options
            'options': {
                'include_agitation_module': True,
                'include_comparison_table': True,
                'include_audience_qualifier': True,
                'include_before_after_slider': False,  # Enable based on product type
                'page_type': 'affiliate',  # 'affiliate', 'direct_sales', 'saas'
                'product_type': 'supplement',  # 'supplement', 'software', 'course', 'service'
            }
        }

    def initialize_session_state(self):
        """Initialize session state with default values if not already set"""
        if 'workflow_data' not in st.session_state:
            st.session_state.workflow_data = self.default_workflow_data.copy()

        # Ensure all required keys exist (for backwards compatibility)
        for key, value in self.default_workflow_data.items():
            if key not in st.session_state.workflow_data:
                st.session_state.workflow_data[key] = value

    def mark_step_completed(self, step_number: int):
        """Mark a specific step as completed"""
        if 1 <= step_number <= 8:
            st.session_state.workflow_data[f'step_{step_number}_completed'] = True
            st.session_state.workflow_data['last_updated'] = datetime.now().isoformat()

            # Auto-advance to next step if not at the end
            if step_number < 8:
                st.session_state.workflow_data['current_step'] = step_number + 1

    def save_step_data(self, step_number: int, data: Dict[str, Any]):
        """Save data for a specific step"""
        if 1 <= step_number <= 8:
            st.session_state.workflow_data[f'step_{step_number}_data'] = data
            st.session_state.workflow_data['last_updated'] = datetime.now().isoformat()

    def get_step_data(self, step_number: int) -> Dict[str, Any]:
        """Retrieve data for a specific step"""
        if 1 <= step_number <= 8:
            return st.session_state.workflow_data.get(f'step_{step_number}_data', {})
        return {}

    def is_step_completed(self, step_number: int) -> bool:
        """Check if a specific step is completed"""
        if 1 <= step_number <= 8:
            return st.session_state.workflow_data.get(f'step_{step_number}_completed', False)
        return False

    def get_current_step(self) -> int:
        """Get the current active step"""
        return st.session_state.workflow_data.get('current_step', 1)

    def set_current_step(self, step_number: int):
        """Set the current active step"""
        if 1 <= step_number <= 8:
            st.session_state.workflow_data['current_step'] = step_number

    def get_progress_percentage(self) -> float:
        """Calculate overall workflow completion percentage"""
        completed_steps = sum([
            self.is_step_completed(i) for i in range(1, 9)
        ])
        return (completed_steps / 8) * 100

    def can_proceed_to_step(self, step_number: int) -> bool:
        """Check if user can proceed to a specific step based on prerequisites"""
        if step_number == 1:
            return True  # Can always start with step 1

        # Must complete previous steps in order
        for i in range(1, step_number):
            if not self.is_step_completed(i):
                return False
        return True

    def get_all_completed_data(self) -> Dict[str, Any]:
        """Get all data from completed steps for final assembly"""
        completed_data = {}

        for step in range(1, 9):
            if self.is_step_completed(step):
                step_data = self.get_step_data(step)
                if step_data:
                    completed_data[f'step_{step}'] = step_data

        return completed_data

    def export_project_state(self) -> str:
        """Export current project state as JSON string"""
        export_data = st.session_state.workflow_data.copy()
        export_data['exported_at'] = datetime.now().isoformat()
        return json.dumps(export_data, indent=2, default=str)

    def import_project_state(self, json_data: str) -> bool:
        """Import project state from JSON string"""
        try:
            imported_data = json.loads(json_data)

            # Validate required fields
            required_fields = ['project_name', 'current_step']
            for field in required_fields:
                if field not in imported_data:
                    return False

            # Update session state
            st.session_state.workflow_data.update(imported_data)
            st.session_state.workflow_data['last_updated'] = datetime.now().isoformat()

            return True

        except (json.JSONDecodeError, KeyError):
            return False

    def reset_workflow(self):
        """Reset entire workflow to initial state"""
        st.session_state.workflow_data = self.default_workflow_data.copy()

    def get_step_dependencies(self, step_number: int) -> Dict[str, Any]:
        """Get data dependencies for a specific step"""
        dependencies = {}

        # Step 2 needs Step 1 data
        if step_number == 2 and self.is_step_completed(1):
            dependencies['step_1'] = self.get_step_data(1)

        # Step 3 needs Steps 1-2 data
        elif step_number == 3:
            for i in range(1, 3):
                if self.is_step_completed(i):
                    dependencies[f'step_{i}'] = self.get_step_data(i)

        # Step 4 needs Steps 1-3 data (terminology consistency)
        elif step_number == 4:
            for i in range(1, 4):
                if self.is_step_completed(i):
                    dependencies[f'step_{i}'] = self.get_step_data(i)

        # And so on... each step can access previous steps' data
        elif step_number > 4:
            for i in range(1, step_number):
                if self.is_step_completed(i):
                    dependencies[f'step_{i}'] = self.get_step_data(i)

        return dependencies

    def validate_workflow_integrity(self) -> Dict[str, Any]:
        """Validate workflow data integrity and flag potential issues"""
        issues = []
        warnings = []

        # Check for missing required data
        if self.is_step_completed(1):
            step_1_data = self.get_step_data(1)
            if not step_1_data.get('product_name'):
                issues.append("Step 1: Missing product name")
            if not step_1_data.get('target_url'):
                warnings.append("Step 1: No target URL provided for research")

        # Check terminology consistency across steps
        if self.is_step_completed(2):
            step_2_data = self.get_step_data(2)
            terminology = step_2_data.get('terminology_standards', {})

            # Check if later steps use consistent terminology
            for step in range(3, 9):
                if self.is_step_completed(step):
                    step_data = self.get_step_data(step)
                    # This would need more specific validation logic
                    # based on the actual data structure

        return {
            'issues': issues,
            'warnings': warnings,
            'is_valid': len(issues) == 0
        }
