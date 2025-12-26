from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import SessionLocal, engine
import models, schemas

# Create tables FIRST
models.Base.metadata.create_all(bind=engine)

# Créer l'application FastAPI
app = FastAPI(
    title="Contacts API",
    description="API pour gérer les contacts",
    version="1.0.0"
)

# CORS Configuration - CRITICAL: This MUST be the FIRST middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # For production, use specific origins like ["https://yourdomain.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,                  # Cache preflight requests for 1 hour
)

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

# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "contacts-api"
    }

@app.get("/contacts", response_model=list[schemas.ContactResponse])
def list_contacts(db: Session = Depends(get_db)):
    contacts = db.query(models.Contact).all()
    return contacts

@app.post("/contacts", response_model=schemas.ContactResponse, status_code=201)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    """Créer un nouveau contact"""
    new_contact = models.Contact(
        nom_complet=contact.nom_complet,
        email=contact.email,
        entreprise=contact.entreprise,
        besoin=contact.besoin
    )

    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)

    return new_contact

@app.delete("/contacts/{contact_id}", status_code=200)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    """Supprimer un contact"""
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact non trouvé")

    db.delete(contact)
    db.commit()
    return {"message": "Contact supprimé avec succès"}

@app.get("/contacts/{contact_id}", response_model=schemas.ContactResponse)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    """Récupérer un contact par son ID"""
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact non trouvé")
    return contact