# PDD Scope Rule

## 🎯 Alcance del PDD

El Process Definition Document (PDD) define cómo funciona el proceso actual (AS-IS) antes de su automatización.
Su alcance es documentar, analizar y estandarizar cada paso, actor, regla y sistema involucrado, para permitir el diseño técnico y la automatización segura, escalable y mantenible del proceso.

## 🔹 Incluye

- Descripción funcional del proceso manual actual
- Entradas, salidas, actores y sistemas involucrados
- Reglas de negocio y excepciones
- Flujos y diagramas del proceso AS-IS
- Métricas de desempeño (volumen, frecuencia, tiempos)
- Identificación de oportunidades de automatización

## 🔸 No incluye

- Diseño técnico de la solución automatizada (eso pertenece al CDD/SDD)
- Implementación ni configuración de herramientas
- Pruebas o despliegue en producción

## 🧩 Objetivo final

Proporcionar una base clara, verificable y aprobada por el negocio que sirva como entrada directa para el diseño y desarrollo de la automatización (fase TO-BE).

## 🧾 AS-IS – Estado Actual del Proceso

### 🧠 Descripción general

El proceso actual consiste en la transformación manual de una lista de correos electrónicos corporativos con el fin de generar un nuevo listado con formato estandarizado y dominio actualizado.
El proceso es ejecutado por un analista de soporte administrativo o de datos, quien realiza las tareas utilizando herramientas de ofimática convencionales (Bloc de notas, Excel, y explorador de archivos).

### 👥 Actor principal

**Rol:** Analista de Datos / Administrativo

**Responsabilidades:**
- Recepción y validación de archivos fuente
- Limpieza y normalización de información
- Generación de reportes de salida
- Comunicación de resultados al solicitante

### ⚙️ Flujo detallado del proceso actual

**1. Recepción del archivo fuente**
- El área solicitante envía un archivo .txt por correo o a través de una carpeta compartida (SharePoint o red local)
- El archivo contiene una lista de correos con el formato: nombre.apellido@example.com
- El analista descarga el archivo y lo guarda en su estación de trabajo local

**2. Revisión inicial**
- El analista abre el archivo con un editor de texto (Notepad o VS Code) para verificar:
  - Que todos los correos estén en líneas separadas
  - Que sigan el formato esperado (nombre.apellido@dominio)
  - Que no existan errores tipográficos, espacios o caracteres especiales

**3. Extracción y separación de campos**
- Copia el contenido y lo pega en Excel
- Usa funciones manuales (Texto en columnas, delimitador "." y "@") para separar:
  - Nombre
  - Apellido
  - Dominio original

**4. Normalización de formato**
- Aplica fórmulas o ediciones manuales para capitalizar
- Corrige inconsistencias como nombres compuestos o faltas de ortografía

**5. Generación de nuevo correo**
- Crea una nueva columna en Excel y concatena: nombre.apellido@nuevo.com
- Verifica visualmente que el formato del nuevo correo sea correcto

**6. Validación final**
- Revisa que no existan duplicados ni celdas vacías
- Si hay errores, los corrige manualmente
- Guarda el resultado en un archivo .csv o .xlsx

**7. Entrega**
- Nombra el archivo como expected_output.csv
- Envía el resultado al solicitante por correo electrónico o lo carga a la carpeta compartida

### 🧩 Entradas
- **Archivo de texto:** sample_emails.txt con correos en formato nombre.apellido@example.com
- **Instrucciones:** Documento enviado por correo o referencia al procedimiento interno

### 📤 Salidas
- **Archivo CSV:** expected_output.csv con columnas: Nombre, Apellido, Correo Ejemplo, Correo Nuevo
- **Evidencia:** Capturas de pantalla del proceso, logs o registros manuales

### 🧱 Herramientas utilizadas
- Microsoft Excel
- Bloc de Notas / VS Code
- Correo corporativo o carpeta compartida (para transferir archivos)

### 🕒 Duración promedio
- **Archivos pequeños (10–100 correos):** 10–15 minutos
- **Archivos grandes (1000+ correos):** 30–45 minutos (depende del nivel de revisión manual)

### ⚠️ Puntos débiles y oportunidades de mejora
- **Eficiencia:** El proceso es 100% manual y no escalable
- **Calidad:** Propenso a errores humanos al capitalizar o concatenar datos
- **Tiempo:** Se desperdicia tiempo en tareas repetitivas y validaciones visuales
- **Trazabilidad:** No existen registros automáticos de ejecución ni validaciones automáticas
- **Seguridad:** Riesgo de exposición de datos si los archivos se manejan fuera de entornos seguros

## 📝 Aplicación

Cuando se edite, actualice o modifique el PDD (`docs/PDD.md`):
- Mantener enfoque en documentación del proceso AS-IS (manual, antes de automatización)
- No incluir detalles de implementación técnica (tecnologías, frameworks, arquitecturas)
- Describir el proceso desde la perspectiva del negocio y el usuario
- Asegurar que todas las secciones estén completas y aprobadas
- Actualizar diagramas Mermaid si el flujo cambia
- Regenerar SVGs ejecutando `sh docs/diagrams/convert.sh`
