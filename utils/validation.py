import streamlit as st
import re
from urllib.parse import urlparse
from typing import Dict, Any, List, Optional

class ValidationHelper:
    """Utility class for input validation and data verification"""

    @staticmethod
    def validate_url(url: str) -> Dict[str, Any]:
        """Validate URL format and accessibility"""
        if not url:
            return {'valid': False, 'error': 'URL is empty'}

        try:
            result = urlparse(url)
            if not result.scheme or not result.netloc:
                return {'valid': False, 'error': 'Invalid URL format'}

            if result.scheme not in ['http', 'https']:
                return {'valid': False, 'error': 'URL must use http or https'}

            return {'valid': True, 'parsed': result}

        except Exception as e:
            return {'valid': False, 'error': f'URL parsing error: {str(e)}'}

    @staticmethod
    def validate_email(email: str) -> Dict[str, Any]:
        """Validate email format"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if re.match(email_pattern, email):
            return {'valid': True}
        else:
            return {'valid': False, 'error': 'Invalid email format'}

    @staticmethod
    def validate_phone(phone: str) -> Dict[str, Any]:
        """Validate phone number format"""
        # Remove all non-digit characters
        digits_only = re.sub(r'[^0-9]', '', phone)

        if len(digits_only) >= 10:
            return {'valid': True, 'cleaned': digits_only}
        else:
            return {'valid': False, 'error': 'Phone number must have at least 10 digits'}

    @staticmethod
    def validate_text_length(text: str, min_length: int = 0, max_length: int = None) -> Dict[str, Any]:
        """Validate text length constraints"""
        length = len(text.strip())

        if length < min_length:
            return {'valid': False, 'error': f'Text must be at least {min_length} characters'}

        if max_length and length > max_length:
            return {'valid': False, 'error': f'Text must be no more than {max_length} characters'}

        return {'valid': True, 'length': length}

    @staticmethod
    def validate_keyword_density(text: str, keywords: List[str], max_density: float = 0.05) -> Dict[str, Any]:
        """Validate keyword density for SEO"""
        if not text or not keywords:
            return {'valid': True, 'densities': {}}

        text_lower = text.lower()
        word_count = len(text.split())
        densities = {}
        issues = []

        for keyword in keywords:
            keyword_lower = keyword.lower()
            keyword_count = text_lower.count(keyword_lower)
            density = keyword_count / word_count if word_count > 0 else 0
            densities[keyword] = {
                'count': keyword_count,
                'density': density,
                'percentage': density * 100
            }

            if density > max_density:
                issues.append(f"Keyword '{keyword}' density {density*100:.1f}% exceeds {max_density*100}%")

        return {
            'valid': len(issues) == 0,
            'densities': densities,
            'issues': issues
        }

    @staticmethod
    def validate_reading_level(text: str, target_grade_level: int = 8) -> Dict[str, Any]:
        """Estimate reading level using Flesch-Kincaid grade level"""
        if not text:
            return {'valid': False, 'error': 'No text provided'}

        # Simple approximation (in production, use textstat library)
        sentences = len(re.split(r'[.!?]+', text))
        words = len(text.split())
        syllables = len(re.findall(r'[aeiouAEIOU]', text))  # Rough syllable count

        if sentences == 0 or words == 0:
            return {'valid': False, 'error': 'Invalid text structure'}

        # Simplified Flesch-Kincaid formula
        avg_sentence_length = words / sentences
        avg_syllables_per_word = syllables / words
        grade_level = (0.39 * avg_sentence_length) + (11.8 * avg_syllables_per_word) - 15.59

        return {
            'valid': grade_level <= target_grade_level,
            'grade_level': max(1, round(grade_level, 1)),
            'target': target_grade_level,
            'recommendation': 'Consider shorter sentences' if grade_level > target_grade_level else 'Good readability'
        }

    @staticmethod
    def validate_cta_text(cta_text: str) -> Dict[str, Any]:
        """Validate CTA button text for best practices"""
        issues = []
        warnings = []

        # Length check
        if len(cta_text) < 2:
            issues.append("CTA text too short")
        elif len(cta_text) > 25:
            warnings.append("CTA text may be too long for mobile")

        # Action words
        action_words = ['get', 'start', 'try', 'download', 'buy', 'order', 'join', 'access', 'claim', 'discover']
        has_action = any(word in cta_text.lower() for word in action_words)

        if not has_action:
            warnings.append("Consider adding an action word (Get, Start, Try, etc.)")

        # Urgency/value indicators
        urgency_words = ['now', 'today', 'free', 'instant', 'immediately', 'limited', 'exclusive']
        has_urgency = any(word in cta_text.lower() for word in urgency_words)

        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings,
            'has_action_word': has_action,
            'has_urgency': has_urgency,
            'length': len(cta_text)
        }

    @staticmethod
    def validate_headline_structure(headline: str) -> Dict[str, Any]:
        """Validate headline for best practices"""
        issues = []
        warnings = []

        # Length check
        word_count = len(headline.split())
        if word_count < 4:
            issues.append("Headline too short (minimum 4 words)")
        elif word_count > 12:
            warnings.append("Headline may be too long (consider 6-10 words)")

        # Character count for SEO
        char_count = len(headline)
        if char_count > 60:
            warnings.append("Headline over 60 characters may be truncated in search results")

        # Power words check
        power_words = [
            'secret', 'proven', 'guaranteed', 'exclusive', 'limited', 'breakthrough',
            'ultimate', 'complete', 'essential', 'advanced', 'professional', 'expert'
        ]
        has_power_words = any(word in headline.lower() for word in power_words)

        # Numbers check
        has_numbers = bool(re.search(r'\d', headline))

        # Question format
        is_question = headline.strip().endswith('?')

        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings,
            'word_count': word_count,
            'character_count': char_count,
            'has_power_words': has_power_words,
            'has_numbers': has_numbers,
            'is_question': is_question,
            'recommendations': [
                'Add specific numbers or statistics' if not has_numbers else None,
                'Consider adding power words for impact' if not has_power_words else None,
                'Keep under 60 characters for SEO' if char_count > 60 else None
            ]
        }

    @staticmethod
    def validate_json_structure(json_data: Dict[str, Any], required_fields: List[str]) -> Dict[str, Any]:
        """Validate JSON data structure"""
        missing_fields = []

        for field in required_fields:
            if field not in json_data:
                missing_fields.append(field)

        return {
            'valid': len(missing_fields) == 0,
            'missing_fields': missing_fields,
            'provided_fields': list(json_data.keys())
        }

    @staticmethod
    def validate_color_hex(color: str) -> Dict[str, Any]:
        """Validate hex color code"""
        hex_pattern = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'

        if re.match(hex_pattern, color):
            return {'valid': True}
        else:
            return {'valid': False, 'error': 'Invalid hex color format (use #RRGGBB or #RGB)'}

    @staticmethod
    def validate_image_requirements(image_info: Dict[str, Any]) -> Dict[str, Any]:
        """Validate image meets requirements"""
        issues = []
        warnings = []

        # File size check (if provided)
        if 'file_size' in image_info:
            size_kb = image_info['file_size'] / 1024
            if size_kb > 100:
                warnings.append(f"Image size {size_kb:.0f}KB exceeds 100KB recommendation")

        # Format check
        if 'format' in image_info:
            recommended_formats = ['webp', 'jpg', 'jpeg', 'png']
            if image_info['format'].lower() not in recommended_formats:
                warnings.append(f"Consider using WebP, JPEG, or PNG format")

        # Dimensions check
        if 'width' in image_info and 'height' in image_info:
            width, height = image_info['width'], image_info['height']
            aspect_ratio = width / height

            # Common aspect ratios
            if aspect_ratio < 0.5 or aspect_ratio > 3:
                warnings.append("Unusual aspect ratio may cause layout issues")

        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings
        }
