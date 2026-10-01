import psutil
from modules.optimizer.cleaner import SystemCleaner
from modules.optimizer.startup import StartupManager
from modules.analyzer.smart_disk import SmartDiskAnalyzer
from modules.analyzer.security_audit import SecurityAuditor

class HealthScoreCalculator:
    """Calculador de puntuación general de salud del sistema (0-100) y diagnóstico profundo."""

    @classmethod
    def evaluate(cls) -> dict:
        score = 100
        recs = []

        # 1. Evaluación de Espacio y Archivos Basura
        junk_scan = SystemCleaner.scan()
        junk_mb = junk_scan["_summary"]["total_mb"]
        if junk_mb > 5000:
            score -= 15
            recs.append({
                "id": "clean_junk",
                "priority": "ALTA",
                "title": f"Archivos temporales excesivos ({round(junk_mb/1024, 1)} GB)",
                "desc": "Hay una cantidad considerable de caché y temporales acumulados ralentizando lecturas.",
                "action_label": "Limpiar Basura"
            })
        elif junk_mb > 1500:
            score -= 8
            recs.append({
                "id": "clean_junk",
                "priority": "MEDIA",
                "title": f"Archivos temporales acumulados ({junk_mb} MB)",
                "desc": "Se recomienda una limpieza periódica para mantener el disco ágil.",
                "action_label": "Limpiar Basura"
            })

        # 2. Evaluación de Almacenamiento en Disco C:
        disk_c = psutil.disk_usage('C:\\')
        if disk_c.percent > 90:
            score -= 20
            recs.append({
                "id": "disk_full",
                "priority": "ALTA",
                "title": f"Disco principal casi lleno ({disk_c.percent}%)",
                "desc": "Windows necesita al menos un 15% de espacio libre para paginación y actualizaciones.",
                "action_label": "Liberar Espacio"
            })
        elif disk_c.percent > 80:
            score -= 10
            recs.append({
                "id": "disk_warning",
                "priority": "MEDIA",
                "title": f"Almacenamiento por encima del 80%",
                "desc": "Considera mover archivos pesados o realizar limpieza preventiva.",
                "action_label": "Examinar Archivos"
            })

        # 3. Evaluación de RAM en uso
        mem = psutil.virtual_memory()
        if mem.percent > 85:
            score -= 12
            recs.append({
                "id": "optimize_ram",
                "priority": "MEDIA",
                "title": f"Uso de Memoria RAM muy alto ({mem.percent}%)",
                "desc": "Muchos procesos están ocupando el conjunto de trabajo activo.",
                "action_label": "Optimizar RAM"
            })

        # 4. Programas de Inicio
        startup_apps = StartupManager.get_startup_apps()
        enabled_startup = [a for a in startup_apps if a.get("enabled", True)]
        if len(enabled_startup) > 8:
            score -= 10
            recs.append({
                "id": "trim_startup",
                "priority": "MEDIA",
                "title": f"{len(enabled_startup)} aplicaciones arrancan con Windows",
                "desc": "Demasiadas aplicaciones al inicio aumentan notablemente el tiempo de encendido.",
                "action_label": "Gestionar Inicio"
            })

        # 5. Seguridad
        sec = SecurityAuditor.audit_security()
        if not sec["defender_realtime"]:
            score -= 15
            recs.append({
                "id": "fix_defender",
                "priority": "ALTA",
                "title": "Protección en tiempo real desactivada",
                "desc": "Tu equipo está vulnerable a amenazas y malware de día cero.",
                "action_label": "Abrir Seguridad"
            })
        if not sec["firewall_active"]:
            score -= 10
            recs.append({
                "id": "fix_firewall",
                "priority": "MEDIA",
                "title": "Firewall de Windows inactivo",
                "desc": "El tráfico entrante no deseado no está siendo bloqueado adecuadamente.",
                "action_label": "Revisar Firewall"
            })

        # 6. Salud de Discos (SMART)
        disks = SmartDiskAnalyzer.get_disks_health()
        for d in disks:
            if not d.get("is_ok", True):
                score -= 25
                recs.append({
                    "id": "disk_smart_error",
                    "priority": "ALTA",
                    "title": f"Alerta SMART en unidad {d.get('name')}",
                    "desc": "El disco duro reporta anomalías físicas. ¡Haz copia de seguridad inmediata!",
                    "action_label": "Ver Detalles"
                })

        score = max(0, min(100, score))

        if score >= 90:
            status_text = "Excelente"
            color = "#10B981"  # Verde
        elif score >= 75:
            status_text = "Buen Estado"
            color = "#3B82F6"  # Azul
        elif score >= 50:
            status_text = "Mejorable"
            color = "#F59E0B"  # Ámbar
        else:
            status_text = "Atención Requerida"
            color = "#EF4444"  # Rojo

        return {
            "score": score,
            "status_text": status_text,
            "color": color,
            "junk_mb": junk_mb,
            "startup_count": len(enabled_startup),
            "disks": disks,
            "recommendations": recs
        }
