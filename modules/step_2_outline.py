import streamlit as st
from ai_providers.ai_manager import AIManager
from utils.state_management import StateManager

class OutlineModule:
    """Step 2: Landing Page Outline - V2.0 Enhanced Structure"""

    def __init__(self):
        self.ai_manager = AIManager()
        self.state_manager = StateManager()

    def render(self):
        st.markdown("# 📋 Step 2: Landing Page Outline & Structure")
        st.markdown("*V2.0 Enhanced with Agitation Module & Affiliate Sections*")

        # Progress
        st.progress(2/8, text="Step 2 of 8")

        # Check if previous step is completed
        if not self.state_manager.is_step_completed(1):
            st.warning("⚠️ Please complete Step 1 (Product Research) first")
            return

        # Check if current step is completed
        if self.state_manager.is_step_completed(2):
            self._show_completed_summary()
            if st.button("🔄 Regenerate Outline"):
                self._reset_step()
                st.rerun()
            return

        # Configuration options
        st.markdown("## ⚙️ Landing Page Configuration")

        col1, col2 = st.columns(2)

        with col1:
            page_type = st.selectbox(
                "Page Type",
                ["Affiliate/Review", "Direct Product Sales", "SaaS/Software", "Course/Education"],
                help="Affects which sections are included"
            )

            include_agitation = st.checkbox(
                "Include Agitation Module",
                value=True,
                help="V2.0 Enhancement: Amplifies urgency between problem and solution"
            )

            include_comparison = st.checkbox(
                "Include Comparison Table", 
                value=(page_type == "Affiliate/Review"),
                help="Compare your product vs competitors"
            )

        with col2:
            include_qualifier = st.checkbox(
                "Include Audience Qualifier",
                value=True,
                help="'Is this for you?' section builds trust"
            )

            include_before_after = st.checkbox(
                "Include Before/After Showcase",
                value=False,
                help="For visual transformation products only"
            )

            product_type = st.selectbox(
                "Product Type",
                ["Supplement/Health", "Software/App", "Course/Education", "Physical Product", "Service"]
            )

        # Generate outline button
        if st.button("📋 Generate Landing Page Outline", type="primary"):
            self._generate_outline({
                'page_type': page_type,
                'product_type': product_type,
                'include_agitation': include_agitation,
                'include_comparison': include_comparison,
                'include_qualifier': include_qualifier,
                'include_before_after': include_before_after
            })

    def _generate_outline(self, config):
        """Generate outline based on configuration"""

        with st.spinner("📋 Generating enhanced landing page structure..."):

            # Get Step 1 data for context
            step_1_data = self.state_manager.get_step_data(1)

            # Simplified outline generation (would use full V2.0 prompt in production)
            outline_data = {
                'structure': {
                    'section_1_hero': {'include': True, 'purpose': 'Above-fold conversion'},
                    'section_2_problem': {'include': True, 'purpose': 'Validation + rapport'},
                    'section_3_agitation': {'include': config['include_agitation'], 'purpose': 'Emotional urgency'},
                    'section_4_solution': {'include': True, 'purpose': 'Relief + resolution'},
                    'section_5_benefits': {'include': True, 'purpose': 'Justification'},
                    'section_6_qualifier': {'include': config['include_qualifier'], 'purpose': 'Relevance + trust'},
                    'section_7_social_proof': {'include': True, 'purpose': 'Credibility'},
                    'section_8_comparison': {'include': config['include_comparison'], 'purpose': 'Choice guidance'},
                    'section_9_before_after': {'include': config['include_before_after'], 'purpose': 'Visual proof'},
                    'section_10_final_cta': {'include': True, 'purpose': 'Final conversion'},
                    'section_11_footer': {'include': True, 'purpose': 'Compliance'}
                },
                'terminology_standards': {
                    'pain_point_primary': step_1_data.get('ai_response', {}).get('target_audience_profile', {}).get('primary_pain_points', [{}])[0].get('pain', 'primary concern'),
                    'timeframe_primary': '48 hours',  # Would extract from research
                    'product_benefit_primary': 'key outcome'  # Would extract from research
                },
                'configuration': config
            }

            # Save data
            self.state_manager.save_step_data(2, {
                'configuration': config,
                'outline_structure': outline_data,
                'generated_at': st.session_state.workflow_data['last_updated']
            })
            self.state_manager.mark_step_completed(2)

            st.success("✅ Landing page outline generated!")
            st.rerun()

    def _show_completed_summary(self):
        st.success("✅ **Step 2 Complete** - Landing page outline generated!")

        step_data = self.state_manager.get_step_data(2)
        config = step_data.get('configuration', {})

        # Show configuration summary
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Page Type", config.get('page_type', 'N/A'))

        with col2:
            sections_count = sum([1 for section in step_data.get('outline_structure', {}).get('structure', {}).values() if section.get('include')])
            st.metric("Sections Included", sections_count)

        with col3:
            st.metric("V2.0 Enhancements", 
                     sum([config.get('include_agitation', False),
                          config.get('include_comparison', False), 
                          config.get('include_qualifier', False)]))

        # Show structure overview
        with st.expander("📋 View Landing Page Structure"):
            structure = step_data.get('outline_structure', {}).get('structure', {})
            for section_key, section_data in structure.items():
                if section_data.get('include'):
                    section_name = section_key.replace('_', ' ').title()
                    st.write(f"✅ **{section_name}** - {section_data.get('purpose', '')}")

    def _reset_step(self):
        st.session_state.workflow_data['step_2_completed'] = False
        st.session_state.workflow_data['step_2_data'] = {}
