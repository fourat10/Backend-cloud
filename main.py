from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import SessionLocal, engine
import models, schemas

app = FastAPI()

# Create tables
models.Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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