import os
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker

os.makedirs("workspace", exist_ok=True)
DATABASE_URL = "sqlite:///./workspace/app.db"

# Create a robust SQLite engine
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class OAuthToken(Base):
    __tablename__ = "oauth_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, unique=True, index=True) # e.g., 'youtube', 'tiktok', 'instagram'
    access_token = Column(Text, nullable=True)
    refresh_token = Column(Text, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)
    topic = Column(String, nullable=False)
    job_type = Column(String, default="pipeline") # pipeline, clipper, director, explainer, studio
    status = Column(String, default="queued", index=True) # queued, running, awaiting_approval, completed, failed, cancelled, interrupted
    progress = Column(Integer, default=0) # stored as percentage 0-100 or float representation
    step = Column(String, default="Queued")
    result = Column(Text, nullable=True)
    error = Column(Text, nullable=True)
    params_json = Column(Text, nullable=True)
    checkpoints_json = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    created_at = Column(DateTime, default=func.now(), index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class JobLog(Base):
    __tablename__ = "job_logs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, index=True, nullable=False)
    timestamp = Column(DateTime, default=func.now())
    level = Column(String, default="INFO")
    message = Column(Text, nullable=False)

class JobStage(Base):
    __tablename__ = "job_stages"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, index=True, nullable=False)
    stage_name = Column(String, nullable=False)
    status = Column(String, default="pending") # pending, running, completed, failed, skipped
    stage_data_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class EditingStyleProfile(Base):
    __tablename__ = "editing_styles"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    target_duration = Column(Integer, default=45)
    config_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class MemoryRecord(Base):
    __tablename__ = "memory_records"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True, nullable=False) # user_preference, channel_memory, creative_memory, performance_memory
    key = Column(String, index=True, nullable=False)
    value_json = Column(Text, nullable=False)
    confidence = Column(Integer, default=100)
    source_ref = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class AnalyticsSnapshot(Base):
    __tablename__ = "analytics_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, index=True, nullable=False)
    video_id = Column(String, index=True, nullable=False)
    title = Column(String, nullable=True)
    metrics_json = Column(Text, nullable=False) # views, likes, ctr, avg_retention, comments
    recorded_at = Column(DateTime, default=func.now(), index=True)

class ContentCampaign(Base):
    __tablename__ = "content_campaigns"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    niche = Column(String, nullable=False)
    target_region = Column(String, default="Global")
    frequency = Column(String, default="Weekly")
    status = Column(String, default="active") # active, paused, completed
    strategy_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

# Create all tables cleanly
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
