from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from database import Base


# ==========================================================
# USUÁRIO
# ==========================================================

class Usuario(Base):

    __tablename__ = "usuarios"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nome = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(150),
        unique=True,
        nullable=False,
        index=True
    )

    senha = Column(
        String(255),
        nullable=False
    )

    curso = Column(
        String(100),
        nullable=False
    )

    bio = Column(
        Text,
        nullable=True
    )

    foto = Column(
        String(255),
        nullable=True
    )

    data_cadastro = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    # ======================================================
    # RELACIONAMENTO COM POSTS
    # ======================================================

    posts = relationship(
        "Post",
        back_populates="autor",
        cascade="all, delete-orphan"
    )

    # ======================================================
    # SEGUINDO
    # ======================================================

    seguindo = relationship(
        "Seguidor",
        foreign_keys="Seguidor.seguidor_id",
        back_populates="seguidor",
        cascade="all, delete-orphan"
    )

    # ======================================================
    # SEGUIDORES
    # ======================================================

    seguidores = relationship(
        "Seguidor",
        foreign_keys="Seguidor.seguido_id",
        back_populates="seguido",
        cascade="all, delete-orphan"
    )


# ==========================================================
# POST
# ==========================================================

class Post(Base):

    __tablename__ = "posts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    titulo = Column(
        String(200),
        nullable=False
    )

    conteudo = Column(
        Text,
        nullable=False
    )

    data_criacao = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False
    )

    # Relacionamento com usuário
    autor = relationship(
        "Usuario",
        back_populates="posts"
    )


# ==========================================================
# SEGUIDORES
# ==========================================================

class Seguidor(Base):

    __tablename__ = "seguidores"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Usuário que está seguindo
    seguidor_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False
    )

    # Usuário que está sendo seguido
    seguido_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False
    )

    data_seguida = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    # ======================================================
    # RELACIONAMENTO COM QUEM SEGUE
    # ======================================================

    seguidor = relationship(
        "Usuario",
        foreign_keys=[seguidor_id],
        back_populates="seguindo"
    )

    # ======================================================
    # RELACIONAMENTO COM QUEM É SEGUIDO
    # ======================================================

    seguido = relationship(
        "Usuario",
        foreign_keys=[seguido_id],
        back_populates="seguidores"
    )