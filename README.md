# Travel Planner AI

AI-powered travel planning using CrewAI, Streamlit, and Google Gemini 2.5 Pro.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure API keys in `.env`:
```
GOOGLE_API_KEY=your_gemini_api_key_here
LANGTRACE_API_KEY=your_langtrace_api_key_here
```

3. Run the application:
```bash
streamlit run app.py
```

## Features

- **Flight Agent**: Finds optimal flight options
- **Stay Agent**: Recommends accommodations within budget  
- **Activities Agent**: Suggests local attractions and activities
- **Metrics Tracking**: Monitors tokens, costs, and performance
- **Interactive UI**: Clean Streamlit interface with collapsible sections

## Architecture

- `app.py`: Main Streamlit application
- `crew.py`: CrewAI orchestration and metrics
- `agents.py`: Agent definitions
- `tasks.py`: Task specifications
- `travel_metrics.json`: Generated metrics file