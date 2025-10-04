import streamlit as st
from ai_providers.ai_manager import AIManager
from utils.state_management import StateManager

class PASModule:
    """Step 4: Problem-Agitate-Solution Copy - V2.0 Enhanced"""

    def __init__(self):
        self.ai_manager = AIManager()
        self.state_manager = StateManager()

    def render(self):
        st.markdown("# 📝 Step 4: Problem-Agitate-Solution Copy")
        st.markdown("*V2.0 Enhanced with dedicated Agitation Module*")

        st.progress(4/8, text="Step 4 of 8")

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
                    ["Consequence-Based Bullets", "Failure Narrative", "Risk Statistics"]
                )

                benefits_format = st.selectbox(
                    "Benefits Format",
                    ["FAB Grid (Feature-Advantage-Benefit)", "Benefit Blocks"]
                )

            with col2:
                emotional_intensity = st.slider(
                    "Emotional Intensity", 
                    min_value=1, max_value=5, value=3,
                    help="1=Subtle, 3=Balanced, 5=High urgency"
                )

                include_statistics = st.checkbox(
                    "Include Supporting Statistics",
                    value=True
                )

            submitted = st.form_submit_button("📝 Generate PAS Copy", type="primary")

        if submitted:
            self._generate_pas_copy({
                'agitation_format': agitation_format,
                'benefits_format': benefits_format,
                'emotional_intensity': emotional_intensity,
                'include_statistics': include_statistics
            })

    def _generate_pas_copy(self, config):
        with st.spinner("📝 Generating Problem-Agitate-Solution copy..."):

            # Simplified PAS generation (would use full V2.0 prompt)
            pas_data = {
                'section_1_problem_identification': {
                    'problem_headline': {'copy': 'Struggling With Keto Flu Symptoms?'},
                    'empathetic_paragraph': {'copy': 'You've tried keto before. Day 3 hits and the headaches start. Brain fog sets in. Energy crashes. You end up quitting before you even enter ketosis, convinced keto "doesn't work for you."'}
                },
                'section_2_agitation_module': {
                    'agitation_headline': {'copy': 'Here's What Happens When You Keep Struggling'},
                    'agitation_content': {
                        'format_selected': config['agitation_format'],
                        'consequence_bullets': {
                            'bullets': [
                                {'consequence': 'Your keto attempts fail before reaching ketosis (wasted effort, ongoing frustration)'},
                                {'consequence': 'You experience 3-5 days of severe headaches (lost productivity, missed commitments)'},
                                {'consequence': 'You regain lost weight within weeks (yo-yo dieting damages metabolism)'},
                                {'consequence': 'You miss out on sustained fat loss and mental clarity benefits'}
                            ]
                        }
                    }
                },
                'section_3_solution_reveal': {
                    'solution_headline': {'copy': 'Enter Ketosis in 48 Hours—Without the Miserable Transition'},
                    'how_it_works': {
                        'steps': [
                            {'action': 'Take 2 capsules with breakfast', 'outcome': 'Floods cells with key electrolytes'},
                            {'action': 'Maintain optimal hydration', 'outcome': 'Prevent headaches and brain fog'},
                            {'action': 'Enter ketosis smoothly', 'outcome': 'Fat-burning mode without the crash'}
                        ]
                    }
                },
                'section_4_benefits_matrix': {
                    'format_selected': config['benefits_format'],
                    'benefit_blocks': {
                        'blocks': [
                            {
                                'headline': 'Rapid Ketosis Entry',
                                'feature_statement': 'Patent-pending electrolyte ratio',
                                'benefit_statement': 'Enter ketosis 40% faster than diet alone',
                                'emotional_payoff': 'Experience mental clarity from day one'
                            },
                            {
                                'headline': 'Zero Keto Flu',
                                'feature_statement': 'Balanced sodium, potassium, magnesium',
                                'benefit_statement': 'Prevent headaches and fatigue entirely',
                                'emotional_payoff': 'Stay productive during transition'
                            }
                        ]
                    }
                },
                'configuration': config
            }

            # Save data
            self.state_manager.save_step_data(4, {
                'pas_copy': pas_data,
                'configuration': config,
                'generated_at': st.session_state.workflow_data['last_updated']
            })
            self.state_manager.mark_step_completed(4)

            st.success("✅ Problem-Agitate-Solution copy generated!")
            st.rerun()

    def _show_completed_summary(self):
        st.success("✅ **Step 4 Complete** - PAS copy generated with V2.0 Agitation Module!")

        step_data = self.state_manager.get_step_data(4)
        pas_data = step_data.get('pas_copy', {})

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
                for bullet in bullets:
                    st.write(f"• {bullet.get('consequence', 'N/A')}")

            # Solution section
            st.markdown("### ✅ Solution Section")
            solution_data = pas_data.get('section_3_solution_reveal', {})
            st.write(f"**Headline:** {solution_data.get('solution_headline', {}).get('copy', 'N/A')}")

            steps = solution_data.get('how_it_works', {}).get('steps', [])
            if steps:
                st.write("**How It Works:**")
                for i, step in enumerate(steps, 1):
                    st.write(f"{i}. **{step.get('action', 'N/A')}** - {step.get('outcome', 'N/A')}")

    def _reset_step(self):
        st.session_state.workflow_data['step_4_completed'] = False
        st.session_state.workflow_data['step_4_data'] = {}
