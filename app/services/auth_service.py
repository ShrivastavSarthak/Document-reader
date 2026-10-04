from datetime import datetime,timedelta,timezone
from jose import jwt
from pwdlib import PasswordHash

ACCESS_TOKEN_TTL = 60
SECRETE_KEY = "thisIsTheSecreteKey"
ALGO= "HS256"

def createAccessToken(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_TTL
    )
    to_encode.update({
        "exp":expire
    })
    
    return jwt.encode(
        to_encode,
        SECRETE_KEY,
        algorithm=ALGO
    )

password_hash = PasswordHash.recommended()

def hashPassword(password:str)->str:
    return password_hash.hash(password)

def verifyPassword(password:str,hashPassword:str)->str:
    return password_hash.verify(password,hashPassword)