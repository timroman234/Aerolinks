# app.py
"""
AeroLinks: The Physics of the Flight
Interactive golf ball trajectory simulator with AI Caddy feedback.
"""
import streamlit as st
from dotenv import load_dotenv

from physics import calculate_flight
from caddy import get_caddy_feedback
from frontend.styles import get_carbon_css, get_header_html, get_section_header_html
from frontend.components import (
    create_trajectory_chart,
    create_animated_trajectory_chart,
    render_animated_chart,
    render_metrics_row,
    render_physics_explainer,
)

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AeroLinks // Flight Tracking",
    page_icon="⛳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Carbon Design styling
st.markdown(get_carbon_css(), unsafe_allow_html=True)

# Header
st.markdown(get_header_html("AeroLinks", "Project SpinRate"), unsafe_allow_html=True)

# --- Initialize Session State ---
if "sim_results" not in st.session_state:
    st.session_state.sim_results = None
if "swing_count" not in st.session_state:
    st.session_state.swing_count = 0

# --- Sidebar Controls ---
with st.sidebar:
    st.markdown(
        "<h4 style='font-weight:600; margin-bottom:16px; color:#212529;'>Telemetry Controls</h4>",
        unsafe_allow_html=True
    )

    club_type = st.selectbox(
        "Club Selection",
        options=["Driver", "5-Iron", "7-Iron", "PW"],
        index=0,
        help="Select club type - affects launch angle, spin rate, and smash factor"
    )

    club_speed = st.slider(
        "Club Head Speed (mph)",
        min_value=60,
        max_value=120,
        value=95,
        step=1,
        help="Swing speed affects initial ball velocity"
    )

    wind_speed = st.slider(
        "Wind Speed (mph)",
        min_value=0,
        max_value=40,
        value=10,
        step=1,
        help="Wind magnitude affects drag and carry distance"
    )

    wind_direction = st.radio(
        "Wind Direction",
        options=["Headwind", "Tailwind"],
        horizontal=True,
        help="Headwind reduces carry, tailwind extends it"
    )

    st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)

    swing_button = st.button("Swing", type="primary", use_container_width=True)

# --- Handle Swing Button Press ---
just_swung = False
if swing_button:
    # Calculate trajectory
    st.session_state.sim_results = calculate_flight(club_type, club_speed, wind_speed, wind_direction)
    st.session_state.swing_count += 1
    just_swung = True

# --- Main Content Area ---
if st.session_state.sim_results is not None:
    results = st.session_state.sim_results

    # Show animated chart only when Swing was just pressed
    if just_swung:
        fig = create_animated_trajectory_chart(results["x_arr"], results["y_arr"], num_frames=50)
        render_animated_chart(fig, key=f"anim_{st.session_state.swing_count}")
    else:
        # Static chart for subsequent renders
        fig = create_trajectory_chart(results["x_arr"], results["y_arr"])
        st.plotly_chart(fig, use_container_width=True, key=f"trajectory_{st.session_state.swing_count}")

    # Telemetry metrics
    render_metrics_row(
        results["carry"],
        results["apex"],
        results["time"],
        results["landing_angle"]
    )

    # AI Caddy section
    st.markdown(get_section_header_html("AI Caddy Assessment"), unsafe_allow_html=True)

    feedback_text = get_caddy_feedback(
        club_type,
        club_speed,
        wind_speed,
        wind_direction,
        results["carry"],
        results["apex"],
        results["landing_angle"]
    )

    with st.chat_message("assistant", avatar="⛳"):
        st.markdown(
            f"<p style='color:#343a40; font-size:1rem; line-height:1.6; margin:0;'>{feedback_text}</p>",
            unsafe_allow_html=True
        )
else:
    # Initial state - show empty chart placeholder
    fig = create_trajectory_chart([0], [0])
    st.plotly_chart(fig, use_container_width=True, key="trajectory_empty")

    st.markdown(
        "<p style='color:#6c757d; text-align:center; padding:20px;'>Adjust parameters and press <strong>Swing</strong> to simulate ball flight</p>",
        unsafe_allow_html=True
    )

# Physics explainer (always visible)
st.markdown("<div style='margin-top:32px;'></div>", unsafe_allow_html=True)
render_physics_explainer()
