"""
Views for DadBods Coaching Application System.
Handles multi-step submission, scoring calculation, email notifications, and staff dashboard.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Q, Avg
import logging

from .models import CoachingApplication, ApplicationNote
from .forms import CoachingApplicationForm
from .scoring import calculate_qualification_score

logger = logging.getLogger(__name__)


@require_http_methods(["GET", "POST"])
def apply_view(request):
    """
    Renders and processes the 6-step coaching application.
    Calculates qualification score on submission and routes to success.
    """
    if request.method == "POST":
        form = CoachingApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)

            # Compute transparent qualification scoring
            score_data = calculate_qualification_score(form.cleaned_data)
            application.qualification_score = score_data["score"]
            application.qualification_status = score_data["status"]
            application.qualification_breakdown = score_data["breakdown"]
            application.requires_medical_review = score_data["requires_medical_review"]

            application.save()

            # Store recent application in session for friendly confirmation page
            request.session["submitted_app_id"] = application.id
            request.session["submitted_name"] = application.full_name
            request.session["submitted_email"] = application.email

            # Dispatch notification emails (Console backend for dev)
            _send_application_notifications(application, score_data)

            return redirect("applications:success")
        else:
            messages.error(
                request,
                "Please review the highlighted fields in the application form.",
            )
    else:
        form = CoachingApplicationForm()

    return render(
        request,
        "applications/apply.html",
        {
            "form": form,
            "page_title": "Apply for DadBods Coaching | Client Selection",
        },
    )


def application_success_view(request):
    """
    Displays clean post-submission confirmation screen.
    """
    app_id = request.session.get("submitted_app_id")
    applicant_name = request.session.get("submitted_name", "Applicant")

    return render(
        request,
        "applications/success.html",
        {
            "applicant_name": applicant_name,
            "page_title": "Application Received | DadBods",
        },
    )


def _send_application_notifications(application: CoachingApplication, score_data: dict):
    """
    Sends console notifications for new applications (Admin alert + Applicant confirmation).
    Safe against mail failures so client submission is never interrupted.
    """
    admin_email = getattr(settings, "ADMIN_NOTIFICATION_EMAIL", "team@dadbods.in")
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "notifications@dadbods.in")

    # 1. Admin Alert Email
    admin_subject = f"[DadBods New Application] {application.full_name} — Score: {application.qualification_score}/100 ({application.get_qualification_status_display()})"
    admin_body = (
        f"A new client application has been submitted to DadBods!\n\n"
        f"Applicant: {application.full_name}\n"
        f"Instagram: {application.instagram_username}\n"
        f"WhatsApp: {application.whatsapp_number}\n"
        f"Email: {application.email}\n"
        f"City: {application.city}\n"
        f"Goal: {application.get_goal_display()}\n"
        f"Budget Tier: {application.coaching_budget}\n"
        f"Start Timeline: {application.get_start_timeline_display()}\n\n"
        f"--- QUALIFICATION ENGINE ---\n"
        f"Score: {application.qualification_score} / 100\n"
        f"Status: {application.get_qualification_status_display()}\n"
        f"Medical/Injury Flag: {'YES (Needs Human Review)' if application.requires_medical_review else 'No issues reported'}\n\n"
        f"Review directly in DadBods Admin CRM."
    )

    # 2. Applicant Confirmation Email
    applicant_subject = "We received your DadBods Coaching Application"
    applicant_body = (
        f"Hi {application.full_name},\n\n"
        f"Thank you for taking the time to apply for DadBods online coaching.\n\n"
        f"The DadBods coaching team (Athish, Karan, and Shri) reviews every application "
        f"based on current goals, commitment level, and coaching spot availability.\n\n"
        f"If you are selected for the next step, one of our coaches will reach out to you via WhatsApp "
        f"or Instagram to schedule your discovery call.\n\n"
        f"Best regards,\n"
        f"Athish, Karan & Shri\n"
        f"The DadBods Coaching Team"
    )

    try:
        send_mail(
            admin_subject,
            admin_body,
            from_email,
            [admin_email],
            fail_silently=True,
        )
        send_mail(
            applicant_subject,
            applicant_body,
            from_email,
            [application.email],
            fail_silently=True,
        )
    except Exception as e:
        logger.warning(f"Email dispatch error: {e}")


@staff_member_required
def admin_dashboard_summary_view(request):
    """
    Dedicated CRM Executive Summary Dashboard for Athish, Karan, and Shri.
    Provides real-time stats on total leads, qualification distribution, goals, and pipeline status.
    """
    total_apps = CoachingApplication.objects.count()
    new_apps = CoachingApplication.objects.filter(admin_status=CoachingApplication.STATUS_NEW).count()
    priority_leads = CoachingApplication.objects.filter(qualification_status=CoachingApplication.QUAL_PRIORITY).count()
    qualified_leads = CoachingApplication.objects.filter(qualification_status=CoachingApplication.QUAL_QUALIFIED).count()
    calls_booked = CoachingApplication.objects.filter(admin_status=CoachingApplication.STATUS_CALL_BOOKED).count()
    accepted_clients = CoachingApplication.objects.filter(admin_status=CoachingApplication.STATUS_ACCEPTED).count()
    rejected_apps = CoachingApplication.objects.filter(admin_status=CoachingApplication.STATUS_REJECTED).count()
    medical_flagged = CoachingApplication.objects.filter(requires_medical_review=True).count()

    avg_score = CoachingApplication.objects.aggregate(avg=Avg("qualification_score"))["avg"] or 0

    # Breakdown by Goal
    by_goal = (
        CoachingApplication.objects.values("goal")
        .annotate(total=Count("id"))
        .order_by("-total")
    )
    # Breakdown by Status
    by_status = (
        CoachingApplication.objects.values("admin_status")
        .annotate(total=Count("id"))
        .order_by("-total")
    )
    # Breakdown by Start Timeline
    by_timeline = (
        CoachingApplication.objects.values("start_timeline")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    # Score Ranges
    score_ranges = {
        "80-100 (Priority)": CoachingApplication.objects.filter(qualification_score__gte=80).count(),
        "65-79 (Qualified)": CoachingApplication.objects.filter(qualification_score__gte=65, qualification_score__lt=80).count(),
        "45-64 (Review)": CoachingApplication.objects.filter(qualification_score__gte=45, qualification_score__lt=65).count(),
        "0-44 (Low Priority)": CoachingApplication.objects.filter(qualification_score__lt=45).count(),
    }

    # Recent 10 applications
    recent_applications = CoachingApplication.objects.select_related("reviewed_by")[:10]

    context = {
        "total_apps": total_apps,
        "new_apps": new_apps,
        "priority_leads": priority_leads,
        "qualified_leads": qualified_leads,
        "calls_booked": calls_booked,
        "accepted_clients": accepted_clients,
        "rejected_apps": rejected_apps,
        "medical_flagged": medical_flagged,
        "avg_score": round(avg_score, 1),
        "by_goal": by_goal,
        "by_status": by_status,
        "by_timeline": by_timeline,
        "score_ranges": score_ranges,
        "recent_applications": recent_applications,
        "page_title": "DadBods Client Pipeline Dashboard",
    }
    return render(request, "admin/applications/dashboard.html", context)
