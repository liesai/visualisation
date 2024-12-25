from sqlalchemy import create_engine, Column, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import datetime

# Définition du modèle de base
Base = declarative_base()

# Définition de la classe Topic
class Topic(Base):
    __tablename__ = "topics"

    name = Column(String, primary_key=True)
    format = Column(String, nullable=False)
    schema = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Configuration de l'URL pour PostgreSQL
DATABASE_URL = "postgresql://admin:admin123@localhost:5432/kafka_dashboard"

# Fonction pour créer la base de données si elle n'existe pas
def create_database_if_not_exists():
    try:
        # Se connecter à la base de données postgres par défaut
        conn = connect(
            dbname="postgres", user="admin", password="admin123", host="localhost", port=5432
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'kafka_dashboard';")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute("CREATE DATABASE kafka_dashboard;")
            print("Base de données 'kafka_dashboard' créée avec succès.")
        else:
            print("La base de données 'kafka_dashboard' existe déjà.")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erreur lors de la vérification ou de la création de la base de données : {e}")

# Création de l'engine
engine = create_engine(DATABASE_URL)

# Création de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Création des tables
def init_db():
    print("Création des tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables créées avec succès.")

# Point d'entrée principal
if __name__ == "__main__":
    # Créer la base de données si nécessaire
    create_database_if_not_exists()
    # Créer les tables
    init_db()
