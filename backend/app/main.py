# app/main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pony.orm import Database, Required, db_session
from pydantic import BaseModel

app = FastAPI()

# Configuración CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de la base de datos (usando SQLite en este ejemplo)
db = Database(provider="sqlite", filename=":memory:")

# Definición de modelos
class Huerta(db.Entity):
    nombre = Required(str)

# Configuración de la base de datos
db.generate_mapping(create_tables=True)

# Definición de modelos Pydantic para validación en las rutas
class HuertaCreate(BaseModel):
    nombre: str

class HuertaResponse(BaseModel):
    nombre: str

# Ruta para crear una nueva huerta
@app.post("/huertas", response_model=HuertaResponse)
@db_session
def create_huerta(huerta: HuertaCreate):
    nueva_huerta = Huerta(nombre=huerta.nombre)
    commit()
    return HuertaResponse(**huerta.dict())

# Ruta para obtener todas las huertas
@app.get("/huertas", response_model=list[HuertaResponse])
@db_session
def get_huertas():
    huertas = Huerta.select()[:]
    return [HuertaResponse(nombre=h.nombre) for h in huertas]


