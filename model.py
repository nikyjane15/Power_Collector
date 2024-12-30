from pydantic import BaseModel, Field
from typing import List, Optional
from time import time

case_0 = True
maxtime = 20    #2500 for na hour


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


class Energy(BaseModel):
    zone: str
    value: str


class List_Zones(BaseModel):
    timestamp: int
    powercap: List[Energy]


