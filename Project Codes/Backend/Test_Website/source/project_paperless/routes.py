from django.urls import path
from channels.routing import URLRouter
import creative_content.routes

routing_patterns = [
    path('content/', URLRouter(creative_content.routes.routing_patterns))
]
