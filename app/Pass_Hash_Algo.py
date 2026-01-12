from pwdlib import PasswordHash

# Initialize the hasher with recommended settings
passwords = PasswordHash.recommended()

def get_password_hash(password: str) -> str:
    """Converts plain text password to a secure hash."""
    return passwords.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Checks if a plain text password matches the stored hash."""
    return passwords.verify(plain_password, hashed_password)