from crewai.tools import tool

@tool
def flight_search_tool(source: str, destination: str, start_date: str, end_date: str, budget: float) -> str:
    """Search for flight options between source and destination within budget."""
    return f"Search completed for flights from {source} to {destination} on {start_date} returning {end_date} with budget ${budget}. Use your expertise to provide realistic flight recommendations with airlines, prices, times, and booking advice."

@tool
def hotel_search_tool(destination: str, start_date: str, end_date: str, budget: float) -> str:
    """Search for hotel accommodations in destination within budget."""
    return f"Search completed for accommodations in {destination} from {start_date} to {end_date} with budget ${budget}. Use your expertise to recommend hotels with realistic pricing, amenities, ratings, and locations."

@tool  
def activities_search_tool(destination: str, start_date: str, end_date: str, budget: float) -> str:
    """Search for activities and attractions in destination within budget."""
    return f"Search completed for activities in {destination} from {start_date} to {end_date} with budget ${budget}. Use your expertise to create a detailed itinerary with attractions, experiences, dining, and realistic costs."