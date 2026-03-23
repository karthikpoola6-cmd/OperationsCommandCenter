"""
AI Incident Summarizer

Uses Claude API to generate root-cause analysis summaries and
recommended actions for operational incidents.
"""

import os
import httpx
from typing import Optional


ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
MODEL = "claude-sonnet-4-20250514"


async def generate_incident_summary(
    title: str,
    incident_type: str,
    description: str,
    severity: str,
) -> Optional[str]:
    """Generate an AI-powered root-cause summary and recommended actions."""
    if not ANTHROPIC_API_KEY:
        return _fallback_summary(title, incident_type, description, severity)

    prompt = f"""You are an operations analyst at a supply chain command center.
Analyze this incident and provide:
1. A concise root-cause summary (2-3 sentences)
2. Recommended immediate actions (3-5 bullet points)
3. Preventive measures (2-3 bullet points)

Incident Details:
- Title: {title}
- Type: {incident_type}
- Severity: {severity}
- Description: {description}
"""

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": ANTHROPIC_API_KEY,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": MODEL,
                    "max_tokens": 500,
                    "messages": [{"role": "user", "content": prompt}],
                },
            )
            resp.raise_for_status()
            data = resp.json()
            return data["content"][0]["text"]
    except Exception:
        return _fallback_summary(title, incident_type, description, severity)


def _fallback_summary(title: str, incident_type: str, description: str, severity: str) -> str:
    """Rule-based fallback when API is unavailable."""
    actions = {
        "shipment_delay": (
            f"**Root Cause Analysis:** {title}\n"
            f"The {severity}-severity delay is likely caused by carrier capacity issues, "
            "weather disruptions, or upstream supply bottlenecks.\n\n"
            "**Recommended Actions:**\n"
            "- Contact carrier for updated ETA and status\n"
            "- Evaluate rerouting options for priority shipments\n"
            "- Notify downstream customers of revised delivery timeline\n"
            "- Escalate to logistics manager if delay exceeds 24 hours\n\n"
            "**Preventive Measures:**\n"
            "- Implement multi-carrier redundancy for critical routes\n"
            "- Add predictive delay scoring based on historical patterns"
        ),
        "system_outage": (
            f"**Root Cause Analysis:** {title}\n"
            f"System outage ({severity}) may be caused by infrastructure failure, "
            "deployment issues, or resource exhaustion.\n\n"
            "**Recommended Actions:**\n"
            "- Check system health dashboards and recent deployments\n"
            "- Initiate failover if available\n"
            "- Notify affected teams and stakeholders\n"
            "- Begin incident timeline documentation\n\n"
            "**Preventive Measures:**\n"
            "- Implement automated health checks and circuit breakers\n"
            "- Review capacity planning and scaling thresholds"
        ),
        "sla_breach": (
            f"**Root Cause Analysis:** {title}\n"
            f"SLA breach ({severity}) indicates resolution time exceeded targets, "
            "likely due to resource constraints or inadequate triage.\n\n"
            "**Recommended Actions:**\n"
            "- Reassign to senior team or additional resources\n"
            "- Review incident priority and escalation path\n"
            "- Communicate revised timeline to stakeholders\n\n"
            "**Preventive Measures:**\n"
            "- Improve initial triage accuracy\n"
            "- Add automated escalation rules for aging incidents"
        ),
    }

    return actions.get(
        incident_type,
        (
            f"**Root Cause Analysis:** {title}\n"
            f"Incident type '{incident_type}' with {severity} severity requires investigation. "
            f"{description}\n\n"
            "**Recommended Actions:**\n"
            "- Investigate root cause and gather additional data\n"
            "- Assign to appropriate team for resolution\n"
            "- Track resolution progress and update stakeholders"
        ),
    )
