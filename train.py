import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# 1. Cargar los 200 registros
data = pd.read_csv("data/tickets.csv")

# 2. Dividir: 80% (160) entrenar y 20% (40) evaluar
X_train, X_test, y_train, y_test = train_test_split(
    data["message"], data["category"], test_size=0.2,
    stratify=data["category"], random_state=42
)

# 3. Entrenar modelo
model = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
    ("classifier", LogisticRegression(max_iter=1000))
])
model.fit(X_train, y_train)

# 4. Guardar modelo
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/ticket_classifier.joblib")

# 5. Evaluar y mostrar métricas
y_pred = model.predict(X_test)
print(f"Entrenados: {len(X_train)} | Evaluados: {len(X_test)}")
print(f"Precisión: {model.score(X_test, y_test) * 100:.2f}%\n")
print(classification_report(y_test, y_pred))
