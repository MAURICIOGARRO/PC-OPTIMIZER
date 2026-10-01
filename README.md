# OptiCore // Optimización, Diagnóstico y Reparación de Sistema
> **Suite moderna y minimalista para Windows: Rendimiento, Control de Servicios en Segundo Plano, Optimización de Controladores (Drivers), Salud y Despliegue Modular de Office**

Una suite integral construida con **Python** y **CustomTkinter** con estética **Oscura Minimalista (Clean Slate & Zinc Dark)**, controles sobrios, tipografía clara, telemetría estable en tiempo real y consola de operaciones en vivo, **100% en español**.

---

## 🧭 Arquitectura Modular (7 Módulos Especializados)

### 1. 📊 Panel Principal
- **Especificaciones de Hardware:** Detección en vivo de tu GPU y detalles de CPU (hilos, núcleos físicos y velocidad en GHz).
- **Indicadores de Telemetría Minimalistas:**
  - `Carga de CPU` (muestreo continuo y preciso sin caídas a 0%)
  - `Memoria RAM` (consumo actual en GB y porcentaje)
  - `Almacenamiento (C:)` (espacio libre y total en GB)
  - `Tráfico de Red` (velocidad de bajada y subida en tiempo real)
- **⚡ Botón Optimización Rápida:** En 1 solo clic purga memoria RAM (`EmptyWorkingSet`), limpia archivos temporales, activa el plan de energía *Máximo Rendimiento* y aplica ajustes de latencia mínima.
- **Monitor de Procesos:** Lista de programas con mayor consumo de memoria y botón para finalizar tareas pesadas.

### 2. ⚡ Optimización & RAM
- **🌐 Optimizador de Google Chrome:**
  - Evita que Chrome siga ejecutándose en segundo plano al cerrar la ventana (`BackgroundModeEnabled = 0`).
  - Activa el modo de Ahorro de Memoria de alta eficiencia para suspender pestañas inactivas.
  - Pasa los servicios de actualización automática a manual.
  - Botón para purgar la memoria RAM de Chrome en vivo y botón para cerrar procesos colgados.
- **Limpieza Profunda de Archivos Temporales:** Limpieza de `%TEMP%`, Windows Temp, Prefetch, volcados de error y cachés residuales de navegadores.
- **Liberador Activo de RAM:** Vaciado de la memoria en espera mediante la API nativa de Windows `EmptyWorkingSet`.
- **Ajustes de Latencia Mínima:** Priorización multimedia en el registro, desactivación de Game DVR y optimización de red TCP.
- **Gestor de Arranque:** Control y desactivación de programas de inicio automático con Windows.

### 3. 🛑 Servicios en Fondo
- **📡 TeamViewer & Acceso Remoto:**
  - Configura el servicio de TeamViewer en modo **"Solo bajo demanda" (Manual)** para que no consuma CPU, RAM ni red las 24 horas del día.
  - Botón de deshabilitar o restaurar con un clic.
- **🎮 Xbox & Gaming Services:**
  - Detiene y deshabilita `GamingServices`, `GamingServicesNet` y servicios de Xbox si juegas en Steam, Epic o no usas Game Pass.
  - Botón de restauración inmediata para cuando desees jugar en Xbox App o Game Pass.
- **💻 Telemetría y Servicios OEM Universales (Cualquier Marca):**
  - Detección automática del fabricante (Lenovo, HP, Dell, ASUS, Acer, MSI, Razer, Samsung) y desactivación de sus servicios pesados de fondo.
- **🤖 Desactivación Total de Windows Copilot & Búsquedas Bing:**
  - Suprime Copilot en la barra de tareas, Edge y las sugerencias de Bing en el menú Inicio (evitando que `SearchHost` y procesos zombis de `WebView2` saturen la RAM).
- **🛡️ Privacidad & Telemetría de Windows:** Desactiva servicios de diagnóstico invasivo (`DiagTrack`, `dmwappushservice`).

### 4. 🎮 Controladores & Drivers *(NUEVO)*
- **Auditoría e Inventario de Controladores:**
  - Consulta del adaptador de pantalla (GPU) y versión de controlador de video activa.
  - Conteo total de paquetes de controladores registrados en `DriverStore`.
  - Detección de dispositivos con conflictos o controladores ausentes.
- **Optimización de Dispositivos PNP:**
  - Re-escaneo forzado de buses de hardware (`pnputil.exe /scan-devices`) para re-sincronizar periféricos y eliminar bloqueos de comunicación.
- **Purga de Caché de Shaders Gráficos:**
  - Limpieza de cachés corruptas de DirectX (`D3DSCache`), NVIDIA (`DXCache`/`GLCache`), AMD (`DxCache`) e Intel para eliminar tirones (*stuttering*) y caídas de FPS.
- **Búsqueda Oficial de Drivers:**
  - Disparo de escaneo interactivo de controladores certificados (WHQL) en Windows Update.
  - Acceso directo al Administrador de Dispositivos y re-sincronización de pantalla (`Win + Ctrl + Shift + B`).

### 5. 🛠️ Salud & Reparación del Sistema
- **Puntuación de Salud (0 a 100):** Diagnóstico multicriterio con recomendaciones de 1 clic.
- **Salud Física de Discos (SMART):** Monitoreo del estado físico y desgaste de SSDs y HDDs.
- **Punto de Restauración del Sistema:** Creación de puntos de control de Windows antes de hacer cambios.
- **Integridad de Archivos (DISM + SFC):** Escaneo y restauración en vivo de la imagen del sistema Windows.
- **Restablecimiento Total de Red:** Reseteo de Winsock, TCP/IP, vaciado de DNS y renovación de IP.
- **Reparador de Windows Update:** Limpieza de la base de datos `SoftwareDistribution` corrupta y reinicio de servicios.
- **Comprobación de Disco CHKDSK:** Análisis online de consistencia y programación para el siguiente reinicio.

### 6. 📑 Gestor de Office Click-to-Run
- **Detección de Versión:** Lectura del registro C2R para mostrar la versión activa, arquitectura (x64/x86) y binarios presentes (Word, Excel, PowerPoint, Access, etc.).
- **Instalación Modular Selectiva (ODT Oficial de Microsoft):**
  - Casillas para elegir exactamente qué aplicaciones instalar (por ejemplo, solo PowerPoint).
  - Atajos rápidos: `SOLO POWERPOINT`, `BÁSICO (WORD+EXCEL+PPT)`, `SELECCIONAR TODO`.
- **Actualización Oficial:** Disparo del cliente oficial `OfficeC2RClient.exe /update user` para forzar actualizaciones desde el CDN de Microsoft.

### 7. 📦 Software & Utilidades
- **Desinstalador de Bloatware de Tienda:** Desinstalación desatendida de apps basura preinstaladas de Windows Store (Bing Noticias, Visor 3D, Solitario, etc.).
- **Instalador de Software Esencial en 1 Clic (Winget):** Instalación silenciosa de navegadores, reproductores, compresores y herramientas.
- **Librerías & Runtimes:** Paquete completo Visual C++ (2015-2022 x86/x64) y DirectX para evitar errores de `.dll`.
- **Cambiador Rápido de DNS & Ping:** Selector entre Cloudflare (1.1.1.1), Google (8.8.8.8), AdGuard (Anti-Publicidad), Quad9 (Anti-Malware) y test de latencia en milisegundos.
- **Power Tools:** Consulta de la clave de producto de Windows, apagado programado y accesos directos de administrador.

---

## 🚀 Cómo Iniciar la Aplicación

Haz doble clic en:
```
iniciar.bat
```
*(Solicita permisos de Administrador automáticamente si aún no los tiene).*
