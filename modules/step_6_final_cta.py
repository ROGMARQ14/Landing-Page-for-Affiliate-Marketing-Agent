import streamlit as st
from ai_providers.ai_manager import AIManager
from utils.state_management import StateManager

class FinalCTAModule:
    """Step 6: Final CTA + What Happens Next Roadmap (V2.0)"""

    def __init__(self):
        self.ai_manager = AIManager()
        self.state_manager = StateManager()

    def render(self):
        st.markdown("# 🎬 Step 6: Final CTA & What Happens Next")
        st.markdown("*V2.0 Enhanced with post-click roadmap (+10-15% conversion)*")

        st.progress(6/8, text="Step 6 of 8")

        if not self.state_manager.is_step_completed(5):
            st.warning("⚠️ Please complete Step 5 (Social Proof) first")
            return

        if self.state_manager.is_step_completed(6):
            self._show_completed_summary()
            if st.button("🔄 Regenerate Final CTA"):
                self._reset_step()
                st.rerun()
            return

        # CTA configuration
        with st.form("final_cta_form"):
            st.markdown("## 🎬 Final CTA Configuration")

            col1, col2 = st.columns(2)

            with col1:
                urgency_type = st.selectbox(
                    "Urgency Element",
                    ["Countdown Timer", "Limited Quantity", "Bonus Stack", "Price Increase Warning"]
                )

                include_roadmap = st.checkbox(
                    "Include 'What Happens Next' Roadmap (V2.0)",
                    value=True,
                    help="Shows 3-step post-click process (+10-15% conversion)"
                )

            with col2:
                guarantee_type = st.selectbox(
                    "Risk Reversal",
                    ["Money-Back Guarantee", "Free Trial", "No-Risk Promise", "Satisfaction Guarantee"]
                )

                include_secondary_cta = st.checkbox(
                    "Include Secondary CTA",
                    value=True,
                    help="For fence-sitters (Learn More, FAQ, etc.)"
                )

            submitted = st.form_submit_button("🎬 Generate Final CTA", type="primary")

        if submitted:
            self._generate_final_cta({
                'urgency_type': urgency_type,
                'guarantee_type': guarantee_type,
                'include_roadmap': include_roadmap,
                'include_secondary_cta': include_secondary_cta
            })

    def _generate_final_cta(self, config):
        with st.spinner("🎬 Generating final CTA with V2.0 roadmap..."):

            # Simplified generation (would use full V2.0 prompt)
            cta_data = {
                'cta_headline': {
                    'copy': 'Join 12,000+ People Who Beat Keto Flu—Starting Today',
                    'urgency_element': config['urgency_type']
                },
                'sub_copy': {
                    'copy': 'Don't let another keto attempt fail due to headaches and fatigue. Our patent-pending formula ensures smooth ketosis entry in just 48 hours.',
                    'word_count': 25
                },
                'what_happens_next_roadmap': {
                    'include': config['include_roadmap'],
                    'headline': 'What Happens After You Click:',
                    'steps': [
                        {
                            'step_number': 1,
                            'action': 'Click "Get Started Risk-Free"',
                            'outcome': 'Secure checkout page opens (256-bit SSL)',
                            'icon': '🛒'
                        },
                        {
                            'step_number': 2,
                            'action': 'Enter Your Details',
                            'outcome': 'Takes 60 seconds, completely secure',
                            'icon': '🔒'
                        },
                        {
                            'step_number': 3,
                            'action': 'Receive Welcome Package',
                            'outcome': 'Instant email + tracking + keto guide',
                            'icon': '📧'
                        }
                    ]
                },
                'primary_cta_button': {
                    'copy': 'Get Started Risk-Free',
                    'style': 'primary',
                    'size': 'large'
                },
                'button_subtext': {
                    'copy': '90-Day Money-Back Guarantee • Free Shipping • No Subscription',
                    'elements': ['guarantee', 'shipping', 'subscription']
                },
                'urgency_element': {
                    'type': config['urgency_type'],
                    'copy': 'Limited Time: Save 40% + Free Bonus Guide (Expires in 24 hours)',
                    'ethical': True
                },
                'secondary_cta': {
                    'include': config['include_secondary_cta'],
                    'copy': 'Still have questions? View our FAQ →',
                    'style': 'ghost'
                },
                'trust_signals': [
                    'Secure 256-bit SSL checkout',
                    'No hidden fees or subscriptions',
                    '24/7 customer support',
                    'Made in FDA-approved facility'
                ],
                'configuration': config
            }

            # Save data
            self.state_manager.save_step_data(6, {
                'final_cta': cta_data,
                'configuration': config,
                'generated_at': st.session_state.workflow_data['last_updated']
            })
            self.state_manager.mark_step_completed(6)

            st.success("✅ Final CTA with V2.0 roadmap generated!")
            st.rerun()

    def _show_completed_summary(self):
        st.success("✅ **Step 6 Complete** - Final CTA with 'What Happens Next' roadmap!")

        step_data = self.state_manager.get_step_data(6)
        config = step_data.get('configuration', {})
        cta_data = step_data.get('final_cta', {})

        # Metrics
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Urgency Type", config.get('urgency_type', 'N/A'))
        with col2:
            st.metric("V2.0 Roadmap", "✅" if config.get('include_roadmap') else "❌")
        with col3:
            st.metric("Secondary CTA", "✅" if config.get('include_secondary_cta') else "❌")

        # Preview CTA
        with st.expander("🎬 Preview Final CTA Section"):

            # Main headline
            st.markdown("### CTA Headline")
            st.write(f"**{cta_data.get('cta_headline', {}).get('copy', 'N/A')}**")

            # Sub-copy
            st.markdown("### Sub-Copy")
            st.write(cta_data.get('sub_copy', {}).get('copy', 'N/A'))

            # What Happens Next Roadmap (V2.0)
            if config.get('include_roadmap'):
                st.markdown("### 🗺️ What Happens Next Roadmap (V2.0 NEW)")
                roadmap = cta_data.get('what_happens_next_roadmap', {})
                st.write(f"**{roadmap.get('headline', 'N/A')}**")

                for step in roadmap.get('steps', []):
                    st.write(f"{step.get('icon', '')} **Step {step.get('step_number')}:** {step.get('action', 'N/A')}")
                    st.write(f"   → {step.get('outcome', 'N/A')}")

            # CTA Button
            st.markdown("### CTA Button")
            primary_cta = cta_data.get('primary_cta_button', {}).get('copy', 'N/A')
            button_subtext = cta_data.get('button_subtext', {}).get('copy', 'N/A')

            st.button(f"🚀 {primary_cta}", disabled=True, use_container_width=True)
            st.caption(button_subtext)

            # Trust signals
            st.markdown("### Trust Signals")
            for signal in cta_data.get('trust_signals', []):
                st.write(f"✅ {signal}")

    def _reset_step(self):
        st.session_state.workflow_data['step_6_completed'] = False
        st.session_state.workflow_data['step_6_data'] = {}
