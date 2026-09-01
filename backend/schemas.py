from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ==========================================================
# CADASTRO
# ==========================================================

class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    curso: str
    bio: Optional[str] = None


# ==========================================================
# RESPOSTA DO USUÁRIO
# ==========================================================

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    curso: str
    bio: Optional[str] = None
    foto: Optional[str] = None

    class Config:
        from_attributes = True


# ==========================================================
# USUÁRIO PÚBLICO
# ==========================================================

class UsuarioPublico(BaseModel):
    id: int
    nome: str
    curso: str
    foto: Optional[str] = None

    class Config:
        from_attributes = True


# ==========================================================
# LOGIN
# ==========================================================

class LoginRequest(BaseModel):
    email: EmailStr
    senha: str


# ==========================================================
# POSTS
# ==========================================================

class PostCreate(BaseModel):
    titulo: str
    conteudo: str


class PostResponse(BaseModel):
    id: int
    titulo: str
    conteudo: str
    usuario_id: int
    data_criacao: datetime

    autor: UsuarioPublico

    class Config:
        from_attributes = True


# ==========================================================
# ATUALIZAR POST
# ==========================================================

class PostUpdate(BaseModel):
    titulo: str
    conteudo: str


# ==========================================================
# ATUALIZAR USUÁRIO
# ==========================================================

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    curso: Optional[str] = None
    bio: Optional[str] = None
    foto: Optional[str] = None
