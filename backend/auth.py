from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

SECRET_KEY = "codelink-chave-secreta"
ALGORITHM = "HS256"
TEMPO_TOKEN = 60


def criptografar_senha(senha: str) -> str:
    return pwd_context.hash(senha)


def verificar_senha(senha: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha, senha_hash)


def criar_token(dados: dict) -> str:
    dados_token = dados.copy()

    expiracao = datetime.now(timezone.utc) + timedelta(
        minutes=TEMPO_TOKEN
    )

    dados_token["exp"] = expiracao

    token = jwt.encode(
        dados_token,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token
