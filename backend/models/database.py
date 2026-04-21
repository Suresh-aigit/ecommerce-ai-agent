from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)
    price = Column(Float)
    stock_quantity = Column(Integer, default=0)
    category = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255), unique=True)
    phone = Column(String(50))
    preferences = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
    product_ids = Column(Text)
    total_amount = Column(Float)
    status = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
    agent_type = Column(String(50))
    message = Column(Text)
    response = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

def get_engine():
    database_url = os.getenv("DATABASE_URL", "sqlite:///./ecommerce.db")
    return create_engine(database_url, connect_args={"check_same_thread": False} if "sqlite" in database_url else {})

def init_db():
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    return engine

def get_session():
    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

def get_db():
    session = get_session()
    try:
        yield session
    finally:
        session.close()

# NEW: Save conversation to database
def save_conversation(db_session, customer_id: int, agent_type: str, message: str, response: str):
    conversation = Conversation(
        customer_id=customer_id,
        agent_type=agent_type,
        message=message,
        response=response,
        timestamp=datetime.utcnow()
    )
    db_session.add(conversation)
    db_session.commit()
    return conversation

# NEW: Get conversation history
def get_conversation_history(db_session, customer_id: int, limit: int = 10):
    return db_session.query(Conversation).filter(
        Conversation.customer_id == customer_id
    ).order_by(Conversation.timestamp.desc()).limit(limit).all()
