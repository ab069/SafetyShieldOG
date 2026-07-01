from collections import Counter
from statistics import mean

SEVERITY_WEIGHTS = {"critical": 40, "high": 30, "medium": 20, "low": 10}

def analyze_incident_trends(incidents: list) -> dict:
    total = len(incidents)
    if total == 0:
        return {"trend": "no_data", "recurring_root_causes": [], "severity_distribution": {}}

    severity_dist = Counter(i.severity for i in incidents)
    type_dist = Counter(i.incident_type for i in incidents)

    all_causes = []
    for i in incidents:
        if i.root_cause:
            for cause in i.root_cause:
                if isinstance(cause, dict):
                    all_causes.append(cause.get("cause", str(cause)))
                else:
                    all_causes.append(str(cause))
    recurring = [item for item, count in Counter(all_causes).most_common(5) if count > 1]

    dominant_type = type_dist.most_common(1)[0][0] if type_dist else None
    dominant_severity = severity_dist.most_common(1)[0][0] if severity_dist else None

    return {
        "trend": "increasing" if total > 10 else "stable",
        "total_incidents": total,
        "dominant_type": dominant_type,
        "dominant_severity": dominant_severity,
        "recurring_root_causes": recurring,
        "severity_distribution": dict(severity_dist),
        "type_distribution": dict(type_dist),
    }

def calculate_safety_score(
    incidents_severity: list[str],
    observations_closed: int,
    permits_compliant: int,
    total_permits: int = 1,
    total_observations: int = 1,
) -> int:
    if not incidents_severity:
        return 100

    severity_scores = [max(0, 100 - SEVERITY_WEIGHTS.get(s, 10)) for s in incidents_severity]
    avg_severity = mean(severity_scores)

    obs_rate = (observations_closed / max(total_observations, 1)) * 100
    permit_rate = (permits_compliant / max(total_permits, 1)) * 100

    score = int(avg_severity * 0.5 + obs_rate * 0.25 + permit_rate * 0.25)
    return max(0, min(100, score))

def assess_permit_risk(work_type: str, risk_assessment: list) -> dict:
    risk_map = {
        "hot_work": {"level": "high", "factors": ["fire", "burns", "explosion"]},
        "confined_space": {"level": "critical", "factors": ["asphyxiation", "toxic_gases", "entrapment"]},
        "height": {"level": "high", "factors": ["fall", "dropped_objects"]},
        "electrical": {"level": "high", "factors": ["shock", "arc_flash", "fire"]},
        "excavation": {"level": "medium", "factors": ["collapse", "underground_services"]},
        "cold_work": {"level": "low", "factors": ["general_safety"]},
    }

    base = risk_map.get(work_type, {"level": "medium", "factors": ["general"]})
    mitigating = len(risk_assessment) if risk_assessment else 0
    level = base["level"]

    if mitigating >= 5:
        level = {"critical": "high", "high": "medium", "medium": "low", "low": "low"}.get(level, "low")

    return {
        "work_type": work_type,
        "risk_level": level,
        "hazards": base["factors"],
        "mitigation_count": mitigating,
        "recommendations": [
            f"Implement controls for: {', '.join(base['factors'])}",
            "Ensure all personnel are trained and equipped",
            "Maintain constant communication with permit issuer",
        ],
    }

def generate_hse_report(safety_score: int, findings: dict) -> str:
    rating = "Excellent" if safety_score >= 80 else "Good" if safety_score >= 60 else "Needs Improvement" if safety_score >= 40 else "Critical"
    return (
        f"HSE Performance Report\n"
        f"{'=' * 40}\n"
        f"Safety Score: {safety_score}/100 ({rating})\n\n"
        f"Key Findings:\n"
        f"- Total incidents: {findings.get('incidents', {}).get('total', 'N/A')}\n"
        f"- Open incidents: {findings.get('incidents', {}).get('open', 'N/A')}\n"
        f"- Active permits: {findings.get('permits', {}).get('active', 'N/A')}\n"
        f"- Open observations: {findings.get('observations', {}).get('open', 'N/A')}\n\n"
        f"Recurring root causes: {', '.join(findings.get('trends', {}).get('recurring_root_causes', [])) or 'None identified'}\n"
        f"Recommendation: {'Continue current HSE practices' if safety_score >= 60 else 'Immediate HSE review required'}"
    )
