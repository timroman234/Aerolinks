# caddy.py
"""
AeroLinks AI Caddy
OpenAI-powered golf shot analysis with witty, professional feedback.
"""
import os
from openai import OpenAI


def get_caddy_feedback(
    club_type: str,
    club_speed: float,
    wind_speed: float,
    wind_direction: str,
    carry: float,
    apex: float,
    landing_angle: float
) -> str:
    """
    Generate AI caddy feedback for a golf shot using OpenAI GPT-4o-mini.
    Falls back to rule-based responses if API key is absent.

    Args:
        club_type: Selected club
        club_speed: Club head speed in mph
        wind_speed: Wind speed in mph
        wind_direction: "Headwind" or "Tailwind"
        carry: Carry distance in yards
        apex: Maximum height in feet
        landing_angle: Descent angle in degrees

    Returns:
        Caddy feedback string
    """
    api_key = os.environ.get("OPENAI_API_KEY")

    # Construct context payload for the AI
    context = f"""
Club Selected: {club_type}
Swing Speed: {club_speed} mph
Wind Vector: {wind_speed} mph {wind_direction}
Simulated Carry: {carry} yards
Ball Flight Apex: {apex} feet
Descent Landing Angle: {landing_angle} degrees
"""

    system_prompt = """You are an elite, highly technical PGA Tour Caddy.
You analyze shot tracking data with clinical accuracy, combined with a sharp, dry wit.
Deliver a concise, 2-to-3 sentence critique of this shot execution.
Highlight how the environment or backspin interacted with club selection.
If the user hit a high-lofted short iron into strong headwind, explain why the ball ballooned.
Keep the tone authentic, direct, and conversational. No intro/outro filler."""

    # Fallback to rule-based responses if no API key
    if not api_key:
        return _get_fallback_feedback(club_type, club_speed, wind_speed, wind_direction, carry, apex, landing_angle)

    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=150,
            temperature=0.75,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": context}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return _get_fallback_feedback(club_type, club_speed, wind_speed, wind_direction, carry, apex, landing_angle)


def _get_fallback_feedback(
    club_type: str,
    club_speed: float,
    wind_speed: float,
    wind_direction: str,
    carry: float,
    apex: float,
    landing_angle: float
) -> str:
    """Rule-based fallback responses when API is unavailable."""

    # High-lofted club into strong headwind - ballooning
    if wind_speed > 25 and wind_direction == "Headwind" and club_type in ["7-Iron", "PW"]:
        return (
            f"That high-lofted {club_type} ballooned straight up into the {wind_speed} mph gale. "
            f"The backspin created excessive lift against the wind. "
            f"Consider punching a lower-spin 5-iron to pierce through that wall of air."
        )

    # Strong tailwind with driver - maximizing distance
    if wind_speed > 20 and wind_direction == "Tailwind" and club_type == "Driver":
        return (
            f"Outstanding execution. You rode that {wind_speed} mph tailwind perfectly. "
            f"{carry} yards of carry with minimized relative drag - that's textbook wind management."
        )

    # Headwind reducing carry significantly
    if wind_speed > 15 and wind_direction == "Headwind":
        lost_yards = int(wind_speed * 1.5)
        return (
            f"The {wind_speed} mph headwind cost you roughly {lost_yards} yards on that {club_type}. "
            f"Your {landing_angle}° descent angle shows good trajectory control despite the conditions."
        )

    # High apex with short iron
    if apex > 80 and club_type in ["7-Iron", "PW"]:
        return (
            f"That {club_type} peaked at {apex} feet - plenty of height to hold a firm green. "
            f"The {landing_angle}° landing angle will stop the ball quickly with minimal roll-out."
        )

    # Low trajectory driver
    if apex < 90 and club_type == "Driver":
        return (
            f"A penetrating ball flight at {apex} feet apex. "
            f"Good choice for control, though you might add 10-15 yards with a higher launch angle."
        )

    # Default solid shot feedback
    return (
        f"A solid, clinical strike with the {club_type}. "
        f"Carrying it {carry} yards to an apex of {apex} feet gives you a controllable "
        f"{landing_angle}° descent angle onto the green."
    )
