from dataclasses import dataclass


@dataclass
class JwtConfig:
    secret: str
    algorithm: str = "HS256"
