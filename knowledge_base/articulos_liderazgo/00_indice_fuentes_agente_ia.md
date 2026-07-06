# Índice de fuentes para el agente IA de Dambo

Estos archivos resumen las fuentes académicas que alimentarán el asistente de liderazgo de Dambo. Están escritos en formato Markdown para colocarse en la carpeta de conocimiento del proyecto Streamlit.

## Archivos generados

1. `01_argyris_aprendizaje_doble_bucle.md`  
   Uso: detectar defensividad, baja capacidad de aprendizaje y necesidad de conversaciones reflexivas.

2. `02_google_oxygen_liderazgo.md`  
   Uso: convertir reclamos y encuestas en acciones concretas de liderazgo basadas en comportamientos de buenos gerentes.

3. `03_google_aristoteles_seguridad_psicologica.md`  
   Uso: recomendar acciones para mejorar equipos, confianza, participación y seguridad psicológica.

4. `04_felicidad_en_el_trabajo.md`  
   Uso: interpretar encuestas de salida, felicidad, bienestar, compromiso y productividad.

5. `05_kahneman_sesgos_decision.md`  
   Uso: ayudar al jefe a tomar decisiones menos sesgadas frente a reclamos, datos incompletos o presión operativa.

6. `06_goleman_inteligencia_emocional.md`  
   Uso: recomendar prácticas de autoconciencia, autocontrol, empatía y gestión de relaciones.

7. `07_edmondson_organizacion_sin_miedo.md`  
   Uso: crear recomendaciones sobre seguridad psicológica, voz del empleado, aprendizaje de errores y respuesta productiva del líder.

## Carpeta recomendada en el proyecto

Coloca estos `.md` en:

```text
dambo_lideres_streamlit/knowledge_base/articulos_liderazgo/
```

El archivo `src/gpt_recommender.py` ya está preparado para leer los documentos de esa carpeta mediante `read_knowledge_sources()`.

## Regla para el agente IA

Cuando use estas fuentes, el asistente debe responder con acciones concretas para jefes de sucursal retail. No debe quedarse en teoría. Cada recomendación debe indicar:

- problema detectado;
- acción sugerida;
- responsable;
- con quién hablar;
- herramienta de gestión;
- urgencia;
- evidencia de datos: reclamos, encuesta, KPI o comentario.
