# AI Support Engine
Motor hibrido de clasificacion y respuesta automatica de solicitudes de soporte tecnico mediante IA Simbolica (Reglas) e IA Generativa (Gemini API).

## Instrucciones de Ejecucion
1. Activar entorno virtual: python3 -m venv venv && source venv/bin/activate
2. Instalar dependencias: pip install -r requirements.txt
3. Configurar GEMINI_API_KEY en .env
4. Iniciar servidor: uvicorn main:app --reload
5. Correr pruebas: python benchmark.py

## Conclusion Tecnica
El motor generativo supero significativamente al motor tradicional en precision global, especialmente en solicitudes ambiguas y ataques de prompt injection. Mientras que el motor basado en reglas depende estrictamente de coincidencias lexicas —fallando cuando una solicitud de nueva funcionalidad menciona palabras como "iniciar sesion" (caso 8) o cuando un incidente de seguridad usa lenguaje coloquial sin palabras clave explicitas (caso 6)—, el modelo generativo comprende la intencion semantica real del usuario. Asimismo, mediante instrucciones de sistema delimitadas y esquemas JSON estrictos con Pydantic, el motor generativo resistio los intentos de manipulacion de prioridad y genero respuestas empaticas y contextualizadas. El motor tradicional sigue siendo util como respaldo de baja latencia y costo cero, pero la IA generativa ofrece una automatizacion mucho mas robusta y confiable para produccion.
