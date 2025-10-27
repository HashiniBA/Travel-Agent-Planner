
import os
import time
import json
from dotenv import load_dotenv
from langtrace_python_sdk import langtrace, with_langtrace_root_span
from crewai import Crew

from .agents import TravelAgents
from .tasks import TravelTasks

load_dotenv()

# Fix Unicode encoding for Windows console
os.environ['PYTHONIOENCODING'] = 'utf-8'

try:
    langtrace.init(api_key=os.getenv("LANGTRACE_API_KEY"))
except UnicodeEncodeError:
    # Fallback if Unicode issues persist
    pass

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
            verbose=True,
            manager_llm=self.llm,
            memory=True
        )

@with_langtrace_root_span("travel_planning_crew")
def run_crew(source, destination, start_date, end_date, budget):
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
            "langtrace_enabled": True,
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
            "langtrace_enabled": True
        }
        return f"Error: {str(e)}", metrics
