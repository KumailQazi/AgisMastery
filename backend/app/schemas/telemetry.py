from pydantic import BaseModel
from typing import Optional
from datetime import date

class TelemetryDashboard(BaseModel):
    course_id: int
    completion_rate: float
    mastery_rate: float
    drop_off_points: list
    cognitive_load_heatmap: list
