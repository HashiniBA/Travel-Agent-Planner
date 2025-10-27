#!/usr/bin/env python
"""
Travel Planner AI - Main Entry Point
"""
import sys
from .crew import run_crew

def main():
    """
    Main function for CrewAI deployment
    """
    # Default values for testing
    source = "New York"
    destination = "Paris" 
    start_date = "2024-06-01"
    end_date = "2024-06-10"
    budget = 2000
    
    # Override with command line arguments if provided
    if len(sys.argv) >= 6:
        source = sys.argv[1]
        destination = sys.argv[2]
        start_date = sys.argv[3]
        end_date = sys.argv[4]
        budget = float(sys.argv[5])
    
    print(f"Planning travel from {source} to {destination}")
    print(f"Dates: {start_date} to {end_date}")
    print(f"Budget: ${budget}")
    
    result, metrics = run_crew(source, destination, start_date, end_date, budget)
    
    print(f"\nExecution completed in {metrics['execution_time']}s")
    print(f"Success: {metrics['success']}")
    
    return result

if __name__ == "__main__":
    main()