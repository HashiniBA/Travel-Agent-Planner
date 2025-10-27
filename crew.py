
import os
import time
import json
from dotenv import load_dotenv
from crewai import Crew

# Handle langtrace import gracefully
try:
    from langtrace_python_sdk import langtrace, with_langtrace_root_span
    LANGTRACE_AVAILABLE = True
except ImportError:
    LANGTRACE_AVAILABLE = False
    # Create dummy decorator if langtrace is not available
    def with_langtrace_root_span(name):
        def decorator(func):
            return func
        return decorator

try:
    from src.travel_planner_ai.agents import TravelAgents
    from src.travel_planner_ai.tasks import TravelTasks
except ImportError:
    # Fallback for different import paths
    try:
        from travel_planner_ai.agents import TravelAgents
        from travel_planner_ai.tasks import TravelTasks
    except ImportError:
        raise ImportError("Could not import TravelAgents and TravelTasks. Check your project structure.")

load_dotenv()

# Fix Unicode encoding for Windows console
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Initialize langtrace if available
if LANGTRACE_AVAILABLE:
    try:
        langtrace.init(api_key=os.getenv("LANGTRACE_API_KEY"))
    except Exception:
        # Fallback if langtrace initialization fails
        LANGTRACE_AVAILABLE = False

class TravelCrew:
    def __init__(self):
        os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
        self.llm = "gemini/gemini-2.0-flash-exp"
        self.agents = TravelAgents()
        self.tasks = TravelTasks()
        # Memory configuration
        os.makedirs("outputs", exist_ok=True)
    
    def create_crew(self, agents, tasks) -> Crew:
        """Travel planning crew with long-term memory"""
        return Crew(
            agents=agents,
            tasks=tasks,
            verbose=False,
            memory=False
        )

# Apply langtrace decorator only if available
if LANGTRACE_AVAILABLE:
    @with_langtrace_root_span("travel_planning_crew")
    def run_crew(source, destination, start_date, end_date, budget):
        return _run_crew_impl(source, destination, start_date, end_date, budget)
else:
    def run_crew(source, destination, start_date, end_date, budget):
        return _run_crew_impl(source, destination, start_date, end_date, budget)

def _run_crew_impl(source, destination, start_date, end_date, budget):
    start_time = time.time()
    try:
        travel_crew = TravelCrew()

        # Create agents once to ensure they are the same instances
        flight_agent = travel_crew.agents.flight_agent()
        stay_agent = travel_crew.agents.stay_agent()
        activities_agent = travel_crew.agents.activities_agent()

        # Create tasks using the methods from the TravelTasks class
        flight_task = travel_crew.tasks.flight_task(flight_agent, source, destination, start_date, end_date, budget)
        stay_task = travel_crew.tasks.stay_task(stay_agent, source, destination, start_date, end_date, budget)
        activities_task = travel_crew.tasks.activities_task(activities_agent, source, destination, start_date, end_date, budget)

        agents = [flight_agent, stay_agent, activities_agent]
        tasks = [flight_task, stay_task, activities_task]

        crew = travel_crew.create_crew(agents, tasks)
        result = crew.kickoff()
        execution_time = round(time.time() - start_time, 1)
        
        metrics = {
            "execution_time": execution_time,
            "agents_used": [agent.role for agent in crew.agents],
            "tasks_completed": len(crew.tasks),
            "success": True,
            "langtrace_enabled": LANGTRACE_AVAILABLE,
            "usage_metrics": str(crew.usage_metrics) if hasattr(crew, 'usage_metrics') else None
        }
        
        with open("outputs/travel_metrics.json", "w") as f:
            json.dump(metrics, f, indent=2)
        
        return result, metrics
        
    except Exception as e:
        metrics = {
            "execution_time": round(time.time() - start_time, 1),
            "agents_used": [],
            "tasks_completed": 0,
            "success": False,
            "error": str(e),
            "langtrace_enabled": LANGTRACE_AVAILABLE
        }
        return f"Error: {str(e)}", metrics
