from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey, Date
from app.db.base import Base

class CourseAnalytics(Base):
    __tablename__ = "course_analytics"
    analytics_id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.course_id"), nullable=False)
    date = Column(Date, nullable=False)
    total_learners = Column(Integer, default=0)
    completion_rate = Column(Numeric(5, 2), default=0.0)
    mastery_rate = Column(Numeric(5, 2), default=0.0)
    average_attempts_to_mastery = Column(Numeric(5, 2), default=0.0)
    drop_off_scenario_id = Column(Integer, ForeignKey("scenarios.scenario_id"), nullable=True)
    cognitive_load_score = Column(Numeric(5, 2), default=0.0)
