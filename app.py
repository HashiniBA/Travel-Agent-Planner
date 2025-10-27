import streamlit as st
import os
import sys
from dotenv import load_dotenv
import json

# Add src directory to Python path for local imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from crew import run_crew
except ImportError:
    st.error("Failed to import crew module. Please check your dependencies.")
    st.stop()

load_dotenv()

# Ensure required environment variables are set
if not os.getenv("GOOGLE_API_KEY"):
    st.error("GOOGLE_API_KEY not found. Please set it in your Streamlit secrets or .env file.")
    st.stop()

def display_content(content: str):
    """Display content directly"""
    st.markdown(content)

st.set_page_config(page_title="Travel Planner AI", page_icon="✈️", layout="wide")

st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <h1 style='color: #ff6b6b; font-size: 3em;'>✈️ Travel Planner AI 🌍</h1>
    <p style='font-size: 1.2em; color: #666;'>✨ Plan your perfect trip with AI-powered recommendations! ✨</p>
</div>
""", unsafe_allow_html=True)

# Input form
with st.form("travel_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        source = st.text_input("Source City", placeholder="New York")
        destination = st.text_input("Destination", placeholder="Paris")
        budget = st.number_input("Budget ($)", min_value=100, value=2000)
    
    with col2:
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
    
    submitted = st.form_submit_button("🚀 Generate Travel Plan")

if submitted:
    if all([source, destination, start_date, end_date, budget]):
        with st.spinner("Planning your perfect trip..."):
            try:
                result, metrics = run_crew(
                    source, destination, str(start_date), str(end_date), budget
                )
            except Exception as e:
                st.error(f"Error running crew: {str(e)}")
                st.stop()
        
        st.balloons()
        st.success("✨ Your Amazing Travel Plan is Ready! ✨")
        
        # Flight Section
        st.markdown("---")
        st.markdown("<h2 style='text-align: center; color: #1f77b4;'>✈️ Flight Recommendations</h2>", unsafe_allow_html=True)
        with st.container():
            st.markdown("""
            <div style='background: linear-gradient(90deg, #e3f2fd 0%, #bbdefb 100%); 
                        padding: 20px; border-radius: 15px; margin: 10px 0;'>
            """, unsafe_allow_html=True)
            try:
                with open("outputs/flight_recommendations.md", "r", encoding="utf-8") as f:
                    flight_content = f.read()
                display_content(flight_content)
            except FileNotFoundError:
                st.info("🔍 Flight recommendations are being generated...")
            except UnicodeDecodeError:
                st.warning("⚠️ Flight recommendations contain special characters. Please check the file.")
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Hotel Section  
        st.markdown("---")
        st.markdown("<h2 style='text-align: center; color: #ff6b6b;'>🏨 Hotel Recommendations</h2>", unsafe_allow_html=True)
        with st.container():
            st.markdown("""
            <div style='background: linear-gradient(90deg, #fff3e0 0%, #ffcc80 100%); 
                        padding: 20px; border-radius: 15px; margin: 10px 0;'>
            """, unsafe_allow_html=True)
            try:
                with open("outputs/hotel_recommendations.md", "r", encoding="utf-8") as f:
                    hotel_content = f.read()
                display_content(hotel_content)
            except FileNotFoundError:
                st.info("🏨 Hotel recommendations are being generated...")
            except UnicodeDecodeError:
                st.warning("⚠️ Hotel recommendations contain special characters. Please check the file.")
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Activities Section
        st.markdown("---")
        st.markdown("<h2 style='text-align: center; color: #4caf50;'>🎯 Activities & Experiences</h2>", unsafe_allow_html=True)
        with st.container():
            st.markdown("""
            <div style='background: linear-gradient(90deg, #e8f5e8 0%, #a5d6a7 100%); 
                        padding: 20px; border-radius: 15px; margin: 10px 0;'>
            """, unsafe_allow_html=True)
            try:
                with open("outputs/activities_itinerary.md", "r", encoding="utf-8") as f:
                    activities_content = f.read()
                display_content(activities_content)
            except FileNotFoundError:
                st.info("🎯 Activities recommendations are being generated...")
            except UnicodeDecodeError:
                st.warning("⚠️ Activities recommendations contain special characters. Please check the file.")
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Metrics Section
        st.markdown("---")
        st.markdown("<h2 style='text-align: center; color: #ff9800;'>📊 Planning Metrics</h2>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("⏱️ Execution Time", f"{metrics['execution_time']}s")
        with col2:
            st.metric("🤖 Agents Used", len(metrics['agents_used']))
        with col3:
            st.metric("✅ Tasks Completed", metrics['tasks_completed'])
        with col4:
            st.metric("🎆 Status", "Success" if metrics['success'] else "Failed")
        
        # Summary Section
        st.markdown("---")
        st.markdown("<h2 style='text-align: center; color: #9c27b0;'>📝 Complete Travel Summary</h2>", unsafe_allow_html=True)
        with st.expander("🚀 View Complete Travel Plan", expanded=False):
            st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        color: white; padding: 20px; border-radius: 15px;'>
            """, unsafe_allow_html=True)
            st.write(result)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Langtrace Metrics Info
        with st.expander("📊 View Langtrace Metrics", expanded=False):
            try:
                with open("outputs/travel_metrics.json", "r", encoding="utf-8") as f:
                    st.json(json.load(f))
            except FileNotFoundError:
                st.info("Metrics file not found")
            except UnicodeDecodeError:
                st.warning("⚠️ Metrics file contains special characters. Please check the file.")
    else:
        st.error("Please fill in all fields!")
