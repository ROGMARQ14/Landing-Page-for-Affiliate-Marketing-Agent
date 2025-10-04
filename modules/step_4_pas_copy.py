import streamlit as st
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional

# Import with error handling
try:
    from ai_providers.ai_manager import AIManager
    from utils.state_management import StateManager
except ImportError as e:
    st.error(f"Module import error: {str(e)}")

class PASModule:
    """Step 4: Problem-Agitate-Solution Copy Generator"""

    def __init__(self):
        try:
            self.ai_manager = AIManager()
            self.state_manager = StateManager()
        except Exception as e:
            st.error(f"Error initializing PASModule: {str(e)}")
            self.ai_manager = None
            self.state_manager = None

    def render(self):
        """Render Step 4 UI"""
        st.markdown("# 📝 Step 4: Problem-Agitate-Solution Copy")
        st.markdown("*Generate compelling PAS copy that converts*")

        st.progress(4/8, text="Step 4 of 8")

        if not self.state_manager:
            st.error("❌ State management not available")
            return

        if not self.state_manager.is_step_completed(3):
            st.warning("⚠️ Please complete Step 3 first")
            return

        if self.state_manager.is_step_completed(4):
            self._show_completed_summary()
            if st.button("🔄 Regenerate PAS Copy"):
                self._reset_step()
                st.rerun()
            return

        # Simple form for PAS generation
        with st.form("pas_form"):
            st.markdown("## 📝 PAS Configuration")

            col1, col2 = st.columns(2)

            with col1:
                agitation_style = st.selectbox(
                    "Agitation Style",
                    ["Strong", "Medium", "Gentle"],
                    index=1
                )

                problem_focus = st.selectbox(
                    "Problem Focus",
                    ["Pain Points", "Frustrations", "Challenges"],
                    index=0
                )

            with col2:
                solution_emphasis = st.selectbox(
                    "Solution Emphasis", 
                    ["Benefits", "Features", "Results"],
                    index=0
                )

                urgency_level = st.slider(
                    "Urgency Level",
                    min_value=1, max_value=5, value=3
                )

            submitted = st.form_submit_button("📝 Generate PAS Copy", type="primary")

        if submitted:
            self._generate_pas_copy({
                'agitation_style': agitation_style,
                'problem_focus': problem_focus,
                'solution_emphasis': solution_emphasis,
                'urgency_level': urgency_level
            })

    def _generate_pas_copy(self, config: Dict[str, Any]):
        """Generate PAS copy"""

        if not self.ai_manager or not self.state_manager:
            st.error("❌ Required services not available")
            return

        with st.spinner("📝 Generating PAS copy..."):

            # Get previous step data
            try:
                step_1_data = self.state_manager.get_step_data(1)
                step_2_data = self.state_manager.get_step_data(2)
                step_3_data = self.state_manager.get_step_data(3)
            except Exception as e:
                st.error(f"Error getting previous data: {str(e)}")
                return

            # Create simple PAS structure (no AI needed for now)
            pas_data = self._create_simple_pas_structure(config)

            # Save the data
            try:
                self.state_manager.save_step_data(4, {
                    'pas_copy': pas_data,
                    'configuration': config,
                    'generated_at': datetime.now().isoformat()
                })
                self.state_manager.mark_step_completed(4)

                st.success("✅ PAS copy generated successfully!")
                time.sleep(1)
                st.rerun()

            except Exception as e:
                st.error(f"❌ Error saving PAS data: {str(e)}")

    def _create_simple_pas_structure(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a simple PAS structure without AI"""

        pas_data = {
            'problem_section': {
                'headline': 'Are You Struggling With This Common Problem?',
                'description': 'Many people face this challenge every day. You are not alone in feeling frustrated and looking for a real solution.',
                'pain_points': [
                    'Feeling stuck with current options',
                    'Wasting time on ineffective methods',
                    'Not seeing the results you want'
                ]
            },
            'agitation_section': {
                'headline': 'What Happens If You Do Nothing?',
                'consequences': [
                    'The problem continues to get worse',
                    'You waste more time and money',
                    'Opportunities slip away',
                    'Frustration keeps building'
                ],
                'style': config.get('agitation_style', 'Medium')
            },
            'solution_section': {
                'headline': 'Finally, A Solution That Actually Works',
                'description': 'Our proven approach addresses the root cause and delivers real results.',
                'benefits': [
                    'Get results quickly and effectively',
                    'Save time with our proven method',
                    'Feel confident in your choice',
                    'Enjoy lasting transformation'
                ],
                'emphasis': config.get('solution_emphasis', 'Benefits')
            },
            'configuration': config
        }

        return pas_data

    def _show_completed_summary(self):
        """Show completed PAS summary"""

        if not self.state_manager:
            return

        st.success("✅ **Step 4 Complete** - PAS copy generated!")

        step_data = self.state_manager.get_step_data(4)
        pas_data = step_data.get('pas_copy', {})
        config = step_data.get('configuration', {})

        # Show basic metrics
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Agitation Style", config.get('agitation_style', 'N/A'))
        with col2:
            st.metric("Problem Focus", config.get('problem_focus', 'N/A'))
        with col3:
            st.metric("Solution Emphasis", config.get('solution_emphasis', 'N/A'))

        # Show PAS sections
        with st.expander("📖 Preview PAS Copy"):

            # Problem section
            problem_section = pas_data.get('problem_section', {})
            st.markdown("### 🔍 Problem Section")
            st.write(f"**Headline:** {problem_section.get('headline', 'N/A')}")
            st.write(f"**Description:** {problem_section.get('description', 'N/A')}")

            pain_points = problem_section.get('pain_points', [])
            if pain_points:
                st.write("**Pain Points:**")
                for point in pain_points:
                    st.write(f"• {point}")

            # Agitation section
            agitation_section = pas_data.get('agitation_section', {})
            st.markdown("### 🔥 Agitation Section")
            st.write(f"**Headline:** {agitation_section.get('headline', 'N/A')}")

            consequences = agitation_section.get('consequences', [])
            if consequences:
                st.write("**Consequences:**")
                for consequence in consequences:
                    st.write(f"• {consequence}")

            # Solution section
            solution_section = pas_data.get('solution_section', {})
            st.markdown("### ✅ Solution Section")
            st.write(f"**Headline:** {solution_section.get('headline', 'N/A')}")
            st.write(f"**Description:** {solution_section.get('description', 'N/A')}")

            benefits = solution_section.get('benefits', [])
            if benefits:
                st.write("**Benefits:**")
                for benefit in benefits:
                    st.write(f"• {benefit}")

    def _reset_step(self):
        """Reset step 4"""
        if self.state_manager:
            st.session_state.workflow_data['step_4_completed'] = False
            st.session_state.workflow_data['step_4_data'] = {}
