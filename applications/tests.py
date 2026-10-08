"""
Test suite for DadBods Applications system:
Tests form validation, scoring calculation, honeypot anti-spam, and admin CRM views.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
import time

from .models import CoachingApplication, ApplicationNote
from .scoring import calculate_qualification_score

User = get_user_model()


class ScoringEngineTests(TestCase):
    """Tests the Python qualification scoring service."""

    def test_priority_applicant_scoring(self):
        """A serious, committed applicant should score >= 80 (PRIORITY)."""
        data = {
            "goal": "muscle_gain",
            "target_description": "I want to gain 5 kg of lean muscle, improve my deadlift to 180kg, and lower my body fat percentage.",
            "realistic_training_commitment": "5",
            "preferred_training_location": "Gym",
            "nutrition_tracking_readiness": "very_willing",
            "diet_consistency": "fairly_consistent",
            "follow_through_score": 9,
            "start_timeline": "immediately",
            "coaching_budget": "tier_premium",
            "why_dadbods": "I follow Athish, Karan, and Shri on Instagram. I love that you understand South Indian diets and focus on real progressive overload instead of generic routines.",
            "biggest_obstacle": "Lack of accountability and knowing how to adjust my calories when weight stalls.",
            "previous_attempts": "Followed random YouTube split routines for a few months, but had no structure or nutrition tracking.",
            "previous_injury": False,
            "medical_condition": False,
            "medication": False,
        }
        res = calculate_qualification_score(data)
        self.assertGreaterEqual(res["score"], 80)
        self.assertEqual(res["status"], "PRIORITY")
        self.assertFalse(res["requires_medical_review"])

    def test_medical_condition_flags_review_without_deduction(self):
        """Medical disclosures must set requires_medical_review=True without dropping the applicant to zero."""
        data = {
            "goal": "fat_loss",
            "target_description": "Lose 12 kg of visceral fat and gain athletic stamina.",
            "realistic_training_commitment": "4",
            "preferred_training_location": "Gym",
            "nutrition_tracking_readiness": "willing",
            "diet_consistency": "somewhat_inconsistent",
            "follow_through_score": 8,
            "start_timeline": "within_1_week",
            "coaching_budget": "tier_standard",
            "why_dadbods": "I trust your authentic approach to sustainable coaching.",
            "biggest_obstacle": "Cravings and long desk job hours.",
            "previous_attempts": "Keto diet in 2022 but regained everything.",
            "previous_injury": True,
            "medical_condition": True,
            "medication": False,
        }
        res = calculate_qualification_score(data)
        self.assertTrue(res["requires_medical_review"])
        self.assertIn("medical_review_flag", res["breakdown"])
        self.assertTrue(res["breakdown"]["medical_review_flag"]["flagged"])


class CoachingApplicationWorkflowTests(TestCase):
    """Tests the full application submission flow via HTTP Client."""

    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username="testadmin",
            email="testadmin@dadbods.in",
            password="adminpassword123",
        )

    def test_get_apply_page(self):
        """GET /apply/ renders successfully with status 200."""
        response = self.client.get(reverse("applications:apply"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "01 ABOUT YOU")
        self.assertContains(response, "LET'S GET TO KNOW YOU")

    def test_successful_application_submission(self):
        """POST /apply/ with valid answers saves application and computes score."""
        payload = {
            # Step 1
            "full_name": "Kavitha R",
            "age": 28,
            "gender": "female",
            "instagram_username": "@kavitha_lifts",
            "whatsapp_number": "+91 98401 23456",
            "email": "kavitha@example.com",
            "occupation": "working_professional",
            "city": "Chennai",
            # Step 2
            "height": "165 cm",
            "weight": "68 kg",
            "goal": "body_recomposition",
            "target_description": "Want to drop body fat from 30% to 22% while building noticeable glutes and back definition.",
            # Step 3
            "fitness_experience": "1_2_years",
            "training_days": "4",
            "preferred_training_location": "Gym",
            "current_training_routine": "Upper Lower 4-day split at local gym.",
            # Step 4
            "activity_level": "moderately_active",
            "high_activity_work": "no",
            "sleep_hours": "7-8",
            "diet_preference": "vegetarian",
            "diet_consistency": "fairly_consistent",
            "nutrition_difficulty": "protein_intake",
            "coaching_budget": "tier_standard",
            # Step 5
            "realistic_training_commitment": "4",
            "nutrition_tracking_readiness": "very_willing",
            "follow_through_score": 9,
            "consistency_problem": "Office snack temptations and evening energy dips.",
            # Step 6
            "previous_attempts": "Tried cutting carbs completely but felt dizzy and stopped.",
            "biggest_obstacle": "Understanding how to hit 100g+ protein as a South Indian vegetarian.",
            "why_dadbods": "Because Shri and Athish understand authentic vegetarian meals without just recommending raw paneer.",
            "start_timeline": "within_1_week",
            "preferred_call_timing": "evening",
            "agreement_accepted": True,
            "website": "",  # Honeypot empty
            "form_load_timestamp": time.time() - 10,  # 10s elapsed
        }

        response = self.client.post(reverse("applications:apply"), data=payload)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("applications:success"))

        # Verify record in database
        app = CoachingApplication.objects.get(email="kavitha@example.com")
        self.assertEqual(app.full_name, "Kavitha R")
        self.assertGreater(app.qualification_score, 0)
        self.assertIn(app.qualification_status, ["PRIORITY", "QUALIFIED"])
        self.assertFalse(app.requires_medical_review)

    def test_honeypot_spam_rejection(self):
        """Bots that fill the honeypot website field are rejected."""
        payload = {
            "full_name": "Spam Bot",
            "email": "bot@spam.com",
            "website": "https://spamlink.com",  # Honeypot filled!
        }
        response = self.client.post(reverse("applications:apply"), data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CoachingApplication.objects.filter(email="bot@spam.com").exists())

    def test_staff_dashboard_access(self):
        """Staff members can view the Executive Dashboard."""
        self.client.login(username="testadmin", password="adminpassword123")
        response = self.client.get(reverse("applications:admin_dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "DadBods Client Acquisition CRM")
