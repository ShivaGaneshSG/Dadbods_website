"""
DadBods Application Qualification Scoring Service.
Evaluates applicant submissions using weights configured in `config/scoring.py`.
Transparent, deterministic, and modular.
"""

from config.scoring import SCORING_WEIGHTS, STATUS_THRESHOLDS, STATUS_LABELS


def word_count(text: str) -> int:
    """Helper to count words in a free-text field."""
    if not text:
        return 0
    return len(text.strip().split())


def calculate_qualification_score(data: dict) -> dict:
    """
    Computes qualification score (0-100), qualification status, medical review flag,
    and a detailed point breakdown for coach transparency.
    """
    breakdown = {}
    total = 0.0

    # 1. Goal Clarity & Specificity (Max 10)
    w_goal = SCORING_WEIGHTS["goal_clarity"]
    goal_pts = 0
    if data.get("goal") and data.get("goal") != "other":
        goal_pts += w_goal["valid_goal_points"]
    else:
        goal_pts += 2

    target_words = word_count(data.get("target_description", ""))
    if target_words >= w_goal["detailed_target_min_words"]:
        goal_pts += w_goal["detailed_target_full_points"]
    elif target_words >= 5:
        goal_pts += w_goal["detailed_target_short_points"]
    else:
        goal_pts += 1

    goal_pts = min(goal_pts, w_goal["max_points"])
    breakdown["goal_clarity"] = {
        "points": goal_pts,
        "max": w_goal["max_points"],
        "detail": f"Goal selected; target description contains {target_words} words.",
    }
    total += goal_pts

    # 2. Training Commitment & Environment (Max 15)
    w_train = SCORING_WEIGHTS["training_commitment"]
    train_pts = 0
    commit_days = str(data.get("realistic_training_commitment") or data.get("training_days") or "4")
    train_pts += w_train["days_points"].get(commit_days, 6)

    location = data.get("preferred_training_location", "Gym")
    train_pts += w_train["location_points"].get(location, 4)

    train_pts = min(train_pts, w_train["max_points"])
    breakdown["training_commitment"] = {
        "points": train_pts,
        "max": w_train["max_points"],
        "detail": f"Can commit {commit_days} days/week at {location}.",
    }
    total += train_pts

    # 3. Nutrition Readiness & Consistency (Max 15)
    w_nutr = SCORING_WEIGHTS["nutrition_readiness"]
    nutr_pts = 0
    track_readiness = str(data.get("nutrition_tracking_readiness", "willing"))
    nutr_pts += w_nutr["tracking_willingness"].get(track_readiness, 5)

    consistency = str(data.get("diet_consistency", "somewhat_inconsistent"))
    nutr_pts += w_nutr["diet_consistency"].get(consistency, 3)

    nutr_pts = min(nutr_pts, w_nutr["max_points"])
    breakdown["nutrition_readiness"] = {
        "points": nutr_pts,
        "max": w_nutr["max_points"],
        "detail": f"Tracking readiness: {track_readiness}; Current consistency: {consistency}.",
    }
    total += nutr_pts

    # 4. Coach Follow-Through Score (Max 15)
    w_ft = SCORING_WEIGHTS["follow_through"]
    raw_ft = data.get("follow_through_score", 7)
    try:
        raw_ft = int(raw_ft)
    except (ValueError, TypeError):
        raw_ft = 7
    raw_ft = max(1, min(10, raw_ft))
    ft_pts = round(raw_ft * w_ft["scale_multiplier"], 1)
    ft_pts = min(ft_pts, w_ft["max_points"])
    breakdown["follow_through"] = {
        "points": ft_pts,
        "max": w_ft["max_points"],
        "detail": f"Self-rated coach compliance: {raw_ft}/10.",
    }
    total += ft_pts

    # 5. Readiness to Start Timeline (Max 15)
    w_time = SCORING_WEIGHTS["start_timeline"]
    timeline = str(data.get("start_timeline", "within_1_week"))
    time_pts = w_time["timeline_points"].get(timeline, 6)
    time_pts = min(time_pts, w_time["max_points"])
    breakdown["start_timeline"] = {
        "points": time_pts,
        "max": w_time["max_points"],
        "detail": f"Desired start timeline: {timeline.replace('_', ' ').title()}.",
    }
    total += time_pts

    # 6. Coaching Budget / Investment Range (Max 15)
    w_budget = SCORING_WEIGHTS["coaching_budget"]
    budget_choice = str(data.get("coaching_budget", "tier_core"))
    budget_pts = w_budget["budget_points"].get(budget_choice, 8)
    budget_pts = min(budget_pts, w_budget["max_points"])
    breakdown["coaching_budget"] = {
        "points": budget_pts,
        "max": w_budget["max_points"],
        "detail": f"Investment tier: {budget_choice}.",
    }
    total += budget_pts

    # 7. Written Response Effort & Coachability (Max 15)
    w_effort = SCORING_WEIGHTS["written_effort"]
    effort_pts = 0

    why_words = word_count(data.get("why_dadbods", ""))
    if why_words >= w_effort["why_dadbods_threshold_words"]:
        effort_pts += w_effort["each_detailed_field_points"]
    elif why_words >= 4:
        effort_pts += w_effort["each_short_field_points"]

    obstacle_words = word_count(data.get("biggest_obstacle", ""))
    if obstacle_words >= w_effort["obstacle_threshold_words"]:
        effort_pts += w_effort["each_detailed_field_points"]
    elif obstacle_words >= 3:
        effort_pts += w_effort["each_short_field_points"]

    attempts_words = word_count(data.get("previous_attempts", ""))
    if attempts_words >= w_effort["attempts_threshold_words"]:
        effort_pts += w_effort["each_detailed_field_points"]
    elif attempts_words >= 3:
        effort_pts += w_effort["each_short_field_points"]

    effort_pts = min(effort_pts, w_effort["max_points"])
    breakdown["written_effort"] = {
        "points": effort_pts,
        "max": w_effort["max_points"],
        "detail": (
            f"Written effort: Why DadBods ({why_words} words), "
            f"Obstacle ({obstacle_words} words), "
            f"Past attempts ({attempts_words} words)."
        ),
    }
    total += effort_pts

    # Clamp total score 0 - 100
    final_score = int(round(min(100.0, max(0.0, total))))

    # Determine status based on thresholds
    if final_score >= STATUS_THRESHOLDS["PRIORITY"]:
        status = "PRIORITY"
    elif final_score >= STATUS_THRESHOLDS["QUALIFIED"]:
        status = "QUALIFIED"
    elif final_score >= STATUS_THRESHOLDS["REVIEW"]:
        status = "REVIEW"
    else:
        status = "LOW_PRIORITY"

    # Health & Medical Check: Flags for human review without penalizing score
    has_injury = bool(data.get("previous_injury"))
    has_medical = bool(data.get("medical_condition"))
    has_medication = bool(data.get("medication"))
    requires_medical_review = has_injury or has_medical or has_medication

    medical_notes = []
    if has_injury:
        medical_notes.append("Disclosed previous injury")
    if has_medical:
        medical_notes.append("Disclosed medical condition")
    if has_medication:
        medical_notes.append("Disclosed active medication")

    breakdown["medical_review_flag"] = {
        "flagged": requires_medical_review,
        "reasons": medical_notes,
    }

    return {
        "score": final_score,
        "status": status,
        "status_label": STATUS_LABELS.get(status, status),
        "requires_medical_review": requires_medical_review,
        "breakdown": breakdown,
    }
