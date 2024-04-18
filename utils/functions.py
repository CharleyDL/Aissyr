import bcrypt




## --------------------------- PASSWORD MANAGER ----------------------------- ##

def hash_bcrypt(plain_text: str) -> bytes:
    """
    Hashes the input plaintext using the bcrypt algorithm.

    Args:
    -----
    plain_text (str): The plaintext string to be hashed.

    Returns:
    --------
    bytes: The hashed representation of the plaintext.
    """
    plain_text_bytes = plain_text.encode()
    return bcrypt.hashpw(plain_text_bytes, bcrypt.gensalt(12))


def verify_password_hash(account_info: dict, input_pwd:str) -> bool:
    """
    Check if a password provided by the user matches the hashed password 
    stored in the database.

    Args:
        account_info (dict): A dictionary containing account information, 
        including the hashed password.
        input_pwd (str): The password provided by the user to be checked.

    Returns:
        bool: True if the provided password matches the hashed password 
        in the database, otherwise False.
    """
    input_pwd_bytes = input_pwd.encode()
    hashed_password = account_info["pwd_hash"].tobytes()

    return bcrypt.checkpw(input_pwd_bytes, hashed_password)


## ------------------------------ PREDICTION -------------------------------- ##