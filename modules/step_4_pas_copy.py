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
    """Step 4: Problem-Agitate-Solution Copy - V2.0 Enhanced"""

    def __init__(self):
        # Initialize with error handling
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
        st.markdown("*V2.0 Enhanced with dedicated Agitation Module*")

        st.progress(4/8, text="Step 4 of 8")

        # Check if state manager is available
        if not self.state_manager:
            st.error("❌ State management not available. Please check your installation.")
            return

        if not self.state_manager.is_step_completed(3):
            st.warning("⚠️ Please complete Step 3 (Hero Section) first")
            return

        if self.state_manager.is_step_completed(4):
            self._show_completed_summary()
            if st.button("🔄 Regenerate PAS Copy"):
                self._reset_step()
                st.rerun()
            return

        # PAS configuration
        with st.form("pas_copy_form"):
            st.markdown("## 🔥 Problem-Agitate-Solution Configuration")

            col1, col2 = st.columns(2)

            with col1:
                agitation_format = st.selectbox(
                    "Agitation Format (V2.0)",
                    ["Consequence-Based Bullets", "Failure Narrative", "Risk Statistics"],
                    help="V2.0 Enhancement: Choose how to amplify emotional urgency"
                )

                benefits_format = st.selectbox(
                    "Benefits Format",
                    ["FAB Grid (Feature-Advantage-Benefit)", "Benefit Blocks"],
                    help="How to present product benefits"
                )

            with col2:
                emotional_intensity = st.slider(
                    "Emotional Intensity", 
                    min_value=1, max_value=5, value=3,
                    help="1=Subtle, 3=Balanced, 5=High urgency"
                )

                include_statistics = st.checkbox(
                    "Include Supporting Statistics",
                    value=True,
                    help="Add credible statistics to support claims"
                )

            # Advanced options
            with st.expander("🔧 Advanced PAS Options"):
                pain_amplification = st.selectbox(
                    "Pain Amplification Strategy",
                    ["Current State Focus", "Future Consequences", "Comparison Contrast"],
                    help="How to emphasize the problem"
                )

                solution_presentation = st.selectbox(
                    "Solution Presentation Style",
                    ["Direct Reveal", "Gradual Build-up", "Contrast Method"],
                    help="How to present your solution"
                )

                social_validation = st.checkbox(
                    "Include Social Validation in Benefits",
                    value=True,
                    help="Add testimonials or social proof to benefits"
                )

            submitted = st.form_submit_button("📝 Generate PAS Copy", type="primary")

        if submitted:
            self._generate_pas_copy({
                'agitation_format': agitation_format,
                'benefits_format': benefits_format,
                'emotional_intensity': emotional_intensity,
                'include_statistics': include_statistics,
                'pain_amplification': pain_amplification,
                'solution_presentation': solution_presentation,
                'social_validation': social_validation
            })

    def _generate_pas_copy(self, config: Dict[str, Any]):
        """Generate Problem-Agitate-Solution copy"""

        if not self.ai_manager or not self.state_manager:
            st.error("❌ Required services not available")
            return

        with st.spinner("📝 Generating Problem-Agitate-Solution copy..."):

            # Get previous steps data for context
            try:
                step_1_data = self.state_manager.get_step_data(1)
                step_2_data = self.state_manager.get_step_data(2)
                step_3_data = self.state_manager.get_step_data(3)
            except Exception as e:
                st.error(f"Error getting previous step data: {str(e)}")
                return

            # Create the PAS prompt
            pas_prompt = self._create_pas_prompt(config, step_1_data, step_2_data, step_3_data)

            # Generate content using AI Manager
            try:
                response = self.ai_manager.generate_content(
                    prompt=pas_prompt,
                    model=st.session_state.workflow_data['selected_model'],
                    temperature=0.7,
                    max_tokens=3000
                )

                if response.get('success', False):
                    # Create structured PAS data
                    pas_data = self._create_pas_structure(config, response)

                    # Save data
                    self.state_manager.save_step_data(4, {
                        'pas_copy': pas_data,
                        'configuration': config,
                        'ai_response': response,
                        'generated_at': datetime.now().isoformat()
                    })
                    self.state_manager.mark_step_completed(4)

                    st.success("✅ Problem-Agitate-Solution copy generated!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"❌ AI generation failed: {response.get('error', 'Unknown error')}")

            except Exception as e:
                st.error(f"❌ Error generating PAS copy: {str(e)}")

    def _create_pas_prompt(self, config: Dict[str, Any], step_1_data: Dict[str, Any], 
                          step_2_data: Dict[str, Any], step_3_data: Dict[str, Any]) -> str:
        """Create the PAS generation prompt"""

        # Extract context from previous steps
        product_name = step_1_data.get('form_inputs', {}).get('product_name', 'the product')
        target_audience = step_1_data.get('form_inputs', {}).get('target_audience', 'target customers')
        hero_headline = step_3_data.get('hero_copy', {}).get('headline_primary', {}).get('copy', '')

        prompt = f"""# Problem-Agitate-Solution Copy Generation V2.0

## Context
Product: {product_name}
Target Audience: {target_audience}
Hero Headline: {hero_headline}

## Configuration
- Agitation Format: {config['agitation_format']}
- Emotional Intensity: {config['emotional_intensity']}/5
- Benefits Format: {config['benefits_format']}
- Include Statistics: {config['include_statistics']}

## Task
Generate comprehensive Problem-Agitate-Solution copy with V2.0 enhancements.

### Section 1: Problem Identification
Create empathetic problem identification that validates the audience's experience.
Include:
- Problem headline (8-12 words)
- Empathetic paragraph (2-3 sentences)
- Pain point validation

### Section 2: Agitation Module (V2.0 Enhancement)
Amplify emotional urgency using {config['agitation_format']} format.
Include:
- Agitation headline
- Consequence amplification
- Urgency building elements

### Section 3: Solution Reveal
Present the solution as relief and resolution.
Include:
- Solution headline
- Transition statement
- How it works (3-step process)

### Section 4: Benefits Matrix
Present benefits using {config['benefits_format']} format.
Include:
- Section headline
- Feature-Advantage-Benefit breakdown
- Emotional payoffs

Return as structured JSON with clear sections and copy elements.
"""

        return prompt

    def _create_pas_structure(self, config: Dict[str, Any], ai_response: Dict[str, Any]) -> Dict[str, Any]:
        """Create structured PAS data"""

        # This is a simplified structure - in production, you'd parse the AI response
        pas_data = {
            'section_1_problem_identification': {
                'problem_headline': {'copy': 'Struggling With Your Current Challenge?'},
                'empathetic_paragraph': {'copy': 'You have tried everything, but the problem persists. Every day it gets a little worse, and you are running out of options.'},
                'pain_validation': {'copy': 'This frustration is real, and you are not alone in feeling this way.'}
            },
            'section_2_agitation_module': {
                'agitation_headline': {'copy': 'Here Is What Happens If Nothing Changes'},
                'agitation_content': {
                    'format_selected': config['agitation_format'],
                    'consequence_bullets': {
                        'bullets': [
                            {'consequence': 'Your situation continues to deteriorate'},
                            {'consequence': 'You waste more time and money on failed solutions'},
                            {'consequence': 'The opportunity window keeps getting smaller'},
                            {'consequence': 'You miss out on the results you deserve'}
                        ]
                    }
                }
            },
            'section_3_solution_reveal': {
                'solution_headline': {'copy': 'Finally, A Solution That Actually Works'},
                'transition_statement': {'copy': 'But it does not have to be this way.'},
                'how_it_works': {
                    'steps': [
                        {'action': 'Take the first step', 'outcome': 'Immediate relief'},
                        {'action': 'Follow the proven system', 'outcome': 'Consistent progress'},
                        {'action': 'Achieve your goal', 'outcome': 'Lasting transformation'}
                    ]
                }
            },
            'section_4_benefits_matrix': {
                'format_selected': config['benefits_format'],
                'section_headline': {'copy': 'Why This Changes Everything'},
                'benefit_blocks': {
                    'blocks': [
                        {
                            'headline': 'Immediate Results',
                            'feature_statement': 'Fast-acting solution',
                            'benefit_statement': 'See improvements in 24-48 hours',
                            'emotional_payoff': 'Feel relief and confidence right away'
                        },
                        {
                            'headline': 'Long-Term Success',
                            'feature_statement': 'Sustainable approach',
                            'benefit_statement': 'Lasting results without backsliding',
                            'emotional_payoff': 'Enjoy permanent transformation'
                        },
                        {
                            'headline': 'Peace of Mind',
                            'feature_statement': 'Risk-free guarantee',
                            'benefit_statement': 'Complete satisfaction or money back',
                            'emotional_payoff': 'Confidence in your investment'
                        }
                    ]
                }
            },
            'configuration': config
        }

        return pas_data

    def _show_completed_summary(self):
        """Show summary of completed PAS copy"""

        if not self.state_manager:
            return

        st.success("✅ **Step 4 Complete** - PAS copy generated with V2.0 Agitation Module!")

        step_data = self.state_manager.get_step_data(4)
        pas_data = step_data.get('pas_copy', {})
        config = step_data.get('configuration', {})

        # Show PAS sections
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Problem", "✅")
        with col2:
            st.metric("Agitation", "✅ V2.0")
        with col3:
            st.metric("Solution", "✅")
        with col4:
            st.metric("Benefits", "✅")

        # Configuration summary
        with st.expander("⚙️ View Configuration"):
            st.write(f"**Agitation Format:** {config.get('agitation_format', 'N/A')}")
            st.write(f"**Benefits Format:** {config.get('benefits_format', 'N/A')}")
            st.write(f"**Emotional Intensity:** {config.get('emotional_intensity', 'N/A')}/5")
            st.write(f"**Include Statistics:** {config.get('include_statistics', False)}")

        # Preview sections
        with st.expander("📖 Preview PAS Copy"):

            # Problem section
            st.markdown("### 🔍 Problem Section")
            problem_data = pas_data.get('section_1_problem_identification', {})
            st.write(f"**Headline:** {problem_data.get('problem_headline', {}).get('copy', 'N/A')}")
            st.write(f"**Copy:** {problem_data.get('empathetic_paragraph', {}).get('copy', 'N/A')}")

            # Agitation section (V2.0)
            st.markdown("### 🔥 Agitation Section (V2.0 NEW)")
            agitation_data = pas_data.get('section_2_agitation_module', {})
            st.write(f"**Headline:** {agitation_data.get('agitation_headline', {}).get('copy', 'N/A')}")

            bullets = agitation_data.get('agitation_content', {}).get('consequence_bullets', {}).get('bullets', [])
            if bullets:
                st.write("**Consequences:**")
                for bullet in bullets[:3]:  # Show first 3
                    st.write(f"• {bullet.get('consequence', 'N/A')}")

            # Solution section
            st.markdown("### ✅ Solution Section")
            solution_data = pas_data.get('section_3_solution_reveal', {})
            st.write(f"**Headline:** {solution_data.get('solution_headline', {}).get('copy', 'N/A')}")
            st.write(f"**Transition:** {solution_data.get('transition_statement', {}).get('copy', 'N/A')}")

            steps = solution_data.get('how_it_works', {}).get('steps', [])
            if steps:
                st.write("**How It Works:**")
                for i, step in enumerate(steps, 1):
                    st.write(f"{i}. **{step.get('action', 'N/A')}** → {step.get('outcome', 'N/A')}")

            # Benefits section
            st.markdown("### 🎯 Benefits Section")
            benefits_data = pas_data.get('section_4_benefits_matrix', {})
            blocks = benefits_data.get('benefit_blocks', {}).get('blocks', [])

            if blocks:
                for block in blocks[:2]:  # Show first 2 benefit blocks
                    st.write(f"**{block.get('headline', 'N/A')}**")
                    st.write(f"Feature: {block.get('feature_statement', 'N/A')}")
                    st.write(f"Benefit: {block.get('benefit_statement', 'N/A')}")
                    st.write(f"Emotional Payoff: {block.get('emotional_payoff', 'N/A')}")
                    st.write("---")

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
        """Reset step 4 data"""
        if self.state_manager:
            st.session_state.workflow_data['step_4_completed'] = False
            st.session_state.workflow_data['step_4_data'] = {}
