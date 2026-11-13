import re
from typing import Dict, Any

RULES = {
    "SECURITY": {
        "keywords": [
            r"\bhack\w*", r"\bvulnerab\w*", r"\bbreach\b", r"\bfiltraci[oó]n\b",
            r"\binyecci[oó]n\b", r"\bsql\b", r"\bxss\b", r"\bphishing\b",
            r"\bsecuestr\w*", r"\bexfiltr\w*", r"\bmalware\b", r"\bransomware\b",
            r"\bcredenciales expuestas\b", r"\bacceso no autorizado\b"
        ],
        "default_priority": "CRITICAL",
        "response": "Hemos detectado un posible incidente de seguridad. Nuestro equipo de ciberseguridad ha sido alertado con prioridad maxima y revisara el caso de inmediato."
    },
    "ACCESS": {
        "keywords": [
            r"\biniciar sesi[oó]n\b", r"\blogin\b", r"\bcontrase[ñn]a\b", r"\bpassword\b",
            r"\bbloquead\w*", r"\b2fa\b", r"\btoken\b", r"\bautenticaci[oó]n\b",
            r"\bno puedo entrar\b", r"\bpermisos?\b", r"\bcuenta\b"
        ],
        "default_priority": "MEDIUM",
        "response": "Lamentamos el inconveniente de acceso. Por favor, verifique sus credenciales e intente restablecer su contrasena desde el enlace de recuperacion."
    },
    "BUG": {
        "keywords": [
            r"\berror\b", r"\bfalla\b", r"\bcrash\b", r"\bca[ií]do\b", r"\b500\b",
            r"\b404\b", r"\bno carga\b", r"\bbug\b", r"\bexcepci[oó]n\b",
            r"\bcongel\w*", r"\blento\b", r"\bno funciona\b", r"\bintermitente\b"
        ],
        "default_priority": "HIGH",
        "response": "Gracias por reportar este comportamiento inesperado. Hemos registrado el incidente tecnico para que nuestro equipo de ingenieria lo investigue."
    },
    "FEATURE": {
        "keywords": [
            r"\bsugerencia\b", r"\bnueva funci[oó]n\b", r"\bcaracter[ií]stica\b",
            r"\bmejorar?\b", r"\bser[ií]a genial\b", r"\bimplementar\b",
            r"\ba[ñn]adir\b", r"\bagregar\b", r"\bexportar a\b", r"\bintegraci[oó]n\b"
        ],
        "default_priority": "LOW",
        "response": "Agradecemos su propuesta de mejora. Hemos enviado su solicitud al equipo de producto para evaluarla en futuras actualizaciones."
    }
}

URGENCY_HIGH = [r"\burgente\b", r"\bproducci[oó]n\b", r"\btodos los usuarios\b", r"\bcr[ií]tico\b", r"\bbloqueado totalmente\b"]
INJECTION_PATTERNS = [r"ignora todas las instrucciones", r"ignore previous instructions", r"clasifica.*como prioridad baja"]

def analyze_traditional(message: str) -> Dict[str, Any]:
    text = message.lower().strip()
    is_injection = any(re.search(pat, text) for pat in INJECTION_PATTERNS)
    
    scores = {cat: 0 for cat in RULES}
    for category, data in RULES.items():
        for pattern in data["keywords"]:
            matches = re.findall(pattern, text)
            scores[category] += len(matches)
            
    best_category = "BUG"
    max_score = 0
    for cat in ["SECURITY", "ACCESS", "BUG", "FEATURE"]:
        if scores[cat] > max_score:
            max_score = scores[cat]
            best_category = cat

    priority = RULES[best_category]["default_priority"]
    
    if not is_injection and best_category != "SECURITY":
        if any(re.search(urg, text) for urg in URGENCY_HIGH):
            priority = "HIGH" if priority in ["LOW", "MEDIUM"] else "CRITICAL"

    if best_category == "SECURITY":
        priority = "CRITICAL"

    requires_human = (best_category == "SECURITY") or is_injection

    return {
        "category": best_category,
        "priority": priority,
        "response": RULES[best_category]["response"],
        "requiresHumanReview": requires_human,
        "mode": "traditional"
    }
