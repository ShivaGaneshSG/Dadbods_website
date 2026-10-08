"""
Database models for DadBods client acquisition and application scoring system.
"""

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class CoachingApplication(models.Model):
    """
    Coaching Application Model.
    Captures complete 6-step questionnaire, computed qualification scores,
    medical review flags, and coach administrative review states.
    """

    # Admin Pipeline Status
    STATUS_NEW = "NEW"
    STATUS_REVIEWING = "REVIEWING"
    STATUS_QUALIFIED = "QUALIFIED"
    STATUS_CALL_BOOKED = "CALL_BOOKED"
    STATUS_ACCEPTED = "ACCEPTED"
    STATUS_REJECTED = "REJECTED"
    STATUS_ONBOARDING = "ONBOARDING"
    STATUS_NOT_READY = "NOT_READY"

    ADMIN_STATUS_CHOICES = [
        (STATUS_NEW, "New Application"),
        (STATUS_REVIEWING, "Under Review"),
        (STATUS_QUALIFIED, "Qualified"),
        (STATUS_CALL_BOOKED, "Discovery Call Booked"),
        (STATUS_ACCEPTED, "Accepted Client"),
        (STATUS_REJECTED, "Application Rejected"),
        (STATUS_ONBOARDING, "Onboarding in Progress"),
        (STATUS_NOT_READY, "Not Ready for Coaching"),
    ]

    # Automatic Qualification Status
    QUAL_PRIORITY = "PRIORITY"
    QUAL_QUALIFIED = "QUALIFIED"
    QUAL_REVIEW = "REVIEW"
    QUAL_LOW_PRIORITY = "LOW_PRIORITY"

    QUALIFICATION_STATUS_CHOICES = [
        (QUAL_PRIORITY, "Priority (Top Candidate)"),
        (QUAL_QUALIFIED, "Qualified"),
        (QUAL_REVIEW, "Needs Manual Review"),
        (QUAL_LOW_PRIORITY, "Low Priority"),
    ]

    # Step 1: Basic Information
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
        ("prefer_not_to_say", "Prefer not to say"),
    ]

    OCCUPATION_CHOICES = [
        ("student", "Student"),
        ("working_professional", "Working Professional"),
        ("business", "Business Owner / Entrepreneur"),
        ("other", "Other"),
    ]

    full_name = models.CharField("Full Name", max_length=150)
    age = models.PositiveIntegerField("Age")
    gender = models.CharField("Gender", max_length=25, choices=GENDER_CHOICES)
    instagram_username = models.CharField("Instagram Username", max_length=100)
    whatsapp_number = models.CharField("WhatsApp Number", max_length=30)
    email = models.EmailField("Email Address")
    occupation = models.CharField("Occupation", max_length=40, choices=OCCUPATION_CHOICES)
    city = models.CharField("Current City", max_length=100)

    # Step 2: Physique & Goal
    GOAL_CHOICES = [
        ("fat_loss", "Fat Loss"),
        ("muscle_gain", "Muscle Gain"),
        ("body_recomposition", "Body Recomposition"),
        ("strength", "Strength & Performance"),
        ("physique_transformation", "Physique Transformation"),
        ("competition_preparation", "Competition Preparation"),
        ("general_fitness", "General Fitness"),
        ("other", "Other"),
    ]

    height = models.CharField("Height (e.g. 175 cm or 5'9)", max_length=30)
    weight = models.CharField("Current Weight (e.g. 78 kg)", max_length=30)
    goal = models.CharField("Primary Goal", max_length=40, choices=GOAL_CHOICES)
    target_description = models.TextField(
        "What would you like to achieve in the next 3–6 months?",
        help_text="Detailed personal target description.",
    )

    # Step 3: Training
    EXPERIENCE_CHOICES = [
        ("never_trained", "Never trained"),
        ("less_than_6_months", "Less than 6 months"),
        ("6_12_months", "6–12 months"),
        ("1_2_years", "1–2 years"),
        ("2_5_years", "2–5 years"),
        ("5_plus_years", "5+ years"),
    ]

    TRAINING_DAYS_CHOICES = [
        ("0", "0 days"),
        ("1-2", "1–2 days"),
        ("3", "3 days"),
        ("4", "4 days"),
        ("5", "5 days"),
        ("6+", "6+ days"),
    ]

    LOCATION_CHOICES = [
        ("Gym", "Gym"),
        ("Home", "Home"),
        ("Both", "Both (Gym & Home)"),
    ]

    fitness_experience = models.CharField(
        "Fitness Experience", max_length=30, choices=EXPERIENCE_CHOICES
    )
    training_days = models.CharField(
        "Current Training Days Per Week", max_length=10, choices=TRAINING_DAYS_CHOICES
    )
    preferred_training_location = models.CharField(
        "Preferred Training Location", max_length=20, choices=LOCATION_CHOICES
    )
    current_training_routine = models.TextField(
        "Current Training Routine",
        blank=True,
        help_text="Describe your typical workout week or current split.",
    )

    # Step 4: Lifestyle & Nutrition
    ACTIVITY_LEVEL_CHOICES = [
        ("mostly_sedentary", "Mostly sedentary (desk job)"),
        ("lightly_active", "Lightly active"),
        ("moderately_active", "Moderately active"),
        ("very_active", "Very active"),
    ]

    SLEEP_CHOICES = [
        ("under_5", "Less than 5 hours"),
        ("5-6", "5–6 hours"),
        ("6-7", "6–7 hours"),
        ("7-8", "7–8 hours"),
        ("8_plus", "8+ hours"),
    ]

    DIET_PREF_CHOICES = [
        ("non_vegetarian", "Non-vegetarian"),
        ("vegetarian", "Vegetarian"),
        ("eggetarian", "Eggetarian"),
        ("vegan", "Vegan"),
        ("other", "Other"),
    ]

    DIET_CONSISTENCY_CHOICES = [
        ("very_inconsistent", "Very inconsistent"),
        ("somewhat_inconsistent", "Somewhat inconsistent"),
        ("fairly_consistent", "Fairly consistent"),
        ("very_consistent", "Very consistent"),
    ]

    NUTRITION_DIFFICULTY_CHOICES = [
        ("protein_intake", "Meeting protein intake"),
        ("calorie_control", "Calorie control / Portion sizing"),
        ("eating_outside", "Eating outside frequently / Social events"),
        ("consistency", "Maintaining consistency day to day"),
        ("meal_prep", "Meal preparation & cooking time"),
        ("cravings", "Late night cravings & snacking"),
        ("dont_know_what_to_eat", "Don't know what to eat / Nutrition confusion"),
        ("other", "Other"),
    ]

    activity_level = models.CharField(
        "Activity Level", max_length=30, choices=ACTIVITY_LEVEL_CHOICES
    )
    high_activity_work = models.CharField(
        "Does your work involve high physical activity?",
        max_length=5,
        choices=[("yes", "Yes"), ("no", "No")],
        default="no",
    )
    sleep_hours = models.CharField("Average Sleep", max_length=20, choices=SLEEP_CHOICES)
    diet_preference = models.CharField(
        "Diet Preference", max_length=30, choices=DIET_PREF_CHOICES
    )
    diet_consistency = models.CharField(
        "Current Diet Consistency", max_length=30, choices=DIET_CONSISTENCY_CHOICES
    )
    nutrition_difficulty = models.CharField(
        "Biggest Nutrition Difficulty", max_length=40, choices=NUTRITION_DIFFICULTY_CHOICES
    )
    coaching_budget = models.CharField(
        "Monthly Coaching Investment Range",
        max_length=40,
        help_text="Configured from Django settings.",
    )

    # Step 5: Health & Commitment
    previous_injury = models.BooleanField("Previous Injury?", default=False)
    injury_description = models.TextField("Injury Description", blank=True)

    medical_condition = models.BooleanField(
        "Medical Condition affecting exercise/diet?", default=False
    )
    medical_condition_description = models.TextField(
        "Medical Condition Description", blank=True
    )

    medication = models.BooleanField(
        "Current Medication affecting exercise/diet?", default=False
    )
    medication_description = models.TextField("Medication Description", blank=True)

    realistic_training_commitment = models.CharField(
        "Realistic Days/Week You Can Commit",
        max_length=10,
        choices=TRAINING_DAYS_CHOICES,
        default="4",
    )

    TRACKING_READINESS_CHOICES = [
        ("very_willing", "Very willing (ready to use app / scale)"),
        ("willing", "Willing with guidance"),
        ("somewhat_hesitant", "Somewhat hesitant"),
        ("not_willing", "Not willing"),
    ]

    nutrition_tracking_readiness = models.CharField(
        "Willingness to Track Nutrition",
        max_length=25,
        choices=TRACKING_READINESS_CHOICES,
    )
    follow_through_score = models.PositiveSmallIntegerField(
        "Likelihood to follow coach instructions (1-10)", default=8
    )
    consistency_problem = models.TextField(
        "What usually causes you to lose consistency?",
        help_text="Work stress, lack of routine, travel, motivation drop, etc.",
    )

    # Step 6: Motivation & Readiness
    previous_attempts = models.TextField(
        "What have you tried before, and why do you think it didn't work?"
    )
    biggest_obstacle = models.TextField(
        "What is the biggest thing stopping you from achieving your goal right now?"
    )
    why_dadbods = models.TextField("Why do you want to work with DadBods specifically?")

    START_TIMELINE_CHOICES = [
        ("immediately", "Immediately"),
        ("within_1_week", "Within 1 week"),
        ("within_2_weeks", "Within 2 weeks"),
        ("within_1_month", "Within 1 month"),
        ("exploring", "Just exploring for now"),
    ]

    CALL_TIMING_CHOICES = [
        ("morning", "Morning (9:00 AM – 12:00 PM)"),
        ("afternoon", "Afternoon (12:00 PM – 4:00 PM)"),
        ("evening", "Evening (4:00 PM – 8:00 PM)"),
        ("weekend", "Weekend"),
    ]

    start_timeline = models.CharField(
        "When would you ideally like to start?",
        max_length=30,
        choices=START_TIMELINE_CHOICES,
    )
    preferred_call_timing = models.CharField(
        "Preferred Call Timing", max_length=30, choices=CALL_TIMING_CHOICES
    )
    agreement_accepted = models.BooleanField(
        "Application terms acknowledged", default=True
    )

    # Computed Scoring & Flagging
    qualification_score = models.PositiveIntegerField(
        "Qualification Score (0-100)", default=0, db_index=True
    )
    qualification_status = models.CharField(
        "Qualification Status",
        max_length=25,
        choices=QUALIFICATION_STATUS_CHOICES,
        default=QUAL_REVIEW,
        db_index=True,
    )
    qualification_breakdown = models.JSONField(
        "Points Breakdown", default=dict, blank=True
    )
    requires_medical_review = models.BooleanField(
        "Flagged for Medical/Injury Review", default=False, db_index=True
    )

    # Admin Management
    admin_status = models.CharField(
        "Client Status",
        max_length=25,
        choices=ADMIN_STATUS_CHOICES,
        default=STATUS_NEW,
        db_index=True,
    )
    internal_notes = models.TextField("Admin Internal Notes", blank=True)
    reviewed_by = models.ForeignKey(
        User,
        verbose_name="Reviewed By Coach",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="reviewed_applications",
    )
    reviewed_at = models.DateTimeField("Reviewed At", null=True, blank=True)

    created_at = models.DateTimeField("Submitted At", auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField("Updated At", auto_now=True)

    class Meta:
        verbose_name = "Coaching Application"
        verbose_name_plural = "Coaching Applications"
        ordering = ["-qualification_score", "-created_at"]

    def __str__(self):
        return f"{self.full_name} ({self.get_goal_display()}) — Score: {self.qualification_score}"


class ApplicationNote(models.Model):
    """
    Log of internal coach notes and activity updates for each applicant.
    Allows Athish, Karan, and Shri to leave collaborative comments.
    """

    application = models.ForeignKey(
        CoachingApplication,
        on_delete=models.CASCADE,
        related_name="notes",
        verbose_name="Application",
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Coach / Author"
    )
    note = models.TextField("Coach Note")
    created_at = models.DateTimeField("Created At", auto_now_add=True)

    class Meta:
        verbose_name = "Coach Internal Note"
        verbose_name_plural = "Coach Internal Notes"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Note by {self.author} on {self.application.full_name}"
