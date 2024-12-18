from pydantic import BaseModel, Field
from typing import List, Optional
from time import time

tstep = 2
maxtime = 2500


class State(BaseModel):
    state: str
    value: str


class Time(BaseModel):
    cpu: Optional[str] = Field(default=None)
    state: List[State]


class CPU_Time(BaseModel):
    timestamp: int
    block: List[Time]


class CPU_result(BaseModel):
    result: List[CPU_Time]
