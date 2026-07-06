# Daniel Kahneman — Sesgos, pensamiento rápido y toma de decisiones

## Idea central para Dambo

Los jefes toman muchas decisiones bajo presión: reclamos, clientes molestos, trabajadores cansados, ventas bajas y falta de tiempo. En ese contexto pueden usar intuiciones rápidas que ayudan, pero también pueden generar errores sistemáticos.

## Conceptos clave

### Sistema 1

Pensamiento rápido, automático e intuitivo. Es útil en situaciones repetidas, pero puede responder con prejuicios o simplificaciones.

### Sistema 2

Pensamiento más lento, deliberado y analítico. Requiere esfuerzo, pero ayuda a revisar datos, comparar opciones y evitar conclusiones apresuradas.

### Sesgo de disponibilidad

El jefe puede creer que el problema más importante es el último reclamo que recuerda, aunque los datos muestren otra tendencia.

### Efecto halo

Una mala experiencia con un trabajador puede contaminar la evaluación completa de su desempeño.

### Exceso de confianza

El jefe puede creer que ya sabe la causa del problema sin revisar encuestas, reclamos y KPIs.

### Aversión a la pérdida

El líder puede evitar cambios por miedo a perder control, aunque el cambio mejore el clima o la atención.

## Uso para el agente IA

El agente debe activar esta fuente cuando:

- el jefe pida decidir entre acciones;
- haya datos contradictorios;
- se quiera priorizar reclamos;
- un problema reciente parezca dominar toda la interpretación;
- el líder culpe rápido a una persona sin revisar contexto.

## Recomendaciones tipo

### Antes de decidir

Pedir al jefe revisar tres evidencias: reclamos, encuesta de salida y KPI operativo.

### Para evitar sesgo de disponibilidad

Comparar el último reclamo con la frecuencia real por tipo de reclamo.

### Para evitar efecto halo

Separar conducta puntual de evaluación general del trabajador.

### Para evitar exceso de confianza

Preguntar: “¿Qué dato podría demostrar que mi interpretación está incompleta?”

## Prompt interno sugerido

Cuando el usuario pida una recomendación, ayuda a distinguir entre intuición y evidencia. Sugiere una decisión basada en datos, no solo en el reclamo más reciente.
