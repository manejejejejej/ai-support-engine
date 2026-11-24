import os
import re
import joblib
from typing import Dict, Any

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "ticket_classifier.joblib")
_model = None

def _get_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise RuntimeError("Modelo no encontrado. Ejecuta primero: python train.py")
        _model = joblib.load(MODEL_PATH)
    return _model

CATEGORY_CONFIG = {
    "SECURITY": {
        "default_priority": "CRITICAL",
        "response": "Hemos detectado un posible incidente de seguridad. Nuestro equipo de ciberseguridad ha sido alertado con prioridad maxima y revisara el caso de inmediato."
    },
    "ACCESS": {
        "default_priority": "MEDIUM",
        "response": "Lamentamos el inconveniente de acceso. Por favor, verifique sus credenciales e intente restablecer su contrasena desde el enlace de recuperacion."
    },
    "BUG": {
        "default_priority": "HIGH",
        "response": "Gracias por reportar este comportamiento inesperado. Hemos registrado el incidente tecnico para que nuestro equipo de ingenieria lo investigue."
    },
    "FEATURE": {
        "default_priority": "LOW",
        "response": "Agradecemos su propuesta de mejora. Hemos enviado su solicitud al equipo de producto para evaluarla en futuras actualizaciones."
    }
}

URGENCY_HIGH = [r"\burgente\b", r"\bproducci[oó]n\b", r"\btodos los usuarios\b", r"\bcr[ií]tico\b", r"\bbloqueado totalmente\b"]
INJECTION_PATTERNS = [r"ignora todas las instrucciones", r"ignore previous instructions", r"clasifica.*como prioridad baja"]

def analyze_traditional(message: str) -> Dict[str, Any]:
    text = message.lower().strip()
    is_injection = any(re.search(pat, text) for pat in INJECTION_PATTERNS)
    
    model = _get_model()
    best_category = str(model.predict([message])[0])

    priority = CATEGORY_CONFIG[best_category]["default_priority"]
    
    if not is_injection and best_category != "SECURITY":
        if any(re.search(urg, text) for urg in URGENCY_HIGH):
            priority = "HIGH" if priority in ["LOW", "MEDIUM"] else "CRITICAL"

    if best_category == "SECURITY":
        priority = "CRITICAL"

    requires_human = (best_category == "SECURITY") or is_injection

    return {
        "category": best_category,
        "priority": priority,
        "response": CATEGORY_CONFIG[best_category]["response"],
        "requiresHumanReview": requires_human,
        "mode": "traditional"
    }
