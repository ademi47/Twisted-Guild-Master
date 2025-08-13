import os
from sqlalchemy import create_engine, Column, Integer, String, BigInteger, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Database setup
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

# Configure SSL for PostgreSQL connection
engine_config = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Add SSL configuration for PostgreSQL
if DATABASE_URL.startswith('postgresql://'):
    engine_config["connect_args"] = {"sslmode": "require"}

engine = create_engine(DATABASE_URL, **engine_config)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Guild(Base):
    """Guild/Server model"""
    __tablename__ = "guilds"
    
    id = Column(BigInteger, primary_key=True)  # Discord guild ID
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    contributions = relationship("Contribution", back_populates="guild")

class Member(Base):
    """Guild member model"""
    __tablename__ = "members"
    
    id = Column(BigInteger, primary_key=True)  # Discord user ID
    username = Column(String, nullable=False)
    display_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    contributions = relationship("Contribution", back_populates="member")

class Material(Base):
    """Material types model"""
    __tablename__ = "materials"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    display_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    contributions = relationship("Contribution", back_populates="material")

class Contribution(Base):
    """Member contributions model"""
    __tablename__ = "contributions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    guild_id = Column(BigInteger, ForeignKey("guilds.id"), nullable=False)
    member_id = Column(BigInteger, ForeignKey("members.id"), nullable=False)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    guild = relationship("Guild", back_populates="contributions")
    member = relationship("Member", back_populates="contributions")
    material = relationship("Material", back_populates="contributions")

class AIUsage(Base):
    """AI usage tracking for cost control"""
    __tablename__ = "ai_usage"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    guild_id = Column(BigInteger, nullable=False)  # Discord guild ID
    user_id = Column(BigInteger, nullable=False)   # Discord user ID
    prompt_chars = Column(Integer, nullable=False)  # Input character count
    output_tokens = Column(Integer, nullable=False) # Output token count
    model_used = Column(String, nullable=False)     # OpenAI model used
    created_at = Column(DateTime, default=datetime.utcnow)
    date_only = Column(String, nullable=False)      # YYYY-MM-DD for daily tracking

# Create all tables
def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

def get_db_session():
    """Get database session"""
    session = SessionLocal()
    try:
        return session
    except Exception:
        session.close()
        raise

# Initialize default materials
def init_default_materials():
    """Initialize default materials in the database"""
    session = get_db_session()
    try:
        # Check if materials already exist
        if session.query(Material).count() > 0:
            return
            
        # Default materials - you can modify these
        default_materials = [
            {"name": "ironOre", "display_name": "Iron Ore"},
            {"name": "goldOre", "display_name": "Gold Ore"},
            {"name": "wood", "display_name": "Wood"},
            {"name": "stone", "display_name": "Stone"},
            {"name": "coal", "display_name": "Coal"},
            {"name": "diamond", "display_name": "Diamond"},
            {"name": "food", "display_name": "Food"},
            {"name": "fabric", "display_name": "Fabric"},
            {"name": "leather", "display_name": "Leather"},
            {"name": "crystals", "display_name": "Crystals"}
        ]
        
        for material_data in default_materials:
            material = Material(**material_data)
            session.add(material)
            
        session.commit()
        print("Default materials initialized successfully")
        
    except Exception as e:
        session.rollback()
        print(f"Error initializing default materials: {e}")
    finally:
        session.close()