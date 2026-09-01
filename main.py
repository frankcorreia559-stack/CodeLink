from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from auth import (
    criptografar_senha,
    verificar_senha,
    criar_token,
    decodificar_token
)

from database import Base, engine, get_db
from models import Usuario, Post
from schemas import (
    UsuarioCreate,
    UsuarioResponse,
    LoginRequest,
    PostCreate,
    PostResponse,
    PostUpdate
)


# ==========================================================
# CRIAÇÃO DAS TABELAS
# ==========================================================

Base.metadata.create_all(bind=engine)


# ==========================================================
# APLICAÇÃO
# ==========================================================

app = FastAPI(
    title="CodeLink API",
    description="API da rede social para estudantes de ADS",
    version="1.0.0"
)


# ==========================================================
# AUTENTICAÇÃO
# ==========================================================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# ==========================================================
# ROTA INICIAL
# ==========================================================

@app.get("/")
def inicio():
    return {
        "mensagem": "CodeLink API funcionando!"
    }


# ==========================================================
# CADASTRAR USUÁRIO
# ==========================================================

@app.post(
    "/usuarios",
    response_model=UsuarioResponse
)
def criar_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db)
):

    usuario_existente = db.query(Usuario).filter(
        Usuario.email == usuario.email
    ).first()

    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="Email já cadastrado"
        )

    senha_hash = criptografar_senha(usuario.senha)

    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=senha_hash,
        curso=usuario.curso,
        bio=usuario.bio
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario


# ==========================================================
# LOGIN
# ==========================================================

@app.post("/login")
def login(
    email: str,
    senha: str,
    db: Session = Depends(get_db)
):

    usuario = db.query(Usuario).filter(
        Usuario.email == email
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="Email ou senha incorretos"
        )

    senha_correta = verificar_senha(
        senha,
        usuario.senha
    )

    if not senha_correta:
        raise HTTPException(
            status_code=401,
            detail="Email ou senha incorretos"
        )

    token = criar_token({
        "sub": usuario.email
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# ==========================================================
# USUÁRIO ATUAL
# ==========================================================

def get_usuario_atual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    try:

        payload = decodificar_token(token)

        email = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Token inválido"
            )

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado"
        )

    usuario = db.query(Usuario).filter(
        Usuario.email == email
    ).first()

    if usuario is None:
        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado"
        )

    return usuario


# ==========================================================
# MEU PERFIL
# ==========================================================

@app.get(
    "/usuarios/me",
    response_model=UsuarioResponse
)
def meu_perfil(
    usuario: Usuario = Depends(get_usuario_atual)
):

    return usuario

