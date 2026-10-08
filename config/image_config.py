"""
DadBods Image Configuration System.

The SINGLE SOURCE OF TRUTH for all website image paths.
Templates access images via the `dadbods_images` context processor.
Supports dynamic discovery and graceful SVG fallbacks.
"""

from pathlib import Path
import os
import urllib.parse

# Root image directories (configurable)
BASE_DIR = Path(__file__).resolve().parent.parent
IMAGE_ROOT = Path(os.environ.get("DADBODS_IMAGE_ROOT", str(BASE_DIR / "images")))

LOGO_DIR = IMAGE_ROOT / "logo"
ALL_IMAGES_DIR = IMAGE_ROOT / "all"
ATHISH_DIR = IMAGE_ROOT / "athish"
KARAN_DIR = IMAGE_ROOT / "karan"
SHRI_DIR = IMAGE_ROOT / "shri"
TRANSFORMATIONS_DIR = IMAGE_ROOT / "Transformations"

IMAGE_BASE_URL = "/images/"

# Fallbacks
FALLBACK_IMAGE = "/static/img/fallback-image.svg"
FALLBACK_AVATAR = "/static/img/fallback-avatar.svg"


def resolve_image(relative_path: str, fallback: str = FALLBACK_IMAGE) -> str:
    """
    Resolves relative path inside IMAGE_ROOT to a public URL.
    Encodes URL characters (spaces, unicode) and falls back if missing.
    """
    if not relative_path:
        return fallback

    file_path = IMAGE_ROOT / relative_path
    if not file_path.exists():
        return fallback

    parts = relative_path.replace("\\", "/").split("/")
    encoded_parts = [urllib.parse.quote(part) for part in parts]
    return IMAGE_BASE_URL + "/".join(encoded_parts)


def get_logo_path() -> str:
    """Discovers the SVG logo in images/logo/."""
    if LOGO_DIR.exists():
        # Look for SVG first
        svg_files = [f for f in os.listdir(LOGO_DIR) if f.lower().endswith(".svg")]
        if svg_files:
            return resolve_image(f"logo/{svg_files[0]}")
        # Look for PNG fallback if needed
        png_files = [f for f in os.listdir(LOGO_DIR) if f.lower().endswith(".png")]
        if png_files:
            return resolve_image(f"logo/{png_files[0]}")
    return "/images/logo/dadbods_logo.svg"


# Names Only: Athish, Karan, Shri (No roles, titles, or descriptions)
COACH_DATA = {
    "athish": {
        "slug": "athish",
        "name": "Athish",
        "primary_image_rel": "athish/athish.jpg",
        "gallery_rel": [
            "athish/athish.jpg",
            "athish/athish2.jpg",
        ],
    },
    "karan": {
        "slug": "karan",
        "name": "Karan",
        "primary_image_rel": "karan/karan.jpg",
        "gallery_rel": [
            "karan/karan.jpg",
            "karan/karan2.jpg",
        ],
    },
    "shri": {
        "slug": "shri",
        "name": "Shri",
        "primary_image_rel": "shri/shri.jpg",
        "gallery_rel": [
            "shri/shri.jpg",
            "shri/shri2.jpg",
            "shri/shri3.jpg",
            "shri/shri4.jpg",
        ],
    },
}


def get_image_config() -> dict:
    """
    Constructs the master image dictionary used across templates.
    """
    logo_url = get_logo_path()

    # 1. General & Hero Images (from images/all/)
    hero_image = "all/all.jpg"
    if ALL_IMAGES_DIR.exists():
        all_imgs = [
            f for f in os.listdir(ALL_IMAGES_DIR)
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
        ]
        if all_imgs:
            hero_image = f"all/{all_imgs[0]}"

    general = {
        "hero_bg": resolve_image(hero_image),
        "team_banner": resolve_image(hero_image),
    }

    # 2. Coaches
    coaches = {}
    for key, cdata in COACH_DATA.items():
        profile_url = resolve_image(cdata["primary_image_rel"], fallback=FALLBACK_AVATAR)
        gallery_urls = [
            resolve_image(grel, fallback=FALLBACK_AVATAR) for grel in cdata["gallery_rel"]
        ]
        coaches[key] = {
            **cdata,
            "profile_image": profile_url,
            "gallery": gallery_urls,
        }

    # 3. Transformations (Direct from images/Transformations/, no fake claims)
    transformations = []
    if TRANSFORMATIONS_DIR.exists():
        files = sorted(os.listdir(TRANSFORMATIONS_DIR))
        for idx, fname in enumerate(files):
            if fname.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                rel_path = f"Transformations/{fname}"
                transformations.append({
                    "id": f"trans-{idx+1}",
                    "image_url": resolve_image(rel_path),
                    "filename": fname,
                })

    return {
        "logo": logo_url,
        "general": general,
        "coaches": coaches,
        "transformations": transformations,
        "placeholders": {
            "default": FALLBACK_IMAGE,
            "avatar": FALLBACK_AVATAR,
        },
    }
