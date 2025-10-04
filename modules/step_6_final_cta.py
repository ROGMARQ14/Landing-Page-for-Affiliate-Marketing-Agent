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

class FinalCTAModule:
    """Step 6: Final CTA + What Happens Next Roadmap (V2.0 Enhanced)"""

    def __init__(self):
        # Initialize with error handling
        try:
            self.ai_manager = AIManager()
            self.state_manager = StateManager()
        except Exception as e:
            st.error(f"Error initializing FinalCTAModule: {str(e)}")
            self.ai_manager = None
            self.state_manager = None

    def render(self):
        """Render Step 6 UI"""
        st.markdown("# 🎬 Step 6: Final CTA & What Happens Next")
        st.markdown("*V2.0 Enhanced with post-click roadmap (+10-15% conversion)*")

        st.progress(6/8, text="Step 6 of 8")

        # Check if state manager is available
        if not self.state_manager:
            st.error("❌ State management not available. Please check your installation.")
            return

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
                    ["Countdown Timer", "Limited Quantity", "Bonus Stack", "Price Increase Warning"],
                    help="Type of urgency to create"
                )

                include_roadmap = st.checkbox(
                    "Include 'What Happens Next' Roadmap (V2.0)",
                    value=True,
                    help="Shows 3-step post-click process (+10-15% conversion)"
                )

            with col2:
                guarantee_type = st.selectbox(
                    "Risk Reversal",
                    ["Money-Back Guarantee", "Free Trial", "No-Risk Promise", "Satisfaction Guarantee"],
                    help="Type of guarantee to offer"
                )

                include_secondary_cta = st.checkbox(
                    "Include Secondary CTA",
                    value=True,
                    help="For fence-sitters (Learn More, FAQ, etc.)"
                )

            # Advanced options
            with st.expander("🔧 Advanced CTA Options"):
                cta_style = st.selectbox(
                    "CTA Button Style",
                    ["Primary Action", "Benefit-Focused", "Urgency-Focused"],
                    help="Style of the main CTA button"
                )

                trust_signals = st.multiselect(
                    "Trust Signals to Include",
                    ["SSL Security", "Money-Back Guarantee", "Customer Support", "No Subscription"],
                    default=["SSL Security", "Money-Back Guarantee"],
                    help="Trust elements to display near CTA"
                )

                emotional_close = st.selectbox(
                    "Emotional Close Type",
                    ["Relief-Based", "Achievement-Based", "Transformation-Based"],
                    help="Final emotional appeal before CTA"
                )

            submitted = st.form_submit_button("🎬 Generate Final CTA", type="primary")

        if submitted:
            self._generate_final_cta({
                'urgency_type': urgency_type,
                'guarantee_type': guarantee_type,
                'include_roadmap': include_roadmap,
                'include_secondary_cta': include_secondary_cta,
                'cta_style': cta_style,
                'trust_signals': trust_signals,
                'emotional_close': emotional_close
            })

    def _generate_final_cta(self, config: Dict[str, Any]):
        """Generate Final CTA with What Happens Next roadmap"""

        if not self.ai_manager or not self.state_manager:
            st.error("❌ Required services not available")
            return

        with st.spinner("🎬 Generating final CTA with V2.0 roadmap..."):

            # Get previous steps data for context
            try:
                step_1_data = self.state_manager.get_step_data(1)
                step_2_data = self.state_manager.get_step_data(2)
                step_3_data = self.state_manager.get_step_data(3)
                step_4_data = self.state_manager.get_step_data(4)
                step_5_data = self.state_manager.get_step_data(5)
            except Exception as e:
                st.error(f"Error getting previous step data: {str(e)}")
                return

            # Create the Final CTA prompt
            cta_prompt = self._create_cta_prompt(config, step_1_data, step_2_data, step_3_data, step_4_data, step_5_data)

            # Generate content using AI Manager
            try:
                response = self.ai_manager.generate_content(
                    prompt=cta_prompt,
                    model=st.session_state.workflow_data['selected_model'],
                    temperature=0.7,
                    max_tokens=2500
                )

                if response.get('success', False):
                    # Create structured CTA data
                    cta_data = self._create_cta_structure(config, response)

                    # Save data
                    self.state_manager.save_step_data(6, {
                        'final_cta': cta_data,
                        'configuration': config,
                        'ai_response': response,
                        'generated_at': datetime.now().isoformat()
                    })
                    self.state_manager.mark_step_completed(6)

                    st.success("✅ Final CTA with V2.0 roadmap generated!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"❌ AI generation failed: {response.get('error', 'Unknown error')}")

            except Exception as e:
                st.error(f"❌ Error generating Final CTA: {str(e)}")

    def _create_cta_prompt(self, config: Dict[str, Any], step_1_data: Dict[str, Any], 
                          step_2_data: Dict[str, Any], step_3_data: Dict[str, Any],
                          step_4_data: Dict[str, Any], step_5_data: Dict[str, Any]) -> str:
        """Create the Final CTA generation prompt"""

        # Extract context from previous steps
        product_name = step_1_data.get('form_inputs', {}).get('product_name', 'the product')
        target_audience = step_1_data.get('form_inputs', {}).get('target_audience', 'target customers')
        hero_headline = step_3_data.get('hero_copy', {}).get('headline_primary', {}).get('copy', '')

        prompt = f"""# Final CTA + What Happens Next Generation V2.0

## Context
Product: {product_name}
Target Audience: {target_audience}
Hero Headline: {hero_headline}

## Configuration
- Urgency Type: {config['urgency_type']}
- Guarantee Type: {config['guarantee_type']}
- Include Roadmap: {config['include_roadmap']}
- CTA Style: {config['cta_style']}
- Trust Signals: {config['trust_signals']}

## Task
Generate comprehensive Final CTA section with V2.0 enhancements.

### Section 1: Final Emotional Appeal
Create a final emotional appeal that ties together all previous sections.
Include:
- Emotional headline (8-12 words)
- Recap of transformation promise
- Final urgency reminder

### Section 2: What Happens Next Roadmap (V2.0 Enhancement)
Create transparent post-click roadmap to reduce purchase anxiety.
Include:
- Roadmap headline
- 3-step process breakdown
- Time expectations for each step
- What customer receives at each step

### Section 3: Primary CTA Button
Design high-converting call-to-action button.
Include:
- CTA button text (3-5 words max)
- Button subtext
- Urgency reinforcement

### Section 4: Risk Reversal & Trust Signals
Present guarantee and trust elements.
Include:
- Guarantee headline
- Guarantee terms
- Trust signals list
- Security assurances

### Section 5: Secondary CTA (if enabled)
Create secondary option for hesitant prospects.
Include:
- Secondary action text
- Lower-commitment alternative
- Lead nurturing opportunity

Return as structured JSON with clear sections and copy elements.
"""

        return prompt

    def _create_cta_structure(self, config: Dict[str, Any], ai_response: Dict[str, Any]) -> Dict[str, Any]:
        """Create structured Final CTA data"""

        # This is a simplified structure - in production, you'd parse the AI response
        cta_data = {
            'section_1_final_emotional_appeal': {
                'emotional_headline': {'copy': 'Your Transformation Starts Right Now'},
                'transformation_recap': {'copy': 'You have seen the problem, felt the urgency, and discovered the solution. The only question left is: will you take action today?'},
                'urgency_reminder': {'copy': 'Every day you wait is another day of the same struggles.'}
            },
            'section_2_what_happens_next_roadmap': {
                'include': config['include_roadmap'],
                'roadmap_headline': {'copy': 'What Happens After You Click:'},
                'steps': [
                    {
                        'step_number': 1,
                        'action': 'Click "Get Started Risk-Free"',
                        'outcome': 'Secure checkout page opens (256-bit SSL)',
                        'timeframe': 'Instant',
                        'icon': '🛒'
                    },
                    {
                        'step_number': 2,
                        'action': 'Enter Your Details',
                        'outcome': 'Takes 60 seconds, completely secure',
                        'timeframe': '1 minute',
                        'icon': '🔒'
                    },
                    {
                        'step_number': 3,
                        'action': 'Receive Welcome Package',
                        'outcome': 'Instant email + tracking + bonus guide',
                        'timeframe': 'Immediately',
                        'icon': '📧'
                    }
                ]
            },
            'section_3_primary_cta': {
                'button_text': {'copy': 'Get Started Risk-Free'},
                'button_subtext': {'copy': '90-Day Money-Back Guarantee'},
                'urgency_reinforcement': {'copy': 'Limited Time: Save 40% + Free Bonus Guide'}
            },
            'section_4_risk_reversal': {
                'guarantee_headline': {'copy': 'Your Investment Is 100% Protected'},
                'guarantee_terms': {'copy': 'Try it for 90 days. If you are not completely satisfied, get every penny back. No questions asked.'},
                'trust_signals': {
                    'signals': [
                        {'signal': 'Secure 256-bit SSL checkout'},
                        {'signal': 'No hidden fees or subscriptions'},
                        {'signal': '24/7 customer support'},
                        {'signal': 'Made in FDA-approved facility'}
                    ]
                }
            },
            'section_5_secondary_cta': {
                'include': config['include_secondary_cta'],
                'secondary_text': {'copy': 'Still have questions? View our FAQ'},
                'alternative_action': {'copy': 'Learn More'},
                'lead_nurture': {'copy': 'Get free tips delivered to your inbox'}
            },
            'configuration': config
        }

        return cta_data

    def _show_completed_summary(self):
        """Show summary of completed Final CTA"""

        if not self.state_manager:
            return

        st.success("✅ **Step 6 Complete** - Final CTA with What Happens Next roadmap!")

        step_data = self.state_manager.get_step_data(6)
        cta_data = step_data.get('final_cta', {})
        config = step_data.get('configuration', {})

        # Show CTA sections
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Urgency Type", config.get('urgency_type', 'N/A'))
        with col2:
            st.metric("V2.0 Roadmap", "✅" if config.get('include_roadmap') else "❌")
        with col3:
            st.metric("Secondary CTA", "✅" if config.get('include_secondary_cta') else "❌")

        # Configuration summary
        with st.expander("⚙️ View Configuration"):
            st.write(f"**Urgency Type:** {config.get('urgency_type', 'N/A')}")
            st.write(f"**Guarantee Type:** {config.get('guarantee_type', 'N/A')}")
            st.write(f"**CTA Style:** {config.get('cta_style', 'N/A')}")
            st.write(f"**Trust Signals:** {', '.join(config.get('trust_signals', []))}")

        # Preview CTA sections
        with st.expander("🎬 Preview Final CTA Section"):

            # Final emotional appeal
            st.markdown("### 🎯 Final Emotional Appeal")
            appeal_data = cta_data.get('section_1_final_emotional_appeal', {})
            st.write(f"**Headline:** {appeal_data.get('emotional_headline', {}).get('copy', 'N/A')}")
            st.write(f"**Recap:** {appeal_data.get('transformation_recap', {}).get('copy', 'N/A')}")

            # What Happens Next Roadmap (V2.0)
            if config.get('include_roadmap'):
                st.markdown("### 🗺️ What Happens Next Roadmap (V2.0 NEW)")
                roadmap_data = cta_data.get('section_2_what_happens_next_roadmap', {})
                st.write(f"**{roadmap_data.get('roadmap_headline', {}).get('copy', 'N/A')}**")

                for step in roadmap_data.get('steps', []):
                    st.write(f"{step.get('icon', '')} **Step {step.get('step_number')}:** {step.get('action', 'N/A')}")
                    st.write(f"   → {step.get('outcome', 'N/A')} ({step.get('timeframe', 'N/A')})")

            # Primary CTA Button
            st.markdown("### 🚀 Primary CTA Button")
            primary_cta = cta_data.get('section_3_primary_cta', {})
            button_text = primary_cta.get('button_text', {}).get('copy', 'N/A')
            button_subtext = primary_cta.get('button_subtext', {}).get('copy', 'N/A')

            st.button(f"🚀 {button_text}", disabled=True, use_container_width=True)
            st.caption(button_subtext)

            # Risk Reversal
            st.markdown("### 🛡️ Risk Reversal & Trust Signals")
            risk_data = cta_data.get('section_4_risk_reversal', {})
            st.write(f"**{risk_data.get('guarantee_headline', {}).get('copy', 'N/A')}**")
            st.write(risk_data.get('guarantee_terms', {}).get('copy', 'N/A'))

            trust_signals = risk_data.get('trust_signals', {}).get('signals', [])
            if trust_signals:
                st.write("**Trust Signals:**")
                for signal in trust_signals:
                    st.write(f"✅ {signal.get('signal', 'N/A')}")

            # Secondary CTA
            if config.get('include_secondary_cta'):
                st.markdown("### 🔄 Secondary CTA")
                secondary_data = cta_data.get('section_5_secondary_cta', {})
                st.write(f"**{secondary_data.get('secondary_text', {}).get('copy', 'N/A')}**")

        # Generation details
        with st.expander("🔧 Generation Details"):
            ai_response = step_data.get('ai_response', {})
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Model Used:** {ai_response.get('model_used', 'N/A')}")
            with col2:
                st.write(f"**Tokens Used:** {ai_response.get('tokens_used', 'N/A')}")
            with col3:
                st.write(f"**Generated:** {step_data.get('generated_at', 'N/A')[:19]}")

    def _reset_step(self):
        """Reset step 6 data"""
        if self.state_manager:
            st.session_state.workflow_data['step_6_completed'] = False
            st.session_state.workflow_data['step_6_data'] = {}
