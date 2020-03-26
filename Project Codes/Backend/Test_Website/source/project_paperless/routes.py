from django.urls import path
from channels.routing import URLRouter
import creative_content.routes

routing_patterns = [
    path('', URLRouter(creative_content.routes.routing_patterns))
]
