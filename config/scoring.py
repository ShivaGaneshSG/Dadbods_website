"""
DadBods Coaching Qualification Scoring Configuration.

Defines weights, scoring criteria, and status thresholds for automatic applicant scoring.
The score runs from 0 to 100 and assesses goal clarity, training availability,
nutrition readiness, self-rated follow-through, start urgency, budget fit, and written depth.
Medical conditions or injuries flag the profile for human review without penalizing the score.
"""

SCORING_WEIGHTS = {
    # 1. Goal clarity & depth (Max 10 pts)
    "goal_clarity": {
        "max_points": 10,
        "valid_goal_points": 4,
        "detailed_target_min_words": 15,
        "detailed_target_full_points": 6,
        "detailed_target_short_points": 3,
    },
    # 2. Training availability & environment (Max 15 pts)
    "training_commitment": {
        "max_points": 15,
        "days_points": {
            "4": 10,
            "5": 10,
            "3": 8,
            "6+": 7,
            "1–2": 4,
            "1-2": 4,
            "0": 1,
        },
        "location_points": {
            "Gym": 5,
            "Both": 5,
            "Home": 3,
        },
    },
    # 3. Nutrition tracking willingness & consistency (Max 15 pts)
    "nutrition_readiness": {
        "max_points": 15,
        "tracking_willingness": {
            "very_willing": 10,
            "willing": 8,
            "somewhat_hesitant": 4,
            "not_willing": 1,
        },
        "diet_consistency": {
            "very_consistent": 5,
            "fairly_consistent": 4,
            "somewhat_inconsistent": 3,
            "very_inconsistent": 2,
        },
    },
    # 4. Coach follow-through commitment (Max 15 pts, based on 1-10 scale)
    "follow_through": {
        "max_points": 15,
        "scale_multiplier": 1.5,  # 10 * 1.5 = 15 pts
    },
    # 5. Readiness to start timeline (Max 15 pts)
    "start_timeline": {
        "max_points": 15,
        "timeline_points": {
            "immediately": 15,
            "within_1_week": 13,
            "within_2_weeks": 10,
            "within_1_month": 6,
            "exploring": 2,
        },
    },
    # 6. Coaching investment / budget tier alignment (Max 15 pts)
    "coaching_budget": {
        "max_points": 15,
        "budget_points": {
            "tier_premium": 15,    # ₹10,000+ / month
            "tier_standard": 13,   # ₹7,000 - ₹10,000 / month
            "tier_core": 10,       # ₹5,000 - ₹7,000 / month
            "tier_entry": 6,       # ₹3,500 - ₹5,000 / month
            "tier_budget": 2,      # Under ₹3,500 / month
        },
    },
    # 7. Written response effort & coachability (Max 15 pts)
    # Evaluates word count and effort in: why_dadbods, consistency_problem, biggest_obstacle
    "written_effort": {
        "max_points": 15,
        "why_dadbods_threshold_words": 12,
        "obstacle_threshold_words": 10,
        "attempts_threshold_words": 10,
        "each_detailed_field_points": 5,
        "each_short_field_points": 2,
    },
}

# Qualification Status Thresholds
STATUS_THRESHOLDS = {
    "PRIORITY": 80,       # 80 - 100
    "QUALIFIED": 65,      # 65 - 79
    "REVIEW": 45,         # 45 - 64
    "LOW_PRIORITY": 0,    # 0 - 44
}

STATUS_LABELS = {
    "PRIORITY": "Priority Lead",
    "QUALIFIED": "Qualified Lead",
    "REVIEW": "Manual Review Needed",
    "LOW_PRIORITY": "Low Priority",
}
