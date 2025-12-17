from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from faker import Faker
import random
from datetime import datetime
from fastapi import HTTPException

from ..database import get_db
from ..views.persona import PersonaCreate, PersonaUpdate, PersonaRead, PoblarRequest
from ..services import persona_service

router = APIRouter(prefix="/personas", tags=["personas"])


@router.post("", response_model=PersonaRead, status_code=status.HTTP_201_CREATED)
def create_persona(persona_in: PersonaCreate, db: Session = Depends(get_db)):
    """Create a new Persona delegating to service layer."""
    # Let domain errors bubble up to global handlers
    return persona_service.create_persona(db, persona_in)


@router.get("", response_model=List[PersonaRead])
def list_personas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """List Personas with pagination via service layer."""
    return persona_service.list_personas(db, skip=skip, limit=limit)


@router.get("/{persona_id}", response_model=PersonaRead)
def get_persona(persona_id: int, db: Session = Depends(get_db)):
    """Retrieve a Persona by ID via service layer."""
    return persona_service.get_persona(db, persona_id)


@router.put("/{persona_id}", response_model=PersonaRead)
def update_persona(persona_id: int, persona_in: PersonaUpdate, db: Session = Depends(get_db)):
    """Update an existing Persona (partial) via service layer."""
    return persona_service.update_persona(db, persona_id, persona_in)


@router.post("/poblar", response_model=dict, status_code=status.HTTP_201_CREATED)
def poblar_personas_endpoint(
    request: PoblarRequest,
    db: Session = Depends(get_db)
):
    """Poblar la base de datos con datos falsos usando Faker"""
    
    if request.cantidad <= 0 or request.cantidad > 1000:
        raise HTTPException(
            status_code=400,
            detail="La cantidad debe estar entre 1 y 1000"
        )
    
    fake = Faker('es_ES')
    
    try:
        # Importar aquí para evitar dependencia circular
        from ..models.persona import Persona
        
        for i in range(request.cantidad):
            # Generar datos
            first_name = fake.first_name()
            last_name = fake.last_name()
            
            # Crear email válido
            email_base = f"{first_name.lower()}.{last_name.lower()}"
            email_base = email_base.replace(' ', '').replace('ñ', 'n')
            email_base = email_base.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
            
            dominios = ["gmail.com", "hotmail.com", "outlook.com", "yahoo.com", "icloud.com"]
            email = f"{email_base}@{random.choice(dominios)}"
            
            # Crear objeto Persona
            persona = Persona(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=fake.phone_number(),
                birth_date=fake.date_of_birth(minimum_age=18, maximum_age=80),
                is_active=random.choice([True, False]),
                notes=fake.sentence(nb_words=random.randint(3, 10)) if random.random() > 0.3 else None,
                created_at=datetime.utcnow()
            )
            
            db.add(persona)
            
            # Para mejor performance
            if i % 50 == 0:
                db.flush()
        
        db.commit()
        
        return {
            "mensaje": f"Base de datos poblada exitosamente con {request.cantidad} registros",
            "cantidad": request.cantidad,
            "status": "success"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al poblar la base de datos: {str(e)}"
        ) 
@router.delete("/reset", response_model=dict)
def reset_database(db: Session = Depends(get_db)):
    """
    Elimina todos los registros de la tabla personas.
    
    - *¡CUIDADO!*: Esta operación es irreversible.
    - Retorna el número de registros eliminados.
    """
    try:
        from ..models.persona import Persona
        
        # Contar antes de borrar
        count = db.query(Persona).count()
        
        # Borrar todos los registros
        db.query(Persona).delete()
        db.commit()
        
        return {
            "message": "Base de datos limpiada. Se eliminaron todos los registros.",
            "deleted_count": count
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al limpiar la base de datos: {str(e)}"
        )
@router.delete("/{persona_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_persona(persona_id: int, db: Session = Depends(get_db)):
    """Delete a Persona by ID via service layer."""
    persona_service.delete_persona(db, persona_id)
    return None