import os
import pickle
import time

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

MODELS_DIR = "backend\models"

def load_data(data_path):
    df = pd.read_csv(data_path)

    feature_columns = df.columns[:-1].tolist()

    X = df[feature_columns]
    y = df.iloc[:, -1]

    return X, y

def train_model_big(
        data_path: str,
        model_name: str,
        train_size: float,
        max_iter: int
):

    X, y = load_data(data_path)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        train_size=train_size,
        random_state=None
    )

    model = LogisticRegression(max_iter=max_iter)
    # time.sleep(10)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    model_score = accuracy_score(y_test, preds)

    model_path = os.path.join(MODELS_DIR, f"{model_name}.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    return model_score