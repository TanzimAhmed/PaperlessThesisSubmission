from django.urls import path
from .consumers import CommentsConsumer

routing_patterns = [
    path('comments/<content_id>/', CommentsConsumer)
]
