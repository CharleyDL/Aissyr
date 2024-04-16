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


def verify_password_hash(account_info, input_pwd) -> bool:
    input_pwd_bytes_test = bcrypt.hashpw(input_pwd.encode(), bcrypt.gensalt(12))
    hashed_password = account_info["password_hash"].tobytes()

    print(input_pwd)
    print(input_pwd_bytes_test)
    print(hashed_password)

    return bcrypt.checkpw(input_pwd_bytes_test, hashed_password)




# remote_server_uri="https://dagshub.com/CharleyDL/neo_aissyr.mlflow"
# mlf.set_tracking_uri(remote_server_uri)

# model_uri = 'runs:/d104fc5e1dd8470a8dde5b0c7a760814/model'
# model = mlflow.pyfunc.load_model(model_uri)

# print(model)

# class DetectionRequest(BaseModel):
#     def prediction_glyph():
#         return {"message": "From Functions Detect Page"}