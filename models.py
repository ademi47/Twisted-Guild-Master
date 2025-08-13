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
    value = Column(Integer, nullable=False, default=100)  # Points per unit (stored as int, divide by 100 for decimals)
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
    amount = Column(BigInteger, nullable=False)
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
    user_id = Column(BigInteger, nullable=False)  # Discord user ID
    prompt_chars = Column(Integer, nullable=False)  # Input character count
    output_tokens = Column(Integer, nullable=False)  # Output token count
    model_used = Column(String, nullable=False)  # OpenAI model used
    created_at = Column(DateTime, default=datetime.utcnow)
    date_only = Column(String, nullable=False)  # YYYY-MM-DD for daily tracking


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

        # Default materials with values in integer format (multiply by 100)
        default_materials = [{
            "name": "ironOre",
            "display_name": "Iron Ore",
            "value": 10  # 0.1 * 100
        }, {
            "name": "ironIngot",
            "display_name": "Iron Ingot",
            "value": 40  # 0.4 * 100
        }, {
            "name": "carbonOre",
            "display_name": "Carbon Ore",
            "value": 10  # 0.1 * 100
        }, {
            "name": "steelIngot",
            "display_name": "Steel Ingot",
            "value": 40  # 0.4 * 100
        }, {
            "name": "aluminiumOre",
            "display_name": "Aluminium Ore",
            "value": 10  # 0.1 * 100
        }, {
            "name": "aluminiumIngot",
            "display_name": "Aluminium Ingot",
            "value": 40  # 0.4 * 100
        }, {
            "name": "copperOre",
            "display_name": "Copper Ore",
            "value": 10  # 0.1 * 100
        }, {
            "name": "copperIngot",
            "display_name": "Copper Ingot",
            "value": 40  # 0.4 * 100
        }, {
            "name": "jasmiumCrystal",
            "display_name": "Jasmium Crystal",
            "value": 200  # 2 * 100
        }, {
            "name": "duraluminumIngot",
            "display_name": "Duraluminum Ingot",
            "value": 350  # 3.5 * 100
        }, {
            "name": "etheriteCrystal",
            "display_name": "Etherite Crystal",
            "value": 230  # 2.3 * 100
        }, {
            "name": "basaltStone",
            "display_name": "Basalt Stone",
            "value": 5  # 0.05 * 100
        }, {
            "name": "plastone",
            "display_name": "Plastone",
            "value": 5  # 0.05 * 100
        }, {
            "name": "siliconBlock",
            "display_name": "Silicon Block",
            "value": 10  # 0.1 * 100
        }, {
            "name": "titaniumOre",
            "display_name": "Titanium Ore",
            "value": 250  # 2.5 * 100
        }, {
            "name": "plastaniumIngot",
            "display_name": "Plastanium Ingot",
            "value": 1000  # 10 * 100
        }, {
            "name": "stravidiumMass",
            "display_name": "Stravidium Mass",
            "value": 250  # 2.5 * 100
        }, {
            "name": "stravidiumFibre",
            "display_name": "Stravidium Fibre",
            "value": 700  # 7 * 100
        }, {
            "name": "spiceSand",
            "display_name": "Spice Sand",
            "value": 50  # 0.5 * 100
        }, {
            "name": "spiceMelange",
            "display_name": "Spice Melange",
            "value": 2500  # 25 * 100
        }, {
            "name": "deadBody",
            "display_name": "Dead Body",
            "value": 200  # 2 * 100
        }, {
            "name": "agaveSeeds",
            "display_name": "Agave Seeds",
            "value": 5  # 0.05 * 100
        }, {
            "name": "cobaltPaste",
            "display_name": "Cobalt Paste",
            "value": 100  # 1 * 100
        }, {
            "name": "flourSand",
            "display_name": "Flour Sand",
            "value": 5  # 0.05 * 100
        }, {
            "name": "fuelCell",
            "display_name": "Fuel Cell",
            "value": 150  # 1.5 * 100
        }, {
            "name": "graniteStone",
            "display_name": "Granite Stone",
            "value": 5  # 0.05 * 100
        }, {
            "name": "vehicleFuelCell",
            "display_name": "Vehicle Fuel Cell",
            "value": 200  # 2 * 100
        }, {
            "name": "spiceInfusedDuraluminiumDust",
            "display_name": "Spice Infused Duraluminium Dust",
            "value": 1500  # 15 * 100
        }, {
            "name": "spiceInfusedPlastaniumDust",
            "display_name": "Spice Infused Plastanium Dust",
            "value": 4500  # 45 * 100
        }]

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
