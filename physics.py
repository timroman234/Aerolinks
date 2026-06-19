# physics.py
"""
AeroLinks Physics Engine
2D golf ball trajectory simulation using Euler numerical integration.
Accounts for gravity, aerodynamic drag, and Magnus lift from spin decay.
"""
import numpy as np


def calculate_flight(club_type: str, club_speed_mph: float, wind_speed_mph: float, wind_direction: str) -> dict:
    """
    Calculates a 2D golf ball trajectory using Euler numerical integration.

    Args:
        club_type: Club selection ("Driver", "5-Iron", "7-Iron", "PW")
        club_speed_mph: Club head speed in mph
        wind_speed_mph: Wind speed in mph
        wind_direction: "Headwind" or "Tailwind"

    Returns:
        Dictionary containing trajectory data and flight metrics
    """
    # --- Physical Constants ---
    g = 9.81              # Gravity (m/s^2)
    m = 0.04593           # Mass of standard golf ball (kg)
    radius = 0.02135      # Radius of golf ball (m)
    A = np.pi * (radius**2)  # Cross-sectional area (m^2)
    rho = 1.225           # Sea-level air density (kg/m^3)
    Cd = 0.23             # Drag coefficient (dimpled ball, turbulent flow)
    dt = 0.005            # Integration time step (seconds)

    # --- Club Mapping Configuration Matrix ---
    # {Club: (Launch Angle in Degrees, Initial Backspin in RPM, Smash Factor)}
    club_matrix = {
        "Driver": (12.0, 2500.0, 1.48),
        "5-Iron": (19.0, 5000.0, 1.38),
        "7-Iron": (27.0, 7000.0, 1.33),
        "PW": (42.0, 9000.0, 1.23)
    }

    launch_angle_deg, spin_rpm, smash_factor = club_matrix.get(club_type, (12.0, 2500.0, 1.48))

    # --- Unit Conversions to Metric System ---
    club_speed_ms = club_speed_mph * 0.44704
    ball_speed_ms = club_speed_ms * smash_factor
    wind_speed_ms = wind_speed_mph * 0.44704

    # Wind vector: Headwind opposes ball motion, Tailwind assists
    v_wind_x = -wind_speed_ms if wind_direction == "Headwind" else wind_speed_ms

    # Initial state kinematic vectors
    launch_angle_rad = np.radians(launch_angle_deg)
    vx = ball_speed_ms * np.cos(launch_angle_rad)
    vy = ball_speed_ms * np.sin(launch_angle_rad)
    omega = spin_rpm * (2 * np.pi / 60.0)  # Convert RPM to radians/sec

    # Positional trackers
    x, y = 0.0, 0.0
    x_history = [x]
    y_history = [y]
    t = 0.0
    max_height_m = 0.0

    # --- Explicit Euler Integration Loop ---
    while y >= 0.0:
        # Calculate ball's velocity relative to the moving air mass
        v_rel_x = vx - v_wind_x
        v_rel_y = vy
        v_rel_mag = np.sqrt(v_rel_x**2 + v_rel_y**2)

        if v_rel_mag < 0.001:
            v_rel_mag = 0.001

        # Determine the relative air-flow flight angle (phi)
        phi = np.arctan2(v_rel_y, v_rel_x)

        # 1. Compute Drag Force (opposes relative motion vector)
        Fd = 0.5 * rho * (v_rel_mag**2) * Cd * A

        # 2. Compute Magnus Lift Force (perpendicular to relative motion vector)
        # Lift coefficient based on spin parameter with empirical golf ball calibration
        # Higher spin creates more lift but with diminishing returns
        spin_ratio = (omega * radius / v_rel_mag) if v_rel_mag > 0 else 0
        # Empirical model: lift scales with spin but saturates at high spin rates
        Cl = 0.21 + 0.18 * min(spin_ratio * 10, 1.0)  # Range: 0.21 to 0.39
        Fl = 0.5 * rho * (v_rel_mag**2) * Cl * A

        # Resolve fluid force vectors to standard grid coordinates
        Fx_drag = -Fd * np.cos(phi)
        Fy_drag = -Fd * np.sin(phi)
        Fx_lift = -Fl * np.sin(phi)
        Fy_lift = Fl * np.cos(phi)

        # Combine forces and derive current acceleration step
        ax = (Fx_drag + Fx_lift) / m
        ay = -g + (Fy_drag + Fy_lift) / m

        # Update velocities via Euler integration step
        vx += ax * dt
        vy += ay * dt

        # Update ground coordinates
        x += vx * dt
        y += vy * dt

        # Dynamic exponential spin decay over time
        omega *= np.exp(-0.05 * dt)
        t += dt

        # Track peak altitude metrics
        if y > max_height_m:
            max_height_m = y

        # Append parameters if ball is above ground
        if y >= 0.0:
            x_history.append(x)
            y_history.append(y)

    # --- Terminal Landing Calculations & Unit Conversions ---
    carry_distance_yards = x * 1.09361
    apex_height_feet = max_height_m * 3.28084
    landing_angle_deg = np.abs(np.degrees(np.arctan2(vy, vx)))

    # Scale spatial histories to yards for display
    x_history_yards = [val * 1.09361 for val in x_history]
    y_history_yards = [val * 1.09361 for val in y_history]

    return {
        "x_arr": x_history_yards,
        "y_arr": y_history_yards,
        "carry": round(carry_distance_yards, 1),
        "apex": round(apex_height_feet, 1),
        "time": round(t, 2),
        "landing_angle": round(landing_angle_deg, 1)
    }
