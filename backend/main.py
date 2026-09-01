from fastapi import FastAPI, Depends, HTTPException, status

from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm
)

from sqlalchemy.orm import Session, joinedload
from jose import jwt, JWTError

from auth import (
    criptografar_senha,
    verificar_senha,
    criar_token,
    SECRET_KEY,
    ALGORITHM
)

from database import Base, engine, get_db

from models import Usuario, Post, Seguidor

from schemas import (
    UsuarioCreate,
    UsuarioResponse,
    LoginRequest,
    UsuarioUpdate,
    PostCreate,
    PostResponse,
    PostUpdate,
    UsuarioPublico
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


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================================
# CONFIGURAÇÃO DO JWT
# ==========================================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)


# ==========================================================
# ROTA PRINCIPAL
# ==========================================================

@app.get("/")
def inicio():
    return {
        "mensagem": "Bem-vindo ao CodeLink!",
        "status": "online"
    }


# ==========================================================
# CADASTRAR USUÁRIO
# ==========================================================

@app.post(
    "/usuarios",
    response_model=UsuarioResponse,
    status_code=201
)
def cadastrar_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db)
):

    usuario_existente = (
        db.query(Usuario)
        .filter(Usuario.email == usuario.email)
        .first()
    )

    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="Este e-mail já está cadastrado."
        )

    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=criptografar_senha(usuario.senha),
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
    dados: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    usuario = (
        db.query(Usuario)
        .filter(Usuario.email == dados.username)
        .first()
    )

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha incorretos."
        )

    senha_correta = verificar_senha(
        dados.password,
        usuario.senha
    )

    if not senha_correta:
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha incorretos."
        )

    token = criar_token({
        "sub": str(usuario.id),
        "email": usuario.email
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# ==========================================================
# USUÁRIO AUTENTICADO
# ==========================================================

def get_usuario_atual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    credenciais_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais.",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        usuario_id = payload.get("sub")

        if usuario_id is None:
            raise credenciais_exception

    except JWTError:
        raise credenciais_exception

    usuario = (
        db.query(Usuario)
        .filter(Usuario.id == int(usuario_id))
        .first()
    )

    if usuario is None:
        raise credenciais_exception

    return usuario


# ==========================================================
# MEU USUÁRIO
# ==========================================================

@app.get(
    "/usuarios/me",
    response_model=UsuarioResponse
)
def usuario_logado(
    usuario: Usuario = Depends(get_usuario_atual)
):

    return usuario

# ==========================================================
# PERFIL PÚBLICO DO USUÁRIO
# ==========================================================

@app.get(
    "/usuarios/{usuario_id}",
    response_model=UsuarioPublico
)
def buscar_usuario_publico(
    usuario_id: int,
    db: Session = Depends(get_db)
):

    usuario = (
        db.query(Usuario)
        .filter(Usuario.id == usuario_id)
        .first()
    )

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado."
        )

    return usuario

# ==========================================================
# LISTAR SEGUIDORES
# ==========================================================

@app.get(
    "/usuarios/{usuario_id}/seguidores",
    response_model=list[UsuarioPublico]
)
def listar_seguidores(
    usuario_id: int,
    db: Session = Depends(get_db)
):

    usuario = (
        db.query(Usuario)
        .filter(Usuario.id == usuario_id)
        .first()
    )

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado."
        )

    seguidores = [
        relacionamento.seguidor
        for relacionamento in usuario.seguidores
    ]

    return seguidores


# ==========================================================
# LISTAR QUEM O USUÁRIO SEGUE
# ==========================================================

@app.get(
    "/usuarios/{usuario_id}/seguindo",
    response_model=list[UsuarioPublico]
)
def listar_seguindo(
    usuario_id: int,
    db: Session = Depends(get_db)
):

    usuario = (
        db.query(Usuario)
        .filter(Usuario.id == usuario_id)
        .first()
    )

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado."
        )

    seguindo = [
        relacionamento.seguido
        for relacionamento in usuario.seguindo
    ]

    return seguindo

# ==========================================================
# SEGUIR USUÁRIO
# ==========================================================

@app.post(
    "/usuarios/{usuario_id}/seguir",
    status_code=200
)
def seguir_usuario(
    usuario_id: int,
    usuario: Usuario = Depends(get_usuario_atual),
    db: Session = Depends(get_db)
):

    # Não pode seguir a si mesmo
    if usuario_id == usuario.id:
        raise HTTPException(
            status_code=400,
            detail="Você não pode seguir a si mesmo."
        )

    # Verifica se o usuário existe
    usuario_seguido = (
        db.query(Usuario)
        .filter(Usuario.id == usuario_id)
        .first()
    )

    if usuario_seguido is None:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado."
        )

    # Verifica se já está seguindo
    relacionamento_existente = (
        db.query(Seguidor)
        .filter(
            Seguidor.seguidor_id == usuario.id,
            Seguidor.seguido_id == usuario_id
        )
        .first()
    )

    if relacionamento_existente:
        raise HTTPException(
            status_code=400,
            detail="Você já segue este usuário."
        )

    # Cria o relacionamento
    novo_seguidor = Seguidor(
        seguidor_id=usuario.id,
        seguido_id=usuario_id
    )

    db.add(novo_seguidor)
    db.commit()
    db.refresh(novo_seguidor)

    return {
        "mensagem": f"Você começou a seguir {usuario_seguido.nome}."
    }


# ==========================================================
# ATUALIZAR MEU USUÁRIO
# ==========================================================

@app.put(
    "/usuarios/me",
    response_model=UsuarioResponse
)
def atualizar_usuario(
    dados: UsuarioUpdate,
    usuario: Usuario = Depends(get_usuario_atual),
    db: Session = Depends(get_db)
):

    if dados.nome is not None:
        usuario.nome = dados.nome

    if dados.curso is not None:
        usuario.curso = dados.curso

    if dados.bio is not None:
        usuario.bio = dados.bio

    if dados.foto is not None:
        usuario.foto = dados.foto

    db.commit()
    db.refresh(usuario)

    return usuario

# ==========================================================
# LISTAR USUÁRIOS
# ==========================================================

@app.get(
    "/usuarios",
    response_model=list[UsuarioResponse]
)
def listar_usuarios(
    db: Session = Depends(get_db)
):

    usuarios = db.query(Usuario).all()

    return usuarios


# ==========================================================
# CRIAR POST
# ==========================================================

@app.post(
    "/posts",
    response_model=PostResponse,
    status_code=201
)
def criar_post(
    post: PostCreate,
    usuario: Usuario = Depends(get_usuario_atual),
    db: Session = Depends(get_db)
):

    novo_post = Post(
        titulo=post.titulo,
        conteudo=post.conteudo,
        usuario_id=usuario.id
    )

    db.add(novo_post)
    db.commit()
    db.refresh(novo_post)

    return novo_post

# ==========================================================
# LISTAR POSTS
# ==========================================================

@app.get(
    "/posts",
    response_model=list[PostResponse]
)
def listar_posts(
    db: Session = Depends(get_db)
):

    posts = (
        db.query(Post)
        .option(joinedload(Post.autor))
        .order_by(Post.data_criacao.desc())
        .all()
    )

    return posts

# ==========================================================
# BUSCAR POST POR ID
# ==========================================================

@app.get(
    "/posts/{post_id}",
    response_model=PostResponse
)
def buscar_post(
    post_id: int,
    db: Session = Depends(get_db)
):

    post = (
        db.query(Post)
        .option(joinedload(Post.autor))
        .filter(Post.id == post_id)
        .first()
    )

    if post is None:
        raise HTTPException(
            status_code=404,
            detail="Post não encontrado."
        )

    return post

# ==========================================================
# ATUALIZAR POST
# ==========================================================

@app.put(
    "/posts/{post_id}",
    response_model=PostResponse
)
def atualizar_post(
    post_id: int,
    dados: PostUpdate,
    usuario: Usuario = Depends(get_usuario_atual),
    db: Session = Depends(get_db)
):

    post = (
        db.query(Post)
        .filter(Post.id == post_id)
        .first()
    )

    if post is None:
        raise HTTPException(
            status_code=404,
            detail="Post não encontrado."
        )

    if post.usuario_id != usuario.id:
        raise HTTPException(
            status_code=403,
            detail="Você não pode editar este post."
        )

    post.titulo = dados.titulo
    post.conteudo = dados.conteudo

    db.commit()
    db.refresh(post)

    return post


    # ==========================================================
# EXCLUIR POST
# ==========================================================

@app.delete(
    "/posts/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def excluir_post(
    post_id: int,
    usuario: Usuario = Depends(get_usuario_atual),
    db: Session = Depends(get_db)
):

    post = (
        db.query(Post)
        .filter(Post.id == post_id)
        .first()
    )

    if post is None:
        raise HTTPException(
            status_code=404,
            detail="Post não encontrado."
        )

    # Verifica se o post pertence ao usuário logado
    if post.usuario_id != usuario.id:
        raise HTTPException(
            status_code=403,
            detail="Você não pode excluir este post."
        )

    db.delete(post)
    db.commit()

    return None