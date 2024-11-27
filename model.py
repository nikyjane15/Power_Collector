from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class State(BaseModel):
    state: str
    value: str

class Time(BaseModel):
    cpu: Optional[str] = Field(default=None)
    state: List[State]

class CPU_Time(BaseModel):
    timestamp: datetime
    block: List[Time]