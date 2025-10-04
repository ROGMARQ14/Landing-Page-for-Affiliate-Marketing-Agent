import streamlit as st
import json
import time
from datetime import datetime
import base64
from io import BytesIO
import zipfile
import re

# Page configuration
st.set_page_config(
    page_title="PPC Landing Page Generator V2.0",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import custom modules - with error handling
try:
    from modules.step_1_research import ProductResearchModule
    from modules.step_2_outline import OutlineModule  
    from modules.step_3_hero import HeroModule
    from modules.step_4_pas_copy import PASModule
    from modules.step_5_social_proof import SocialProofModule
    from modules.step_6_final_cta import FinalCTAModule
    from modules.step_7_assembly import AssemblyModule
    from modules.step_8_design import DesignModule
    from ai_providers.ai_manager import AIManager
    from outputs.output_generator import OutputGenerator
    from utils.state_management import StateManager
    from utils.validation import ValidationHelper
except ImportError as e:
    st.error(f"Import Error: {str(e)}")
    st.error("Please ensure all module files are present and correctly formatted.")
    st.stop()

# Custom CSS for better UI
def load_custom_css():
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #FF6B35, #F7931E);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }

    .step-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #FF6B35;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }

    .progress-bar {
        background: #f0f0f0;
        border-radius: 10px;
        height: 20px;
        margin: 1rem 0;
    }

    .progress-fill {
        background: linear-gradient(90deg, #FF6B35, #F7931E);
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }

    .sidebar-nav {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }

    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }

    .warning-message {
        background: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #ffeaa7;
        margin: 1rem 0;
    }

    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    load_custom_css()

    # Initialize state management
    state_manager = StateManager()
    state_manager.initialize_session_state()

    # Header
    st.markdown('<div class="main-header">🚀 PPC Landing Page Generator V2.0</div>', unsafe_allow_html=True)
    st.markdown("*Powered by Problem-Agitate-Solution Framework & Affiliate Marketing Best Practices*")

    # Sidebar - Project Info & Navigation
    with st.sidebar:
        st.markdown("## 📋 Project Dashboard")

        # Project Name Input
        project_name = st.text_input(
            "Project Name",
            value=st.session_state.workflow_data.get('project_name', ''),
            placeholder="e.g., Keto Supplement Landing Page"
        )
        if project_name:
            st.session_state.workflow_data['project_name'] = project_name

        # AI Model Selection
        st.markdown("### 🤖 AI Model Selection")
        ai_models = {
            "GPT-4 Turbo": {"model": "gpt-4-turbo-preview", "cost": "$$", "speed": "Medium"},
            "Claude 3.5 Sonnet": {"model": "claude-3-5-sonnet-20240620", "cost": "$$$", "speed": "Fast"},
            "Gemini 1.5 Pro": {"model": "gemini-1.5-pro", "cost": "$", "speed": "Fast"},
            "GPT-4": {"model": "gpt-4", "cost": "$$$", "speed": "Slow"}
        }

        selected_ai = st.selectbox(
            "Choose AI Model",
            list(ai_models.keys()),
            index=0
        )
        st.session_state.workflow_data['selected_model'] = ai_models[selected_ai]["model"]

        # Display model info
        st.info(f"**Cost:** {ai_models[selected_ai]['cost']} | **Speed:** {ai_models[selected_ai]['speed']}")

        # Progress Tracking
        st.markdown("### 📊 Progress Tracking")
        steps_completed = sum([
            st.session_state.workflow_data.get(f'step_{i}_completed', False) 
            for i in range(1, 9)
        ])
        progress_percentage = (steps_completed / 8) * 100

        # Custom progress bar
        st.markdown(f"""
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress_percentage}%"></div>
        </div>
        <p style="text-align: center; margin: 0.5rem 0;">
            {steps_completed}/8 Steps Complete ({progress_percentage:.0f}%)
        </p>
        """, unsafe_allow_html=True)

        # Navigation Menu
        st.markdown("### 🧭 Navigation")
        step_names = [
            "🔍 Product Research",
            "📋 Landing Page Outline", 
            "🎯 Hero Section Copy",
            "📝 Problem-Agitate-Solution",
            "⭐ Social Proof & Comparisons",
            "🎬 Final CTA & Roadmap",
            "🔧 Assembly & Consistency",
            "🎨 Design & Technical"
        ]

        # Create navigation buttons
        for i, step_name in enumerate(step_names, 1):
            is_completed = st.session_state.workflow_data.get(f'step_{i}_completed', False)
            is_current = st.session_state.workflow_data.get('current_step', 1) == i

            if is_completed:
                status_icon = "✅"
            elif is_current:
                status_icon = "⏳"
            else:
                status_icon = "⏸️"

            button_label = f"{status_icon} Step {i}: {step_name[2:]}"  # Remove emoji from step name

            if st.button(button_label, key=f"nav_{i}", use_container_width=True):
                st.session_state.workflow_data['current_step'] = i
                st.rerun()

        # Project Actions
        st.markdown("### ⚙️ Project Actions")

        # Save/Load Project
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save Project", use_container_width=True):
                save_project()
        with col2:
            if st.button("📁 Load Project", use_container_width=True):
                load_project()

        # Export Options (only show if workflow is complete)
        if steps_completed == 8:
            st.markdown("### 📤 Export Options")
            export_options()

    # Main Content Area
    current_step = st.session_state.workflow_data.get('current_step', 1)

    # Step modules mapping
    step_modules = {
        1: ProductResearchModule(),
        2: OutlineModule(),
        3: HeroModule(),
        4: PASModule(),
        5: SocialProofModule(),
        6: FinalCTAModule(),
        7: AssemblyModule(),
        8: DesignModule()
    }

    # Display current step
    if current_step in step_modules:
        step_modules[current_step].render()

    # Navigation buttons at bottom
    render_navigation_buttons(current_step)

    # Footer
    st.markdown("---")
    st.markdown("*Built with ❤️ using Streamlit | V2.0 Enhanced with Affiliate Marketing Best Practices*")

def save_project():
    """Save current project state to JSON"""
    project_data = st.session_state.workflow_data.copy()
    project_data['saved_at'] = datetime.now().isoformat()

    json_data = json.dumps(project_data, indent=2, default=str)
    st.download_button(
        label="📥 Download Project File",
        data=json_data,
        file_name=f"{project_data.get('project_name', 'landing_page_project')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )

def load_project():
    """Load project state from uploaded JSON"""
    uploaded_file = st.file_uploader(
        "Choose project file",
        type="json",
        key="project_loader"
    )

    if uploaded_file is not None:
        try:
            project_data = json.loads(uploaded_file.getvalue())
            st.session_state.workflow_data.update(project_data)
            st.success("✅ Project loaded successfully!")
            time.sleep(1)
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error loading project: {str(e)}")

def export_options():
    """Generate and provide export options"""
    output_generator = OutputGenerator()

    # HTML Export
    if st.button("📄 Generate HTML Landing Page", use_container_width=True):
        with st.spinner("Generating HTML..."):
            html_content = output_generator.generate_html(st.session_state.workflow_data)
            st.download_button(
                label="📥 Download HTML File",
                data=html_content,
                file_name=f"{st.session_state.workflow_data.get('project_name', 'landing_page')}.html",
                mime="text/html"
            )

    # Markdown Export
    if st.button("📝 Generate Markdown Document", use_container_width=True):
        with st.spinner("Generating Markdown..."):
            markdown_content = output_generator.generate_markdown(st.session_state.workflow_data)
            st.download_button(
                label="📥 Download Markdown File", 
                data=markdown_content,
                file_name=f"{st.session_state.workflow_data.get('project_name', 'landing_page')}.md",
                mime="text/markdown"
            )

    # Word Document Export
    if st.button("📄 Generate Word Document", use_container_width=True):
        with st.spinner("Generating Word Document..."):
            try:
                docx_content = output_generator.generate_docx(st.session_state.workflow_data)
                st.download_button(
                    label="📥 Download Word Document",
                    data=docx_content,
                    file_name=f"{st.session_state.workflow_data.get('project_name', 'landing_page')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            except ImportError:
                st.warning("⚠️ Word document generation requires python-docx package. HTML and Markdown exports are available.")

    # Complete Package Export
    if st.button("📦 Generate Complete Package", use_container_width=True):
        with st.spinner("Generating complete package..."):
            zip_content = output_generator.generate_complete_package(st.session_state.workflow_data)
            st.download_button(
                label="📥 Download Complete Package (ZIP)",
                data=zip_content,
                file_name=f"{st.session_state.workflow_data.get('project_name', 'landing_page')}_package.zip",
                mime="application/zip"
            )

def render_navigation_buttons(current_step):
    """Render Previous/Next navigation buttons"""
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if current_step > 1:
            if st.button("⬅️ Previous Step", use_container_width=True):
                st.session_state.workflow_data['current_step'] = current_step - 1
                st.rerun()

    with col3:
        if current_step < 8:
            # Check if current step is completed before allowing next
            current_step_completed = st.session_state.workflow_data.get(f'step_{current_step}_completed', False)
            if current_step_completed:
                if st.button("Next Step ➡️", use_container_width=True):
                    st.session_state.workflow_data['current_step'] = current_step + 1
                    st.rerun()
            else:
                st.button("Complete Current Step First", disabled=True, use_container_width=True)

if __name__ == "__main__":
    main()
