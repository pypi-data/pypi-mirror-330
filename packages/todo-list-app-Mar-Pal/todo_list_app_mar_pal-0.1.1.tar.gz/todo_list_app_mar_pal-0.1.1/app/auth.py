from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, HTTPException
import secrets

security = HTTPBasic()

USERNAME = "admin"
PASSWORD = "password"

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):

    if not (secrets.compare_digest(credentials.username, USERNAME) and
            secrets.compare_digest(credentials.password, PASSWORD)):
        raise HTTPException(status_code=401, detail="Unautorized")
    return credentials.username