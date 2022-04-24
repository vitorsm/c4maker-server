

class InvalidCredentialsException(Exception):
    def __init__(self, login: str):
        super(f"Invalid credentials for {login}")
