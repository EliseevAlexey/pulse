from dataclasses import dataclass
from enum import Enum
from typing import Optional


class TaskStatus(Enum):
    POSTPONED = "#f5f5f5"
    BLOCKED = "#f8cecc"
    ESTIMATED = "#dae8fc"
    IN_PROGRESS = "#fff2cc"
    DONE = "#d5e8d4"


@dataclass
class ElementData:
    id: str
    epic_name: str
    value: str
    text: str
    is_group_marker: bool
    task_status: TaskStatus
    style: str
    parent: str
    x: float
    y: float
    width: float
    height: float
    link: Optional[str]
    mx_cell: Optional['ElementData']
    group_id: Optional[str]
    group_name: Optional[str]
