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

class OutlineModule:
    """Step 2: Landing Page Outline & Structure (V2.0 Enhanced)"""

    def __init__(self):
        try:
            self.ai_manager = AIManager()
            self.state_manager = StateManager()
        except Exception as e:
            st.error(f"Error initializing OutlineModule: {str(e)}")
            self.ai_manager = None
            self.state_manager = None

    def render(self):
        """Render Step 2 UI"""
        st.markdown("# 📋 Step 2: Landing Page Outline")
        st.markdown("*V2.0 Enhanced with affiliate marketing optimizations*")

        st.progress(2/8, text="Step 2 of 8")

        if not self.state_manager:
            st.error("❌ State management not available. Please check your installation.")
            return

        if not self.state_manager.is_step_completed(1):
            st.warning("⚠️ Please complete Step 1 (Product Research) first")
            return

        if self.state_manager.is_step_completed(2):
            self._show_completed_summary()
            if st.button("🔄 Regenerate Outline"):
                self._reset_step()
                st.rerun()
            return

        # Outline configuration
        with st.form("outline_configuration_form"):
            st.markdown("## 📋 Page Structure Configuration")

            col1, col2 = st.columns(2)

            with col1:
                page_type = st.selectbox(
                    "Landing Page Type",
                    ["Long-Form Sales Page", "Short-Form Squeeze Page", "Video Sales Letter", "Webinar Registration"],
                    help="Type of landing page to create"
                )

                include_comparison_table = st.checkbox(
                    "Include Comparison Table (V2.0)",
                    value=True,
                    help="V2.0: +15-25% conversion boost"
                )

                include_agitation_module = st.checkbox(
                    "Include Agitation Module (V2.0)", 
                    value=True,
                    help="V2.0: +20-35% conversion boost"
                )

            with col2:
                audience_qualifier = st.checkbox(
                    "Include Audience Qualifier (V2.0)",
                    value=True,
                    help="V2.0: +10-20% conversion boost"
                )

                include_roadmap = st.checkbox(
                    "Include What Happens Next Roadmap",
                    value=True,
                    help="V2.0: +10-15% conversion boost"
                )

                mobile_optimization = st.checkbox(
                    "Mobile-First Design",
                    value=True,
                    help="Optimize for mobile users first"
                )

            # Advanced structure options
            with st.expander("🔧 Advanced Structure Options"):
                sections_order = st.multiselect(
                    "Section Order (drag to reorder)",
                    ["Hero", "Problem", "Agitation", "Solution", "Benefits", "Social Proof", "CTA", "FAQ"],
                    default=["Hero", "Problem", "Agitation", "Solution", "Benefits", "Social Proof", "CTA"],
                    help="Order of main sections"
                )

                tone_personality = st.selectbox(
                    "Page Tone & Personality",
                    ["Professional & Trustworthy", "Friendly & Conversational", "Urgent & Direct", "Educational & Authoritative"],
                    help="Overall tone for the landing page"
                )

                content_depth = st.slider(
                    "Content Depth",
                    min_value=1, max_value=5, value=3,
                    help="1=Concise, 5=Very detailed"
                )

            submitted = st.form_submit_button("📋 Generate Outline", type="primary")

        if submitted:
            self._generate_outline({
                'page_type': page_type,
                'include_comparison_table': include_comparison_table,
                'include_agitation_module': include_agitation_module,
                'audience_qualifier': audience_qualifier,
                'include_roadmap': include_roadmap,
                'mobile_optimization': mobile_optimization,
                'sections_order': sections_order,
                'tone_personality': tone_personality,
                'content_depth': content_depth
            })

    def _generate_outline(self, config: Dict[str, Any]):
        """Generate landing page outline"""

        if not self.ai_manager or not self.state_manager:
            st.error("❌ Required services not available")
            return

        with st.spinner("📋 Generating V2.0 enhanced landing page outline..."):

            # Get Step 1 data for context
            try:
                step_1_data = self.state_manager.get_step_data(1)
            except Exception as e:
                st.error(f"Error getting Step 1 data: {str(e)}")
                return

            # Create outline prompt
            outline_prompt = self._create_outline_prompt(config, step_1_data)

            try:
                response = self.ai_manager.generate_content(
                    prompt=outline_prompt,
                    model=st.session_state.workflow_data['selected_model'],
                    temperature=0.4,
                    max_tokens=2500
                )

                if response.get('success', False):
                    # Create structured outline data
                    outline_data = self._create_outline_structure(config, response)

                    # Save data
                    self.state_manager.save_step_data(2, {
                        'outline_structure': outline_data,
                        'configuration': config,
                        'ai_response': response,
                        'generated_at': datetime.now().isoformat()
                    })
                    self.state_manager.mark_step_completed(2)

                    st.success("✅ V2.0 Landing page outline generated!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"❌ Outline generation failed: {response.get('error', 'Unknown error')}")

            except Exception as e:
                st.error(f"❌ Error generating outline: {str(e)}")

    def _create_outline_prompt(self, config: Dict[str, Any], step_1_data: Dict[str, Any]) -> str:
        """Create outline generation prompt"""

        # Extract relevant data from Step 1
        form_inputs = step_1_data.get('form_inputs', {})
        research_insights = step_1_data.get('research_insights', {})

        product_name = form_inputs.get('product_name', 'the product')
        target_audience = form_inputs.get('target_audience', 'target customers')

        prompt = f"""# Landing Page Outline Generation V2.0

## Context
Product: {product_name}
Target Audience: {target_audience}
Page Type: {config['page_type']}

## V2.0 Enhancements
- Include Agitation Module: {config['include_agitation_module']}
- Include Comparison Table: {config['include_comparison_table']}
- Include Audience Qualifier: {config['audience_qualifier']}
- Include What Happens Next: {config['include_roadmap']}

## Configuration
- Tone: {config['tone_personality']}
- Content Depth: {config['content_depth']}/5
- Mobile Optimization: {config['mobile_optimization']}
- Sections Order: {config['sections_order']}

## Task
Create comprehensive landing page outline with V2.0 affiliate marketing enhancements.

### Required Sections:
1. **Hero Section**
   - Headline hierarchy
   - Subheadline and value proposition
   - Hero image/video placeholder
   - Primary CTA button

2. **Problem Identification**
   - Problem statement
   - Pain point validation
   - Emotional connection

3. **Agitation Module (V2.0)**
   - Consequence amplification
   - Urgency building
   - Cost of inaction

4. **Solution Presentation**
   - Product introduction
   - How it works
   - Unique mechanism

5. **Benefits & Features**
   - Feature-Advantage-Benefit matrix
   - Transformation promises
   - Outcome visualization

6. **Social Proof Section**
   - Testimonials strategy
   - Before/after showcases
   - Authority endorsements

7. **Comparison Table (V2.0)**
   - Product vs alternatives
   - Feature comparison
   - Value justification

8. **Final CTA Section**
   - Primary call-to-action
   - What happens next roadmap
   - Risk reversal elements

Return structured outline with section details, content guidelines, and V2.0 enhancement notes.
"""

        return prompt

    def _create_outline_structure(self, config: Dict[str, Any], ai_response: Dict[str, Any]) -> Dict[str, Any]:
        """Create structured outline data"""

        outline_data = {
            'page_metadata': {
                'page_type': config['page_type'],
                'tone_personality': config['tone_personality'],
                'mobile_first': config['mobile_optimization'],
                'content_depth': config['content_depth'],
                'estimated_length': '3000-5000 words' if config['content_depth'] >= 4 else '2000-3000 words'
            },
            'section_structure': {
                'hero_section': {
                    'order': 1,
                    'components': [
                        'Primary headline (H1)',
                        'Supporting subheadline', 
                        'Value proposition statement',
                        'Hero image or video',
                        'Primary CTA button',
                        'Trust indicators'
                    ],
                    'estimated_words': 150,
                    'mobile_considerations': 'Stack vertically, larger buttons'
                },
                'problem_section': {
                    'order': 2,
                    'components': [
                        'Problem identification headline',
                        'Pain point validation',
                        'Emotional connection copy',
                        'Relatability elements'
                    ],
                    'estimated_words': 200,
                    'v2_enhancement': 'Enhanced emotional resonance'
                },
                'agitation_module': {
                    'order': 3,
                    'include': config['include_agitation_module'],
                    'components': [
                        'Consequence amplification',
                        'Cost of inaction',
                        'Time-sensitive urgency',
                        'Failure scenario painting'
                    ],
                    'estimated_words': 250,
                    'v2_enhancement': '+20-35% conversion boost',
                    'conversion_impact': 'High'
                },
                'solution_section': {
                    'order': 4,
                    'components': [
                        'Solution introduction',
                        'How it works explanation',
                        'Unique mechanism reveal',
                        'Scientific backing'
                    ],
                    'estimated_words': 300,
                    'mobile_considerations': 'Use expandable sections'
                },
                'benefits_section': {
                    'order': 5,
                    'components': [
                        'Feature-Advantage-Benefit matrix',
                        'Transformation promises',
                        'Outcome visualization',
                        'Lifestyle improvements'
                    ],
                    'estimated_words': 400,
                    'layout': 'Icon + headline + description format'
                },
                'social_proof_section': {
                    'order': 6,
                    'components': [
                        'Customer testimonials',
                        'Before/after showcases',
                        'Expert endorsements',
                        'Media mentions',
                        'Usage statistics'
                    ],
                    'estimated_words': 350,
                    'mobile_considerations': 'Carousel format for testimonials'
                },
                'comparison_table': {
                    'order': 7,
                    'include': config['include_comparison_table'],
                    'components': [
                        'Product vs competitors',
                        'Feature comparison matrix',
                        'Value justification',
                        'Unique differentiators'
                    ],
                    'estimated_words': 200,
                    'v2_enhancement': '+15-25% conversion boost',
                    'mobile_considerations': 'Horizontal scrolling table'
                },
                'audience_qualifier': {
                    'order': 8,
                    'include': config['audience_qualifier'],
                    'components': [
                        'Is this right for you quiz',
                        'Qualification criteria',
                        'Exclusion warnings',
                        'Perfect fit indicators'
                    ],
                    'estimated_words': 150,
                    'v2_enhancement': '+10-20% conversion boost'
                },
                'final_cta_section': {
                    'order': 9,
                    'components': [
                        'Final emotional appeal',
                        'Primary CTA button',
                        'What happens next roadmap' if config['include_roadmap'] else None,
                        'Risk reversal guarantee',
                        'Urgency reinforcement',
                        'Secondary CTA option'
                    ],
                    'estimated_words': 300,
                    'conversion_focus': 'Maximum conversion optimization'
                }
            },
            'v2_enhancements_summary': {
                'agitation_module': {
                    'included': config['include_agitation_module'],
                    'impact': '+20-35% conversion boost'
                },
                'comparison_table': {
                    'included': config['include_comparison_table'],
                    'impact': '+15-25% conversion boost'
                },
                'audience_qualifier': {
                    'included': config['audience_qualifier'],
                    'impact': '+10-20% conversion boost'
                },
                'what_happens_next': {
                    'included': config['include_roadmap'],
                    'impact': '+10-15% conversion boost'
                }
            },
            'technical_specifications': {
                'mobile_optimization': config['mobile_optimization'],
                'responsive_breakpoints': ['320px', '768px', '1024px', '1440px'],
                'loading_optimization': 'Progressive enhancement',
                'accessibility_level': 'WCAG 2.1 AA compliance'
            },
            'content_guidelines': {
                'tone': config['tone_personality'],
                'reading_level': 'Grade 8-10 (accessible)',
                'sentence_length': 'Average 15-20 words',
                'paragraph_length': '2-4 sentences max',
                'call_to_action_frequency': 'Every 300-500 words'
            }
        }

        return outline_data

    def _show_completed_summary(self):
        """Show outline summary"""

        if not self.state_manager:
            return

        st.success("✅ **Step 2 Complete** - V2.0 Enhanced landing page outline generated!")

        step_data = self.state_manager.get_step_data(2)
        outline_data = step_data.get('outline_structure', {})
        config = step_data.get('configuration', {})

        # Show outline metrics
        col1, col2, col3, col4 = st.columns(4)

        metadata = outline_data.get('page_metadata', {})
        with col1:
            st.metric("Page Type", config.get('page_type', 'N/A'))
        with col2:
            st.metric("Est. Length", metadata.get('estimated_length', 'N/A'))
        with col3:
            st.metric("Mobile-First", "✅" if config.get('mobile_optimization') else "❌")
        with col4:
            st.metric("Content Depth", f"{config.get('content_depth', 0)}/5")

        # V2.0 Enhancements
        with st.expander("🚀 V2.0 Enhancements Included"):
            v2_enhancements = outline_data.get('v2_enhancements_summary', {})

            for enhancement, details in v2_enhancements.items():
                if details.get('included'):
                    st.write(f"✅ **{enhancement.replace('_', ' ').title()}** - {details.get('impact', 'N/A')}")
                else:
                    st.write(f"❌ **{enhancement.replace('_', ' ').title()}** - Not included")

        # Section structure
        with st.expander("📋 Landing Page Structure"):
            section_structure = outline_data.get('section_structure', {})

            for section_name, section_data in section_structure.items():
                if section_data.get('include', True):  # Include by default if not specified
                    order = section_data.get('order', 0)
                    words = section_data.get('estimated_words', 0)
                    enhancement = section_data.get('v2_enhancement', '')

                    st.write(f"**{order}. {section_name.replace('_', ' ').title()}** ({words} words)")
                    if enhancement:
                        st.write(f"   🚀 V2.0: {enhancement}")

                    components = section_data.get('components', [])
                    if components:
                        for component in components[:3]:  # Show first 3 components
                            if component:  # Skip None values
                                st.write(f"   • {component}")
                    st.write("")

        # Technical specs
        with st.expander("⚙️ Technical Specifications"):
            tech_specs = outline_data.get('technical_specifications', {})
            content_guidelines = outline_data.get('content_guidelines', {})

            col1, col2 = st.columns(2)
            with col1:
                st.write("**Technical:**")
                st.write(f"• Mobile Optimization: {tech_specs.get('mobile_optimization', 'N/A')}")
                st.write(f"• Accessibility: {tech_specs.get('accessibility_level', 'N/A')}")

            with col2:
                st.write("**Content Guidelines:**")
                st.write(f"• Tone: {content_guidelines.get('tone', 'N/A')}")
                st.write(f"• Reading Level: {content_guidelines.get('reading_level', 'N/A')}")

    def _reset_step(self):
        """Reset step 2 data"""
        if self.state_manager:
            st.session_state.workflow_data['step_2_completed'] = False
            st.session_state.workflow_data['step_2_data'] = {}
