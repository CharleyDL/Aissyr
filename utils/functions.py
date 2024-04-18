import bcrypt
import dagshub.auth
import mlflow as mlf
import os

# from mlflow.client import MlflowClient
from mlflow import MlflowClient
from mlflow.pyfunc import PyFuncModel, load_model, get_model_dependencies



DAGSHUB_REPO_OWNER = os.getenv("DAGSHUB_REPO_OWNER")
DAGSHUB_REPO = os.getenv("DAGSHUB_REPO")
# DAGSHUB_USER_TOKEN = os.getenv("DAGSHUB_USER_TOKEN")




## ----------------------------- MODEL MANAGER ------------------------------ ##

class MLFlowHandler:
    def __init__(self, tracking_uri: str) -> None:
        dagshub.init(DAGSHUB_REPO, DAGSHUB_REPO_OWNER, mlflow=True)

        model_uri = 'runs:/2ba4940995154cb6afdd4ccc34928e7e/model'
        # self.model = load_model(model_uri)
        self.model = get_model_dependencies(model_uri)

        # mlf.set_tracking_uri(tracking_uri)
        # self.client = MlflowClient(tracking_uri=tracking_uri)

    def check_mlflow_health(self) -> None:
        try:
            experiments = self.client.search_experiments()
            for rm in experiments:
                print(dict(rm), indent=4)
                return "Service returning experiments"
        except:
            return "Error calling MLFlow"

    # def get_production_model(self, store_id: str) -> PyFuncModel:
    #     model_name = f"prophet-retail-forecaster-store-{store_id}"
    #     model = mlf.pyfunc.load_model(model_uri=f"models:/{model_name}/production")
    #     return model




# def dagshub_connect():
#     dagshub.init(repo_owner="DAGSHUB_REPO_OWNER", 
#                  repo_name="DAGSHUB_REPO",
#                  mlflow=True)

# remote_server_uri="https://dagshub.com/CharleyDL/neo_aissyr.mlflow"
# mlf.set_tracking_uri(remote_server_uri)

# model_uri = 'runs:/2ba4940995154cb6afdd4ccc34928e7e/model'
# model = mlflow.pyfunc.load_model(model_uri)



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






# remote_server_uri="https://dagshub.com/CharleyDL/neo_aissyr.mlflow"
# mlf.set_tracking_uri(remote_server_uri)

# model_uri = 'runs:/d104fc5e1dd8470a8dde5b0c7a760814/model'
# model = mlflow.pyfunc.load_model(model_uri)

# print(model)

# class DetectionRequest(BaseModel):
#     def prediction_glyph():
#         return {"message": "From Functions Detect Page"}