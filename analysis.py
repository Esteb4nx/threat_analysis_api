import pandas as pd
from db_connection import get_db_connection
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data():
    """Carga todos los datos de eventos en un DataFrame de pandas."""
    query = "SELECT * FROM eventos"
    with get_db_connection() as conn:
        return pd.read_sql(query, conn)

def analyze_unauthorized_access(data):
    unauthorized_access = data[data['autorizacion'] == False]
    summary = unauthorized_access['usuario'].value_counts().to_dict()
    details = unauthorized_access[['timestamp', 'usuario', 'accion', 'ubicacion']].to_dict(orient='records')
    return {"summary": summary, "total": len(unauthorized_access), "details": details}

def analyze_out_of_hours_activity(data):
    out_of_hours = data[data['out_of_hours'] == True]
    summary = out_of_hours['usuario'].value_counts().to_dict()
    details = out_of_hours[['timestamp', 'usuario', 'accion', 'ubicacion']].to_dict(orient='records')
    return {"summary": summary, "total": len(out_of_hours), "details": details}

def analyze_login_failures(data):
    data['accion_normalizada'] = data['accion'].str.strip().str.lower()
    login_failures = data[data['accion_normalizada'] == 'failed']
    total_failures = len(login_failures)
    login_failure_details = login_failures.groupby(['usuario', 'ip']).size().reset_index(name='failures_count')
    return {"total_login_failures": total_failures, "details": login_failure_details.to_dict(orient="records")}

def analyze_external_transfers(data):
    data['accion_normalizada'] = data['accion'].str.strip().str.lower()
    external_transfers = data[data['accion_normalizada'].isin(['copy to external device', 'transfer'])]
    total_transfers = len(external_transfers)
    external_transfer_details = external_transfers.groupby(['usuario', 'archivo', 'destination']).size().reset_index(name='transfer_count')
    return {"total_external_transfers": total_transfers, "details": external_transfer_details.to_dict(orient="records")}

def cross_reference_out_of_hours_and_external_transfers(data):
    out_of_hours_transfers = data[(data['out_of_hours'] == True) & (data['accion'].str.strip().str.lower() == 'copy to external device')]
    summary = out_of_hours_transfers['usuario'].value_counts().to_dict()
    details = out_of_hours_transfers[['timestamp', 'usuario', 'device', 'archivo']].to_dict(orient='records')
    return {"summary": summary, "total_out_of_hours_transfers": len(out_of_hours_transfers), "details": details}

def cross_reference_failed_logins_and_unauthorized_access(data):
    unauthorized_access = data[data['autorizacion'] == False]
    failed_logins = data[data['accion'].str.strip().str.lower() == 'failed']
    cross_data = pd.merge(unauthorized_access, failed_logins, on="usuario", suffixes=('_unauthorized', '_failed'))
    details = cross_data[['timestamp_unauthorized', 'timestamp_failed', 'usuario', 'ubicacion_unauthorized', 'ip_failed']].to_dict(orient='records')
    return {"total_failed_and_unauthorized": len(cross_data), "details": details}

def cross_reference_multiple_logins_and_external_transfers(data):
    login_data = data[data['accion'].str.strip().str.lower() == 'success']
    external_transfers = data[data['accion'].str.strip().str.lower() == 'copy to external device']
    login_data['timestamp'] = pd.to_datetime(login_data['timestamp'])
    login_counts = login_data.groupby(['usuario']).resample('15T', on='timestamp').size()
    high_login_counts = login_counts[login_counts > 3].reset_index()
    suspicious_transfers = pd.merge(high_login_counts, external_transfers, on="usuario", suffixes=('_login', '_transfer'))
    details = suspicious_transfers[['timestamp_login', 'timestamp_transfer', 'usuario', 'device', 'archivo']].to_dict(orient='records')
    return {"total_suspicious_transfers_after_logins": len(suspicious_transfers), "details": details}

def analyze_risk(data):
    RISK_POINTS = {
        "unauthorized_access": 5,
        "out_of_hours": 3,
        "external_transfer": 4,
        "login_failure": 2
    }

    risk_score = 0
    unauthorized_access = data[data['autorizacion'] == False]
    out_of_hours = data[data['out_of_hours'] == True]
    external_transfers = data[data['accion'].str.strip().str.lower() == 'copy to external device']
    login_failures = data[data['accion'].str.strip().str.lower() == 'failed']

    risk_score += len(unauthorized_access) * RISK_POINTS["unauthorized_access"]
    risk_score += len(out_of_hours) * RISK_POINTS["out_of_hours"]
    risk_score += len(external_transfers) * RISK_POINTS["external_transfer"]
    risk_score += len(login_failures) * RISK_POINTS["login_failure"]

    if risk_score < 20:
        risk_level = "Bajo"
    elif risk_score < 40:
        risk_level = "Medio"
    elif risk_score < 60:
        risk_level = "Alto"
    else:
        risk_level = "Crítico"

    critical_areas = {
        "usuarios_sospechosos": unauthorized_access['usuario'].value_counts().to_dict(),
        "ubicaciones_riesgosas": out_of_hours['ubicacion'].value_counts().to_dict(),
        "archivos_sensibles": external_transfers['archivo'].value_counts().to_dict(),
        "dispositivos_externos": external_transfers['device'].value_counts().to_dict(),
        "ips_riesgosas": login_failures['ip'].value_counts().to_dict()
    }

    return {"nivel_de_riesgo": risk_level, "puntuacion_riesgo": risk_score, "areas_criticas": critical_areas}

def analyze_summary(data):
    total_events = len(data)
    unauthorized_events = len(data[data['autorizacion'] == False])
    out_of_hours_events = len(data[data['out_of_hours'] == True])
    external_transfers = len(data[data['accion'].str.strip().str.lower() == 'copy to external device'])
    failed_logins = len(data[data['accion'].str.strip().str.lower() == 'failed'])
    
    summary = {
        "total_events": total_events,
        "unauthorized_events": unauthorized_events,
        "out_of_hours_events": out_of_hours_events,
        "external_transfers": external_transfers,
        "failed_logins": failed_logins
    }
    return summary

def analyze_user_behavior(data):
    data['accion_normalizada'] = data['accion'].str.strip().str.lower()
    user_stats = data.groupby('usuario').agg(
        total_events=('accion', 'size'),
        unauthorized_events=('autorizacion', lambda x: (x == False).sum()),
        out_of_hours_events=('out_of_hours', lambda x: (x == True).sum()),
        external_transfers=('accion_normalizada', lambda x: (x == 'copy to external device').sum()),
        failed_logins=('accion_normalizada', lambda x: (x == 'failed').sum())
    ).reset_index()

    user_behavior_details = user_stats.to_dict(orient='records')
    return {"user_behavior": user_behavior_details}
