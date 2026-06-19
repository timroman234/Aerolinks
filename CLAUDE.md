# AeroLinks: The Physics of the Flight

Interactive golf ball trajectory simulator demonstrating fluid dynamics with an AI Caddy.

## Tech Stack

- **Framework**: Streamlit
- **Physics**: NumPy (Euler integration)
- **Visualization**: Plotly
- **AI**: OpenAI SDK (gpt-4o-mini)
- **Styling**: IBM Carbon Design System with golf green accent palette

## Project Structure

```
aerolinks/
├── app.py              # Main Streamlit entry point
├── physics.py          # Trajectory simulation engine
├── caddy.py            # OpenAI-powered AI Caddy
├── frontend/
│   ├── styles.py       # Carbon Design CSS + color palette
│   └── components.py   # Reusable UI components (chart, metrics)
├── pyproject.toml      # Dependencies (managed with uv)
└── .env                # Environment variables (OPENAI_API_KEY)
```

## Running the App

```bash
uv run streamlit run app.py
```

## Key Physics Parameters

| Club   | Launch Angle | Backspin (RPM) | Smash Factor |
|--------|-------------|----------------|--------------|
| Driver | 12°         | 2,500          | 1.48         |
| 5-Iron | 19°         | 5,000          | 1.38         |
| 7-Iron | 27°         | 7,000          | 1.33         |
| PW     | 42°         | 9,000          | 1.23         |

## Development Guidelines

- **Physics changes**: Test with `physics.calculate_flight()` directly before UI testing
- **Expected Driver carry**: ~250-270 yards at 95 mph club speed, no wind
- **Styling**: Use `frontend.COLORS` dict for consistent theming
- **AI Caddy**: Falls back to rule-based responses when `OPENAI_API_KEY` is not set

## Environment Variables

```
OPENAI_API_KEY=your_key_here
```

## Testing Physics

```python
from physics import calculate_flight
result = calculate_flight("Driver", 95, 0, "Headwind")
print(f"Carry: {result['carry']} yards")
```
