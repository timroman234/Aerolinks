# frontend/components.py
"""
AeroLinks Reusable UI Components
Carbon Design System styled components for Streamlit.
"""
import streamlit as st
import plotly.graph_objects as go
from .styles import COLORS


def create_animated_trajectory_chart(x_data: list, y_data: list, num_frames: int = 50) -> go.Figure:
    """
    Creates an animated Plotly trajectory chart that draws the line progressively.
    Animation runs client-side for smooth rendering without flickering.

    Args:
        x_data: X-axis data (distance in yards)
        y_data: Y-axis data (height in yards)
        num_frames: Number of animation frames

    Returns:
        Configured Plotly Figure with animation
    """
    # Calculate axis ranges upfront (fixed during animation)
    max_x = max(320, max(x_data) * 1.1) if x_data and max(x_data) > 0 else 320
    max_y = max(60, max(y_data) * 1.2) if y_data and max(y_data) > 0 else 60

    total_points = len(x_data)

    # Create animation frames
    frames = []
    for i in range(1, num_frames + 1):
        # Calculate how many points to show in this frame
        points_to_show = max(2, int((i / num_frames) * total_points))

        frame = go.Frame(
            data=[go.Scatter(
                x=x_data[:points_to_show],
                y=y_data[:points_to_show],
                mode='lines',
                line=dict(color=COLORS["primary"], width=3),
                hovertemplate='Distance: %{x:.1f} yds<br>Height: %{y:.1f} yds<extra></extra>'
            )],
            name=str(i)
        )
        frames.append(frame)

    # Create figure with initial empty state
    fig = go.Figure(
        data=[go.Scatter(
            x=[x_data[0]],
            y=[y_data[0]],
            mode='lines',
            line=dict(color=COLORS["primary"], width=3),
            hovertemplate='Distance: %{x:.1f} yds<br>Height: %{y:.1f} yds<extra></extra>'
        )],
        frames=frames
    )

    # Add ball marker at the end of the line (animated)
    ball_frames = []
    for i in range(1, num_frames + 1):
        points_to_show = max(2, int((i / num_frames) * total_points))
        ball_x = x_data[points_to_show - 1]
        ball_y = y_data[points_to_show - 1]

        ball_frame = go.Frame(
            data=[
                go.Scatter(
                    x=x_data[:points_to_show],
                    y=y_data[:points_to_show],
                    mode='lines',
                    line=dict(color=COLORS["primary"], width=3),
                    hovertemplate='Distance: %{x:.1f} yds<br>Height: %{y:.1f} yds<extra></extra>'
                ),
                go.Scatter(
                    x=[ball_x],
                    y=[ball_y],
                    mode='markers',
                    marker=dict(color='white', size=12, line=dict(color=COLORS["primary"], width=2)),
                    hoverinfo='skip'
                )
            ],
            name=str(i)
        )
        ball_frames.append(ball_frame)

    fig.frames = ball_frames

    # Add ball marker trace (initial position)
    fig.add_trace(go.Scatter(
        x=[x_data[0]],
        y=[y_data[0]],
        mode='markers',
        marker=dict(color='white', size=12, line=dict(color=COLORS["primary"], width=2)),
        hoverinfo='skip'
    ))

    # Animation settings - auto-play immediately
    fig.update_layout(
        plot_bgcolor=COLORS["surface"],
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=48, r=24, t=16, b=48),
        height=420,
        font=dict(
            family="IBM Plex Sans, -apple-system, sans-serif",
            size=12,
            color=COLORS["text_secondary"]
        ),
        xaxis=dict(
            title=dict(
                text="Downrange Carry Distance (Yards)",
                font=dict(size=12, color=COLORS["text_secondary"]),
                standoff=16
            ),
            gridcolor=COLORS["grid"],
            showline=True,
            linewidth=1,
            linecolor=COLORS["border"],
            zeroline=False,
            range=[0, max_x],
            tickfont=dict(size=11)
        ),
        yaxis=dict(
            title=dict(
                text="Altitude (Yards)",
                font=dict(size=12, color=COLORS["text_secondary"]),
                standoff=16
            ),
            gridcolor=COLORS["grid"],
            showline=True,
            linewidth=1,
            linecolor=COLORS["border"],
            zeroline=False,
            range=[0, max_y],
            tickfont=dict(size=11)
        ),
        showlegend=False,
        hovermode='closest',
        # Auto-play animation on load
        updatemenus=[{
            'type': 'buttons',
            'showactive': False,
            'visible': False,  # Hide buttons, animation auto-plays
            'buttons': [{'label': 'Play', 'method': 'animate', 'args': [None, {
                'frame': {'duration': 40, 'redraw': True},
                'fromcurrent': True,
                'mode': 'immediate',
                'transition': {'duration': 0}
            }]}]
        }]
    )

    return fig


def render_animated_chart(fig: go.Figure, key: str):
    """
    Renders an animated Plotly chart with auto-play.
    Uses JavaScript injection to trigger animation on load.
    """
    import streamlit.components.v1 as components

    # Convert figure to HTML
    fig_html = fig.to_html(
        include_plotlyjs='cdn',
        full_html=False,
        animation_opts={'frame': {'duration': 40, 'redraw': True}, 'transition': {'duration': 0}}
    )

    # Wrap with auto-play JavaScript
    html_with_autoplay = f"""
    <div id="plotly-chart-{key}">
        {fig_html}
    </div>
    <script>
        (function() {{
            // Wait for Plotly to be ready
            function tryAnimate() {{
                var plotDiv = document.querySelector('#plotly-chart-{key} .plotly-graph-div');
                if (plotDiv && window.Plotly) {{
                    Plotly.animate(plotDiv, null, {{
                        frame: {{duration: 40, redraw: true}},
                        transition: {{duration: 0}},
                        mode: 'immediate',
                        fromcurrent: false
                    }});
                }} else {{
                    setTimeout(tryAnimate, 100);
                }}
            }}
            setTimeout(tryAnimate, 200);
        }})();
    </script>
    """

    components.html(html_with_autoplay, height=450, scrolling=False)


def create_trajectory_chart(x_data: list, y_data: list) -> go.Figure:
    """
    Creates a Plotly trajectory chart with Carbon Design styling.

    Args:
        x_data: X-axis data (distance in yards)
        y_data: Y-axis data (height in yards)

    Returns:
        Configured Plotly Figure
    """
    fig = go.Figure()

    # Ball trajectory trace
    fig.add_trace(go.Scatter(
        x=x_data,
        y=y_data,
        mode='lines',
        line=dict(color=COLORS["primary"], width=3),
        name='Ball Flight Path',
        hovertemplate='Distance: %{x:.1f} yds<br>Height: %{y:.1f} yds<extra></extra>'
    ))

    # Calculate dynamic axis ranges
    max_x = max(320, max(x_data) * 1.1) if x_data else 320
    max_y = max(60, max(y_data) * 1.2) if y_data else 60

    # Carbon Design layout configuration
    fig.update_layout(
        plot_bgcolor=COLORS["surface"],
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=48, r=24, t=16, b=48),
        height=420,
        font=dict(
            family="IBM Plex Sans, -apple-system, sans-serif",
            size=12,
            color=COLORS["text_secondary"]
        ),
        xaxis=dict(
            title=dict(
                text="Downrange Carry Distance (Yards)",
                font=dict(size=12, color=COLORS["text_secondary"]),
                standoff=16
            ),
            gridcolor=COLORS["grid"],
            showline=True,
            linewidth=1,
            linecolor=COLORS["border"],
            zeroline=False,
            range=[0, max_x],
            tickfont=dict(size=11)
        ),
        yaxis=dict(
            title=dict(
                text="Altitude (Yards)",
                font=dict(size=12, color=COLORS["text_secondary"]),
                standoff=16
            ),
            gridcolor=COLORS["grid"],
            showline=True,
            linewidth=1,
            linecolor=COLORS["border"],
            zeroline=False,
            range=[0, max_y],
            tickfont=dict(size=11)
        ),
        showlegend=False,
        hovermode='closest'
    )

    return fig


def render_metrics_row(carry: float, apex: float, time: float, landing_angle: float):
    """
    Renders a row of telemetry metric cards.

    Args:
        carry: Carry distance in yards
        apex: Maximum height in feet
        time: Flight time in seconds
        landing_angle: Landing angle in degrees
    """
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Carry", f"{carry} yds")
    c2.metric("Apex Height", f"{apex} ft")
    c3.metric("Flight Time", f"{time} sec")
    c4.metric("Landing Angle", f"{landing_angle}°")


def render_physics_explainer():
    """Renders the physics equations expander with LaTeX formulas."""
    with st.expander("View the Physics Behind the Flight"):
        st.markdown("""
### Aerodynamic Equations of Motion

The simulation resolves forces at each timestep ($\\Delta t = 0.005$ s) using explicit Euler integration:

$$\\frac{dv_x}{dt} = \\frac{-F_d \\cdot \\cos(\\phi) - F_l \\cdot \\sin(\\phi)}{m}$$

$$\\frac{dv_y}{dt} = -g + \\frac{-F_d \\cdot \\sin(\\phi) + F_l \\cdot \\cos(\\phi)}{m}$$

Where $\\phi = \\arctan\\left(\\frac{v_y}{v_x - v_w}\\right)$ is the instantaneous flight path angle.

---

#### Drag Force ($F_d$)

Opposes the ball's velocity relative to the air:

$$F_d = \\frac{1}{2} \\rho ||v_{rel}||^2 C_d A$$

- $\\rho = 1.225$ kg/m³ (air density at sea level)
- $C_d = 0.24$ (drag coefficient)
- $A = \\pi r^2$ (cross-sectional area)

---

#### Magnus Lift Force ($F_l$)

The Magnus effect creates lift perpendicular to the velocity vector due to backspin:

$$F_l = \\frac{1}{2} \\rho ||v_{rel}||^2 C_l A$$

The lift coefficient scales with spin:

$$C_l \\approx 0.2 \\times \\frac{\\omega \\cdot r}{||v_{rel}||}$$

Where $\\omega$ is angular velocity (rad/s) and $r = 0.02135$ m is the ball radius.

---

#### Spin Decay

Backspin decays exponentially during flight:

$$\\omega_{t} = \\omega_{t-1} \\cdot e^{-0.05 \\cdot \\Delta t}$$

This models how air resistance gradually reduces ball rotation.
        """)
