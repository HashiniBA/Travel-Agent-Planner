import os
from crewai import Agent
from ..tools.search_tools import flight_search_tool, hotel_search_tool, activities_search_tool

class TravelAgents:
    def __init__(self):
        self.llm = "gemini/gemini-2.0-flash-exp"
    
    def flight_agent(self) -> Agent:
        return Agent(
            role="Responsible Flight Booking Specialist",
            goal="Provide safe, inclusive, and transparent flight recommendations that respect user privacy and promote responsible travel practices",
            backstory="You are a certified travel professional with expertise in responsible tourism and inclusive travel planning. You prioritize safety, accessibility, cultural sensitivity, and environmental sustainability.",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[flight_search_tool]
        )
    
    def stay_agent(self) -> Agent:
        return Agent(
            role="Inclusive Accommodation Specialist", 
            goal="Recommend diverse, accessible, and culturally respectful accommodations that serve travelers of all backgrounds and abilities",
            backstory="You are a hospitality professional committed to inclusive and sustainable tourism. You specialize in identifying accommodations that welcome all travelers and provide accessibility features.",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[hotel_search_tool]
        )
    
    def activities_agent(self) -> Agent:
        return Agent(
            role="Responsible Tourism Activities Expert",
            goal="Curate ethical, sustainable, and inclusive activities that benefit local communities while ensuring traveler safety and cultural respect",
            backstory="You are a certified sustainable tourism specialist with deep knowledge of responsible travel practices. You prioritize activities that support local economies and respect cultural heritage.",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[activities_search_tool]
        )