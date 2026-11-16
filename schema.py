from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime

class ChatUser(BaseModel):
    role: str
    message: str
    session_id: str