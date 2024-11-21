# Análisis de Amenazas Internas - Herramienta de Análisis

Este proyecto proporciona una herramienta de análisis que permite identificar y evaluar amenazas internas en una organización, utilizando datos almacenados en una base de datos previamente poblada con eventos de seguridad. La herramienta realiza un análisis profundo basado en el criterio del CERT, identificando áreas de riesgo y proporcionando insights cualitativos y cuantitativos sobre posibles amenazas internas.

## Tabla de Contenidos
- [Descripción General](#descripción-general)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Requerimientos del Sistema](#requerimientos-del-sistema)
- [Instalación](#instalación)
- [Uso](#uso)
- [API Endpoints](#api-endpoints)
- [Análisis y Reportes Generados](#análisis-y-reportes-generados)
- [Consideraciones](#consideraciones)

---

## Descripción General

La herramienta de análisis extrae y procesa datos almacenados en una base de datos relacional (por ejemplo, PostgreSQL), generando reportes que ayudan a identificar comportamientos sospechosos en la red, accesos no autorizados, transferencias externas, actividad fuera del horario laboral, y más. Se basa en lineamientos de seguridad del CERT y calcula un puntaje de riesgo para la organización.

### Funcionalidades
1. **Análisis de Accesos No Autorizados**: Agrupa eventos de accesos no permitidos.
2. **Detección de Actividad Fuera del Horario Laboral**: Muestra actividades fuera del horario de trabajo.
3. **Monitoreo de Fallos de Inicio de Sesión**: Agrupa intentos fallidos de inicio de sesión.
4. **Detección de Transferencias Externas**: Identifica transferencias a dispositivos externos.
5. **Análisis de Riesgo**: Evalúa y clasifica el riesgo organizacional.
6. **Resumen de Actividades y Comportamiento del Usuario**: Proporciona estadísticas de eventos y patrones de comportamiento.

---

## Estructura del Proyecto

```
.
├── analysis.py               # Funciones de análisis de eventos y detección de amenazas
├── db_connection.py          # Conexión a la base de datos
├── config.py                 # Archivo de configuración
├── api.py                    # API en Flask
├── requirements.txt          # Dependencias del proyecto
└── README.md                 # Documentación del proyecto
```

---

## Requerimientos del Sistema

- Python 3.8 o superior
- PostgreSQL (o cualquier otra base de datos soportada por SQLAlchemy)
- Paquetes incluidos en `requirements.txt`

---

## Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/tu-repositorio/analisis-amenazas-internas.git
   cd analisis-amenazas-internas
   ```

2. **Instalar las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar la base de datos**:
   Crear una base de datos en PostgreSQL y actualizar la información de conexión en `config.py` para que apunte a la base de datos correcta.


---

## Uso

### Ejecución del análisis

1. **Cargar y analizar datos**:
   Ejecuta el script `analysis.py` para realizar el análisis de los eventos de seguridad. Esto generará una salida detallada de los diferentes aspectos de seguridad en la organización.

   ```bash
   python analysis.py
   ```

2. **Interpreta los resultados**:
   La herramienta proporcionará un análisis detallado en la consola, incluyendo datos como intentos de acceso no autorizados, transferencias a dispositivos externos, actividad fuera del horario laboral, y un puntaje de riesgo.

---


## API Endpoints

### 1. `/analyze/unauthorized-access`
- **Descripción**: Devuelve todos los eventos de acceso no autorizado.
- **Método**: `GET`
- **Respuesta**:
  ```json
  {
      "summary": { "usuario1": 10, "usuario2": 5 },
      "total": 15,
      "details": [
          {"timestamp": "2024-01-01T12:00:00", "usuario": "usuario1", "accion": "Acceso a archivo", "ubicacion": "Remota"},
          ...
      ]
  }
  ```

### 2. `/analyze/out-of-hours-activity`
- **Descripción**: Devuelve actividades realizadas fuera del horario laboral.
- **Método**: `GET`

### 3. `/analyze/login-failures`
- **Descripción**: Devuelve el número total de fallos de inicio de sesión.
- **Método**: `GET`

### 4. `/analyze/external-transfers`
- **Descripción**: Devuelve todas las transferencias externas detectadas.
- **Método**: `GET`

### 5. `/cross-reference/out-of-hours-and-external-transfers`
- **Descripción**: Identifica transferencias externas fuera de horario.
- **Método**: `GET`

### 6. `/cross-reference/failed-logins-and-unauthorized-access`
- **Descripción**: Muestra eventos de acceso no autorizado con intentos fallidos.
- **Método**: `GET`

### 7. `/analyze/risk`
- **Descripción**: Calcula el puntaje de riesgo de la organización.
- **Método**: `GET`
- **Respuesta**:
  ```json
  {
      "nivel_de_riesgo": "Medio",
      "puntuacion_riesgo": 35,
      "areas_criticas": {
          "usuarios_sospechosos": {"usuario1": 5},
          "ubicaciones_riesgosas": {"remota": 3},
          "archivos_sensibles": {"archivo_confidencial": 7},
          ...
      }
  }
  ```

### 8. `/analyze/summary`
- **Descripción**: Muestra un resumen general de todos los eventos registrados.
- **Método**: `GET`

### 9. `/analyze/user-behavior`
- **Descripción**: Proporciona un análisis detallado del comportamiento de cada usuario.
- **Método**: `GET`


---


## Análisis y Reportes Generados

La herramienta proporciona los siguientes reportes:

1. **Accesos No Autorizados**: 
   - **Resumen**: Número de accesos no autorizados por usuario.
   - **Detalles**: Información de cada evento de acceso no autorizado, incluyendo usuario, ubicación, y timestamp.

2. **Actividad Fuera de Horas de Trabajo**:
   - **Resumen**: Total de eventos fuera del horario laboral por usuario.
   - **Detalles**: Listado de eventos fuera de horario, con usuario, timestamp y ubicación.

3. **Fallos de Inicio de Sesión**:
   - **Total**: Número de intentos fallidos de inicio de sesión.
   - **Detalles**: Fallos de inicio de sesión por usuario y IP, útil para identificar cuentas de usuario en riesgo.

4. **Transferencias Externas**:
   - **Total**: Número de transferencias a dispositivos externos.
   - **Detalles**: Listado de transferencias con usuario, archivo y dispositivo.

5. **Análisis de Riesgo**:
   - **Puntaje de Riesgo**: Un puntaje general que clasifica el nivel de riesgo de la organización.
   - **Áreas Críticas**: Usuarios, archivos, y dispositivos con mayores riesgos de seguridad.

6. **Resumen General de Actividades**:
   - **Eventos Totales**: Número total de eventos registrados.
   - **Eventos No Autorizados**: Número de eventos que fueron bloqueados o no autorizados.
   - **Actividades Fuera de Horas**: Número de actividades realizadas fuera del horario de trabajo.

7. **Comportamiento del Usuario**:
   - **Resumen por Usuario**: Datos de cada usuario incluyendo total de eventos, accesos no autorizados y fallos de inicio de sesión.

---

## Consideraciones

- **Configuración de Base de Datos**: Asegúrate de que los datos en la base de datos estén bien estructurados y sigan los esquemas definidos en el proyecto para garantizar un análisis correcto.
- **Interpretación de Resultados**: Los datos proporcionados son una ayuda en la identificación de riesgos, pero siempre deben ser revisados por personal calificado en seguridad.
- **Actualización de Esquemas**: Si los formatos de logs cambian, es necesario actualizar los esquemas en el archivo `log_schemas.json` en el software de ingesta de datos.

---


## Licencia



---
