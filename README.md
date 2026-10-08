# DadBods — Premium Minimal Fitness Coaching & Client Selection Platform

A refined, production-ready Django web application for **DadBods**, an elite Tamil fitness coaching brand founded and run by three coaches: **Athish**, **Karan**, and **Shri**.

Designed with an **Instagram-first, dark, minimal, and modern** aesthetic: high visual impact, editorial typography, cinematic imagery, and virtually no unnecessary text. The backend preserves the complete **client acquisition and qualification system**: an automated 6-step questionnaire, transparent qualification scoring (0–100), and a customized Django Admin CRM for vetting applicants and booking discovery calls.

---

## Key Features

1. **Premium Dark Navy & Indigo Aesthetic**:
   - Palette: Near Black (`#0C1014`), Charcoal (`#2B3036`), Dark Gray (`#181B21`), Deep Navy (`#0B0931`), Dark Indigo (`#0A0724`), and Off-White typography (`#E7E7E4`).
   - Official Brand Slogan: **"RIGHT TIME. RIGHT NOW."**
   - Clean sans-serif typography (`Space Grotesk` headings + `Inter` body).
   - Full-screen cinematic hero powered by `images/all/all.jpg` with layered navy/indigo gradient overlays.
   - Vector SVG logo integration across Navbar, Hero, Application page, and Footer.
2. **Exactly 4 Public Pages (Unified Navigation)**:
   - **HOME (`/`)**: Full-screen hero, "Built for Progress" overview, Athish/Karan/Shri showcase, Transformations preview, 4 Pillars, and Final CTA.
   - **TRANSFORMATIONS (`/transformations/`)**: Responsive masonry gallery with real client shifts and lightbox modal.
   - **ABOUT (`/about/`)**: Team showcase for Athish, Karan, and Shri with authentic bios, "Our Approach" methodology, and brand statement.
   - **GET TRAINED BY DADBODS (`/apply/`)**: Integrated coaching info (4 pillars) + 6-step client selection onboarding wizard.
3. **Dedicated Single Image Configuration (`config/image_config.py`)**: All website images are registered in one file. Templates access them dynamically via context processors without hard-coded paths.
4. **6-Step Application Wizard (`/apply/`)**:
   - Steps: `01 ABOUT YOU`, `02 GOAL`, `03 TRAINING`, `04 LIFESTYLE`, `05 COMMITMENT`, `06 FINAL DETAILS`.
   - Preserves all database models, Django form validation, CSRF, and anti-spam protection.
5. **Transparent Qualification Scoring (0–100)**: Deterministic qualification scoring engine evaluating commitment, goals, and consistency.
6. **Medical / Injury Review Flagging**: Disclosed injuries or medical conditions never penalize the score; they flag the lead with an urgent review badge (`⚠️ Medical Flag`) so coaches can make safe, informed choices.
7. **Executive CRM Dashboard (`/dashboard/`) & Django Admin**: Pipeline filtering, bulk actions, and collaborative coach notes.

---

## Project Structure

```
d:/Dadbods/Website/
│
├── manage.py
│
├── config/                         # Core Project Configuration
│   ├── __init__.py
│   ├── settings.py                 # Django settings, budget choices, env vars
│   ├── urls.py                     # Root routing + dedicated image serve route
│   ├── image_config.py             # SINGLE SOURCE OF TRUTH for all images
│   ├── scoring.py                  # Configurable scoring weights & status thresholds
│   ├── asgi.py
│   └── wsgi.py
│
├── core/                           # Public Brand Pages & Global Processors
│   ├── views.py                    # Home, About, Coaches, Coaching, Transformations
│   ├── urls.py
│   ├── context_processors.py       # Exposes dadbods_images & brand meta to all templates
│   └── tests.py
│
├── applications/                   # Client Acquisition & Scoring Engine
│   ├── models.py                   # CoachingApplication & ApplicationNote models
│   ├── forms.py                    # Multi-step validation, honeypot & widgets
│   ├── views.py                    # Apply view, success view & staff dashboard
│   ├── scoring.py                  # Deterministic qualification scoring engine
│   ├── admin.py                    # Custom Admin CRM with badges, filters & actions
│   ├── urls.py
│   └── tests.py
│
├── templates/
│   ├── base.html                   # HTML5 layout, meta, navbar & footer
│   ├── components/
│   │   ├── navbar.html             # Responsive navbar with mobile drawer
│   │   └── footer.html             # Brand footer & medical disclaimer
│   ├── core/
│   │   ├── home.html               # High-impact hero, pillars, coach previews
│   │   ├── about.html              # DadBods mission, founders story, 3 pillars
│   │   ├── coaches.html            # Athish, Karan, Shri showcases & galleries
│   │   ├── coaching.html           # Training, Nutrition, Accountability, Support
│   │   └── transformations.html    # Real client results gallery
│   ├── applications/
│   │   ├── apply.html              # Multi-step wizard with progress track
│   │   └── success.html            # Post-submission confirmation
│   └── admin/
│       └── applications/
│           └── dashboard.html      # Executive CRM metrics & charts
│
├── static/
│   ├── css/main.css                # Dark premium athletic design system
│   ├── js/main.js                  # Global navbar & micro-interactions
│   ├── js/apply.js                 # Wizard step logic & validation
│   └── img/
│       ├── fallback-image.svg      # Graceful image placeholder
│       └── fallback-avatar.svg     # Graceful coach silhouette placeholder
│
├── images/                         # Existing Website Assets
│   ├── all/                        # Team banner (all.jpg)
│   ├── athish/                     # Athish photos (athish.jpg, athish2.jpg)
│   ├── karan/                      # Karan photos (karan.jpg, karan2.jpg)
│   ├── shri/                       # Shri photos (shri.jpg, shri2.jpg, ...)
│   └── Transformations/            # Authentic client transformation graphics
│
├── .env.example
├── .env
├── requirements.txt
└── README.md
```

---

## Installation & Setup

### 1. Prerequisites
- Python 3.10+
- pip

### 2. Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Activate on Command Prompt:
.\venv\Scripts\activate.bat
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Default `.env` options:
```ini
SECRET_KEY=your-secure-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
ADMIN_NOTIFICATION_EMAIL=team@dadbods.in
DEFAULT_FROM_EMAIL=notifications@dadbods.in

# Optional custom image directory override (defaults to ./images):
# DADBODS_IMAGE_ROOT=D:/Dadbods/Website/images
```

### 5. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Admin Access)
```bash
python manage.py createsuperuser
```
*(Default test account: Username `admin`, Password `adminpassword123`)*

### 7. Run Unit & Integration Tests
```bash
python manage.py test
```
All 13 tests verify scoring math, multi-step validation, honeypot deflection, public views, and image fallbacks.

### 8. Start Development Server
```bash
python manage.py runserver 127.0.0.1:8000
```
Visit:
- **Public Website**: `http://127.0.0.1:8000/`
- **Application Form**: `http://127.0.0.1:8000/apply/`
- **Django Admin CRM**: `http://127.0.0.1:8000/admin/`
- **Executive CRM Dashboard**: `http://127.0.0.1:8000/dashboard/` (Staff only)

---

## Dedicated Image Configuration (`config/image_config.py`)

All image paths are registered in **one file**: `config/image_config.py`.

### How It Works:
1. `IMAGE_ROOT` points to `BASE_DIR / 'images'` (or `DADBODS_IMAGE_ROOT` from `.env`).
2. `resolve_image(rel_path)` checks if the file exists on disk.
   - If found, it safely URL-encodes special characters/emojis (e.g. `Client Transformation from UK 🇬🇧...webp`) and returns `/images/<path>`.
   - If missing, it returns `/static/img/fallback-image.svg` without throwing an error.
3. Templates access images automatically via the `dadbods_images` context processor:
   ```django
   <img src="{{ dadbods_images.general.hero_bg }}">
   <img src="{{ dadbods_images.coaches.athish.profile_image }}">
   <img src="{{ dadbods_images.coaches.karan.profile_image }}">
   <img src="{{ dadbods_images.coaches.shri.profile_image }}">
   ```

### How to Add or Change Images:
- **Add a coach image**: Drop a photo into `images/athish/`, `images/karan/`, or `images/shri/` and update `COACH_DATA` in `config/image_config.py`.
- **Add a transformation**: Drop the file into `images/Transformations/`. The system auto-discovers new transformation files while preserving custom captions in `TRANSFORMATION_METADATA`!

---

## Application Scoring System (`config/scoring.py`)

Every application is evaluated from **0 to 100** points across 7 objective categories:

| Category | Max Pts | Criteria Evaluated |
|---|---|---|
| **Goal Clarity** | 10 | Valid primary goal selected + depth of 3–6 month description |
| **Training Commitment** | 15 | Realistic days committed (3–5 is optimal) + training location (Gym/Home) |
| **Nutrition Readiness** | 15 | Willingness to track food + diet consistency awareness |
| **Follow-Through Score** | 15 | Self-rated compliance scale (1–10) with coach adjustments |
| **Readiness to Start** | 15 | Urgency: Immediately (15), 1 week (13), 2 weeks (10), Exploring (2) |
| **Coaching Budget** | 15 | Tier alignment with coaching investment levels |
| **Written Effort** | 15 | Thoughtfulness and word count in *Why DadBods*, *Obstacle*, and *Past Attempts* |

### Qualification Status Thresholds:
- **Score 80 – 100**: `PRIORITY` (Emerald Badge) — Immediate discovery call recommended.
- **Score 65 – 79**: `QUALIFIED` (Blue Badge) — Strong fit for coaching.
- **Score 45 – 64**: `REVIEW` (Amber Badge) — Requires manual coach review.
- **Score 0 – 44**: `LOW_PRIORITY` (Gray Badge) — May not be ready for 1-on-1 coaching.

### Medical / Injury Handling:
Medical conditions, past injuries, and ongoing medications **do NOT penalize the score**. Instead, they flag the applicant with:
```
requires_medical_review = True (⚠️ Medical Flag)
```
This alerts Athish, Karan, and Shri to review the physical disclosure prior to the discovery call.

### How to Modify Scoring Weights:
Open `config/scoring.py` and adjust `SCORING_WEIGHTS` or `STATUS_THRESHOLDS`.

---

## How to Configure Coaching Budget Tiers

The coaching investment choices are managed in `config/settings.py` via `COACHING_BUDGET_CHOICES`:

```python
COACHING_BUDGET_CHOICES = [
    ("tier_premium", "₹10,000+ / month (Elite 1-on-1 Coaching)"),
    ("tier_standard", "₹7,000 – ₹10,000 / month (Standard Intensive)"),
    ("tier_core", "₹5,000 – ₹7,000 / month (Core Protocol)"),
    ("tier_entry", "₹3,500 – ₹5,000 / month (Essential Guidance)"),
    ("tier_budget", "Under ₹3,500 / month"),
]
```
Modifying this list updates the application dropdown, the model choices, and the scoring engine automatically.

---

## Admin CRM & Client Selection Workflow

1. Navigate to `http://127.0.0.1:8000/admin/`.
2. Click **Coaching Applications**:
   - Inspect applicants ranked by **Qualification Score**.
   - Use right-side filters: *Client Status*, *Qualification Status*, *Medical Flag*, *Goal*, *Start Timeline*, *Budget*.
   - Use search bar to find applicants by name, email, WhatsApp, or Instagram handle.
3. Open an applicant to review their complete 6-step questionnaire and points breakdown.
4. Use **Coach Internal Notes** to log comments between Athish, Karan, and Shri.
5. Use bulk actions to move candidates through the pipeline:
   - *Mark as Under Review*
   - *Mark as Discovery Call Booked*
   - *Mark as Accepted Client*
   - *Mark as Not Ready*
   - *Recalculate Qualification Scores*
6. Click **Executive Dashboard** (`/dashboard/`) for aggregated lead metrics, goal breakdown bars, and pipeline volume.

---

## Future-Ready Architecture

The platform is designed for seamless extension:
- **WhatsApp Automation**: Hook into `applications/views.py` `_send_application_notifications` to dispatch WhatsApp Business API templates via Twilio or Gupshup.
- **Appointment Booking**: Integrate Calendly or Cal.com webhook on `STATUS_CALL_BOOKED`.
- **Payment Gateway**: Connect Razorpay or Stripe on `STATUS_ACCEPTED`.
- **Client Portal**: Extend `applications` model into an active `ClientProfile` with check-in schedules and progress photo uploaders.
