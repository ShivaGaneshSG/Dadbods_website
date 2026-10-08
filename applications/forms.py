"""
Django Forms for DadBods Coaching Application.
Provides server-side validation, clean widgets, anti-spam honeypot, and security checks.
"""

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
import re
import time

from .models import CoachingApplication


class CoachingApplicationForm(forms.ModelForm):
    """
    Multi-step coaching application form with comprehensive server-side validation.
    """

    # Anti-spam Honeypot field (hidden from real users via CSS & widget)
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"autocomplete": "off", "tabindex": "-1", "class": "hp-field"}
        ),
        label="Leave empty",
    )

    # Anti-bot submission timestamp check
    form_load_timestamp = forms.FloatField(
        required=False,
        widget=forms.HiddenInput(),
    )

    class Meta:
        model = CoachingApplication
        exclude = [
            "qualification_score",
            "qualification_status",
            "qualification_breakdown",
            "requires_medical_review",
            "admin_status",
            "internal_notes",
            "reviewed_by",
            "reviewed_at",
            "created_at",
            "updated_at",
        ]
        widgets = {
            # Step 1
            "full_name": forms.TextInput(
                attrs={"placeholder": "e.g. Arun Kumar", "class": "form-control"}
            ),
            "age": forms.NumberInput(
                attrs={"placeholder": "e.g. 27", "min": "16", "max": "80", "class": "form-control"}
            ),
            "gender": forms.Select(attrs={"class": "form-select"}),
            "instagram_username": forms.TextInput(
                attrs={"placeholder": "@yourhandle", "class": "form-control"}
            ),
            "whatsapp_number": forms.TextInput(
                attrs={"placeholder": "+91 98765 43210", "class": "form-control"}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "arun@example.com", "class": "form-control"}
            ),
            "occupation": forms.Select(attrs={"class": "form-select"}),
            "city": forms.TextInput(
                attrs={"placeholder": "e.g. Chennai, Coimbatore, London", "class": "form-control"}
            ),
            # Step 2
            "height": forms.TextInput(
                attrs={"placeholder": "e.g. 178 cm or 5'10\"", "class": "form-control"}
            ),
            "weight": forms.TextInput(
                attrs={"placeholder": "e.g. 82 kg or 180 lbs", "class": "form-control"}
            ),
            "goal": forms.Select(attrs={"class": "form-select"}),
            "target_description": forms.Textarea(
                attrs={
                    "placeholder": "Be specific: What do you want to achieve, how do you want to feel, and what timeline?",
                    "rows": 4,
                    "class": "form-control",
                }
            ),
            # Step 3
            "fitness_experience": forms.Select(attrs={"class": "form-select"}),
            "training_days": forms.Select(attrs={"class": "form-select"}),
            "preferred_training_location": forms.Select(attrs={"class": "form-select"}),
            "current_training_routine": forms.Textarea(
                attrs={
                    "placeholder": "Describe what your weekly workouts look like right now (e.g. 3 day split, cardio, nothing right now)",
                    "rows": 3,
                    "class": "form-control",
                }
            ),
            # Step 4
            "activity_level": forms.Select(attrs={"class": "form-select"}),
            "high_activity_work": forms.Select(attrs={"class": "form-select"}),
            "sleep_hours": forms.Select(attrs={"class": "form-select"}),
            "diet_preference": forms.Select(attrs={"class": "form-select"}),
            "diet_consistency": forms.Select(attrs={"class": "form-select"}),
            "nutrition_difficulty": forms.Select(attrs={"class": "form-select"}),
            "coaching_budget": forms.Select(attrs={"class": "form-select"}),
            # Step 5
            "previous_injury": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "injury_description": forms.Textarea(
                attrs={
                    "placeholder": "If yes, please describe what happened, when, and if it still affects you.",
                    "rows": 2,
                    "class": "form-control",
                }
            ),
            "medical_condition": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "medical_condition_description": forms.Textarea(
                attrs={
                    "placeholder": "If yes, please describe (e.g. hypertension, asthma, thyroid, etc.)",
                    "rows": 2,
                    "class": "form-control",
                }
            ),
            "medication": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "medication_description": forms.Textarea(
                attrs={
                    "placeholder": "If yes, please list ongoing medications.",
                    "rows": 2,
                    "class": "form-control",
                }
            ),
            "realistic_training_commitment": forms.Select(attrs={"class": "form-select"}),
            "nutrition_tracking_readiness": forms.Select(attrs={"class": "form-select"}),
            "follow_through_score": forms.NumberInput(
                attrs={"min": "1", "max": "10", "class": "form-control", "value": "8"}
            ),
            "consistency_problem": forms.Textarea(
                attrs={
                    "placeholder": "What typically causes you to fall off track? (e.g. work stress, lack of routine, travel, lack of motivation)",
                    "rows": 3,
                    "class": "form-control",
                }
            ),
            # Step 6
            "previous_attempts": forms.Textarea(
                attrs={
                    "placeholder": "What fitness/diet approaches have you tried before, and why did they not stick?",
                    "rows": 3,
                    "class": "form-control",
                }
            ),
            "biggest_obstacle": forms.Textarea(
                attrs={
                    "placeholder": "What is the single biggest barrier between you and your target physique today?",
                    "rows": 3,
                    "class": "form-control",
                }
            ),
            "why_dadbods": forms.Textarea(
                attrs={
                    "placeholder": "Why DadBods specifically rather than a generic gym membership or app?",
                    "rows": 3,
                    "class": "form-control",
                }
            ),
            "start_timeline": forms.Select(attrs={"class": "form-select"}),
            "preferred_call_timing": forms.Select(attrs={"class": "form-select"}),
            "agreement_accepted": forms.CheckboxInput(
                attrs={"class": "form-check-input", "required": "required"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dynamically set coaching budget choices from settings
        budget_choices = getattr(
            settings,
            "COACHING_BUDGET_CHOICES",
            [
                ("tier_premium", "₹10,000+ / month"),
                ("tier_standard", "₹7,000 – ₹10,000 / month"),
                ("tier_core", "₹5,000 – ₹7,000 / month"),
                ("tier_entry", "₹3,500 – ₹5,000 / month"),
                ("tier_budget", "Under ₹3,500 / month"),
            ],
        )
        self.fields["coaching_budget"].widget = forms.Select(
            choices=[("", "Select Coaching Investment Tier...")] + list(budget_choices),
            attrs={"class": "form-select"},
        )

        if "high_activity_work" in self.fields:
            self.fields["high_activity_work"].required = False
            self.fields["high_activity_work"].initial = "no"

        # Set initial timestamp if new form
        if not self.is_bound:
            self.initial["form_load_timestamp"] = time.time()

    def clean_website(self):
        """Honeypot field check to deflect spam bots."""
        val = self.cleaned_data.get("website")
        if val:
            raise ValidationError("Spam bot detected. Submission rejected.")
        return val

    def clean_form_load_timestamp(self):
        """Validate human submission speed (must take at least 3 seconds)."""
        timestamp = self.cleaned_data.get("form_load_timestamp")
        if timestamp:
            try:
                elapsed = time.time() - float(timestamp)
                if elapsed < 2.5:
                    raise ValidationError("Form was submitted too rapidly. Please take your time.")
            except (ValueError, TypeError):
                pass
        return timestamp

    def clean_whatsapp_number(self):
        number = self.cleaned_data.get("whatsapp_number", "").strip()
        # Clean standard phone chars
        digits_only = re.sub(r"[^\d]", "", number)
        if len(digits_only) < 7:
            raise ValidationError("Please provide a valid WhatsApp number including country code.")
        return number

    def clean_instagram_username(self):
        handle = self.cleaned_data.get("instagram_username", "").strip()
        if not handle:
            raise ValidationError("Please provide your Instagram username so coaches can review your profile.")
        if not handle.startswith("@"):
            handle = f"@{handle}"
        return handle

    def clean_age(self):
        age = self.cleaned_data.get("age")
        if age is not None and (age < 16 or age > 85):
            raise ValidationError("Applicants must be between 16 and 85 years of age.")
        return age

    def clean_follow_through_score(self):
        score = self.cleaned_data.get("follow_through_score")
        if score is not None and (score < 1 or score > 10):
            raise ValidationError("Score must be between 1 and 10.")
        return score

    def clean_agreement_accepted(self):
        agreed = self.cleaned_data.get("agreement_accepted")
        if not agreed:
            raise ValidationError("You must acknowledge the terms to submit your application.")
        return agreed
