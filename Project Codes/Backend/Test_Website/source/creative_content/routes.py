from django.urls import path
from .consumers import CommentsConsumer

routing_patterns = [
    path('<str:content_id>/show/', CommentsConsumer)
]
