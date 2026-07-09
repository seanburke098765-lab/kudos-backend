from datetime import datetime
from uuid import uuid4
from sqlalchemy import create_engine, Column, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

# Using a local SQLite database file for development
DATABASE_URL = "sqlite:///./kudos.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    company = Column(String)
    bio = Column(String)
    linkedin_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    devices = relationship("Device", back_populates="owner")

class Device(Base):
    __tablename__ = "devices"
    hardware_uuid = Column(String, primary_key=True) 
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    registered_at = Column(DateTime, default=datetime.utcnow)
    owner = relationship("User", back_populates="devices")

class Interaction(Base):
    __tablename__ = "interactions"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    host_device_uuid = Column(String, ForeignKey("devices.hardware_uuid"), nullable=False)
    guest_device_uuid = Column(String, ForeignKey("devices.hardware_uuid"), nullable=False)
    interacted_at = Column(DateTime, nullable=False)
    synced_at = Column(DateTime, default=datetime.utcnow)

# Automatically create the database tables if they don't exist yet
Base.metadata.create_all(bind=engine)
