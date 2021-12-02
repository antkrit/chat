# flake8: noqa F401
"""This package contains modules with web controllers.

Modules:
- `chat_view.py`: defines chat view
- `create_chat_view.py`: defines view for creating chats
- `index_view.py`: defines index view
"""
from src.views.chat_view import chat
from src.views.create_chat_view import create_chat_get, create_chat_post
from src.views.index_view import index
