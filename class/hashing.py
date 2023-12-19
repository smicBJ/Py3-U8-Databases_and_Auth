from passlib.context import CryptContext


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

password = "qwerty"

hashed_password = bcrypt_context.hash(password)

print(hashed_password)
