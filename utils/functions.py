import bcrypt
import dagshub.auth
import mlflow as mlf
import mlflow.pyfunc
import psycopg2 as pg

from pydantic import BaseModel


# DAGSHUB_USER_TOKEN
# DAGSHUB_REPO_OWNER
# DAGSHUB_REPO
# dagshub.init(DAGSHUB_REPO, DAGSHUB_REPO_OWNER)


def hash_bcrypt(plain_text: str) -> bytes:
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




# remote_server_uri="https://dagshub.com/CharleyDL/neo_aissyr.mlflow"
# mlf.set_tracking_uri(remote_server_uri)

# model_uri = 'runs:/d104fc5e1dd8470a8dde5b0c7a760814/model'
# model = mlflow.pyfunc.load_model(model_uri)

# print(model)

# class DetectionRequest(BaseModel):
#     def prediction_glyph():
#         return {"message": "From Functions Detect Page"}