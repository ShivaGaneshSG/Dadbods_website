"""
Global context processors for DadBods website.
Provides image paths, brand metadata, and settings-driven choices to all templates.
"""

from django.conf import settings
from config.image_config import get_image_config


def dadbods_global_context(request):
    """
    Exposes configured image paths, coach profiles, transformation data,
    and site metadata to all Django templates cleanly.
    """
    images_data = get_image_config()

    return {
        "dadbods_images": images_data,
        "coaching_budget_choices": getattr(settings, "COACHING_BUDGET_CHOICES", []),
        "brand": {
            "name": "DadBods",
            "tagline": "Elite Tamil Fitness Coaching",
            "coaches": ["Athish", "Karan", "Shri"],
            "instagram_url": "https://instagram.com",
            "support_email": getattr(settings, "ADMIN_NOTIFICATION_EMAIL", "team@dadbods.in"),
        },
    }
