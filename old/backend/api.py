import os
import pickle
import time

from fastapi import FastAPI
from fastapi import BackgroundTasks

from pydantic import BaseModel

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_digits

from old.backend.ml.train import train_model_big

app = FastAPI()

MODELS_DIR = "backend\models"

class Item(BaseModel):
    x: float
    y: float

class TrainRequest(BaseModel):
    max_iter: int
    name: str

class TrainRequestBig(BaseModel):
    data_path: str
    model_name: str
    train_size: float
    max_iter: int

@app.get("/")
def root():
    return {"message": "Сервер работает!"}

@app.post("/sum")
def calc_sum(item: Item):
    res = item.x + item.y
    return {"result": res}

# таких функций здесь не оставляем
def train_model(req):
    data = load_digits()
    X, y  = data.data, data.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        train_size=0.5,
        random_state=None
    )

    model = LogisticRegression()
    time.sleep(10)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    model_path = os.path.join(MODELS_DIR, f"{req.name}.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(model, f)


@app.post("/train")
def train(req: TrainRequest, background_tasks: BackgroundTasks):

    background_tasks.add_task(train_model, req)

    return {
        "model_name": req.name,
        "message": "Model saved"
    }


@app.post("/train_big")
def train_big(req: TrainRequestBig, background_tasks: BackgroundTasks):

    print(req)
    model_score = background_tasks.add_task(train_model_big, req)

    return {
        "model_name": req.model_name,
        "train_size": req.train_size,
        "model_score": model_score,
        "message": "Model saved!"
    }
