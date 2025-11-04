"""
Multi-Agent System for Meteo Outfit Advisor

This package contains the multi-agent architecture with:
- Coordinator: Routes requests to specialist agents
- Weather Specialist: Deep weather analysis
- Outfit Specialist: Fashion and style recommendations
- Travel Planner: Trip planning and packing lists
- Activity Specialist: Sports and outdoor gear
"""

from agents.coordinator import coordinator, root_agent
from agents.weather_specialist import weather_specialist
from agents.outfit_specialist import outfit_specialist
from agents.travel_planner import travel_planner
from agents.activity_specialist import activity_specialist

__all__ = [
    'root_agent',
    'coordinator',
    'weather_specialist',
    'outfit_specialist',
    'travel_planner',
    'activity_specialist'
]
