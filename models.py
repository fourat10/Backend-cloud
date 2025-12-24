from sqlalchemy import Column, Integer, String, Text
from database import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    nom_complet = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False)
    entreprise = Column(String(150))
    besoin = Column(Text)
