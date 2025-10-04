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

class DesignModule:
    """Step 8: Design & Technical Specifications"""

    def __init__(self):
        try:
            self.ai_manager = AIManager()
            self.state_manager = StateManager()
        except Exception as e:
            st.error(f"Error initializing DesignModule: {str(e)}")
            self.ai_manager = None
            self.state_manager = None

    def render(self):
        """Render Step 8 UI"""
        st.markdown("# 🎨 Step 8: Design & Technical Specifications")
        st.markdown("*Create visual design guidelines and technical requirements*")

        st.progress(8/8, text="Step 8 of 8 - Final Step!")

        if not self.state_manager:
            st.error("❌ State management not available. Please check your installation.")
            return

        if not self.state_manager.is_step_completed(7):
            st.warning("⚠️ Please complete Step 7 (Assembly) first")
            return

        if self.state_manager.is_step_completed(8):
            self._show_completed_summary()
            if st.button("🔄 Regenerate Design Specs"):
                self._reset_step()
                st.rerun()
            return

        # Design configuration
        with st.form("design_specifications_form"):
            st.markdown("## 🎨 Design Configuration")

            col1, col2 = st.columns(2)

            with col1:
                color_scheme = st.selectbox(
                    "Color Scheme",
                    ["Professional Blue", "Conversion Orange", "Health Green", "Trust Navy", "Custom"],
                    help="Primary color scheme for the landing page"
                )

                layout_style = st.selectbox(
                    "Layout Style",
                    ["Modern Minimalist", "Classic Sales Page", "Magazine Style", "Video-First"],
                    help="Overall layout approach"
                )

                font_style = st.selectbox(
                    "Typography Style",
                    ["Modern Sans-Serif", "Classic Serif", "Bold Impact", "Clean Readable"],
                    help="Font family and style approach"
                )

            with col2:
                visual_hierarchy = st.selectbox(
                    "Visual Hierarchy",
                    ["Strong Contrast", "Subtle Gradients", "Bold Headlines", "Balanced Mix"],
                    help="How to create visual emphasis"
                )

                button_style = st.selectbox(
                    "CTA Button Style",
                    ["3D Raised", "Flat Modern", "Gradient", "Outlined"],
                    help="Style for call-to-action buttons"
                )

                image_strategy = st.selectbox(
                    "Image Strategy",
                    ["Product Focus", "Lifestyle Focus", "Before/After Focus", "Mixed Content"],
                    help="Primary image and visual content approach"
                )

            # Advanced design options
            with st.expander("🔧 Advanced Design Options"):
                mobile_first = st.checkbox(
                    "Mobile-First Design",
                    value=True,
                    help="Optimize design for mobile devices first"
                )

                animation_level = st.selectbox(
                    "Animation Level",
                    ["None", "Subtle", "Moderate", "Dynamic"],
                    index=1,
                    help="Level of animations and interactions"
                )

                trust_signals_design = st.multiselect(
                    "Trust Signal Design Elements",
                    ["Security Badges", "Testimonial Cards", "Guarantee Seals", "Social Proof Counters"],
                    default=["Security Badges", "Testimonial Cards", "Guarantee Seals"],
                    help="Visual trust elements to include"
                )

                conversion_optimization_focus = st.selectbox(
                    "Conversion Optimization Focus",
                    ["Button Prominence", "Urgency Elements", "Social Proof", "Risk Reversal"],
                    help="Primary design focus for conversion"
                )

            submitted = st.form_submit_button("🎨 Generate Design Specifications", type="primary")

        if submitted:
            self._generate_design_specs({
                'color_scheme': color_scheme,
                'layout_style': layout_style,
                'font_style': font_style,
                'visual_hierarchy': visual_hierarchy,
                'button_style': button_style,
                'image_strategy': image_strategy,
                'mobile_first': mobile_first,
                'animation_level': animation_level,
                'trust_signals_design': trust_signals_design,
                'conversion_optimization_focus': conversion_optimization_focus
            })

    def _generate_design_specs(self, config: Dict[str, Any]):
        """Generate design and technical specifications"""

        if not self.ai_manager or not self.state_manager:
            st.error("❌ Required services not available")
            return

        with st.spinner("🎨 Generating comprehensive design specifications..."):

            # Get all previous steps data for context
            try:
                all_steps_data = {}
                for step in range(1, 8):
                    if self.state_manager.is_step_completed(step):
                        all_steps_data[f'step_{step}'] = self.state_manager.get_step_data(step)
            except Exception as e:
                st.error(f"Error getting previous steps data: {str(e)}")
                return

            # Create design specifications prompt
            design_prompt = self._create_design_prompt(config, all_steps_data)

            try:
                response = self.ai_manager.generate_content(
                    prompt=design_prompt,
                    model=st.session_state.workflow_data['selected_model'],
                    temperature=0.4,
                    max_tokens=2500
                )

                if response.get('success', False):
                    # Create structured design data
                    design_data = self._create_design_structure(config, response, all_steps_data)

                    # Save data
                    self.state_manager.save_step_data(8, {
                        'design_specifications': design_data,
                        'configuration': config,
                        'ai_response': response,
                        'generated_at': datetime.now().isoformat()
                    })
                    self.state_manager.mark_step_completed(8)

                    st.success("✅ Design specifications generated! Landing page creation complete!")
                    st.balloons()  # Celebration for completing all steps
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error(f"❌ Design generation failed: {response.get('error', 'Unknown error')}")

            except Exception as e:
                st.error(f"❌ Error generating design specifications: {str(e)}")

    def _create_design_prompt(self, config: Dict[str, Any], all_steps_data: Dict[str, Any]) -> str:
        """Create design specifications prompt"""

        # Extract key information from previous steps
        step_1_data = all_steps_data.get('step_1', {})
        form_inputs = step_1_data.get('form_inputs', {}) if step_1_data else {}
        product_category = form_inputs.get('product_category', 'Health & Wellness')
        target_audience = form_inputs.get('target_audience', 'Target customers')

        prompt = f"""# Design & Technical Specifications Generation

## Context
Product Category: {product_category}
Target Audience: {target_audience}

## Design Configuration
- Color Scheme: {config['color_scheme']}
- Layout Style: {config['layout_style']}
- Typography: {config['font_style']}
- Visual Hierarchy: {config['visual_hierarchy']}
- Button Style: {config['button_style']}
- Image Strategy: {config['image_strategy']}
- Mobile First: {config['mobile_first']}
- Animation Level: {config['animation_level']}

## Task
Create comprehensive design and technical specifications for the landing page.

### Design Specifications:

1. **Color Palette & Branding**
   - Primary colors (hex codes)
   - Secondary colors
   - Accent colors for CTAs
   - Background colors
   - Text color hierarchy

2. **Typography System**
   - Font families for headers and body
   - Font sizes for different elements
   - Line heights and spacing
   - Font weights and styles

3. **Layout & Spacing**
   - Grid system specifications
   - Section padding and margins
   - Mobile breakpoints
   - Container widths

4. **Component Design**
   - Button designs and hover states
   - Form element styling
   - Card and testimonial designs
   - Navigation and header

5. **Visual Elements**
   - Image specifications and formats
   - Icon style and usage
   - Graphic element guidelines
   - Video placeholder designs

6. **Mobile Optimization**
   - Responsive breakpoints
   - Mobile-specific adjustments
   - Touch target sizes
   - Performance optimizations

7. **Technical Requirements**
   - HTML structure recommendations
   - CSS framework suggestions
   - JavaScript requirements
   - Performance optimization

8. **Conversion Optimization**
   - CTA button optimization
   - Visual hierarchy for conversion
   - Trust signal placement
   - Urgency element styling

Return structured design specifications ready for implementation.
"""

        return prompt

    def _create_design_structure(self, config: Dict[str, Any], ai_response: Dict[str, Any], 
                                all_steps_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create structured design specifications"""

        # Create comprehensive design specifications
        design_data = {
            'color_palette': {
                'scheme_name': config['color_scheme'],
                'primary_colors': {
                    'primary': '#2563EB' if config['color_scheme'] == 'Professional Blue' else '#EA580C' if config['color_scheme'] == 'Conversion Orange' else '#059669',
                    'primary_dark': '#1D4ED8' if config['color_scheme'] == 'Professional Blue' else '#C2410C' if config['color_scheme'] == 'Conversion Orange' else '#047857',
                    'primary_light': '#3B82F6' if config['color_scheme'] == 'Professional Blue' else '#FB923C' if config['color_scheme'] == 'Conversion Orange' else '#10B981'
                },
                'secondary_colors': {
                    'secondary': '#64748B',
                    'secondary_light': '#94A3B8',
                    'secondary_dark': '#475569'
                },
                'accent_colors': {
                    'cta_primary': '#EF4444',
                    'cta_secondary': '#F59E0B',
                    'success': '#10B981',
                    'warning': '#F59E0B',
                    'error': '#EF4444'
                },
                'neutral_colors': {
                    'white': '#FFFFFF',
                    'gray_50': '#F8FAFC',
                    'gray_100': '#F1F5F9',
                    'gray_200': '#E2E8F0',
                    'gray_800': '#1E293B',
                    'black': '#0F172A'
                },
                'text_colors': {
                    'primary_text': '#0F172A',
                    'secondary_text': '#475569',
                    'light_text': '#64748B',
                    'white_text': '#FFFFFF'
                }
            },
            'typography_system': {
                'font_families': {
                    'primary': 'Inter, system-ui, -apple-system, sans-serif' if config['font_style'] == 'Modern Sans-Serif' else 'Georgia, serif' if config['font_style'] == 'Classic Serif' else 'Poppins, sans-serif',
                    'secondary': 'Inter, system-ui, -apple-system, sans-serif',
                    'monospace': 'JetBrains Mono, monospace'
                },
                'font_sizes': {
                    'h1': {'desktop': '3.5rem', 'mobile': '2.5rem'},
                    'h2': {'desktop': '2.5rem', 'mobile': '2rem'},
                    'h3': {'desktop': '2rem', 'mobile': '1.75rem'},
                    'h4': {'desktop': '1.5rem', 'mobile': '1.25rem'},
                    'body_large': {'desktop': '1.25rem', 'mobile': '1.125rem'},
                    'body': {'desktop': '1rem', 'mobile': '1rem'},
                    'small': {'desktop': '0.875rem', 'mobile': '0.875rem'}
                },
                'line_heights': {
                    'tight': 1.25,
                    'normal': 1.5,
                    'relaxed': 1.75
                },
                'font_weights': {
                    'light': 300,
                    'normal': 400,
                    'medium': 500,
                    'semibold': 600,
                    'bold': 700,
                    'black': 900
                }
            },
            'layout_specifications': {
                'layout_style': config['layout_style'],
                'container_widths': {
                    'max_width': '1200px',
                    'section_max_width': '1000px',
                    'content_max_width': '800px'
                },
                'breakpoints': {
                    'mobile': '640px',
                    'tablet': '768px', 
                    'desktop': '1024px',
                    'large_desktop': '1280px'
                },
                'spacing_system': {
                    'xs': '0.5rem',
                    'sm': '1rem',
                    'md': '1.5rem',
                    'lg': '2rem',
                    'xl': '3rem',
                    'xxl': '4rem'
                },
                'section_spacing': {
                    'hero_padding': {'desktop': '4rem 2rem', 'mobile': '3rem 1rem'},
                    'content_padding': {'desktop': '3rem 2rem', 'mobile': '2rem 1rem'},
                    'section_margin': {'desktop': '4rem 0', 'mobile': '3rem 0'}
                }
            },
            'component_designs': {
                'buttons': {
                    'primary_cta': {
                        'style': config['button_style'],
                        'background': '#EF4444',
                        'color': '#FFFFFF',
                        'padding': '1rem 2rem',
                        'border_radius': '0.5rem',
                        'font_weight': 'bold',
                        'font_size': '1.125rem',
                        'hover_background': '#DC2626',
                        'box_shadow': '0 4px 6px -1px rgba(0, 0, 0, 0.1)' if config['button_style'] == '3D Raised' else 'none',
                        'min_height': '48px',
                        'mobile_full_width': True
                    },
                    'secondary_cta': {
                        'style': 'outlined',
                        'background': 'transparent',
                        'color': '#2563EB',
                        'border': '2px solid #2563EB',
                        'padding': '0.75rem 1.5rem',
                        'border_radius': '0.5rem',
                        'hover_background': '#2563EB',
                        'hover_color': '#FFFFFF'
                    }
                },
                'forms': {
                    'input_fields': {
                        'padding': '0.75rem 1rem',
                        'border': '2px solid #E2E8F0',
                        'border_radius': '0.5rem',
                        'focus_border': '#2563EB',
                        'background': '#FFFFFF',
                        'font_size': '1rem'
                    }
                },
                'cards': {
                    'testimonial_cards': {
                        'background': '#FFFFFF',
                        'border': '1px solid #E2E8F0',
                        'border_radius': '1rem',
                        'padding': '1.5rem',
                        'box_shadow': '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                        'margin_bottom': '1.5rem'
                    }
                }
            },
            'visual_elements': {
                'image_specifications': {
                    'strategy': config['image_strategy'],
                    'hero_image': {
                        'format': 'WebP with JPG fallback',
                        'dimensions': {'desktop': '1200x800', 'mobile': '800x600'},
                        'optimization': 'Compressed for web, lazy loading'
                    },
                    'testimonial_images': {
                        'format': 'WebP with JPG fallback',
                        'dimensions': '150x150 (square)',
                        'style': 'Circular crop with border'
                    },
                    'product_images': {
                        'format': 'PNG with transparent background',
                        'dimensions': 'Various, maintain aspect ratio',
                        'style': 'Clean product shots on white/transparent'
                    }
                },
                'icons': {
                    'style': 'Outline style with consistent stroke width',
                    'size': '24px default, scalable',
                    'color': 'Primary or secondary text color'
                },
                'graphics': {
                    'style': 'Minimal, clean illustrations',
                    'color_usage': 'Brand colors only',
                    'complexity': 'Simple, professional'
                }
            },
            'mobile_optimization': {
                'mobile_first': config['mobile_first'],
                'responsive_strategy': 'Progressive enhancement' if config['mobile_first'] else 'Graceful degradation',
                'touch_targets': {
                    'minimum_size': '44px',
                    'recommended_size': '48px',
                    'spacing': '8px minimum between targets'
                },
                'mobile_specific': {
                    'navigation': 'Hamburger menu for mobile',
                    'forms': 'Single column layout',
                    'images': 'Optimized for mobile screens',
                    'text': 'Larger font sizes for readability'
                },
                'performance': {
                    'image_optimization': 'WebP format, lazy loading',
                    'css_optimization': 'Critical CSS inlined',
                    'javascript': 'Minimal, deferred loading'
                }
            },
            'technical_requirements': {
                'html_structure': {
                    'semantic_markup': True,
                    'accessibility': 'WCAG 2.1 AA compliance',
                    'seo_optimization': 'Proper heading hierarchy, meta tags'
                },
                'css_framework': {
                    'recommended': 'Tailwind CSS or custom CSS Grid/Flexbox',
                    'approach': 'Utility-first or component-based',
                    'browser_support': 'Modern browsers (ES6+)'
                },
                'javascript_requirements': {
                    'framework': 'Vanilla JS or lightweight library',
                    'features': ['Form validation', 'Smooth scrolling', 'Lazy loading'],
                    'performance': 'Minimize bundle size, async loading'
                },
                'performance_targets': {
                    'first_contentful_paint': '< 1.5s',
                    'largest_contentful_paint': '< 2.5s',
                    'cumulative_layout_shift': '< 0.1',
                    'first_input_delay': '< 100ms'
                }
            },
            'conversion_optimization': {
                'focus_area': config['conversion_optimization_focus'],
                'cta_optimization': {
                    'placement': 'Above fold, after social proof, at page end',
                    'color': 'High contrast, attention-grabbing',
                    'size': 'Prominent but not overwhelming',
                    'text': 'Action-oriented, benefit-focused'
                },
                'visual_hierarchy': {
                    'primary_elements': ['Headlines', 'CTA buttons', 'Key benefits'],
                    'secondary_elements': ['Testimonials', 'Features', 'Social proof'],
                    'supporting_elements': ['Fine print', 'Navigation', 'Footer']
                },
                'trust_signals': {
                    'placement': 'Near CTAs and throughout page',
                    'design': config['trust_signals_design'],
                    'prominence': 'Visible but not distracting'
                },
                'urgency_elements': {
                    'design': 'Attention-grabbing but tasteful',
                    'placement': 'Near CTAs and key decision points',
                    'style': 'Countdown timers, limited quantity badges'
                }
            },
            'animation_specifications': {
                'level': config['animation_level'],
                'animations': {
                    'none': [],
                    'subtle': ['Fade in on scroll', 'Button hover effects'],
                    'moderate': ['Slide in animations', 'Counter animations', 'Progress bars'],
                    'dynamic': ['Advanced scroll animations', 'Interactive elements', 'Video backgrounds']
                }[config['animation_level']],
                'performance_considerations': 'Use CSS transforms, avoid layout animations',
                'accessibility': 'Respect prefers-reduced-motion setting'
            }
        }

        return design_data

    def _show_completed_summary(self):
        """Show design specifications summary"""

        if not self.state_manager:
            return

        # Show celebration message
        st.success("🎉 **CONGRATULATIONS!** 🎉")
        st.success("✅ **All 8 Steps Complete** - Your high-converting landing page is ready!")

        step_data = self.state_manager.get_step_data(8)
        design_data = step_data.get('design_specifications', {})
        config = step_data.get('configuration', {})

        # Show design overview
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Color Scheme", config.get('color_scheme', 'N/A'))
        with col2:
            st.metric("Layout Style", config.get('layout_style', 'N/A'))
        with col3:
            st.metric("Typography", config.get('font_style', 'N/A'))
        with col4:
            st.metric("Mobile First", "✅" if config.get('mobile_first') else "❌")

        # Color palette preview
        with st.expander("🎨 Color Palette"):
            color_palette = design_data.get('color_palette', {})
            primary_colors = color_palette.get('primary_colors', {})
            accent_colors = color_palette.get('accent_colors', {})

            col1, col2 = st.columns(2)
            with col1:
                st.write("**Primary Colors:**")
                for color_name, color_code in primary_colors.items():
                    st.write(f"• {color_name.replace('_', ' ').title()}: `{color_code}`")

            with col2:
                st.write("**Accent Colors:**")
                for color_name, color_code in accent_colors.items():
                    st.write(f"• {color_name.replace('_', ' ').title()}: `{color_code}`")

        # Typography system
        with st.expander("📝 Typography System"):
            typography = design_data.get('typography_system', {})
            font_families = typography.get('font_families', {})
            font_sizes = typography.get('font_sizes', {})

            col1, col2 = st.columns(2)
            with col1:
                st.write("**Font Families:**")
                for font_type, font_family in font_families.items():
                    st.write(f"• {font_type.title()}: {font_family}")

            with col2:
                st.write("**Font Sizes (Desktop):**")
                for element, sizes in font_sizes.items():
                    if isinstance(sizes, dict):
                        desktop_size = sizes.get('desktop', 'N/A')
                        st.write(f"• {element.upper()}: {desktop_size}")

        # Layout specifications
        with st.expander("📐 Layout Specifications"):
            layout = design_data.get('layout_specifications', {})
            container_widths = layout.get('container_widths', {})
            breakpoints = layout.get('breakpoints', {})

            col1, col2 = st.columns(2)
            with col1:
                st.write("**Container Widths:**")
                for container, width in container_widths.items():
                    st.write(f"• {container.replace('_', ' ').title()}: {width}")

            with col2:
                st.write("**Responsive Breakpoints:**")
                for device, width in breakpoints.items():
                    st.write(f"• {device.title()}: {width}")

        # Component designs
        with st.expander("🔘 Component Designs"):
            components = design_data.get('component_designs', {})
            buttons = components.get('buttons', {})

            if buttons:
                primary_cta = buttons.get('primary_cta', {})
                st.write("**Primary CTA Button:**")
                st.write(f"• Style: {primary_cta.get('style', 'N/A')}")
                st.write(f"• Background: {primary_cta.get('background', 'N/A')}")
                st.write(f"• Padding: {primary_cta.get('padding', 'N/A')}")
                st.write(f"• Border Radius: {primary_cta.get('border_radius', 'N/A')}")
                st.write(f"• Min Height: {primary_cta.get('min_height', 'N/A')}")

        # Technical requirements
        with st.expander("⚙️ Technical Requirements"):
            technical = design_data.get('technical_requirements', {})
            performance_targets = technical.get('performance_targets', {})

            st.write("**Performance Targets:**")
            for metric, target in performance_targets.items():
                st.write(f"• {metric.replace('_', ' ').title()}: {target}")

            css_framework = technical.get('css_framework', {})
            if css_framework:
                st.write(f"**Recommended CSS Framework:** {css_framework.get('recommended', 'N/A')}")

        # Conversion optimization
        with st.expander("🎯 Conversion Optimization"):
            conversion = design_data.get('conversion_optimization', {})
            cta_optimization = conversion.get('cta_optimization', {})

            st.write("**CTA Optimization:**")
            for aspect, details in cta_optimization.items():
                st.write(f"• {aspect.replace('_', ' ').title()}: {details}")

            trust_signals = conversion.get('trust_signals', {})
            if trust_signals:
                trust_design = trust_signals.get('design', [])
                if trust_design:
                    st.write(f"**Trust Signals:** {', '.join(trust_design)}")

        # Final completion message
        st.markdown("---")
        st.markdown("### 🚀 **YOUR LANDING PAGE IS READY FOR DEPLOYMENT!**")

        completion_stats = {
            "Research Completed": "✅",
            "Structure Defined": "✅", 
            "Copy Generated": "✅",
            "Social Proof Added": "✅",
            "Design Specified": "✅",
            "Ready for Export": "✅"
        }

        cols = st.columns(3)
        for i, (stat, status) in enumerate(completion_stats.items()):
            with cols[i % 3]:
                st.write(f"{status} {stat}")

        st.info("💡 **Next Steps:** Use the Export Options in the sidebar to download your complete landing page package!")

    def _reset_step(self):
        """Reset step 8 data"""
        if self.state_manager:
            st.session_state.workflow_data['step_8_completed'] = False
            st.session_state.workflow_data['step_8_data'] = {}
