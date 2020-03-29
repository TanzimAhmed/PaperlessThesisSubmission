from django.urls import path
from .consumers import DiscussionConsumer

routing_patterns = [
    path('<str:content_id>/show/', DiscussionConsumer)
]
