#!/usr/bin/env python3
"""Test script for news service"""
from news_service import get_event_news
import json

# Test the news service
print("Testing news service...")
result = get_event_news('Fed decision in December?', 5)
print(json.dumps(result, indent=2))
