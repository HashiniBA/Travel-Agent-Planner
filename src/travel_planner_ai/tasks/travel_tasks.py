from crewai import Task
from ..guardrails.content_validator import validate_blog_content

class TravelTasks:
    def flight_task(self, agent, source, destination, start_date, end_date, budget) -> Task:
        description = f"""As a Responsible AI travel assistant, provide inclusive flight recommendations from {source} to {destination} for {start_date} to {end_date} within ${budget}. 
        REQUIREMENTS: 1) Include options for different budgets and accessibility needs 2) Provide transparent pricing with disclaimers 3) Mention safety and travel advisories 4) Avoid bias toward specific airlines 5) Include sustainable travel options when available 6) Respect cultural sensitivities 7) Protect user privacy - do not include personal contact information 8) Add appropriate AI-generated content disclaimers."""
        
        return Task(
            description=description,
            expected_output="Inclusive flight recommendations with: diverse airline options across price ranges, accessibility features, transparent pricing with disclaimers, safety information, sustainable options, cultural considerations, privacy protection, and responsible AI disclaimers.",
            agent=agent,
            output_file="outputs/flight_recommendations.md",
            guardrail=validate_blog_content
        )
    
    def stay_task(self, agent, source, destination, start_date, end_date, budget) -> Task:
        description = f"""As a Responsible AI assistant, recommend inclusive accommodations in {destination} for {start_date} to {end_date} within ${budget}. 
        REQUIREMENTS: 1) Provide diverse options for all budgets and accessibility needs 2) Include family-friendly, solo traveler, and group options 3) Highlight accessibility features and inclusive amenities 4) Ensure transparent pricing with disclaimers 5) Respect local communities and promote sustainable tourism 6) Avoid discrimination based on traveler background 7) Protect privacy - no personal contact details 8) Include responsible AI disclaimers."""
        
        return Task(
            description=description,
            expected_output="Comprehensive accommodation guide with: diverse lodging options, accessibility information, inclusive amenities, transparent pricing, community-respectful choices, sustainability features, privacy protection, and responsible AI disclaimers.",
            agent=agent,
            output_file="outputs/hotel_recommendations.md",
            guardrail=validate_blog_content
        )
    
    def activities_task(self, agent, source, destination, start_date, end_date, budget) -> Task:
        description = f"""As a Responsible AI tourism expert, create an ethical activity itinerary for {destination} from {start_date} to {end_date} within ${budget}. 
        REQUIREMENTS: 1) Promote activities that benefit local communities 2) Include accessible options for travelers with disabilities 3) Respect cultural heritage and local customs 4) Prioritize sustainable and eco-friendly experiences 5) Provide diverse options for different interests and budgets 6) Include safety information and cultural etiquette 7) Avoid activities that exploit people, animals, or environment 8) Protect privacy and include responsible AI disclaimers."""
        
        return Task(
            description=description,
            expected_output="Ethical activity itinerary featuring: community-benefiting experiences, accessible attractions, cultural respect guidelines, sustainable tourism options, diverse interest categories, safety protocols, environmental considerations, and responsible AI disclaimers.",
            agent=agent,
            output_file="outputs/activities_itinerary.md",
            guardrail=validate_blog_content
        )