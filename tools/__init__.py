"""
Tools package for Meteo Outfit Advisor Agent

This package contains weather API tools and outfit recommendation logic.
"""

from tools.weather_api import (
    get_current_weather,
    get_forecast,
    get_weather_summary
)

from tools.outfit_advisor import (
    recommend_outfit,
    format_outfit_recommendation
)

__all__ = [
    'get_current_weather',
    'get_forecast',
    'get_weather_summary',
    'recommend_outfit',
    'format_outfit_recommendation'
]
