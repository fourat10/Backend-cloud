from pydantic import BaseModel, EmailStr

class ContactCreate(BaseModel):
    nom_complet: str
    email: EmailStr
    entreprise: str | None = None
    besoin: str | None = None


class ContactResponse(BaseModel):
    id: int
    nom_complet: str
    email: EmailStr
    entreprise: str | None
    besoin: str | None

    class Config:
        from_attributes = True
