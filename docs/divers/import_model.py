import mlflow.pyfunc

model_name = "sk-learn-random-forest-reg-model"
model_version = 1

model = mlflow.pyfunc.load_model(model_uri=f"models:/{model_name}/{model_version}")

model.predict(data)

logged_model = 'runs:/0915f7f99f224b83b4b31d65821a110c/model'

loaded_model = mlflow.pyfunc.load_model(logged_model)