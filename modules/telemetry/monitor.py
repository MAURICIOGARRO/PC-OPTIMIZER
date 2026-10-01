import time
import psutil
import subprocess

class SystemMonitor:
    """Módulo de recolección de métricas de telemetría del sistema en tiempo real."""

    def __init__(self):
        self._last_net_io = psutil.net_io_counters()
        self._last_time = time.time()
        self._last_cpu_percent = 2.0
        self._gpu_name = self._detect_gpu_name()
        # Inicializar el contador de psutil para que la primera llamada no sea 0
        try:
            psutil.cpu_percent(interval=None)
        except Exception:
            pass

    def _detect_gpu_name(self) -> str:
        try:
            cmd = "Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name"
            res = subprocess.run(
                ["powershell.exe", "-NoProfile", "-Command", cmd],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
                timeout=5
            )
            gpus = [line.strip() for line in res.stdout.strip().splitlines() if line.strip()]
            if gpus:
                return ", ".join(gpus)
            return "Adaptador de pantalla estándar"
        except Exception:
            return "GPU Integrada / Dedicada"

    def get_metrics(self) -> dict:
        """Obtiene métricas instantáneas de CPU, RAM, Disco, Red y GPU."""
        now = time.time()
        time_delta = max(0.1, now - self._last_time)

        # CPU con muestreo preciso (0.2s en hilo de fondo para evitar 0% espurio)
        try:
            raw_cpu = psutil.cpu_percent(interval=0.2)
            if raw_cpu > 0.0:
                self._last_cpu_percent = round(raw_cpu, 1)
            else:
                # Si el muestreo global da 0.0 porque el procesador tiene muchos hilos en reposo,
                # mantener la última lectura válida o calcular una base realista
                self._last_cpu_percent = max(1.0, round(self._last_cpu_percent * 0.9, 1))
        except Exception:
            pass

        cpu_percent = self._last_cpu_percent

        cpu_freq = psutil.cpu_freq()
        cpu_freq_ghz = round(cpu_freq.current / 1000, 2) if cpu_freq and cpu_freq.current else 0.0

        # RAM
        mem = psutil.virtual_memory()

        # Disco C:
        disk_c = psutil.disk_usage('C:\\')

        # Red (Cálculo de velocidad Subida / Bajada en KB/s o MB/s)
        net_io = psutil.net_io_counters()
        bytes_sent_per_sec = (net_io.bytes_sent - self._last_net_io.bytes_sent) / time_delta
        bytes_recv_per_sec = (net_io.bytes_recv - self._last_net_io.bytes_recv) / time_delta

        self._last_net_io = net_io
        self._last_time = now

        def format_speed(bytes_sec):
            kb = bytes_sec / 1024
            if kb > 1024:
                return f"{round(kb / 1024, 2)} MB/s"
            return f"{round(kb, 1)} KB/s"

        return {
            "cpu": {
                "percent": cpu_percent,
                "cores_logical": psutil.cpu_count(logical=True) or 4,
                "cores_physical": psutil.cpu_count(logical=False) or 4,
                "freq_ghz": cpu_freq_ghz
            },
            "ram": {
                "percent": mem.percent,
                "used_gb": round(mem.used / (1024**3), 2),
                "total_gb": round(mem.total / (1024**3), 2),
                "free_gb": round(mem.available / (1024**3), 2)
            },
            "disk": {
                "drive": "C:",
                "percent": disk_c.percent,
                "used_gb": round(disk_c.used / (1024**3), 1),
                "total_gb": round(disk_c.total / (1024**3), 1),
                "free_gb": round(disk_c.free / (1024**3), 1)
            },
            "network": {
                "download_speed": format_speed(bytes_recv_per_sec),
                "upload_speed": format_speed(bytes_sent_per_sec),
            },
            "gpu": {
                "name": self._gpu_name
            }
        }
