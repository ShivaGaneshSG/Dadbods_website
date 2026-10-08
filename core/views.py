"""
Public Views for DadBods Fitness Platform.
Server-rendered Django views with rich brand storytelling and high conversion.
"""

from django.shortcuts import render, redirect
from .youtube import get_latest_youtube_videos, YOUTUBE_CHANNEL_URL


def home_view(request):
    """
    DadBods Homepage: Minimal, visual, full-screen hero with actual YouTube channel content.
    """
    youtube_videos = get_latest_youtube_videos(limit=4)
    return render(
        request,
        "core/home.html",
        {
            "page_title": "DADBODS | RIGHT TIME. RIGHT NOW.",
            "meta_description": "Build your physique. Personalised coaching. Real results.",
            "youtube_videos": youtube_videos,
            "youtube_channel_url": YOUTUBE_CHANNEL_URL,
        },
    )


def about_view(request):
    """
    About Page: Athish, Karan, and Shri, philosophy, and brand statement.
    """
    return render(
        request,
        "core/about.html",
        {
            "page_title": "ABOUT | DADBODS",
            "meta_description": (
                "Athish, Karan, and Shri at DadBods. "
                "Structured training, practical nutrition, and continuous accountability."
            ),
        },
    )


def coaches_view(request):
    """
    Redirects to About page to consolidate the 4 primary navigation routes.
    """
    return redirect("core:about")


def coaching_view(request):
    """
    Redirects to Apply page ('GET TRAINED BY DADBODS') where coaching info is integrated.
    """
    return redirect("applications:apply")


def transformations_view(request):
    """
    Transformations Gallery: Real client results from DadBods coaching.
    """
    return render(
        request,
        "core/transformations.html",
        {
            "page_title": "Client Transformations | Real Results | DadBods",
            "meta_description": (
                "Explore real client transformations coached by Athish, Karan, and Shri. "
                "Proven physique shifts through consistent structure and accountability."
            ),
        },
    )
