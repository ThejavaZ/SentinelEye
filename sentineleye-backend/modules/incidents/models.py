from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from core.database import Base

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    camera_id = Column(Integer, ForeignKey("cameras.id", ondelete="CASCADE"), nullable=False)
    violation_type = Column(String(100), nullable=False)  # Ej: "NO_HELMET", "NO_VEST"
    snapshot_path = Column(String(255), nullable=False)
    confidence_score = Column(Float, nullable=False)
    status = Column(String(20), default="pending", nullable=False)  # pending / resolved / dismissed
    
    resolved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    detected_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    camera = relationship("Camera", back_populates="incidents")
    resolver = relationship("User", foreign_keys=[resolved_by])