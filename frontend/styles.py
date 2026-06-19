# frontend/styles.py
"""
AeroLinks Custom Styling
IBM Carbon Design System with Golf Green accent palette.
"""

# Golf Green Color Palette
COLORS = {
    "primary": "#3a5a40",           # Desaturated golf green
    "primary_hover": "#2f4834",     # Darker green for hover states
    "background": "#f8f9fa",        # Ultra-light gray
    "surface": "#ffffff",           # White surfaces
    "text": "#212529",              # Charcoal text
    "text_secondary": "#6c757d",    # Secondary text
    "border": "#e9ecef",            # Light borders
    "grid": "#f1f3f5",              # Grid lines
}


def get_carbon_css() -> str:
    """Returns custom CSS for IBM Carbon Design with golf green theme."""
    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

    /* Global Typography & Background */
    html, body, [class*="css"] {{
        font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: {COLORS["background"]};
        color: {COLORS["text"]};
    }}

    .stApp {{
        background-color: {COLORS["background"]};
    }}

    /* Carbon Design Metric Cards */
    div[data-testid="stMetricBlock"] {{
        background-color: {COLORS["surface"]} !important;
        border: 1px solid {COLORS["border"]} !important;
        padding: 16px 20px !important;
        border-radius: 0 !important;
        box-shadow: none !important;
    }}

    div[data-testid="stMetricValue"] {{
        color: {COLORS["text"]} !important;
        font-weight: 600 !important;
        font-size: 2rem !important;
        letter-spacing: -0.5px !important;
    }}

    div[data-testid="stMetricLabel"] {{
        color: {COLORS["text_secondary"]} !important;
        text-transform: uppercase !important;
        letter-spacing: 0.32px !important;
        font-size: 0.75rem !important;
        font-weight: 400 !important;
    }}

    /* Carbon Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: {COLORS["surface"]} !important;
        border-right: 1px solid {COLORS["border"]} !important;
    }}

    section[data-testid="stSidebar"] .stMarkdown h4 {{
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        letter-spacing: 0.16px !important;
        margin-bottom: 16px !important;
    }}

    /* Carbon Primary Button */
    .stButton > button {{
        background-color: {COLORS["primary"]} !important;
        color: {COLORS["surface"]} !important;
        border: none !important;
        border-radius: 0 !important;
        padding: 14px 16px !important;
        font-weight: 400 !important;
        font-size: 0.875rem !important;
        letter-spacing: 0.16px !important;
        width: 100% !important;
        transition: background-color 0.11s cubic-bezier(0.2, 0, 0.38, 0.9) !important;
        min-height: 48px !important;
    }}

    .stButton > button:hover {{
        background-color: {COLORS["primary_hover"]} !important;
    }}

    .stButton > button:active {{
        background-color: #1a3320 !important;
    }}

    /* Carbon Select/Dropdown */
    .stSelectbox > div > div {{
        border-radius: 0 !important;
        border-color: {COLORS["border"]} !important;
    }}

    /* Carbon Slider */
    .stSlider > div > div > div {{
        background-color: {COLORS["primary"]} !important;
    }}

    /* Carbon Radio Buttons */
    .stRadio > div {{
        gap: 16px !important;
    }}

    /* Carbon Expander */
    .streamlit-expanderHeader {{
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        background-color: {COLORS["surface"]} !important;
        border: 1px solid {COLORS["border"]} !important;
        border-radius: 0 !important;
    }}

    /* Carbon Chat Message */
    .stChatMessage {{
        background-color: {COLORS["surface"]} !important;
        border: 1px solid {COLORS["border"]} !important;
        border-radius: 0 !important;
        padding: 16px !important;
    }}

    /* Remove default Streamlit branding elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    /* Custom scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}

    ::-webkit-scrollbar-track {{
        background: {COLORS["background"]};
    }}

    ::-webkit-scrollbar-thumb {{
        background: {COLORS["border"]};
        border-radius: 0;
    }}

    ::-webkit-scrollbar-thumb:hover {{
        background: {COLORS["text_secondary"]};
    }}
    </style>
    """


def get_header_html(title: str, subtitle: str) -> str:
    """Returns styled header HTML."""
    return f"""
    <div style="margin-bottom: 24px;">
        <h1 style="
            font-weight: 300;
            font-size: 2.25rem;
            letter-spacing: -0.5px;
            margin: 0;
            color: {COLORS["text"]};
        ">
            {title}
            <span style="
                color: {COLORS["text_secondary"]};
                font-size: 1rem;
                font-weight: 400;
                margin-left: 8px;
            ">// {subtitle}</span>
        </h1>
    </div>
    """


def get_section_header_html(title: str) -> str:
    """Returns styled section header HTML."""
    return f"""
    <h3 style="
        font-weight: 600;
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 0.32px;
        color: {COLORS["text_secondary"]};
        margin: 24px 0 16px 0;
    ">{title}</h3>
    """
