from passlib.context import CryptContext



SECRET_KEY = "dWd_sAxf65ED-6Yyfi6J0JnXM1tNtDmYa6rl479LlYg"

ACCESS_TOKEN_EXPIRE_MINUTES = 60

password_context = CryptContext(schemes=['bcrypt'], deprecated = "auto") 