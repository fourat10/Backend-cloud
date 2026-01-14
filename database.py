from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = (
    "mysql+pymysql://admin:chaimaharzi@database-2.cioorvjuqwr0.us-east-1.rds.amazonaws.com:3306/CloudDB"
)

# Configuration du moteur avec pool de connexions
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Mettre à False en production
    pool_pre_ping=True,  # Vérifie la connexion avant utilisation
    pool_recycle=3600,   # Recycle les connexions après 1h
    pool_size=10,        # Nombre de connexions dans le pool
    max_overflow=20      # Connexions supplémentaires si nécessaire
)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
