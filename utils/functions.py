import dagshub.auth
import mlflow as mlf
import mlflow.pyfunc
import psycopg2 as pg

from pydantic import BaseModel


DAGSHUB_USER_TOKEN='a4069f9e2a4a499a4a760c37d7890d1d775d651b'
DAGSHUB_REPO_OWNER = "CharleyDL"
DAGSHUB_REPO = "neo_aissyr"
dagshub.init(DAGSHUB_REPO, DAGSHUB_REPO_OWNER)

remote_server_uri="https://dagshub.com/CharleyDL/neo_aissyr.mlflow"
mlf.set_tracking_uri(remote_server_uri)

# model_uri = 'runs:/d104fc5e1dd8470a8dde5b0c7a760814/model'
# model = mlflow.pyfunc.load_model(model_uri)

# print(model)

class DetectionRequest(BaseModel):
    # def prediction_glyph():
    #     pass
    print("Detect Page")