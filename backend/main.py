from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
from pydantic import BaseModel

import models as models
from database import engine, get_db
from password_auditor import audit_password

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="IoT Scanner API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScanSubmitPayload(BaseModel):
    target_ip: str
    open_ports: List[Dict[str, Any]]
    vulnerabilities: List[Dict[str, Any]]

class PasswordCheckPayload(BaseModel):
    password: str

@app.post("/api/scan/submit")
def submit_scan_results(payload: ScanSubmitPayload, db: Session = Depends(get_db)):
    # Save the scan results
    for p in payload.open_ports:
        db_scan = models.ScanResult(
            target_ip=payload.target_ip,
            port=p["port"],
            service=p.get("service", "Unknown")
        )
        db.add(db_scan)
        
    # Save vulnerabilities as alerts
    for v in payload.vulnerabilities:
        crack_method = v.get("crack_method", "Attackers scan this service for known version vulnerabilities to run remote code.")
        db_alert = models.Alert(
            severity=v["risk"],
            message=f"Port {v['port']} ({v['service']}) - {v['issue']}: {v['detail']} | Attack Vector: {crack_method}"
        )
        db.add(db_alert)
        
    db.commit()
    return {"status": "success"}

@app.get("/api/scan")
def get_scans(db: Session = Depends(get_db)):
    # Group by latest per port, or just return top 100 recent
    scans = db.query(models.ScanResult).order_by(models.ScanResult.scanned_at.desc()).limit(100).all()
    return {"scans": scans}

@app.get("/api/alerts")
def get_alerts(db: Session = Depends(get_db)):
    alerts = db.query(models.Alert).order_by(models.Alert.created_at.desc()).limit(50).all()
    return {"alerts": alerts}

@app.post("/api/password-check")
def check_password(payload: PasswordCheckPayload):
    result = audit_password(payload.password)
    
    # If weak password, we could technically log an alert, but usually we just return info
    return result

@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    total_ports = db.query(models.ScanResult).count()
    critical_alerts = db.query(models.Alert).filter(models.Alert.severity == "Critical").count()
    high_alerts = db.query(models.Alert).filter(models.Alert.severity == "High").count()
    
    return {
        "scans": total_ports,
        "critical_alerts": critical_alerts,
        "high_alerts": high_alerts
    }
