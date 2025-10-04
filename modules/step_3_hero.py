import streamlit as st
from ai_providers.ai_manager import AIManager
from utils.state_management import StateManager

class HeroModule:
    """Step 3: Hero Section Copy Generation"""

    def __init__(self):
        self.ai_manager = AIManager()
        self.state_manager = StateManager()

    def render(self):
        st.markdown("# 🎯 Step 3: Hero Section Copy")
        st.markdown("*Headlines, subheadlines, and CTAs that convert*")

        st.progress(3/8, text="Step 3 of 8")

        if not self.state_manager.is_step_completed(2):
            st.warning("⚠️ Please complete Step 2 (Landing Page Outline) first")
            return

        if self.state_manager.is_step_completed(3):
            self._show_completed_summary()
            if st.button("🔄 Regenerate Hero Copy"):
                self._reset_step()
                st.rerun()
            return

        # Hero copy generation form
        with st.form("hero_copy_form"):
            st.markdown("## 🎯 Hero Copy Configuration")

            col1, col2 = st.columns(2)

            with col1:
                headline_style = st.selectbox(
                    "Headline Style",
                    ["Problem-Focused", "Benefit-Focused", "Question-Based", "Urgency-Driven"]
                )

                tone = st.selectbox(
                    "Tone of Voice", 
                    ["Professional", "Conversational", "Urgent", "Authoritative", "Friendly"]
                )

            with col2:
                target_emotion = st.selectbox(
                    "Primary Emotion",
                    ["Urgency", "Relief", "Excitement", "Trust", "Fear of Missing Out"]
                )

                cta_style = st.selectbox(
                    "CTA Button Style",
                    ["Action-Oriented", "Benefit-Driven", "Urgency-Based", "Risk-Free"]
                )

            generate_variants = st.slider("Number of Variants", min_value=2, max_value=5, value=3)

            submitted = st.form_submit_button("🚀 Generate Hero Copy", type="primary")

        if submitted:
            self._generate_hero_copy({
                'headline_style': headline_style,
                'tone': tone,
                'target_emotion': target_emotion,
                'cta_style': cta_style,
                'variants': generate_variants
            })

    def _generate_hero_copy(self, config):
        with st.spinner("🎯 Generating compelling hero copy..."):

            # Get previous steps data
            step_1_data = self.state_manager.get_step_data(1)
            step_2_data = self.state_manager.get_step_data(2)

            # Simplified generation (would use full V1.0 prompt in production)
            hero_data = {
                'headline_primary': {
                    'copy': 'Beat Keto Flu in 48 Hours—Without the Miserable Headaches',
                    'style': config['headline_style'],
                    'character_count': 50
                },
                'subheadline_primary': {
                    'copy': 'Our electrolyte-enhanced formula helps you enter ketosis smoothly while maintaining energy and mental clarity from day one.',
                    'word_count': 20
                },
                'cta_button_primary': {
                    'copy': 'Get Started Risk-Free',
                    'style': config['cta_style']
                },
                'variants': [
                    {
                        'headline': 'Finally: Enter Ketosis Without the 3-Day Energy Crash',
                        'subheadline': 'Skip the keto flu entirely with our patent-pending electrolyte blend.',
                        'cta': 'Try Risk-Free Today'
                    },
                    {
                        'headline': 'Why Keto Beginners Choose Our Electrolyte Complex',
                        'subheadline': 'Prevent keto flu headaches and maintain energy during ketosis transition.',
                        'cta': 'Start Your Journey'
                    }
                ],
                'configuration': config
            }

            # Save data
            self.state_manager.save_step_data(3, {
                'hero_copy': hero_data,
                'configuration': config,
                'generated_at': st.session_state.workflow_data['last_updated']
            })
            self.state_manager.mark_step_completed(3)

            st.success("✅ Hero copy generated!")
            st.rerun()

    def _show_completed_summary(self):
        st.success("✅ **Step 3 Complete** - Hero section copy generated!")

        step_data = self.state_manager.get_step_data(3)
        hero_data = step_data.get('hero_copy', {})

        # Display primary hero copy
        st.markdown("### 🎯 Primary Hero Copy")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("**Headline:**")
            st.markdown(f"> {hero_data.get('headline_primary', {}).get('copy', 'N/A')}")

            st.markdown("**Subheadline:**")
            st.markdown(f"> {hero_data.get('subheadline_primary', {}).get('copy', 'N/A')}")

            st.markdown("**CTA Button:**")
            st.markdown(f"> {hero_data.get('cta_button_primary', {}).get('copy', 'N/A')}")

        with col2:
            config = step_data.get('configuration', {})
            st.metric("Headline Style", config.get('headline_style', 'N/A'))
            st.metric("Tone", config.get('tone', 'N/A'))
            st.metric("Variants Created", len(hero_data.get('variants', [])))

        # Show variants
        if hero_data.get('variants'):
            with st.expander("🔄 View A/B Testing Variants"):
                for i, variant in enumerate(hero_data['variants'], 1):
                    st.markdown(f"**Variant {i}:**")
                    st.write(f"• Headline: {variant.get('headline', 'N/A')}")
                    st.write(f"• Subheadline: {variant.get('subheadline', 'N/A')}")
                    st.write(f"• CTA: {variant.get('cta', 'N/A')}")
                    st.markdown("---")

    def _reset_step(self):
        st.session_state.workflow_data['step_3_completed'] = False
        st.session_state.workflow_data['step_3_data'] = {}
