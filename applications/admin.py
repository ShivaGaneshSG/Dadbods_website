"""
Django Admin CRM for DadBods Coaching Platform.
Empowers Athish, Karan, and Shri to review, filter, score, and manage client applications.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.urls import reverse
from .models import CoachingApplication, ApplicationNote
from .scoring import calculate_qualification_score

# Custom Admin Site Branding
admin.site.site_header = "DadBods Fitness Coaching CRM"
admin.site.site_title = "DadBods Admin"
admin.site.index_title = "Client Acquisition & Selection Portal"


class ApplicationNoteInline(admin.TabularInline):
    """Allows coaches to add dated internal notes right inside the application view."""
    model = ApplicationNote
    extra = 1
    readonly_fields = ("created_at",)
    fields = ("author", "note", "created_at")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            kwargs["initial"] = request.user.id
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(CoachingApplication)
class CoachingApplicationAdmin(admin.ModelAdmin):
    """
    Rich CRM admin interface for vetting and selecting fitness coaching clients.
    """

    list_display = (
        "applicant_identity",
        "score_badge",
        "qualification_status_badge",
        "pipeline_status_badge",
        "medical_flag_badge",
        "goal_display",
        "budget_display",
        "start_timeline_display",
        "city",
        "created_at_formatted",
    )

    list_filter = (
        "admin_status",
        "qualification_status",
        "requires_medical_review",
        "goal",
        "start_timeline",
        "fitness_experience",
        "activity_level",
        "diet_preference",
        "occupation",
        "created_at",
    )

    search_fields = (
        "full_name",
        "email",
        "whatsapp_number",
        "instagram_username",
        "city",
        "target_description",
    )

    ordering = ("-qualification_score", "-created_at")
    list_per_page = 25
    inlines = [ApplicationNoteInline]

    readonly_fields = (
        "qualification_score",
        "qualification_status",
        "requires_medical_review",
        "qualification_breakdown_display",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Executive Qualification & Status",
            {
                "classes": ("extrapretty",),
                "fields": (
                    (
                        "qualification_score",
                        "qualification_status",
                        "requires_medical_review",
                    ),
                    "admin_status",
                    ("reviewed_by", "reviewed_at"),
                    "internal_notes",
                    "qualification_breakdown_display",
                ),
            },
        ),
        (
            "Step 1: Contact & Personal Details",
            {
                "fields": (
                    ("full_name", "age", "gender"),
                    ("instagram_username", "whatsapp_number", "email"),
                    ("occupation", "city"),
                )
            },
        ),
        (
            "Step 2: Physique & Primary Target",
            {
                "fields": (
                    ("height", "weight", "goal"),
                    "target_description",
                )
            },
        ),
        (
            "Step 3: Training History & Routine",
            {
                "fields": (
                    ("fitness_experience", "training_days", "preferred_training_location"),
                    "current_training_routine",
                )
            },
        ),
        (
            "Step 4: Lifestyle, Nutrition & Budget",
            {
                "fields": (
                    ("activity_level", "high_activity_work", "sleep_hours"),
                    ("diet_preference", "diet_consistency", "nutrition_difficulty"),
                    "coaching_budget",
                )
            },
        ),
        (
            "Step 5: Health & Commitment Assessment",
            {
                "fields": (
                    ("previous_injury", "injury_description"),
                    ("medical_condition", "medical_condition_description"),
                    ("medication", "medication_description"),
                    ("realistic_training_commitment", "nutrition_tracking_readiness"),
                    "follow_through_score",
                    "consistency_problem",
                )
            },
        ),
        (
            "Step 6: Motivation & Readiness",
            {
                "fields": (
                    "previous_attempts",
                    "biggest_obstacle",
                    "why_dadbods",
                    ("start_timeline", "preferred_call_timing"),
                    "agreement_accepted",
                )
            },
        ),
        (
            "Timestamps",
            {
                "classes": ("collapse",),
                "fields": ("created_at", "updated_at"),
            },
        ),
    )

    # Custom Column Badges & Display
    @admin.display(description="Applicant")
    def applicant_identity(self, obj):
        return format_html(
            "<strong>{}</strong><br><span style='color:#888; font-size:11px;'>{} &bull; {}</span>",
            obj.full_name,
            obj.instagram_username,
            obj.whatsapp_number,
        )

    @admin.display(description="Score", ordering="qualification_score")
    def score_badge(self, obj):
        score = obj.qualification_score
        if score >= 80:
            color = "#10b981"  # Emerald
            bg = "#064e3b"
        elif score >= 65:
            color = "#3b82f6"  # Blue
            bg = "#1e3a8a"
        elif score >= 45:
            color = "#f59e0b"  # Amber
            bg = "#78350f"
        else:
            color = "#ef4444"  # Red
            bg = "#7f1d1d"

        return format_html(
            '<span style="background:{}; color:{}; padding:4px 8px; border-radius:6px; font-weight:700; font-size:12px;">{}/100</span>',
            bg,
            color,
            score,
        )

    @admin.display(description="Qualification", ordering="qualification_status")
    def qualification_status_badge(self, obj):
        colors = {
            "PRIORITY": ("#22c55e", "#14532d"),
            "QUALIFIED": ("#38bdf8", "#0c4a6e"),
            "REVIEW": ("#fbbf24", "#713f12"),
            "LOW_PRIORITY": ("#94a3b8", "#1e293b"),
        }
        fg, bg = colors.get(obj.qualification_status, ("#cbd5e1", "#334155"))
        label = obj.get_qualification_status_display()
        return format_html(
            '<span style="background:{}; color:{}; padding:3px 8px; border-radius:12px; font-weight:600; font-size:11px; text-transform:uppercase;">{}</span>',
            bg,
            fg,
            label,
        )

    @admin.display(description="Pipeline Status", ordering="admin_status")
    def pipeline_status_badge(self, obj):
        colors = {
            "NEW": ("#f1f5f9", "#475569"),
            "REVIEWING": ("#fef08a", "#854d0e"),
            "QUALIFIED": ("#bae6fd", "#0369a1"),
            "CALL_BOOKED": ("#fed7aa", "#c2410c"),
            "ACCEPTED": ("#bbf7d0", "#15803d"),
            "REJECTED": ("#fecaca", "#b91c1c"),
            "ONBOARDING": ("#e9d5ff", "#7e22ce"),
            "NOT_READY": ("#cbd5e1", "#475569"),
        }
        fg, bg = colors.get(obj.admin_status, ("#f1f5f9", "#334155"))
        return format_html(
            '<span style="background:{}; color:{}; padding:3px 8px; border-radius:12px; font-weight:600; font-size:11px;">{}</span>',
            bg,
            fg,
            obj.get_admin_status_display(),
        )

    @admin.display(description="Medical Flag")
    def medical_flag_badge(self, obj):
        if obj.requires_medical_review:
            return format_html(
                '<span style="background:#7f1d1d; color:#fca5a5; padding:2px 6px; border-radius:4px; font-size:10px; font-weight:700;">⚠️ REVIEW</span>'
            )
        return format_html(
            '<span style="color:#64748b; font-size:11px;">Clear</span>'
        )

    @admin.display(description="Goal")
    def goal_display(self, obj):
        return obj.get_goal_display()

    @admin.display(description="Budget")
    def budget_display(self, obj):
        return obj.coaching_budget.replace("tier_", "").title()

    @admin.display(description="Start")
    def start_timeline_display(self, obj):
        return obj.get_start_timeline_display()

    @admin.display(description="Date", ordering="created_at")
    def created_at_formatted(self, obj):
        return obj.created_at.strftime("%d %b, %H:%M")

    @admin.display(description="Scoring Breakdown")
    def qualification_breakdown_display(self, obj):
        if not obj.qualification_breakdown:
            return "No breakdown recorded."
        html = '<div style="background:#1e293b; color:#f8fafc; padding:12px; border-radius:8px; font-family:monospace; font-size:12px;">'
        for key, val in obj.qualification_breakdown.items():
            if isinstance(val, dict):
                pts = val.get("points", "-")
                max_pts = val.get("max", "-")
                detail = val.get("detail", "")
                html += f"<div style='margin-bottom:6px;'><strong>{key.replace('_', ' ').title()}</strong>: {pts}/{max_pts} pts &mdash; <em>{detail}</em></div>"
            elif key == "medical_review_flag":
                html += f"<div style='color:#f87171;'><strong>Medical / Health Flags</strong>: {val.get('reasons')}</div>"
        html += "</div>"
        return format_html(html)

    # Bulk CRM Actions
    actions = [
        "mark_under_review",
        "mark_discovery_call_booked",
        "mark_accepted",
        "mark_not_ready",
        "recalculate_qualification_scores",
    ]

    @admin.action(description="Mark selected leads as 'Under Review'")
    def mark_under_review(self, request, queryset):
        queryset.update(
            admin_status=CoachingApplication.STATUS_REVIEWING,
            reviewed_by=request.user,
            reviewed_at=timezone.now(),
        )
        self.message_user(request, f"{queryset.count()} applications moved to 'Under Review'.")

    @admin.action(description="Mark selected leads as 'Discovery Call Booked'")
    def mark_discovery_call_booked(self, request, queryset):
        queryset.update(admin_status=CoachingApplication.STATUS_CALL_BOOKED)
        self.message_user(request, f"{queryset.count()} applications updated to 'Discovery Call Booked'.")

    @admin.action(description="Mark selected leads as 'Accepted Client'")
    def mark_accepted(self, request, queryset):
        queryset.update(admin_status=CoachingApplication.STATUS_ACCEPTED)
        self.message_user(request, f"{queryset.count()} applications accepted into DadBods Coaching.")

    @admin.action(description="Mark selected leads as 'Not Ready'")
    def mark_not_ready(self, request, queryset):
        queryset.update(admin_status=CoachingApplication.STATUS_NOT_READY)
        self.message_user(request, f"{queryset.count()} applications marked as Not Ready.")

    @admin.action(description="Recalculate qualification scores for selected")
    def recalculate_qualification_scores(self, request, queryset):
        for app in queryset:
            # Reconstruct dictionary from model fields
            data = {
                "goal": app.goal,
                "target_description": app.target_description,
                "realistic_training_commitment": app.realistic_training_commitment,
                "preferred_training_location": app.preferred_training_location,
                "nutrition_tracking_readiness": app.nutrition_tracking_readiness,
                "diet_consistency": app.diet_consistency,
                "follow_through_score": app.follow_through_score,
                "start_timeline": app.start_timeline,
                "coaching_budget": app.coaching_budget,
                "why_dadbods": app.why_dadbods,
                "biggest_obstacle": app.biggest_obstacle,
                "previous_attempts": app.previous_attempts,
                "previous_injury": app.previous_injury,
                "medical_condition": app.medical_condition,
                "medication": app.medication,
            }
            res = calculate_qualification_score(data)
            app.qualification_score = res["score"]
            app.qualification_status = res["status"]
            app.qualification_breakdown = res["breakdown"]
            app.requires_medical_review = res["requires_medical_review"]
            app.save()
        self.message_user(request, f"Recalculated scores for {queryset.count()} applications.")

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["dashboard_url"] = reverse("applications:admin_dashboard")
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(ApplicationNote)
class ApplicationNoteAdmin(admin.ModelAdmin):
    list_display = ("application", "author", "created_at", "short_note")
    search_fields = ("application__full_name", "note")
    list_filter = ("author", "created_at")

    @admin.display(description="Note")
    def short_note(self, obj):
        return (obj.note[:75] + "...") if len(obj.note) > 75 else obj.note
