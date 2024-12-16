from fastapi import Depends, HTTPException, status, APIRouter, Security
from fastapi.security import APIKeyHeader

from service import AuthService
from jwt_utils import JwtToolkit, JwtConfig

from .responses import TokensOut
from transport.requests import UserCredentialsIn


auth_router = APIRouter()


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


config = JwtConfig(SECRET_KEY, ALGORITHM)


def fetch_auth_service():
    return AuthService(JwtToolkit(config))


def api_key_header():
    return APIKeyHeader(name="Authorization", auto_error=False)


@auth_router.post("/sign_in", responses={200: {"model": TokensOut}})
async def sign_in(c: UserCredentialsIn, auth: AuthService = Depends(fetch_auth_service)):
    data = await auth.sign_in(c)

    if not data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return data


@auth_router.post("/sign_up", responses={200: {"model": TokensOut}})  # TODO: NON TESTED
async def sign_up(c: UserCredentialsIn, auth: AuthService = Depends(fetch_auth_service)):
    data = await auth.sign_up(c)

    if not data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return data


@auth_router.post("/verify_token")
async def verify_token(authorization_header: str = Security(api_key_header()),
                       auth: AuthService = Depends(fetch_auth_service)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={"WWW-Authenticate": "Bearer"},
    )

    if "Bearer " not in authorization_header:
        raise credentials_exception

    token = authorization_header.replace("Bearer ", "")

    try:
        auth.verify_token(token)
    except Exception as e:
        credentials_exception.detail = str(e)
        raise credentials_exception

    return authorization_header
