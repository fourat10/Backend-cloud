from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from database import SessionLocal, engine
import models, schemas

# Créer l'application FastAPI
app = FastAPI(
    title="Contacts API",
    description="API pour gérer les contacts",
    version="1.0.0"
)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,              # Liste des origines autorisées
    allow_credentials=True,             # Autorise les cookies/credentials
    allow_methods=["*"],                # Autorise toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],                # Autorise tous les headers
    expose_headers=["*"],               # Expose tous les headers dans la réponse
)


# Create tables
models.Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Route racine
@app.get("/")
def root():
    return {
        "message": "Backend API is running",
        "version": "1.0.0",
        "status": "healthy"
    }
@app.get("/contacts", response_model=list[schemas.ContactResponse])
def list_contacts(db: Session = Depends(get_db)):
    contacts = db.query(models.Contact).all()
    return contacts

@app.post("/contacts")
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    new_contact = models.Contact(
        nom_complet=contact.nom_complet,
        email=contact.email,
        entreprise=contact.entreprise,
        besoin=contact.besoin
    )

    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)

    return {
        "message": "Contact created successfully",
        "data": new_contact
    }


# DELETE un contact
@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    """Supprimer un contact"""
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact non trouvé")

    db.delete(contact)
    db.commit()
    return {"message": "Contact supprimé avec succès"}

# GET un contact par ID
@app.get("/contacts/{contact_id}", response_model=schemas.ContactResponse)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    """Récupérer un contact par son ID"""
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact non trouvé")
    return contact