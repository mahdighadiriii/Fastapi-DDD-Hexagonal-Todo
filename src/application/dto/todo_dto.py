from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class TodoDTO:
    id: str
    title: str
    description: Optional[str]
    status: str
    priority: int
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]
    due_date: Optional[datetime]
    tags: List[str]
    is_overdue: bool
