"""
Test suite for DadBods core public website pages and image configuration.
"""

from django.test import TestCase, Client
from django.urls import reverse
from config.image_config import get_image_config, resolve_image, FALLBACK_IMAGE


class CorePublicPagesTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_status(self):
        """Home page renders status 200 with slogan, hero headline, coaches, and YouTube content."""
        res = self.client.get(reverse("core:home"))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "BUILD YOUR PHYSIQUE")
        self.assertContains(res, "RIGHT TIME. RIGHT NOW.")
        self.assertContains(res, "ATHISH")
        self.assertContains(res, "KARAN")
        self.assertContains(res, "SHRI")
        self.assertContains(res, "DADBODS ON YOUTUBE")
        self.assertContains(res, "WATCH. LEARN. GET BETTER.")
        self.assertContains(res, "https://www.youtube.com/@DADBODS_221")
        # Ensure custom cursor elements are removed
        self.assertNotContains(res, "custom-cursor-dot")
        self.assertNotContains(res, "custom-cursor-ring")

    def test_about_page_status(self):
        """About page renders 200 with team showcase and brand philosophy."""
        res = self.client.get(reverse("core:about"))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "THE PEOPLE BEHIND DADBODS")
        self.assertContains(res, "OUR APPROACH")
        self.assertContains(res, "RIGHT TIME.")
        self.assertContains(res, "RIGHT NOW.")

    def test_coaches_page_redirects_to_about(self):
        """Legacy coaches URL redirects cleanly to the unified About page."""
        res = self.client.get(reverse("core:coaches"))
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse("core:about"))

    def test_coaching_page_redirects_to_apply(self):
        """Legacy coaching URL redirects cleanly to Get Trained By DadBods page."""
        res = self.client.get(reverse("core:coaching"))
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse("applications:apply"))

    def test_transformations_page_status(self):
        """Transformations page renders real client gallery."""
        res = self.client.get(reverse("core:transformations"))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "THE WORK SPEAKS FOR ITSELF")


class ImageConfigurationTests(TestCase):
    def test_image_config_structure(self):
        """Image configuration dictionary contains logo, general, coaches, transformations."""
        cfg = get_image_config()
        self.assertIn("logo", cfg)
        self.assertIn("general", cfg)
        self.assertIn("coaches", cfg)
        self.assertIn("transformations", cfg)
        self.assertIn("athish", cfg["coaches"])
        self.assertIn("karan", cfg["coaches"])
        self.assertIn("shri", cfg["coaches"])

    def test_missing_image_graceful_fallback(self):
        """Missing image paths return fallback rather than crashing."""
        fallback = resolve_image("nonexistent_folder/missing.jpg")
        self.assertEqual(fallback, FALLBACK_IMAGE)
