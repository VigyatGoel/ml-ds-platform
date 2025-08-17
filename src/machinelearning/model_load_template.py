"""Ultra-simple model loading & prediction helper.

Place this file next to your downloaded artifacts:
  - <YourModel>.pkl (e.g. RandomForestClassifier.pkl)
  - scaler.pkl
  - imputer.pkl
  - feature_names.pkl

Minimal usage:
    from model_load import predict
    result = predict({
        "feature1": 5.1,
        "feature2": 3.5,
        "feature3": 1.4,
        # ... all required features
    }, model_path="./RandomForestClassifier.pkl")
    print(result)

Returns: {'prediction': <value>, 'probabilities': [...]/None}

Dependencies: scikit-learn, numpy
Install if needed: pip install scikit-learn numpy
"""

from __future__ import annotations

import pickle
import numpy as np
from typing import Dict, Any, Union, List
import os


def _load(path: str):
    with open(path, "rb") as f:
        return pickle.load(f)


def predict(
    features: Union[Dict[str, Any], List[float]],
    model_path: str,
) -> Dict[str, Any]:
    """Make a single prediction.

    features:
      - dict: keys are feature names
      - list: values already in correct order (only if feature_names.pkl missing)
    model_path: path to your trained model (.pkl)
    """
    model_dir = os.path.dirname(model_path) or "."

    try:
        model = _load(model_path)
        scaler = _load(os.path.join(model_dir, "scaler.pkl"))
        imputer = _load(os.path.join(model_dir, "imputer.pkl"))
    except FileNotFoundError as e:
        return {"error": f"Missing required file: {e}", "status": "error"}

    # Feature order
    feature_names = None
    try:
        feature_names = _load(os.path.join(model_dir, "feature_names.pkl"))
    except Exception:
        pass  # optional

    if isinstance(features, dict):
        if feature_names:
            ordered = [features.get(name, np.nan) for name in feature_names]
        else:
            ordered = list(features.values())
    else:
        ordered = list(features)

    X = np.array(ordered).reshape(1, -1)
    X = imputer.transform(X)
    X = scaler.transform(X)

    pred = model.predict(X)[0]
    probs = (
        model.predict_proba(X)[0].tolist() if hasattr(model, "predict_proba") else None
    )

    return {"prediction": pred, "probabilities": probs, "status": "success"}


if __name__ == "__main__":
    # Quick demo (edit with your real values)
    example = {"feature1": 5.1, "feature2": 3.5, "feature3": 1.4}
    print(predict(example, "./RandomForestClassifier.pkl"))
