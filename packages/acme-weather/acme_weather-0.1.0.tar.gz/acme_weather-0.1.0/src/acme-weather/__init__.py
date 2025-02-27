#!/usr/bin/env python
"""
Experiments with dawn, sunset and weather
"""

from .app import main

# CONSTANTS
TIMEOUT = 2 #seconds
DATE_FORMAT = "%a %b %d"
TIME_FORMAT = "%H:%M"
DATETIME_FORMAT = "%a %b %d %H:%M"
EMOJI = {
    "dawn": "🌄",
    "sunrise": "🌅",
    "noon": "🌞",
    "sunset": "🌇",
    "dusk": "🌃",
}
