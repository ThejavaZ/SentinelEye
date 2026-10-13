from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from core.database import Base

class Zone(Base):
    __tablename__ = "zones"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    cameras = relationship("Camera", back_populates="zone", cascade="all, delete-orphan")


class Camera(Base):
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True, index=True)
    zone_id = Column(Integer, ForeignKey("zones.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    rtsp_url = Column(String(255), nullable=False)
    status = Column(String(20), default="offline", nullable=False)  # online / offline / error
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    zone = relationship("Zone", back_populates="cameras")
    incidents = relationship("Incident", back_populates="camera", cascade="all, delete-orphan")