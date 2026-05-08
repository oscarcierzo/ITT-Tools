# -*- coding: utf-8 -*-
"""
IT Tools — Centro de Comandos IT
by Oscarcierzo · 2026

Compilar a EXE:
  pip install pyinstaller
  pyinstaller --onefile --windowed --uac-admin --name "IT-Tools" wincmd_ricma.py

Contraseña por defecto: ricma2026
"""

import sys, os, hashlib, threading, subprocess, ctypes
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
from pathlib import Path
import ctypes, sys

def _is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def _elevate():
    """Re-lanza el script como Administrador si no lo es ya."""
    if not _is_admin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas",
            sys.executable,
            " ".join(f'"{a}"' for a in sys.argv),
            None, 1
        )
        sys.exit()



# ══════════════════════════════════════════════════════════════
# CONTRASEÑA  (SHA-256 de "ricma2026")
# Para cambiarla: hashlib.sha256("tupass".encode()).hexdigest()
# ══════════════════════════════════════════════════════════════
PWD_HASH = "dddebae3324c7243fb8af122bf20ecdd508340bcf232503009448e9e91df56b2"

# ══════════════════════════════════════════════════════════════
# COLORES
# ══════════════════════════════════════════════════════════════
BG       = "#0e1420"
SURFACE  = "#131c2e"
SURFACE2 = "#1a2540"
BORDER   = "#2a3a58"
TEXT     = "#dde4f0"
MUTED    = "#8a9ab8"
CYAN     = "#00b4d8"
CYAN_DIM = "#0d2535"
GREEN    = "#3dd68c"
RED      = "#e56b6f"
YELLOW   = "#f4a261"
ORANGE   = "#fb923c"
PURPLE   = "#a78bfa"
PINK     = "#ff64c8"
LIME     = "#b8c840"
BLUE     = "#64b5ff"
FONT     = ("Segoe UI", 10)
FONT_B   = ("Segoe UI", 10, "bold")
FONT_M   = ("Consolas", 10)
FONT_MB  = ("Consolas", 10, "bold")
FONT_LG  = ("Segoe UI", 15, "bold")
FONT_XS  = ("Segoe UI", 9)

# ══════════════════════════════════════════════════════════════
# DATOS DE COMANDOS
# ══════════════════════════════════════════════════════════════
FAVORITES_CAT = {"id": "favoritos", "label": "⭐  Favoritos", "color": YELLOW, "cmds": []}

CATEGORIES = [
    {"id": 'sistema', "label": '🖥  Sistema', "color": CYAN,
     "cmds": [
        ('2.1 Información del sistema', 'Detalle completo de hardware y SO', 'systeminfo'),
        ('2.2 Versión de Windows', 'Abre ventana de versión del SO', 'winver'),
        ('2.3 Variables de entorno', 'Lista todas las variables de entorno', 'set'),
        ('2.4 Hostname', 'Nombre del equipo en la red', 'hostname'),
        ('2.5 Fecha y hora', 'Fecha y hora del sistema', 'date /t && time /t'),
        ('2.6 Info BIOS / Placa base', 'Datos de BIOS vía WMI', 'powershell -command \"Get-CimInstance Win32_BaseBoard | Select Product,Manufacturer,Version,SerialNumber | Format-List\"'),
        ('2.7 Número de serie equipo', 'Serie del hardware', 'powershell -command \"(Get-CimInstance Win32_BIOS).SerialNumber\"'),
        ('2.8 Procesador', 'Nombre, núcleos y frecuencia del CPU', 'powershell -command \"Get-CimInstance Win32_Processor | Select Name,NumberOfCores,MaxClockSpeed | Format-List\"'),
        ('2.9 Memoria RAM', 'RAM total y disponible', 'powershell -command \"$os=Get-CimInstance Win32_OperatingSystem; [PSCustomObject]@{Total_GB=[math]::Round($os.TotalVisibleMemorySize/1MB,1); Free_GB=[math]::Round($os.FreePhysicalMemory/1MB,1)} | Format-Table\"'),
        ('2.10 Apagar equipo', 'Apaga el equipo inmediatamente', 'shutdown /s /t 0'),
        ('2.11 Reiniciar equipo', 'Reinicia el equipo inmediatamente', 'shutdown /r /t 0'),
        ('2.12 Cerrar sesión', 'Cierra la sesión actual', 'shutdown /l'),
        ('2.13 Visor de eventos', 'Abre el visor de eventos', 'eventvwr.msc'),
        ('2.14 Panel de control', 'Panel de control clásico', 'control'),
        ('2.15 Abrir carpeta TEMP usuario', 'Abre %temp% en el explorador', 'explorer %temp%'),
        ('2.16 Abrir carpeta TEMP Windows', 'Abre C:\\Windows\\Temp', 'explorer C:\\Windows\\Temp'),
        ('2.17 Borrar TEMP usuario', 'Elimina archivos temporales del usuario', 'cmd /c del /q /f /s %temp%\\*'),
        ('2.18 Borrar TEMP Windows', 'Elimina temporales del sistema', 'cmd /c del /q /f /s C:\\Windows\\Temp\\*'),
        ('2.19 Configuración Windows', 'Abre la app Configuración moderna', 'start ms-settings:'),
        ('2.20 Licencia Windows (estado)', 'Estado activacion y ultimos 5 digitos clave', 'powershell -command "Get-CimInstance SoftwareLicensingProduct -Filter \\"PartialProductKey IS NOT NULL AND Name LIKE \'Windows%\'\\" | Select Name,LicenseStatus,PartialProductKey | Format-List"'),
        ('2.21 Clave producto OEM (BIOS)', 'Lee la clave OEM embebida en la BIOS', 'powershell -command "(Get-CimInstance -Query \'SELECT * FROM SoftwareLicensingService\').OA3xOriginalProductKey"'),
        ('2.22 ID AnyDesk', 'Lee la ID de AnyDesk del registro', 'powershell -command "Get-ItemProperty \'HKCU:\\\\Software\\\\AnyDesk\' -EA SilentlyContinue"'),
        ('2.23 ID TeamViewer', 'Lee la ID de TeamViewer del registro', 'powershell -command "(Get-ItemProperty \'HKLM:\\\\SOFTWARE\\\\TeamViewer\' -EA SilentlyContinue).ClientID"'),
        ('2.24 Exportar informe sistema TXT', 'Genera informe completo en el escritorio', 'powershell -command "$f=[Environment]::GetFolderPath(\'Desktop\')+\'\\\\Informe_\'+(Get-Date -f yyyyMMdd_HHmmss)+\'.txt\'; Get-CimInstance Win32_OperatingSystem,Win32_ComputerSystem | Format-List * | Out-File $f -Encoding UTF8; Start-Process notepad $f"'),
    ]},
    {"id": 'discos', "label": '💾  Discos', "color": YELLOW,
     "cmds": [
        ('3.1 Espacio en discos', 'Espacio libre y total de cada unidad', 'powershell -command \"Get-PSDrive -PSProvider FileSystem | Select Name,@{n=\'Used(GB)\';e={[math]::Round($_.Used/1GB,1)}},@{n=\'Free(GB)\';e={[math]::Round($_.Free/1GB,1)}} | Format-Table -AutoSize\"'),
        ('3.2 Verificar disco CHKDSK', 'Verifica y repara disco C: al reiniciar', 'chkdsk C: /f /r'),
        ('3.3 SFC — Reparar sistema', 'Escanea archivos protegidos del sistema', 'sfc /scannow'),
        ('3.4 DISM — Reparar imagen', 'Repara imagen de Windows vía WU', 'DISM /Online /Cleanup-Image /RestoreHealth'),
        ('3.5 Defragmentar disco C:', 'Desfragmenta la unidad C:', 'defrag C: /U /V'),
        ('3.6 Gestor de discos (GUI)', 'Abre administración de discos', 'diskmgmt.msc'),
        ('3.7 Liberar espacio disco', 'Limpieza de archivos innecesarios', 'cleanmgr /d C:'),
        ('3.8 Información de volúmenes', 'Detalles de todos los volúmenes', 'powershell -command \"Get-Volume | Select DriveLetter,FriendlyName,FileSystemType,@{n=\'Size(GB)\';e={[math]::Round($_.Size/1GB,1)}},@{n=\'Free(GB)\';e={[math]::Round($_.SizeRemaining/1GB,1)}} | Format-Table -AutoSize\"'),
        ('3.9 Disco físico info', 'Información de discos físicos', 'powershell -command \"Get-PhysicalDisk | Select FriendlyName,@{n=\'Size(GB)\';e={[math]::Round($_.Size/1GB,0)}},HealthStatus,OperationalStatus | Format-Table -AutoSize\"'),
        ('3.10 Estado SMART disco', 'Estado SMART del disco duro', 'powershell -command \"Get-PhysicalDisk | Select FriendlyName,SerialNumber,HealthStatus,OperationalStatus | Format-Table -AutoSize\"'),
        ('3.11 Limpieza almacenamiento', 'Storage Sense de Windows', 'start ms-settings:storagesense'),
    ]},
    {"id": 'red', "label": '🌐  Red / Internet', "color": GREEN,
     "cmds": [
        ('4.1 Configuración IP completa', 'IP, máscara, gateway, DNS, MAC', 'ipconfig /all'),
        ('4.2 Ping a Google DNS', 'Test conectividad (4 paquetes)', 'ping -n 4 8.8.8.8'),
        ('4.3 Ping continuo', 'Ping hasta Ctrl+C', 'ping -t 8.8.8.8'),
        ('4.4 Traceroute', 'Traza ruta de paquetes hasta destino', 'tracert 8.8.8.8'),
        ('4.5 Conexiones activas', 'Conexiones, puertos y PIDs activos', 'netstat -ano'),
        ('4.6 Puertos en escucha', 'Solo puertos TCP en LISTENING', 'netstat -ano | findstr LISTENING'),
        ('4.7 Tabla ARP', 'IPs y MACs en la red local', 'arp -a'),
        ('4.8 Tabla de rutas', 'Tabla de enrutamiento del sistema', 'route print'),
        ('4.9 Vaciar caché DNS', 'Limpia el caché DNS del sistema', 'ipconfig /flushdns'),
        ('4.10 Renovar IP DHCP', 'Libera y renueva la concesión DHCP', 'ipconfig /release && ipconfig /renew'),
        ('4.11 Resolución DNS', 'Resuelve dominio a IP', 'nslookup google.com'),
        ('4.12 Red WiFi activa', 'SSID y estado de la WiFi actual', 'netsh wlan show interfaces'),
        ('4.13 Redes WiFi guardadas', 'Lista todos los perfiles WiFi', 'netsh wlan show profiles'),
        ('4.14 Estado Firewall', 'Estado del Firewall de Windows', 'netsh advfirewall show allprofiles'),
        ('4.15 Deshabilitar Firewall', 'Desactiva Firewall en todos los perfiles', 'netsh advfirewall set allprofiles state off'),
        ('4.16 Habilitar Firewall', 'Activa Firewall en todos los perfiles', 'netsh advfirewall set allprofiles state on'),
        ('4.17 Reset Winsock + IP', 'Reinicia pila TCP/IP y Winsock', 'netsh winsock reset && netsh int ip reset'),
        ('4.18 Adaptadores de red (GUI)', 'Panel de conexiones de red', 'ncpa.cpl'),
    ]},
    {"id": 'usuarios', "label": '👤  Usuarios', "color": PURPLE,
     "cmds": [
        ('5.1 Listar usuarios locales', 'Todos los usuarios del sistema', 'net user'),
        ('5.2 Detalle usuario actual', 'Info del usuario activo', 'net user %USERNAME%'),
        ('5.3 Crear usuario local', 'Crea nuevo usuario (edita antes)', 'net user USUARIO CONTRASENA /add'),
        ('5.4 Eliminar usuario', 'Elimina usuario local', 'net user USUARIO /delete'),
        ('5.5 Añadir a Administradores', 'Agrega usuario al grupo Admin', 'net localgroup Administradores USUARIO /add'),
        ('5.6 Listar grupos locales', 'Lista todos los grupos', 'net localgroup'),
        ('5.7 Usuarios del grupo Admin', 'Miembros de Administradores', 'net localgroup Administradores'),
        ('5.8 whoami — usuario actual', 'Usuario, dominio y permisos SID', 'whoami /all'),
        ('5.9 Habilitar cuenta Admin', 'Activa el Administrador integrado', 'net user Administrador /active:yes'),
        ('5.10 Sesiones activas', 'Sesiones de usuarios en el sistema', 'query session'),
        ('5.11 Política de contraseñas', 'Reglas de contraseñas y bloqueo', 'net accounts'),
        ('5.12 Cuentas de usuario (GUI)', 'Gestión de cuentas local', 'lusrmgr.msc'),
    ]},
    {"id": 'procesos', "label": '⚙️  Procesos', "color": BLUE,
     "cmds": [
        ('6.1 Lista de procesos', 'Todos los procesos con PID y memoria', 'tasklist'),
        ('6.2 Procesos con ruta EXE', 'Lista procesos con ruta del ejecutable', 'powershell -command \"Get-Process | Where {$_.Path} | Select Name,Id,Path | Sort Name | Format-Table -AutoSize\"'),
        ('6.3 Matar proceso por nombre', 'Terminar proceso (edita el nombre)', 'taskkill /f /im notepad.exe'),
        ('6.4 Matar proceso por PID', 'Terminar por PID (edita el número)', 'taskkill /f /pid 1234'),
        ('6.5 Lista de servicios', 'Todos los servicios y su estado', 'sc query type= all state= all'),
        ('6.6 Servicios en ejecución', 'Solo servicios activos', 'net start'),
        ('6.7 Iniciar servicio', 'Inicia servicio (edita nombre)', 'net start wuauserv'),
        ('6.8 Detener servicio', 'Detiene servicio (edita nombre)', 'net stop wuauserv'),
        ('6.9 Administrador de tareas', 'Abre el Task Manager', 'taskmgr'),
        ('6.10 Monitor de recursos', 'Monitor de recursos avanzado', 'resmon'),
        ('6.11 Monitor de rendimiento', 'Perfmon completo', 'perfmon'),
        ('6.12 Consola de servicios', 'Gestión gráfica de servicios', 'services.msc'),
        ('6.13 Programador de tareas', 'Tareas programadas del sistema', 'taskschd.msc'),
    ]},
    {"id": 'boot', "label": '🚀  Boot / Arranque', "color": ORANGE,
     "cmds": [
        ('7.1 Ver configuración BCD', 'Todas las entradas del gestor de arranque', 'bcdedit /enum all'),
        ('7.2 Configuración arranque', 'msconfig — inicio y servicios', 'msconfig'),
        ('7.3 Modificar timeout boot (5s)', '5 segundos de espera en menú arranque', 'bcdedit /timeout 5'),
        ('7.4 Reparar BCD', 'Reconstruye el BCD desde cero', 'bootrec /rebuildbcd'),
        ('7.5 Reparar MBR', 'Repara el Master Boot Record', 'bootrec /fixmbr'),
        ('7.6 Reparar sector arranque', 'Escribe nuevo sector de arranque', 'bootrec /fixboot'),
        ('7.7 Activar modo seguro', 'Próximo inicio en Modo Seguro', 'bcdedit /set {current} safeboot minimal'),
        ('7.8 Desactivar modo seguro', 'Elimina opción safeboot del BCD', 'bcdedit /deletevalue {current} safeboot'),
        ('7.9 Activar hibernación', 'Habilita hibernación en Windows', 'powercfg /h on'),
        ('7.10 Desactivar hibernación', 'Deshabilita hibernate + borra hiberfil.sys', 'powercfg /h off'),
        ('7.11 Plan de energía activo', 'Muestra el esquema de energía actual', 'powercfg /getactivescheme'),
        ('7.12 Entorno recuperación (WinRE)', 'Reinicia en Entorno de Recuperación', 'reagentc /boottore'),
    ]},
    {"id": 'registro', "label": '📝  Registro', "color": RED,
     "cmds": [
        ('8.1 Editor de registro', 'Abre regedit', 'regedit'),
        ('8.2 Exportar clave registro', 'Exporta clave a archivo .reg', 'reg export HKLM\\SOFTWARE\\MiClave backup.reg'),
        ('8.3 Importar archivo .reg', 'Importa .reg al registro', 'reg import backup.reg'),
        ('8.4 Consultar clave', 'Lee valor específico del registro', 'reg query HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion /v ProgramFilesDir'),
        ('8.5 Buscar en registro', 'Busca texto en todo el registro', 'reg query HKLM /f "termino" /t REG_SZ /s'),
        ('8.6 Programas inicio (usuario)', 'Inicio automático del usuario', 'reg query HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run'),
        ('8.7 Programas inicio (sistema)', 'Inicio automático del sistema', 'reg query HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run'),
    ]},
    {"id": 'seguridad', "label": '🔒  Seguridad', "color": PINK,
     "cmds": [
        ('9.1 Política seguridad local', 'Editor de directivas de seguridad', 'secpol.msc'),
        ('9.2 Directivas de grupo GPO', 'Editor GPO local', 'gpedit.msc'),
        ('9.3 Certificados sistema', 'Administrador de certificados del equipo', 'certlm.msc'),
        ('9.4 Certificados usuario', 'Certificados del usuario actual', 'certmgr.msc'),
        ('9.5 Permisos NTFS (icacls)', 'Permisos de una carpeta', 'icacls C:\\Windows\\System32'),
        ('9.6 Defender — escaneo rápido', 'Escaneo rápido de Windows Defender', 'MpCmdRun.exe -Scan -ScanType 1'),
        ('9.7 Defender — escaneo completo', 'Escaneo completo del sistema', 'MpCmdRun.exe -Scan -ScanType 2'),
        ('9.8 Usuarios con sesión abierta', 'Sesiones interactivas activas', 'query user'),
    ]},
    {"id": 'ad', "label": '🏢  Active Directory', "color": "#60a5fa",
     "cmds": [
        ('10.1 Info del dominio', 'Nombre y controladores del dominio', 'echo %USERDOMAIN% && echo %LOGONSERVER%'),
        ('10.2 Controladores de dominio', 'Lista los DCs del dominio actual', 'nltest /dclist:%USERDOMAIN%'),
        ('10.3 DC principal (PDC)', 'Localiza el DC con rol PDC', 'netdom query pdc'),
        ('10.4 Roles FSMO', 'Todos los roles FSMO del dominio', 'netdom query fsmo'),
        ('10.5 Equipos del dominio', 'Lista equipos unidos al dominio', 'netdom query workstation'),
        ('10.6 Servidores del dominio', 'Lista servidores del dominio', 'netdom query server'),
        ('10.7 Info usuario AD', 'Detalles del usuario actual en AD', 'net user %USERNAME% /domain'),
        ('10.8 Grupos del usuario (AD)', 'Grupos AD del usuario actual', 'whoami /groups'),
        ('10.9 Grupos del dominio', 'Todos los grupos globales del dominio', 'net group /domain'),
        ('10.10 Admins del dominio', 'Miembros del grupo Domain Admins', 'net group "Administradores del dominio" /domain'),
        ('10.11 Unir equipo al dominio', 'Comando base para unir al dominio', 'netdom join %COMPUTERNAME% /domain:TUDOMINIO /userd:ADMIN /passwordd:*'),
        ('10.12 Expulsar del dominio', 'Elimina el equipo del dominio', 'netdom remove %COMPUTERNAME% /domain:TUDOMINIO /userd:ADMIN /passwordd:*'),
        ('10.13 Sincronizar hora con DC', 'Sincroniza el reloj con el dominio', 'w32tm /resync /force'),
        ('10.14 Estado sincronización hora', 'Diagnóstico de sincronización NTP', 'w32tm /query /status'),
        ('10.15 Política de grupo (gpupdate)', 'Fuerza actualización de GPOs', 'gpupdate /force'),
        ('10.16 Resultado GPO aplicada', 'GPOs aplicadas al usuario/equipo', 'gpresult /r'),
        ('10.17 Usuarios y Equipos AD', 'Consola ADUC (requiere RSAT)', 'dsa.msc'),
        ('10.18 DNS Manager', 'Consola DNS (requiere RSAT)', 'dnsmgmt.msc'),
        ('10.19 Sites y Servicios AD', 'Consola Sites and Services', 'dssite.msc'),
    ]},
    {"id": 'impresoras', "label": '🖨  Impresoras', "color": "#94a3b8",
     "cmds": [
        ('11.1 Lista de impresoras', 'Impresoras instaladas en el sistema', 'powershell -command \"Get-Printer | Select Name,PortName,PrinterStatus,Default | Format-Table -AutoSize\"'),
        ('11.2 Impresora predeterminada', 'Nombre de la impresora por defecto', 'powershell -command \"Get-Printer | Where-Object {$_.Default} | Select Name,PrinterStatus | Format-Table -AutoSize\"'),
        ('11.3 Estado de impresoras', 'Estado de todas las impresoras', 'powershell -command \"Get-Printer | Select Name,WorkOffline,PrinterStatus | Format-Table -AutoSize\"'),
        ('11.4 Cola de impresión', 'Trabajos pendientes de impresión', 'powershell -command \"Get-PrintJob -PrinterName * | Select PrinterName,Document,JobStatus | Format-Table -AutoSize\"'),
        ('11.5 Cancelar todos los trabajos', 'Limpia la cola de impresión', 'net stop spooler && net start spooler'),
        ('11.6 Reiniciar Spooler', 'Reinicia el servicio de impresión', 'net stop spooler && net start spooler'),
        ('11.7 Borrar caché spooler', 'Elimina trabajos atascados del spooler', 'cmd /c net stop spooler && del /q /f /s C:\\Windows\\System32\\spool\\PRINTERS\\* && net start spooler'),
        ('11.8 Panel de impresoras', 'Abre dispositivos e impresoras', 'control printers'),
        ('11.9 Gestor de impresión (GUI)', 'Print Management Console', 'printmanagement.msc'),
        ('11.10 Puertos de impresora', 'Lista los puertos de impresoras', 'powershell -command \"Get-PrinterPort | Select Name,PortType,Status | Format-Table -AutoSize\"'),
        ('11.11 Drivers de impresora', 'Drivers instalados de impresoras', 'powershell -command \"Get-PrinterDriver | Select Name,InfPath,DriverPath | Format-Table -AutoSize\"'),
        ('Exportar lista impresoras CSV',  'Exporta lista a CSV y abre Notepad',            'powershell -command \"Get-Printer | Select Name,PortName,PrinterStatus | Export-Csv impresoras.csv -NoTypeInformation -Encoding UTF8; Start-Process notepad impresoras.csv\"'),
        ('11.12 Exportar config impresoras', 'Backup completo impresoras con PrintBRM (Admin requerido)', r'C:\Windows\System32\spool\tools\PrintBRM.exe -B -F C:\impresoras_backup.printerExport'),
        ('11.13 Importar config impresoras', 'Restaurar backup impresoras con PrintBRM', r'C:\Windows\System32\spool\tools\PrintBRM.exe -R -F C:\impresoras_backup.printerExport'),
        ('Abrir asistente impresoras',      'GUI exportar/importar impresoras (printbrmui)',          'printbrmui.exe'),
    ]},
    {"id": 'windows_update', "label": '🔄  Windows Update', "color": BLUE,
     "cmds": [
        ('12.1 Buscar actualizaciones', 'Abre Windows Update', 'start ms-settings:windowsupdate'),
        ('12.2 Buscar actualizaciones (PS)', 'Fuerza busqueda de actualizaciones por PowerShell', 'powershell -command "& {Install-Module PSWindowsUpdate -Force -EA SilentlyContinue; Get-WindowsUpdate}"'),
        ('12.3 Instalar todas las updates', 'Descarga e instala todas las actualizaciones pendientes', 'powershell -command "Install-Module PSWindowsUpdate -Force -EA SilentlyContinue; Install-WindowsUpdate -AcceptAll -AutoReboot"'),
        ('12.4 Historial de actualizaciones', 'Lista las ultimas actualizaciones instaladas', 'powershell -command "Get-HotFix | Sort InstalledOn -Descending | Select HotFixID,Description,InstalledOn | Select -First 20 | Format-Table -AutoSize"'),
        ('12.5 Actualizaciones pendientes (PS)', 'Lista updates pendientes sin instalar', 'powershell -command "Get-WindowsUpdate -EA SilentlyContinue | Format-Table -AutoSize"'),
        ('12.6 Pausar WU 7 dias', 'Pausa Windows Update durante 7 dias', 'powershell -command "Set-ItemProperty HKLM:\\SOFTWARE\\Microsoft\\WindowsUpdate\\UX\\Settings PauseUpdatesExpiryTime ((Get-Date).AddDays(7).ToString(\'yyyy-MM-ddTHH:mm:ssZ\'))"'),
        ('12.7 Reanudar Windows Update', 'Quita la pausa de Windows Update', 'powershell -command "Remove-ItemProperty HKLM:\\SOFTWARE\\Microsoft\\WindowsUpdate\\UX\\Settings PauseUpdatesExpiryTime -EA SilentlyContinue"'),
        ('12.8 Reiniciar servicio WU', 'Detiene y reinicia el servicio de Windows Update', 'powershell -command "Stop-Service wuauserv,bits -Force; Start-Service wuauserv,bits; Write-Host WU reiniciado"'),
        ('12.9 Borrar cache de Windows Update', 'Limpia SoftwareDistribution y reinicia WU', 'powershell -command "Stop-Service wuauserv,bits -Force; Remove-Item ($env:windir+\'\\\\SoftwareDistribution\\\\Download\\\\*\') -Recurse -Force -EA SilentlyContinue; Start-Service wuauserv,bits; Write-Host Cache WU limpiada"'),
        ('12.10 Desactivar actualizaciones auto', 'Deshabilita Windows Update automatico (GPO)', 'powershell -command "New-ItemProperty HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate\\AU AUOptions -Type DWord -Value 1 -Force; Write-Host WU automatico desactivado"'),
        ('12.11 Activar actualizaciones auto', 'Reactiva Windows Update automatico', 'powershell -command "Remove-ItemProperty HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate\\AU AUOptions -EA SilentlyContinue; Write-Host WU automatico reactivado"'),
        ('12.12 Hotfixes instalados (lista)', 'Todos los parches KB instalados en el sistema', 'wmic qfe list brief /format:table'),
        ('12.13 Configuracion Windows Update', 'Panel de configuracion de Windows Update', 'start ms-settings:windowsupdate-options'),
    ]},
    {"id": 'rdp', "label": '🖥  RDP / Remoto', "color": PURPLE,
     "cmds": [
        ('13.1 Habilitar RDP', 'Activa el escritorio remoto en este equipo', 'powershell -command "Set-ItemProperty \'HKLM:\\System\\CurrentControlSet\\Control\\Terminal Server\' fDenyTSConnections 0; Enable-NetFirewallRule -DisplayGroup \'Remote Desktop\'; Write-Host RDP habilitado"'),
        ('13.2 Deshabilitar RDP', 'Desactiva el escritorio remoto', 'powershell -command "Set-ItemProperty \'HKLM:\\System\\CurrentControlSet\\Control\\Terminal Server\' fDenyTSConnections 1; Write-Host RDP deshabilitado"'),
        ('13.3 Estado RDP', 'Comprueba si RDP esta habilitado', 'powershell -command "$v=(Get-ItemProperty \'HKLM:\\System\\CurrentControlSet\\Control\\Terminal Server\').fDenyTSConnections; if($v -eq 0){Write-Host RDP: HABILITADO -ForegroundColor Green}else{Write-Host RDP: DESHABILITADO -ForegroundColor Red}"'),
        ('13.4 Ver sesiones activas RDP', 'Lista todas las sesiones de usuario activas', 'query session'),
        ('13.5 Ver usuarios conectados', 'Usuarios con sesion abierta en el equipo', 'query user'),
        ('13.6 Conectar por RDP a equipo', 'Abre el cliente RDP (mstsc)', 'mstsc'),
        ('13.7 Cerrar sesion RDP por ID', 'Cierra una sesion por su ID (logoff ID)', 'logoff'),
        ('13.8 Puerto RDP actual', 'Muestra el puerto configurado para RDP', 'powershell -command "(Get-ItemProperty \'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server\\WinStations\\RDP-Tcp\').PortNumber"'),
        ('13.9 Cambiar puerto RDP a 3389', 'Restaura el puerto RDP al valor por defecto', 'powershell -command "Set-ItemProperty \'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server\\WinStations\\RDP-Tcp\' PortNumber 3389; Write-Host Puerto RDP: 3389"'),
        ('13.10 Firewall — abrir puerto RDP', 'Abre el puerto 3389 en el firewall', 'powershell -command "New-NetFirewallRule -DisplayName RDP-3389 -Direction Inbound -Protocol TCP -LocalPort 3389 -Action Allow -EA SilentlyContinue; Write-Host Puerto 3389 abierto"'),
        ('13.11 Configuracion acceso remoto', 'Panel de acceso remoto de Windows', 'SystemPropertiesRemote.exe'),
        ('13.12 Credenciales guardadas RDP', 'Gestiona credenciales almacenadas', 'rundll32.exe keymgr.dll,KRShowKeyMgr'),
        ('13.13 Timeouts RDP idle=30 disc=60 active=480', 'Aplica timeouts: inactivo=30min desconectado=60min activo=8h EndOnLimit=On', 'cmd /c reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server\\WinStations\\RDP-Tcp" /v MaxIdleTime /t REG_DWORD /d 1800000 /f && reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server\\WinStations\\RDP-Tcp" /v MaxDisconnectionTime /t REG_DWORD /d 3600000 /f && reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server\\WinStations\\RDP-Tcp" /v MaxConnectionTime /t REG_DWORD /d 28800000 /f && reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server\\WinStations\\RDP-Tcp" /v fResetBroken /t REG_DWORD /d 1 /f && echo Timeouts RDP aplicados: idle=30 disc=60 active=480 EndOnLimit=On && echo Ejecuta gpupdate /force para aplicar del todo'),
    ]},
    {"id": 'inventario', "label": '📦  Inventario', "color": ORANGE,
     "cmds": [
        ('14.1 Inventario hardware completo', 'CPU, RAM, disco, GPU, placa, BIOS en un informe', 'powershell -command "Get-CimInstance Win32_ComputerSystem,Win32_Processor,Win32_PhysicalMemory,Win32_DiskDrive,Win32_VideoController,Win32_BaseBoard,Win32_BIOS | Format-List *"'),
        ('14.2 Software instalado (lista)', 'Todos los programas instalados con version', 'powershell -command "Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select DisplayName,DisplayVersion,Publisher,InstallDate | Sort DisplayName | Format-Table -AutoSize"'),
        ('14.3 Software instalado (32bit)', 'Programas de 32 bits en sistema 64 bits', 'powershell -command "Get-ItemProperty HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select DisplayName,DisplayVersion,Publisher | Sort DisplayName | Format-Table -AutoSize"'),
        ('14.4 Exportar software a CSV', 'Guarda lista de programas en el escritorio', 'powershell -command "Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select DisplayName,DisplayVersion,Publisher,InstallDate | Sort DisplayName | Export-Csv ($env:USERPROFILE+\'\\\\Desktop\\\\software.csv\') -NoTypeInformation -Encoding UTF8; Write-Host Exportado a Desktop\\\\software.csv"'),
        ('14.5 Drivers instalados', 'Lista todos los drivers del sistema', 'powershell -command "Get-WindowsDriver -Online | Select Driver,ClassName,Version,Date | Format-Table -AutoSize"'),
        ('14.6 Drivers firmados (driverquery)', 'Lista drivers con estado y firma', 'driverquery /v /fo table'),
        ('14.7 Hotfixes instalados', 'Parches KB con fecha de instalacion', 'powershell -command "Get-HotFix | Sort InstalledOn -Descending | Select HotFixID,Description,InstalledOn | Format-Table -AutoSize"'),
        ('14.8 Exportar hotfixes a CSV', 'Guarda parches KB en CSV en el escritorio', 'powershell -command "Get-HotFix | Sort InstalledOn -Descending | Export-Csv ($env:USERPROFILE+\'\\\\Desktop\\\\hotfixes.csv\') -NoTypeInformation -Encoding UTF8; Write-Host Exportado"'),
        ('14.9 Exportar hardware a TXT', 'Informe completo de hardware en el escritorio', 'powershell -command "$f=$env:USERPROFILE+\'\\\\Desktop\\\\hardware_\'+(Get-Date -f yyyyMMdd_HHmmss)+\'.txt\'; Get-CimInstance Win32_ComputerSystem,Win32_Processor,Win32_PhysicalMemory,Win32_DiskDrive,Win32_VideoController | Format-List * | Out-File $f -Encoding UTF8; Start-Process notepad $f; Write-Host Exportado: $f"'),
        ('14.10 Servicios instalados', 'Lista todos los servicios del sistema', 'powershell -command "Get-Service | Select Name,DisplayName,Status,StartType | Sort Status | Format-Table -AutoSize"'),
        ('14.11 Tareas programadas activas', 'Muestra tareas del programador activas', 'powershell -command "Get-ScheduledTask | Where State -ne Disabled | Select TaskName,TaskPath,State | Format-Table -AutoSize"'),
        ('14.12 msinfo32 — Info del sistema', 'Herramienta nativa de informacion de sistema', 'msinfo32'),
    ]},
    {"id": 'dns', "label": '🌍  DNS / Puertos', "color": GREEN,
     "cmds": [
        ('15.1 nslookup dominio', 'Resolucion DNS de un dominio (edita el comando)', 'nslookup google.com'),
        ('15.2 Test DNS rapido (8.8.8.8)', 'Resolucion usando Google DNS', 'nslookup google.com 8.8.8.8'),
        ('15.3 Test DNS Cloudflare (1.1.1.1)', 'Resolucion usando Cloudflare DNS', 'nslookup google.com 1.1.1.1'),
        ('15.4 Registros MX de dominio', 'Consulta registros de correo de un dominio', 'powershell -command "Resolve-DnsName google.com -Type MX | Format-Table"'),
        ('15.5 Registros A de dominio', 'Consulta IPs de un dominio', 'powershell -command "Resolve-DnsName google.com -Type A | Format-Table"'),
        ('15.6 Limpiar cache DNS', 'Vacia la cache DNS local', 'ipconfig /flushdns'),
        ('15.7 Ver cache DNS local', 'Muestra entradas en cache DNS del sistema', 'ipconfig /displaydns'),
        ('15.8 Test puerto TCP (Test-NetConn)', 'Comprueba si un puerto esta abierto', 'powershell -command "Test-NetConnection -ComputerName google.com -Port 443 | Select ComputerName,RemotePort,TcpTestSucceeded | Format-List"'),
        ('15.9 Escanear puertos locales abiertos', 'Lista puertos TCP en escucha', 'powershell -command "Get-NetTCPConnection -State Listen | Select LocalAddress,LocalPort,OwningProcess | Sort LocalPort | Format-Table -AutoSize"'),
        ('15.10 Tracert a Google', 'Traza la ruta hasta Google', 'tracert google.com'),
        ('15.11 Ruta IP (route print)', 'Tabla de enrutamiento del sistema', 'route print'),
        ('15.12 IP publica (via PS)', 'Obtiene la IP publica actual', 'powershell -command "(Invoke-RestMethod -Uri \'https://api.ipify.org?format=json\' -TimeoutSec 5).ip"'),
        ('15.13 Conexiones activas (netstat)', 'Conexiones TCP/UDP activas con procesos', 'netstat -abno'),
        ('15.14 Estadisticas de red', 'Estadisticas TCP/IP del adaptador', 'netstat -s'),
        ('15.15 Configuracion DNS adaptadores', 'DNS asignado a cada adaptador de red', 'powershell -command "Get-DnsClientServerAddress | Select InterfaceAlias,AddressFamily,ServerAddresses | Format-Table -AutoSize"'),
        ('15.16 Cambiar DNS a Google (8.8.8.8)', 'Establece Google DNS en todos los adaptadores', 'powershell -command "Get-NetAdapter | Where Status -eq Up | ForEach {Set-DnsClientServerAddress -InterfaceIndex $_.ifIndex -ServerAddresses 8.8.8.8,8.8.4.4}; Write-Host DNS cambiado a Google"'),
        ('15.17 Cambiar DNS a Cloudflare', 'Establece Cloudflare DNS (1.1.1.1)', 'powershell -command "Get-NetAdapter | Where Status -eq Up | ForEach {Set-DnsClientServerAddress -InterfaceIndex $_.ifIndex -ServerAddresses 1.1.1.1,1.0.0.1}; Write-Host DNS cambiado a Cloudflare"'),
        ('15.18 Restablecer DNS automatico', 'Vuelve a DNS por DHCP en todos los adaptadores', 'powershell -command "Get-NetAdapter | Where Status -eq Up | ForEach {Set-DnsClientServerAddress -InterfaceIndex $_.ifIndex -ResetServerAddresses}; Write-Host DNS restablecido a DHCP"'),
    ]},
    {"id": 'reparaciones', "label": '🔧  Reparaciones', "color": RED,
     "cmds": [
        ('16.1 DISM + SFC seguidos', 'Repara imagen y archivos del sistema en secuencia', 'powershell -command "dism /Online /Cleanup-Image /RestoreHealth; sfc /scannow"'),
        ('16.2 DISM — RestoreHealth', 'Repara imagen de Windows (solo DISM)', 'DISM /Online /Cleanup-Image /RestoreHealth'),
        ('16.3 SFC — Escanear sistema', 'Verifica y repara archivos protegidos', 'sfc /scannow'),
        ('16.4 Reparar Windows Update', 'Para WU, borra cache y reinicia servicios', 'powershell -command "Stop-Service wuauserv,bits,cryptSvc -Force; Remove-Item ($env:windir+\'\\\\SoftwareDistribution\') -Recurse -Force -EA SilentlyContinue; Start-Service wuauserv,bits,cryptSvc; Write-Host WU OK"'),
        ('16.5 Reparar red completa', 'Winsock + TCP/IP + DHCP + DNS + ARP', 'cmd /c netsh winsock reset && netsh int ip reset && ipconfig /release && ipconfig /renew && ipconfig /flushdns'),
        ('16.6 Reiniciar spooler impresion', 'Limpia cola y reinicia servicio de impresion', 'powershell -command "Stop-Service spooler -Force; Remove-Item ($env:windir+\'\\\\System32\\\\spool\\\\PRINTERS\\\\*\') -Force -EA SilentlyContinue; Start-Service spooler; Write-Host Spooler OK"'),
        ('16.7 Limpiar TEMP + Prefetch', 'Borra archivos temporales y prefetch', 'cmd /c del /q /f /s "%TEMP%\\*" && del /q /f /s "C:\\Windows\\Temp\\*" && del /q /f /s "C:\\Windows\\Prefetch\\*"'),
        ('16.8 Reparar arranque BCD', 'bootrec rebuildbcd + fixmbr + fixboot', 'cmd /c bootrec /fixmbr && bootrec /fixboot && bootrec /rebuildbcd'),
        ('16.9 Forzar chkdsk C: al arranque', 'Programa verificacion de disco en reinicio', 'chkdsk C: /f /r /x'),
        ('16.10 Limpiar DNS + cache ARP', 'Limpia DNS local y tabla ARP', 'cmd /c ipconfig /flushdns && arp -d *'),
        ('16.11 Vaciar Papelera (silencioso)', 'Vacia la papelera sin confirmacion', 'powershell -command "Clear-RecycleBin -Force -EA SilentlyContinue; Write-Host Papelera vaciada"'),
        ('16.12 Reinstalar tienda Windows', 'Reinstala Microsoft Store y apps base', 'powershell -command "Get-AppxPackage -AllUsers Microsoft.WindowsStore | ForEach {Add-AppxPackage -DisableDevelopmentMode -Register ($_.InstallLocation+\'\\\\AppXManifest.xml\')}"'),
    ]},
    {"id": 'optimizacion', "label": '⚡  Optimización', "color": LIME,
     "cmds": [
        ('17.1 Plan maximo rendimiento', 'Activa High Performance', 'powercfg /setactive SCHEME_MIN'),
        ('17.2 Plan equilibrado', 'Vuelve al plan Balanced por defecto', 'powercfg /setactive SCHEME_BALANCED'),
        ('17.3 Plan ahorro energia', 'Activa plan Power Saver', 'powercfg /setactive SCHEME_MAX'),
        ('17.4 Desactivar SysMain/Superfetch', 'Recomendable en SSD', 'powershell -command "Stop-Service SysMain -Force; Set-Service SysMain -StartupType Disabled; Write-Host SysMain desactivado"'),
        ('17.5 Activar SysMain/Superfetch', 'Reactiva Superfetch para HDD', 'powershell -command "Set-Service SysMain -StartupType Automatic; Start-Service SysMain; Write-Host SysMain activado"'),
        ('17.6 Efectos visuales rendimiento', 'Modo mejor rendimiento sin animaciones', 'powershell -command "Set-ItemProperty \'HKCU:\\\\Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Explorer\\\\VisualEffects\' VisualFXSetting 2"'),
        ('17.7 Efectos visuales apariencia', 'Restaura efectos visuales completos', 'powershell -command "Set-ItemProperty \'HKCU:\\\\Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Explorer\\\\VisualEffects\' VisualFXSetting 1"'),
        ('17.8 Desactivar telemetria', 'Para DiagTrack y dmwappushservice', 'powershell -command "Stop-Service DiagTrack,dmwappushservice -Force; Set-Service DiagTrack,dmwappushservice -StartupType Disabled; Write-Host Telemetria desactivada"'),
        ('17.9 Activar TRIM SSD', 'Habilita TRIM en todas las unidades', 'fsutil behavior set DisableDeleteNotify 0'),
        ('17.10 God Mode en escritorio', 'Carpeta con todos los ajustes avanzados', 'powershell -command "$d=[Environment]::GetFolderPath(\'Desktop\'); New-Item -Path ($d+\'\\\\GodMode.{ED7BA470-8E54-465E-825C-99712043E01C}\') -ItemType Directory -EA SilentlyContinue; Write-Host God Mode creado"'),
        ('17.11 Prioridad primer plano', 'Mas recursos a la app activa', 'powershell -command "Set-ItemProperty \'HKLM:\\\\SYSTEM\\\\CurrentControlSet\\\\Control\\\\PriorityControl\' Win32PrioritySeparation 38"'),
        ('17.12 Apps en inicio de Windows', 'Gestiona que apps arrancan con Windows', 'start ms-settings:startupapps'),
        ('17.13 Opciones de energia', 'Panel de configuracion de energia', 'powercfg.cpl'),
    ]},
    {"id": 'tests', "label": '🧪  Tests & Diagnóstico', "color": PURPLE,
     "cmds": [
        ('18.1 Test RAM — reiniciar ahora', 'Diagnostico completo de memoria (requiere reinicio)', 'mdsched.exe'),
        ('18.2 Test RAM — programar arranque', 'Programa el test en el proximo inicio sin reiniciar ya', 'mdsched.exe /s'),
        ('18.3 Resultado ultimo test RAM', 'Lee el resultado del ultimo test de memoria en el sistema', 'powershell -command "Get-WinEvent -LogName System | Where {$_.Id -eq 1101 -or $_.Id -eq 1102} | Select -First 5 | Format-List TimeCreated,Message"'),
        ('18.4 WinSAT — Benchmark completo', 'Test oficial Microsoft: CPU+RAM+disco+graficos (~5 min)', 'winsat formal'),
        ('18.5 WinSAT — solo CPU', 'Benchmark solo del procesador', 'winsat cpu'),
        ('18.6 WinSAT — solo RAM', 'Benchmark solo de la memoria', 'winsat mem'),
        ('18.7 WinSAT — solo disco C:', 'Benchmark velocidad disco C:', 'winsat disk -drive c'),
        ('18.8 WinSAT — solo graficos 3D', 'Benchmark DirectX/3D de la GPU', 'winsat d3d'),
        ('18.9 Ver puntuacion WinSAT (ultima)', 'Muestra el ultimo resultado sin volver a medir', 'powershell -command "Get-CimInstance Win32_WinSAT | Format-List"'),
        ('18.10 DxDiag — ventana completa', 'Info GPU, DirectX, audio y drivers', 'dxdiag'),
        ('18.11 DxDiag — exportar TXT escritorio', 'Genera informe DxDiag sin abrir ventana', 'dxdiag /t %USERPROFILE%\\Desktop\\dxdiag_informe.txt'),
        ('18.12 Info GPU (nombre y driver)', 'Datos de tarjeta grafica, driver y resolucion', 'powershell -command "Get-CimInstance Win32_VideoController | Select Name,DriverVersion,VideoModeDescription,CurrentRefreshRate | Format-List"'),
        ('18.13 GPU uso en tiempo real', 'Abre el Administrador de tareas en pestana GPU', 'taskmgr'),
        ('18.14 SMART estado discos', 'Estado de salud de discos fisicos', 'powershell -command "Get-PhysicalDisk | Select FriendlyName,HealthStatus,OperationalStatus,@{n=\'Size(GB)\';e={[math]::Round($_.Size/1GB,0)}} | Format-Table -AutoSize"'),
        ('18.15 Test velocidad disco C: (WinSAT)', 'Velocidad real de lectura/escritura en disco C:', 'winsat disk -drive c'),
        ('18.16 Informe rendimiento (60 seg)', 'Analisis de 60s y genera informe HTML completo', 'perfmon /report'),
        ('18.17 Monitor de confiabilidad', 'Historial de errores y eventos del sistema', 'perfmon /rel'),
        ('18.18 Informe energia (perfmon)', 'Detecta problemas energeticos, genera HTML', 'powercfg /energy'),
        ('18.19 Informe bateria (portatiles)', 'Estado y degradacion de la bateria', 'powercfg /batteryreport /output %USERPROFILE%\\Desktop\\bateria.html && start %USERPROFILE%\\Desktop\\bateria.html'),
        ('18.20 Info hardware completo (msinfo32)', 'Toda la informacion de hardware en una ventana', 'msinfo32'),
        ('18.21 Monitor de rendimiento (GUI)', 'Abre el monitor de rendimiento de Windows', 'perfmon'),
        ('18.22 Administrador de tareas', 'Procesos, CPU, RAM, disco, red y GPU en tiempo real', 'taskmgr'),
    ]},
    {"id": 'powershell', "label": '💡  PowerShell', "color": LIME,
     "cmds": [
        ('19.1 Versión PowerShell', 'Versión instalada de PS', 'powershell -command "$PSVersionTable.PSVersion"'),
        ('19.2 Procesos top RAM', 'Top 10 procesos por uso de RAM', 'powershell -command "Get-Process | Sort-Object WorkingSet -Desc | Select -First 10 | ft Name,Id,CPU,WorkingSet -Auto"'),
        ('19.3 Política de ejecución', 'Política actual de scripts PS', 'powershell -command "Get-ExecutionPolicy -List"'),
        ('19.4 Habilitar scripts PS', 'Permite scripts no firmados', 'powershell -command "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"'),
        ('19.5 Servicios activos', 'Lista servicios en estado Running', 'powershell -command "Get-Service | Where {$_.Status -eq \'Running\'} | Sort Name | ft -Auto"'),
        ('19.6 Config red completa', 'Adaptadores y configuración IP', 'powershell -command "Get-NetIPConfiguration | Format-List"'),
        ('19.7 Últimos 20 errores sistema', 'Errores del log del sistema', 'powershell -command "Get-EventLog -LogName System -EntryType Error -Newest 20 | ft TimeGenerated,Source,Message -Auto"'),
        ('19.8 Usuarios locales (PS)', 'Get-LocalUser con último acceso', 'powershell -command "Get-LocalUser | ft Name,Enabled,LastLogon -Auto"'),
        ('19.9 Info discos físicos (PS)', 'Tipo y tamaño de discos físicos', 'powershell -command "Get-PhysicalDisk | ft FriendlyName,MediaType,Size -Auto"'),
        ('19.10 Actualizaciones instaladas', 'Historial de actualizaciones de Windows', 'powershell -command "Get-HotFix | Sort-Object InstalledOn -Desc | Select -First 20 | ft HotFixID,Description,InstalledOn -Auto"'),
    ]},
]

CTRL_PANEL = {
    'sistema':    ('⚙ Configuración',     'start ms-settings:'),
    'discos':     ('💾 Gestión de discos', 'diskmgmt.msc'),
    'red':        ('🌐 Conexiones de red', 'ncpa.cpl'),
    'usuarios':   ('👤 Cuentas usuario',   'ms-settings:accounts'),
    'procesos':   ('📊 Administrador',     'taskmgr'),
    'boot':       ('🚀 msconfig',          'msconfig'),
    'registro':   ('📝 Regedit',           'regedit'),
    'seguridad':  ('🔒 Seguridad',         'ms-settings:windowsdefender'),
    'ad':         ('🏢 Usuarios AD',       'dsa.msc'),
    'impresoras': ('🖨 Impresoras',        'ms-settings:printers'),
    'windows_update': ('🔄 Windows Update', 'start ms-settings:windowsupdate'),
    'rdp':            ('🖥 Acceso remoto',   'SystemPropertiesRemote.exe'),
    'inventario':     ('📦 msinfo32',         'msinfo32'),
    'dns':            ('🌍 Conexiones red',   'ncpa.cpl'),
    'reparaciones': ('🔧 Herramientas Windows', 'ms-settings:'),
    'optimizacion': ('⚡ Opciones de energía', 'powercfg.cpl'),
    'tests':      ('🧪 Diagnóstico Windows', 'perfmon'),
    'powershell': ('💡 PowerShell ISE',    'powershell_ise'),
}

# ══════════════════════════════════════════════════════════════
# VENTANA DE LOGIN
# ══════════════════════════════════════════════════════════════
class Tooltip:
    def __init__(self, widget, text):
        self.widget=widget; self.text=text; self.tw=None
        widget.bind("<Enter>", self._show); widget.bind("<Leave>", self._hide)
    def _show(self, e=None):
        x=self.widget.winfo_rootx()+10; y=self.widget.winfo_rooty()+self.widget.winfo_height()+4
        self.tw=tk.Toplevel(self.widget); self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry(f"+{x}+{y}"); self.tw.attributes("-topmost",True)
        tk.Label(self.tw,text=self.text,bg="#1e2a3a",fg=TEXT,font=("Segoe UI",8),padx=8,pady=4).pack()
    def _hide(self, e=None):
        if self.tw: self.tw.destroy(); self.tw=None

class SplashScreen:
    def __init__(self):
        self.root=tk.Tk(); self.root.overrideredirect(True)
        self.root.configure(bg=BG, highlightthickness=2, highlightbackground=CYAN)
        w,h=420,220; sw=self.root.winfo_screenwidth(); sh=self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        self.root.attributes("-topmost",True)
        tk.Label(self.root,text="🛠",bg=BG,fg=CYAN,font=("Segoe UI",38)).pack(pady=(26,4))
        tk.Label(self.root,text="IT Tools",bg=BG,fg=CYAN,font=("Segoe UI",22,"bold")).pack()
        tk.Label(self.root,text="by Oscarcierzo  ·  2026",bg=BG,fg=MUTED,font=("Segoe UI",9)).pack(pady=(2,14))
        self.bf=tk.Frame(self.root,bg=SURFACE2,height=4); self.bf.pack(fill="x",padx=40)
        self.bar=tk.Frame(self.bf,bg=CYAN,height=4,width=0); self.bar.place(x=0,y=0,relheight=1)
        self._p=0; self._animate()
    def _animate(self):
        self._p=min(self._p+3,100); w=self.bf.winfo_width() or 340
        self.bar.place_configure(width=int(w*self._p/100))
        if self._p<100: self.root.after(18,self._animate)
        else: self.root.after(250,self.root.destroy)
    def show(self): self.root.mainloop()


class LoginWindow:
    def __init__(self, root=None):
        self.ok = False
        self.attempts = 0
        self.root = root if root else tk.Tk()
        self.root.title("IT Tools — Acceso")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        self.root.geometry("400x320")
        self.root.eval('tk::PlaceWindow . center')
        self.root.overrideredirect(True)   # sin borde
        self._build()
        self.root.bind("<Return>", lambda e: self._login())
        # Mover ventana arrastrando
        self.root.bind("<ButtonPress-1>",   self._drag_start)
        self.root.bind("<B1-Motion>",        self._drag_move)

    def _drag_start(self, e):
        self._dx = e.x; self._dy = e.y
    def _drag_move(self, e):
        x = self.root.winfo_x() + e.x - self._dx
        y = self.root.winfo_y() + e.y - self._dy
        self.root.geometry(f"+{x}+{y}")

    def _build(self):
        # Barra superior
        bar = tk.Frame(self.root, bg=SURFACE, height=32)
        bar.pack(fill="x")
        tk.Label(bar, text="IT Tools", bg=SURFACE, fg=CYAN,
                 font=FONT_MB).pack(side="left", padx=12, pady=6)
        tk.Button(bar, text="✕", bg=SURFACE, fg=MUTED, bd=0, cursor="hand2",
                  font=FONT_B, activebackground=RED, activeforeground="white",
                  command=self.root.destroy).pack(side="right", padx=8, pady=4)

        # Cuerpo
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=30, pady=20)

        tk.Label(body, text="🖥", bg=BG, font=("Segoe UI Emoji", 36)).pack(pady=(10,4))
        tk.Label(body, text="Centro de Comandos IT", bg=BG, fg=TEXT, font=FONT_LG).pack()
        tk.Label(body, text="by Oscarcierzo", bg=BG, fg=MUTED, font=FONT_XS).pack(pady=(0,16))

        # Campo contraseña
        pw_frame = tk.Frame(body, bg=SURFACE2, highlightbackground=BORDER, highlightthickness=1)
        pw_frame.pack(fill="x", pady=(0,10))
        tk.Label(pw_frame, text="🔑", bg=SURFACE2, fg=MUTED, font=FONT).pack(side="left", padx=8)
        self.pwd_var = tk.StringVar()
        self.pwd_entry = tk.Entry(pw_frame, textvariable=self.pwd_var, show="●",
                                  bg=SURFACE2, fg=TEXT, insertbackground=CYAN,
                                  relief="flat", font=FONT, bd=4)
        self.pwd_entry.pack(side="left", fill="x", expand=True, pady=6, padx=(0,8))
        self.pwd_entry.focus()

        # Botón entrar
        tk.Button(body, text="  Entrar al sistema  ", bg=CYAN, fg="#000",
                  font=FONT_B, relief="flat", cursor="hand2", bd=0,
                  activebackground="#0096b4", activeforeground="#000",
                  command=self._login).pack(fill="x", ipady=6)

        # Error
        self.err_lbl = tk.Label(body, text="", bg=BG, fg=RED, font=FONT_XS)
        self.err_lbl.pack(pady=(8,0))

        tk.Label(body, text="v1.0.0 · 2026", bg=BG, fg="#2d3a50", font=FONT_XS).pack(side="bottom", pady=4)

    def _login(self):
        pwd = self.pwd_var.get()
        h = hashlib.sha256(pwd.encode('utf-8')).hexdigest()
        if h == PWD_HASH:
            self.ok = True
            self.root.withdraw()
            self.root.quit()
        else:
            self.attempts += 1
            msg = "⛔ Demasiados intentos" if self.attempts >= 3 else "❌ Contraseña incorrecta"
            self.err_lbl.config(text=msg)
            self.pwd_var.set("")
            self.pwd_entry.focus()
            self.root.after(3000, lambda: self.err_lbl.config(text=""))


    # ── EXPORTAR / IMPORTAR ───────────────────────────────────
    def _export_cmds(self):
        from tkinter import filedialog
        all_cmds = {
            "version": "1.0",
            "custom_commands": self.custom_cmds
        }
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json"), ("Todos", "*.*")],
            title="Exportar comandos personalizados",
            initialfile="wincmd_ricma_comandos.json"
        )
        if path:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(all_cmds, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Exportado", f"Comandos exportados a:\n{path}")

    def _import_cmds(self):
        from tkinter import filedialog
        path = filedialog.askopenfilename(
            filetypes=[("JSON", "*.json"), ("Todos", "*.*")],
            title="Importar comandos personalizados"
        )
        if not path:
            return
        try:
            with open(path, encoding='utf-8') as f:
                data = json.load(f)
            imported = data.get("custom_commands", [])
            if not isinstance(imported, list):
                raise ValueError("Formato incorrecto")
            added = 0
            for c in imported:
                if c not in self.custom_cmds:
                    self.custom_cmds.append(c)
                    added += 1
            self._save_custom()
            self._select_cat(self.current_cat)
            messagebox.showinfo("Importado", f"Se importaron {added} comandos nuevos.")
        except Exception as ex:
            messagebox.showerror("Error", f"No se pudo importar:\n{ex}")

    def run(self):
        self.root.deiconify()
        self.root.mainloop()
        return self.ok


# ══════════════════════════════════════════════════════════════
# APLICACIÓN PRINCIPAL
# ══════════════════════════════════════════════════════════════
class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("IT Tools — Centro de Comandos IT  v1.3")
        self.root.configure(bg=BG)
        self.root.geometry("1280x800")
        self.root.minsize(960, 640)
        self.root.eval('tk::PlaceWindow . center')

        # Configurar estilos ttk
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Vertical.TScrollbar",
                        background=SURFACE2, troughcolor=BG,
                        arrowcolor=MUTED, bordercolor=BG, lightcolor=SURFACE2)
        style.configure("TEntry", fieldbackground=SURFACE2, foreground=TEXT,
                        insertcolor=CYAN, bordercolor=BORDER)

        self.current_cat = 0
        self.search_var  = tk.StringVar()
        self.search_var.trace_add("write", self._on_search)

        # Inicializar listas ANTES de _build_ui para evitar AttributeError
        self.favs        = []
        self.history     = []
        self.custom_cmds = []

        # Rutas de persistencia
        self.custom_file  = Path(__file__).parent / "custom_commands.json"
        self.favs_file    = Path(__file__).parent / "favoritos.json"
        self.history_file = Path(__file__).parent / "historial.json"

        # Cargar datos del disco
        self.custom_cmds = self._load_custom()
        self._load_favs()
        self._load_history()

        self._build_ui()
        self._select_cat(0)

        # Cerrar con X
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

    # ── Persistencia comandos personalizados ───────────────────
    def _custom_file(self):
        base = os.environ.get('APPDATA', os.path.expanduser('~'))
        return os.path.join(base, 'wincmd_ricma_custom.json')


    def _load_favs(self):
        """Carga favoritos desde JSON y actualiza FAVORITES_CAT."""
        try:
            if self.favs_file.exists():
                self.favs = json.load(open(self.favs_file, encoding='utf-8'))
            else:
                self.favs = []
        except Exception:
            self.favs = []
        self._rebuild_favs_cat()

    def _save_favs(self):
        try:
            json.dump(self.favs, open(self.favs_file, 'w', encoding='utf-8'),
                      ensure_ascii=False, indent=2)
        except Exception:
            pass
        self._rebuild_favs_cat()
        # Actualizar contador total
        if hasattr(self, 'total_lbl'):
            total = sum(len(c["cmds"]) for c in CATEGORIES) + len(self.custom_cmds)
            self.total_lbl.config(text=f"· {total} comandos totales")

    def _rebuild_favs_cat(self):
        """Reconstruye la lista de cmds en FAVORITES_CAT y actualiza sidebar."""
        FAVORITES_CAT["cmds"].clear()
        for f in self.favs:
            FAVORITES_CAT["cmds"].append((f["name"], f["desc"], f["cmd"]))
        # Insertar/retirar del listado de categorías
        had_favs = FAVORITES_CAT in CATEGORIES
        if had_favs:
            CATEGORIES.remove(FAVORITES_CAT)
        if FAVORITES_CAT["cmds"]:
            CATEGORIES.insert(0, FAVORITES_CAT)
        # Solo reconstruir botones si cambió la presencia de la categoría favoritos
        has_favs = FAVORITES_CAT in CATEGORIES
        if hasattr(self, 'cat_btns') and had_favs != has_favs:
            self._rebuild_cat_buttons()
        elif hasattr(self, 'cat_btns'):
            # Solo actualizar textos y colores sin destruir
            for i, (btn, cat) in enumerate(zip(self.cat_btns, CATEGORIES)):
                btn.config(text=f"  {cat['label']}")

    def _rebuild_cat_buttons(self):
        """Destruye solo los botones de categoría y los recrea."""
        for btn in self.cat_btns:
            btn.destroy()
        self.cat_btns = []
        # Insertar botones justo después del label CATEGORÍAS (índice 0 en sidebar)
        # Encontrar la posición de referencia — el separador de acciones
        sep = None
        for w in self.sidebar.winfo_children():
            if isinstance(w, tk.Frame) and w.cget("height") == 1:
                sep = w
                break
        for i, cat in enumerate(CATEGORIES):
            btn = tk.Button(
                self.sidebar,
                text=f"  {cat['label']}  {len(cat['cmds'])}",
                bg=SURFACE, fg=MUTED, font=FONT,
                relief="flat", bd=0, anchor="w",
                cursor="hand2", activebackground=SURFACE2,
                command=lambda idx=i: self._select_cat(idx)
            )
            if sep:
                btn.pack(fill="x", ipady=5, padx=4, before=sep)
            else:
                btn.pack(fill="x", ipady=5, padx=4)
            self.cat_btns.append(btn)
        idx = min(self.current_cat, len(CATEGORIES) - 1)
        self._select_cat(idx)

    def _is_fav(self, cmd):
        return any(f["cmd"] == cmd for f in self.favs)

    def _toggle_fav(self, name, desc, cmd):
        if self._is_fav(cmd):
            self.favs = [f for f in self.favs if f["cmd"] != cmd]
        else:
            self.favs.append({"name": name, "desc": desc, "cmd": cmd})
        self._save_favs()
        # Re-renderizar la categoría actual sin cambiar de categoría
        q = self.search_var.get() if hasattr(self, 'search_var') else ""
        if q in ("", "Buscar comandos…"):
            self._render_cards("")
        else:
            self._render_cards(q)


    # ── HISTORIAL ──────────────────────────────────────────────
    def _load_history(self):
        try:
            if self.history_file.exists():
                self.history = json.load(open(self.history_file, encoding='utf-8'))
            else:
                self.history = []
        except Exception:
            self.history = []

    def _save_history(self):
        try:
            json.dump(self.history, open(self.history_file, 'w', encoding='utf-8'),
                      ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _add_to_history(self, name, cmd, status="ejecutado"):
        from datetime import datetime
        entry = {
            "ts":     datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name":   name,
            "cmd":    cmd,
            "status": status
        }
        self.history.insert(0, entry)
        self.history = self.history[:200]   # máximo 200 entradas
        self._save_history()
        # Actualizar badge del botón historial si existe
        if hasattr(self, 'hist_btn'):
            self.hist_btn.config(text=f"📋 Historial ({len(self.history)})")

    def _show_history(self):
        """Ventana flotante con el historial de ejecuciones."""
        hw = tk.Toplevel(self.root)
        hw.title("Historial de ejecuciones — IT Tools")
        hw.configure(bg=BG)
        hw.geometry("750x500")
        hw.resizable(True, True)

        # Barra superior
        bar = tk.Frame(hw, bg=SURFACE2, height=40)
        bar.pack(fill="x")
        tk.Label(bar, text="📋  Historial de ejecuciones", bg=SURFACE2,
                 fg=CYAN, font=FONT_B).pack(side="left", padx=12, pady=8)
        tk.Label(bar, text=f"{len(self.history)} entradas",
                 bg=SURFACE2, fg=MUTED, font=FONT_XS).pack(side="left")

        # Botones
        btn_bar = tk.Frame(hw, bg=BG)
        btn_bar.pack(fill="x", padx=10, pady=6)
        tk.Button(btn_bar, text="🗑 Limpiar historial", bg=SURFACE2, fg=RED,
                  font=FONT_XS, relief="flat", bd=0, cursor="hand2",
                  command=lambda: self._clear_history(hw)).pack(side="left", ipadx=8, ipady=3)
        tk.Button(btn_bar, text="💾 Exportar TXT", bg=SURFACE2, fg=MUTED,
                  font=FONT_XS, relief="flat", bd=0, cursor="hand2",
                  command=self._export_history).pack(side="left", padx=6, ipadx=8, ipady=3)

        # Lista con scroll
        frame = tk.Frame(hw, bg=BG)
        frame.pack(fill="both", expand=True, padx=10, pady=(0,10))
        vsb = tk.Scrollbar(frame, orient="vertical")
        vsb.pack(side="right", fill="y")
        txt = tk.Text(frame, bg=SURFACE, fg=TEXT, font=FONT_M,
                      relief="flat", bd=0, yscrollcommand=vsb.set,
                      state="normal", wrap="word", padx=10, pady=8)
        txt.pack(fill="both", expand=True)
        vsb.config(command=txt.yview)

        # Colores de tag
        txt.tag_config("ts",     foreground=MUTED)
        txt.tag_config("name",   foreground=CYAN)
        txt.tag_config("cmd",    foreground=GREEN)
        txt.tag_config("status", foreground=YELLOW)
        txt.tag_config("sep",    foreground=BORDER)

        if not self.history:
            txt.insert("end", "No hay ejecuciones registradas todavía.", "ts")
        else:
            for e in self.history:
                txt.insert("end", "[" + e["ts"] + "]  ", "ts")
                txt.insert("end", e["name"] + "\n", "name")
                txt.insert("end", "  " + e["cmd"] + "\n", "cmd")
                txt.insert("end", "  Estado: " + e["status"] + "\n", "status")
                txt.insert("end", "─" * 80 + "\n", "sep")

        txt.config(state="disabled")

    def _clear_history(self, parent_win=None):
        if messagebox.askyesno("Limpiar historial",
                               "¿Borrar todo el historial de ejecuciones?",
                               parent=parent_win):
            self.history = []
            self._save_history()
            if hasattr(self, 'hist_btn'):
                self.hist_btn.config(text="📋 Historial")
            if parent_win:
                parent_win.destroy()

    def _export_history(self):
        from tkinter import filedialog
        from datetime import datetime
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Texto", "*.txt"), ("Todos", "*.*")],
            initialfile=f"historial_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            title="Exportar historial"
        )
        if not path:
            return
        try:
            lines = ["IT Tools — Historial de ejecuciones",
                     "=" * 60, ""]
            for e in self.history:
                lines.append(f"[{e['ts']}]  {e['name']}")
                lines.append(f"  CMD: {e['cmd']}")
                lines.append(f"  Estado: {e['status']}")
                lines.append("-" * 60)
            Path(path).write_text("\n".join(lines), encoding="utf-8")
            messagebox.showinfo("Exportado", f"Historial guardado en:\n{path}")
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def _load_custom(self):
        try:
            with open(self._custom_file(), encoding='utf-8') as f:
                return json.load(f)
        except:
            return []

    def _save_custom(self):
        try:
            with open(self._custom_file(), 'w', encoding='utf-8') as f:
                json.dump(self.custom_cmds, f, ensure_ascii=False, indent=2)
        except:
            pass

    # ── BUILD UI ───────────────────────────────────────────────
    def _build_ui(self):
        root = self.root

        # ── TOPBAR ────────────────────────────────────────────
        topbar = tk.Frame(root, bg=SURFACE, height=54)
        topbar.pack(fill="x", side="top")
        topbar.pack_propagate(False)

        # Icono grande
        tk.Label(topbar, text="🛠", bg=SURFACE, fg=CYAN,
                 font=("Segoe UI", 20)).pack(side="left", padx=(14,4), pady=6)
        # Nombre grande
        tk.Label(topbar, text="IT Tools", bg=SURFACE, fg=CYAN,
                 font=("Segoe UI", 17, "bold")).pack(side="left", pady=6)
        # Subtítulo pequeño
        tk.Label(topbar, text="  by Oscarcierzo", bg=SURFACE, fg=MUTED,
                 font=("Segoe UI", 9)).pack(side="left", pady=6)
        tk.Label(topbar, text="", bg=SURFACE, fg=MUTED, font=("Segoe UI", 9)).pack(side="left", pady=8, padx=(0,20))

        # Buscador
        sf = tk.Frame(topbar, bg=SURFACE2, highlightbackground=BORDER, highlightthickness=1)
        sf.pack(side="left", pady=10, ipadx=4)
        tk.Label(sf, text="🔍", bg=SURFACE2, fg=MUTED, font=FONT).pack(side="left", padx=4)
        self.search_entry = tk.Entry(sf, textvariable=self.search_var,
                                     bg=SURFACE2, fg=TEXT, insertbackground=CYAN,
                                     relief="flat", font=FONT, width=28, bd=2)
        self.search_entry.pack(side="left", pady=2, padx=(0,6))
        self.search_entry.insert(0, "Buscar comandos…")
        self.search_entry.config(fg=MUTED)
        self.search_entry.bind("<FocusIn>",  self._search_focus_in)
        self.search_entry.bind("<FocusOut>", self._search_focus_out)

        # Badge admin
        _admin_bg = CYAN if _is_admin() else "#0d2535"
        _admin_fg = "#000000" if _is_admin() else CYAN
        _admin_txt = " ✔ ADMIN " if _is_admin() else " ● ADMIN "
        tk.Label(topbar, text=_admin_txt, bg=_admin_bg, fg=_admin_fg,
                 font=FONT_MB, relief="flat").pack(side="right", padx=8, pady=10)

        # Botón exportar/importar
        tk.Button(topbar, text="⬆ Export", bg=SURFACE2, fg=MUTED,
                  font=FONT_B, relief="flat", cursor="hand2", bd=0,
                  activebackground=SURFACE2, padx=8,
                  command=self._export_cmds).pack(side="right", pady=10, padx=2)
        tk.Button(topbar, text="⬇ Import", bg=SURFACE2, fg=MUTED,
                  font=FONT_B, relief="flat", cursor="hand2", bd=0,
                  activebackground=SURFACE2, padx=8,
                  command=self._import_cmds).pack(side="right", pady=10, padx=2)
        # Botón añadir
        tk.Button(topbar, text="+ Añadir", bg=CYAN, fg="#000",
                  font=FONT_B, relief="flat", cursor="hand2", bd=0,
                  activebackground="#0096b4", padx=10,
                  command=self._add_command_dialog).pack(side="right", pady=10, padx=4)

        # Botón terminal
        self.hist_btn = tk.Button(topbar, text="📋 Historial",
                                   bg=SURFACE, fg=MUTED, font=FONT_XS,
                                   relief="flat", bd=0, cursor="hand2",
                                   activebackground=SURFACE2, activeforeground=TEXT,
                                   command=self._show_history)
        self.hist_btn.pack(side="right", ipadx=10, ipady=4, padx=(0,4))
        Tooltip(self.hist_btn, "Historial de comandos ejecutados")

        self.btn_term = tk.Button(topbar, text="⬛ Terminal", bg=SURFACE2, fg=CYAN,
                                  font=FONT_B, relief="flat", cursor="hand2", bd=0,
                                  activebackground=SURFACE2, padx=8,
                                  command=self._toggle_terminal)
        self.btn_term.pack(side="right", pady=10, padx=4)

        # ── SEPARADOR ─────────────────────────────────────────
        tk.Frame(root, bg=BORDER, height=1).pack(fill="x")

        # ── BODY (sidebar + main) ─────────────────────────────
        body = tk.Frame(root, bg=BG)
        body.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = tk.Frame(body, bg=SURFACE, width=210)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="CATEGORÍAS", bg=SURFACE, fg="#3d4a60",
                 font=("Segoe UI", 7, "bold")).pack(anchor="w", padx=12, pady=(10,2))

        self.cat_btns = []
        for i, cat in enumerate(CATEGORIES):
            btn = tk.Button(self.sidebar,
                            text=f"  {cat['label']}  {len(cat['cmds'])}",
                            bg=SURFACE, fg=MUTED,
                            font=FONT, relief="flat", bd=0, anchor="w",
                            cursor="hand2", activebackground=SURFACE2,
                            command=lambda idx=i: self._select_cat(idx))
            btn.pack(fill="x", ipady=5, padx=4)
            self.cat_btns.append(btn)

        tk.Frame(self.sidebar, bg=BORDER, height=1).pack(fill="x", padx=8, pady=8)
        tk.Label(self.sidebar, text="ACCIONES", bg=SURFACE, fg="#3d4a60",
                 font=("Segoe UI", 7, "bold")).pack(anchor="w", padx=12, pady=(0,2))

        tk.Button(self.sidebar, text="  📊  Informe del equipo",
                  bg=SURFACE, fg=CYAN, font=FONT, relief="flat", bd=0, anchor="w",
                  cursor="hand2", activebackground=SURFACE2,
                  command=self._informe_rapido).pack(fill="x", ipady=4, padx=4)

        tk.Button(self.sidebar, text="  🗑  Limpiar terminal",
                  bg=SURFACE, fg=MUTED, font=FONT, relief="flat", bd=0, anchor="w",
                  cursor="hand2", activebackground=SURFACE2,
                  command=self._clear_terminal).pack(fill="x", ipady=4, padx=4)

        # Separador vertical
        tk.Frame(body, bg=BORDER, width=1).pack(side="left", fill="y")

        # Main area (canvas scrollable + terminal)
        main_col = tk.Frame(body, bg=BG)
        main_col.pack(side="left", fill="both", expand=True)

        # Header de sección
        self.sec_header = tk.Frame(main_col, bg=BG)
        self.sec_header.pack(fill="x", padx=16, pady=(12,4))
        self.sec_title_lbl = tk.Label(self.sec_header, text="", bg=BG, fg=TEXT, font=FONT_LG)
        self.sec_title_lbl.pack(side="left")
        self.sec_count_lbl = tk.Label(self.sec_header, text="", bg=BG, fg=MUTED, font=FONT)
        self.sec_count_lbl.pack(side="left", padx=8)

        # Total comandos — cuenta dinámica incluyendo personalizados
        total_base = sum(len(c["cmds"]) for c in CATEGORIES)
        self.total_lbl = tk.Label(self.sec_header,
                                  text=f"· {total_base} comandos totales",
                                  bg=BG, fg="#3a4d68", font=FONT_XS)
        self.total_lbl.pack(side="left")

        # Botón acceso directo al Panel de Control de la categoría
        self.ctrl_btn = tk.Button(self.sec_header, text="", bg=BG, fg=MUTED,
                                  relief="flat", bd=0, cursor="hand2", font=FONT_XS,
                                  activebackground=SURFACE2, activeforeground=CYAN,
                                  state="disabled")
        self.ctrl_btn.pack(side="right", padx=6, ipadx=8, ipady=3)

        # Canvas con scroll para las tarjetas
        canvas_frame = tk.Frame(main_col, bg=BG)
        canvas_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(canvas_frame, bg=BG, highlightthickness=0, bd=0)
        vsb = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.cards_frame = tk.Frame(self.canvas, bg=BG)
        self.canvas_window = self.canvas.create_window((0,0), window=self.cards_frame, anchor="nw")

        self.cards_frame.bind("<Configure>", self._on_cards_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.cmd_history = []
        self.hist_idx    = -1
        self.term_win    = None   # ventana flotante — se crea lazy

        # Crear terminal flotante al arrancar (oculta)
        self.root.after(200, self._build_float_terminal)

    # ── SEARCH ────────────────────────────────────────────────
    def _search_focus_in(self, e):
        if self.search_entry.get() == "Buscar comandos…":
            self.search_entry.delete(0, "end")
            self.search_entry.config(fg=TEXT)

    def _search_focus_out(self, e):
        if not self.search_entry.get():
            self.search_entry.insert(0, "Buscar comandos…")
            self.search_entry.config(fg=MUTED)

    def _on_search(self, *args):
        if not hasattr(self, 'canvas'):
            return
        q = self.search_var.get()
        if q == "Buscar comandos…": q = ""
        self._render_cards(q)

    # ── CATEGORÍAS ───────────────────────────────────────────
    def _select_cat(self, idx):
        self.current_cat = idx
        for i, btn in enumerate(self.cat_btns):
            if i == idx:
                btn.config(bg=CYAN_DIM, fg=CYAN, font=FONT_B)
            else:
                btn.config(bg=SURFACE, fg=MUTED, font=FONT)
        # Limpiar búsqueda al cambiar categoría
        self.search_var.set("")
        self.search_entry.delete(0, "end")
        self.search_entry.insert(0, "Buscar comandos…")
        self.search_entry.config(fg=MUTED)
        # Botón acceso directo panel de control
        cat_id = CATEGORIES[idx]["id"]
        if hasattr(self, 'ctrl_btn') and cat_id in CTRL_PANEL:
            lbl, cmd = CTRL_PANEL[cat_id]
            self.ctrl_btn.config(text=lbl, state="normal", fg=CYAN,
                                 command=lambda c=cmd: self._open_ctrl(c))
        elif hasattr(self, 'ctrl_btn'):
            self.ctrl_btn.config(text="", state="disabled")
        self._render_cards("")

    def _open_ctrl(self, cmd):
        try:
            subprocess.Popen(f'cmd /c start "" {cmd}', shell=True,
                             creationflags=subprocess.CREATE_NO_WINDOW)
        except Exception as ex:
            messagebox.showerror("Error al abrir panel", str(ex))


    def _get_cmds(self, cat_idx):
        base = list(CATEGORIES[cat_idx]["cmds"])
        cat_id = CATEGORIES[cat_idx]["id"]
        extra = [(c["name"], c["desc"], c["cmd"]) for c in self.custom_cmds if c.get("cat") == cat_id]
        return base + extra

    def _get_cmds_by_id(self, cat_id):
        base = []
        for cat in CATEGORIES:
            if cat["id"] == cat_id:
                base = list(cat["cmds"])
                break
        extra = [(c["name"], c["desc"], c["cmd"]) for c in self.custom_cmds if c.get("cat") == cat_id]
        return base + extra

    # ── TARJETAS ─────────────────────────────────────────────
    def _render_cards(self, query=""):
        if not hasattr(self, 'canvas'):
            return
        # Ocultar canvas mientras se reconstruye para evitar parpadeo
        self.canvas.pack_forget()
        for w in self.cards_frame.winfo_children():
            w.destroy()

        q = query.lower().strip()

        if q:
            # Buscar en TODAS las categorías cuando hay texto
            cmds = []
            for cat_data in CATEGORIES:
                for name, desc, cmd in self._get_cmds_by_id(cat_data["id"]):
                    if q in name.lower() or q in desc.lower() or q in cmd.lower():
                        cmds.append((name, desc, cmd, cat_data["color"]))
            # Añadir custom de todas las cats
            self.sec_title_lbl.config(text=f"🔍  Resultados para: {query}", fg=CYAN)
            self.sec_count_lbl.config(text=f"— {len(cmds)} comandos en todas las categorías")
            COLS = 3
            for idx, (name, desc, cmd, color) in enumerate(cmds):
                self._make_card(self.cards_frame, idx//COLS, idx%COLS, name, desc, cmd, color)
        else:
            cat  = CATEGORIES[self.current_cat]
            cmds = self._get_cmds(self.current_cat)
            self.sec_title_lbl.config(text=cat["label"], fg=cat["color"])
            self.sec_count_lbl.config(text=f"— {len(cmds)} comandos")
            COLS = 3
            for idx, (name, desc, cmd) in enumerate(cmds):
                self._make_card(self.cards_frame, idx//COLS, idx%COLS, name, desc, cmd, cat["color"])

        # Pad vacío si no hay resultados
        if not cmds:
            tk.Label(self.cards_frame, text="🔍  Sin resultados",
                     bg=BG, fg=MUTED, font=FONT_LG).grid(row=0, column=0, padx=40, pady=60)

        self.cards_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.yview_moveto(0)
        # Mostrar canvas de nuevo
        self.canvas.pack(side="left", fill="both", expand=True)

    def _make_card(self, parent, row, col, name, desc, cmd, accent):
        card = tk.Frame(parent, bg=SURFACE, bd=0, highlightthickness=1, highlightbackground=BORDER)
        card.grid(row=row, column=col, padx=8, pady=6, sticky="nsew")
        parent.columnconfigure(col, weight=1)

        # Línea de acento superior
        accent_bar = tk.Frame(card, bg=SURFACE, height=3)
        accent_bar.pack(fill="x")

        inner = tk.Frame(card, bg=SURFACE, padx=10, pady=8)
        inner.pack(fill="both", expand=True)

        # Nombre
        tk.Label(inner, text=name, bg=SURFACE, fg=TEXT, font=FONT_B,
                 wraplength=220, justify="left", anchor="w").pack(fill="x")

        # Descripción
        tk.Label(inner, text=desc, bg=SURFACE, fg=MUTED, font=FONT_XS,
                 wraplength=220, justify="left", anchor="w").pack(fill="x", pady=(2,6))

        # Código
        code_frame = tk.Frame(inner, bg="#080c14", highlightthickness=1, highlightbackground=BORDER)
        code_frame.pack(fill="x", pady=(0,8))
        code_lbl = tk.Label(code_frame, text=cmd, bg="#080c14", fg=accent,
                            font=FONT_M, wraplength=220, justify="left", anchor="w",
                            cursor="xterm", padx=8, pady=4)
        code_lbl.pack(fill="x")

        # Botones
        btn_row = tk.Frame(inner, bg=SURFACE)
        btn_row.pack(fill="x")

        tk.Button(btn_row, text="▶  Ejecutar", bg=CYAN_DIM, fg=CYAN,
                  font=FONT_B, relief="flat", bd=0, cursor="hand2",
                  activebackground=CYAN, activeforeground="#000",
                  command=lambda c=cmd, n=name: self._run_cmd(c, n)).pack(side="left", fill="x", expand=True, ipady=4, padx=(0,4))

        tk.Button(btn_row, text="⎘ Copiar", bg="#080c14", fg=MUTED,
                  font=FONT_B, relief="flat", bd=0, cursor="hand2",
                  activebackground=SURFACE2, activeforeground=TEXT,
                  command=lambda c=cmd: self._copy_cmd(c)).pack(side="left", ipadx=8, ipady=4)

        # Botón favorito ⭐
        is_fav = self._is_fav(cmd)
        fav_color = YELLOW if is_fav else MUTED
        fav_text  = "★" if is_fav else "☆"
        tk.Button(btn_row, text=fav_text, bg=SURFACE, fg=fav_color,
                  font=("Segoe UI", 13), relief="flat", bd=0, cursor="hand2",
                  activebackground=SURFACE2, activeforeground=YELLOW,
                  command=lambda n=name, d=desc, c=cmd: self._toggle_fav(n, d, c)
                  ).pack(side="right", ipadx=6, ipady=2)

        # Hover effect
        def _hover_on(e, f=card, ab=accent_bar, a=accent):
            f.config(highlightbackground=a)
            ab.config(bg=a)
        def _hover_off(e, f=card, ab=accent_bar):
            f.config(highlightbackground=BORDER)
            ab.config(bg=SURFACE)
        for w in [card, inner, accent_bar, code_frame]:
            w.bind("<Enter>", _hover_on)
            w.bind("<Leave>", _hover_off)

    # ── SCROLL ───────────────────────────────────────────────
    def _on_cards_configure(self, e):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, e):
        self.canvas.itemconfig(self.canvas_window, width=e.width)

    def _on_mousewheel(self, e):
        try:
            if self.term_win and e.widget.winfo_toplevel() == self.term_win:
                return
        except Exception:
            pass
        if hasattr(self, 'canvas'):
            self.canvas.yview_scroll(int(-1*(e.delta/120)), "units")

    # ── TERMINAL FLOTANTE ────────────────────────────────────
    def _build_float_terminal(self):
        """Crea la ventana flotante del terminal."""
        tw = tk.Toplevel(self.root)
        tw.title("Terminal — IT Tools")
        tw.configure(bg="#0a0e1a")
        tw.geometry("760x360+80+420")
        tw.resizable(True, True)
        tw.minsize(480, 220)
        tw.overrideredirect(True)          # sin borde nativo
        tw.attributes("-topmost", False)

        self.term_win = tw
        self._term_topmost = False

        # ── Barra de título ───────────────────────────────────
        bar = tk.Frame(tw, bg="#111827", cursor="fleur")
        bar.pack(fill="x")

        dot_f = tk.Frame(bar, bg="#111827")
        dot_f.pack(side="left", padx=10, pady=6)
        # Rojo=cerrar, Amarillo=minimizar, Verde=topmost
        btn_close = tk.Label(dot_f, text="●", bg="#111827", fg=RED,    font=("Segoe UI",11), cursor="hand2")
        btn_min   = tk.Label(dot_f, text="●", bg="#111827", fg=YELLOW, font=("Segoe UI",11), cursor="hand2")
        btn_top   = tk.Label(dot_f, text="●", bg="#111827", fg=GREEN,  font=("Segoe UI",11), cursor="hand2")
        btn_close.pack(side="left", padx=2)
        btn_min.pack(side="left",   padx=2)
        btn_top.pack(side="left",   padx=2)

        btn_close.bind("<Button-1>", lambda e: self._hide_terminal())
        btn_min.bind("<Button-1>",   lambda e: self._minimize_terminal())
        btn_top.bind("<Button-1>",   lambda e: self._toggle_topmost())

        self.term_title_lbl = tk.Label(bar, text="▶ Terminal CMD — IT Tools",
                                        bg="#111827", fg="#5a6a88", font=FONT_M)
        self.term_title_lbl.pack(side="left", padx=8)

        tk.Button(bar, text="🗑", bg="#111827", fg=MUTED, relief="flat", bd=0,
                  cursor="hand2", font=FONT,
                  command=self._clear_terminal).pack(side="right", padx=6, pady=3)

        # Drag to move
        bar.bind("<ButtonPress-1>",  self._term_drag_start)
        bar.bind("<B1-Motion>",      self._term_drag_move)
        self.term_title_lbl.bind("<ButtonPress-1>", self._term_drag_start)
        self.term_title_lbl.bind("<B1-Motion>",     self._term_drag_move)

        # ── Output ────────────────────────────────────────────
        out_frame = tk.Frame(tw, bg="#080c14")
        out_frame.pack(fill="both", expand=True)

        self.term_out = tk.Text(out_frame, bg="#080c14", fg="#8a9ab8",
                                font=FONT_M, relief="flat", bd=6,
                                state="disabled", wrap="char",
                                insertbackground=CYAN, selectbackground=SURFACE2,
                                highlightthickness=0)
        t_vsb = ttk.Scrollbar(out_frame, orient="vertical", command=self.term_out.yview)
        self.term_out.configure(yscrollcommand=t_vsb.set)
        t_vsb.pack(side="right", fill="y")
        self.term_out.pack(side="left", fill="both", expand=True)

        self.term_out.tag_config("cmd",    foreground=CYAN,   font=FONT_MB)
        self.term_out.tag_config("out",    foreground=TEXT)
        self.term_out.tag_config("err",    foreground=RED)
        self.term_out.tag_config("ok_bar", foreground="#0a1a0a", background=GREEN, font=FONT_B)
        self.term_out.tag_config("err_bar", foreground="#1a0a0a", background=RED, font=FONT_B)
        self.term_out.tag_config("ok",     foreground=GREEN)
        self.term_out.tag_config("info",   foreground=YELLOW)
        self.term_out.tag_config("prompt", foreground=CYAN,   font=FONT_MB)
        self.term_out.tag_config("muted",  foreground=MUTED)

        # ── Input EDITABLE ────────────────────────────────────
        input_bar = tk.Frame(tw, bg="#0d1525")
        input_bar.pack(fill="x", side="bottom")
        tk.Label(input_bar, text=r"C:\>", bg="#0d1525", fg=CYAN,
                 font=FONT_MB).pack(side="left", padx=(10,4), pady=6)
        self.term_input = tk.Entry(input_bar, bg="#0d1525", fg=TEXT,
                                   insertbackground=CYAN, relief="flat",
                                   font=FONT_M, bd=2)
        self.term_input.pack(side="left", fill="x", expand=True, pady=6, padx=(0,8))
        self.term_input.bind("<Return>",  self._term_enter)
        self.term_input.bind("<Up>",      self._hist_up)
        self.term_input.bind("<Down>",    self._hist_down)
        self.term_input.insert(0, "Escribe o pega un comando y pulsa Enter…")
        self.term_input.config(fg=MUTED)
        self.term_input.bind("<FocusIn>",  self._term_focus_in)
        self.term_input.bind("<FocusOut>", self._term_focus_out)

        # Welcome
        self._term_info("╔══════════════════════════════════════════════╗")
        self._term_info("║  IT Tools  —  by Oscarcierzo                ║")
        self._term_info("║  Centro de Comandos IT · Modo Administrador ║")
        self._term_info("╚══════════════════════════════════════════════╝")
        self._term_write("\n", "muted")
        self._term_ok("✓ Sistema listo")
        self._term_write("  Edita el comando en la barra inferior y pulsa Enter\n", "muted")

        # Ocultar hasta que el usuario la abra
        tw.withdraw()

    def _term_drag_start(self, e):
        self._tdx = e.x_root - self.term_win.winfo_x()
        self._tdy = e.y_root - self.term_win.winfo_y()

    def _term_drag_move(self, e):
        x = e.x_root - self._tdx
        y = e.y_root - self._tdy
        self.term_win.geometry(f"+{x}+{y}")

    def _toggle_topmost(self):
        self._term_topmost = not self._term_topmost
        self.term_win.attributes("-topmost", self._term_topmost)


    def _export_terminal(self):
        from tkinter import filedialog
        from datetime import datetime
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Texto", "*.txt"), ("Todos", "*.*")],
            initialfile=f"terminal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            title="Guardar log del terminal"
        )
        if not path:
            return
        try:
            content = self.term_out.get("1.0", "end")
            Path(path).write_text(content, encoding="utf-8")
            messagebox.showinfo("Guardado", f"Log guardado en:\n{path}")
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def _hide_terminal(self):
        self.term_win.withdraw()
        self.btn_term.config(text="▶ Terminal")

    def _minimize_terminal(self):
        self.term_win.iconify()

    def _toggle_terminal(self):
        if self.term_win is None:
            return
        if self.term_win.state() == "withdrawn":
            self.term_win.deiconify()
            self.term_win.lift()
            self.btn_term.config(text="⬛ Terminal")
        else:
            self._hide_terminal()

    def _term_write(self, text, tag="out"):
        self.term_out.config(state="normal")
        self.term_out.insert("end", text, tag)
        self.term_out.see("end")
        self.term_out.config(state="disabled")

    def _term_ok(self,   t): self._term_write(t + "\n", "ok")
    def _term_err(self,  t): self._term_write(t + "\n", "err")
    def _term_info(self, t): self._term_write(t + "\n", "info")

    def _clear_terminal(self):
        self.term_out.config(state="normal")
        self.term_out.delete("1.0", "end")
        self.term_out.config(state="disabled")
        self._term_info(f"[Terminal limpiada]")

    # ── EJECUTAR COMANDOS ─────────────────────────────────────
    def _run_cmd(self, cmd, name, focus_input=False):
        """Ejecuta cmd real. Si focus_input=True, solo pega en el campo sin ejecutar."""
        if self.term_win is None:
            return
        # Abrir terminal si estaba oculta
        if self.term_win.state() == "withdrawn":
            self.term_win.deiconify()
            self.term_win.lift()
            self.btn_term.config(text="⬛ Terminal")
        if focus_input:
            # Solo pegar en el input para que el usuario lo edite antes de ejecutar
            self.term_input.config(fg=TEXT)
            self.term_input.delete(0, "end")
            self.term_input.insert(0, cmd)
            self.term_input.focus_set()
            self.term_input.icursor("end")
            return
        self._term_write(f"\nC:\\> ", "prompt")
        self._term_write(f"{cmd}\n", "cmd")
        self.cmd_history.insert(0, cmd)
        self.hist_idx = -1
        self._add_to_history(name, cmd)
        threading.Thread(target=self._exec, args=(cmd,), daemon=True).start()

    def _exec(self, cmd):
        try:
            remote=getattr(self,"remote_var",None); remote=remote.get().strip() if remote else ""
            if remote: cmd=f'powershell -command "Invoke-Command -ComputerName {remote} -ScriptBlock {{ {cmd} }}"'
            proc = subprocess.Popen(
                cmd, shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                stdin=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            stdout, stderr = proc.communicate(timeout=60)
            # Intentar decodificar con cp850 (CMD español), fallback utf-8
            for enc in ('cp850', 'utf-8', 'latin-1'):
                try:
                    out = stdout.decode(enc)
                    err = stderr.decode(enc)
                    break
                except:
                    pass
            self.root.after(0, lambda o=out, e=err, r=proc.returncode: self._show_result(o, e, r))
        except subprocess.TimeoutExpired:
            self.root.after(0, lambda: self._term_err("⚠ Timeout — el comando tardó más de 60 segundos"))
        except Exception as ex:
            self.root.after(0, lambda x=str(ex): self._term_err(f"ERROR: {x}"))

    def _show_result(self, out, err, code):
        if out.strip():
            self._term_write(out, "out")
        if err.strip():
            self._term_write(err, "err")
        if code == 0:
            self._term_write("\n● Completado\n", "ok_bar")
        else:
            self._term_write(f"\n● Error codigo: {code}\n", "err_bar")

    # ── TERMINAL INPUT (teclado) ──────────────────────────────
    def _term_focus_in(self, e):
        if self.term_input.get().startswith("Escribe"):
            self.term_input.delete(0, "end")
            self.term_input.config(fg=TEXT)

    def _term_focus_out(self, e):
        if not self.term_input.get():
            self.term_input.insert(0, "Escribe un comando aquí… (↑↓ historial · Enter ejecutar)")
            self.term_input.config(fg=MUTED)

    def _term_enter(self, e):
        cmd = self.term_input.get().strip()
        if not cmd or cmd.startswith("Escribe"): return
        if cmd.lower() in ("cls", "clear"):
            self._clear_terminal()
        else:
            self._run_cmd(cmd, "Comando manual")
        self.term_input.delete(0, "end")

    def _hist_up(self, e):
        if not self.cmd_history: return
        self.hist_idx = min(self.hist_idx + 1, len(self.cmd_history) - 1)
        self.term_input.delete(0, "end")
        self.term_input.insert(0, self.cmd_history[self.hist_idx])
        self.term_input.config(fg=TEXT)

    def _hist_down(self, e):
        if self.hist_idx <= 0:
            self.hist_idx = -1
            self.term_input.delete(0, "end")
        else:
            self.hist_idx -= 1
            self.term_input.delete(0, "end")
            self.term_input.insert(0, self.cmd_history[self.hist_idx])

    # ── COPIAR ────────────────────────────────────────────────


    def _informe_rapido(self):
        self._term_info('\n================================')
        self._term_info('  Generando informe del equipo...')
        self._term_info('================================\n')
        def _run():
            import datetime
            data = {}
            for key, cmd in [
                ('hostname', 'hostname'),
                ('ip',       'powershell -command "(Get-WmiObject Win32_NetworkAdapterConfiguration | Where {$_.IPAddress} | Select -First 1).IPAddress[0]"'),
                ('os',       'powershell -command "(Get-WmiObject Win32_OperatingSystem).Caption"'),
                ('cpu',      'powershell -command "(Get-WmiObject Win32_Processor | Select -First 1).Name"'),
                ('ram',      'powershell -command "[math]::Round((Get-WmiObject Win32_ComputerSystem).TotalPhysicalMemory/1GB,1)"'),
                ('disco',    'wmic logicaldisk where DeviceID=C: get FreeSpace,Size /format:list'),
                ('gpu',      'powershell -command "(Get-WmiObject Win32_VideoController | Select -First 1).Name"'),
                ('serie',    'powershell -command "(Get-WmiObject Win32_BIOS).SerialNumber"'),
                ('licencia', 'powershell -command "(Get-WmiObject SoftwareLicensingProduct | Where {$_.PartialProductKey} | Select -First 1).Name"'),
                ('anydesk',  'powershell -command "Get-ItemProperty HKLM:\\SOFTWARE\\AnyDesk -EA SilentlyContinue | Select -ExpandProperty ad.anynet.id -EA SilentlyContinue"'),
            ]:
                try:
                    r = subprocess.run(cmd, shell=True, capture_output=True, timeout=12)
                    data[key] = r.stdout.decode('cp850','replace').strip() or 'N/D'
                except Exception:
                    data[key] = 'N/D'
            ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            out_path = Path.home() / 'Desktop' / ('informe_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html')
            trs = ''.join('<tr><td>' + k + '</td><td>' + v + '</td></tr>' for k,v in [
                ('Hostname',  data.get('hostname','N/D')),
                ('IP local',  data.get('ip','N/D')),
                ('SO',        data.get('os','N/D')),
                ('CPU',       data.get('cpu','N/D')),
                ('RAM',       data.get('ram','N/D') + ' GB'),
                ('Disco C:',  data.get('disco','N/D')),
                ('GPU',       data.get('gpu','N/D')),
                ('Serie BIOS',data.get('serie','N/D')),
                ('Licencia',  data.get('licencia','N/D')),
                ('AnyDesk',   data.get('anydesk','N/D')),
            ])
            css = 'body{font-family:Segoe UI,sans-serif;background:#0d1117;color:#c9d1d9;padding:24px}h1{color:#58a6ff;border-bottom:1px solid #21262d;padding-bottom:8px}table{width:100%;border-collapse:collapse}td{padding:7px 12px;border-bottom:1px solid #21262d;font-size:13px}td:first-child{color:#8b949e;width:180px}.ts{color:#484f58;font-size:11px}'
            html = '<!DOCTYPE html><html><head><meta charset="utf-8"><title>Informe IT</title><style>' + css + '</style></head><body><h1>\U0001f6e0 IT Tools Informe</h1><p class="ts">Generado: ' + ts + ' by Oscarcierzo</p><table>' + trs + '</table></body></html>'
            out_path.write_text(html, encoding='utf-8')
            self.root.after(0, lambda p=str(out_path): self._informe_done(p))
        threading.Thread(target=_run, daemon=True).start()

    def _informe_done(self, path):
        self._term_write('\n Informe guardado: ' + path + '\n', 'ok_bar')
        import webbrowser; webbrowser.open(path)

    def _copy_cmd(self, cmd):
        """Copia al portapapeles del sistema."""
        self.root.clipboard_clear()
        self.root.clipboard_append(cmd)
        self.root.update()

    # ── AÑADIR COMANDO PERSONALIZADO ──────────────────────────
    def _add_command_dialog(self):
        dlg = tk.Toplevel(self.root)
        dlg.title("Añadir comando")
        dlg.configure(bg=SURFACE)
        dlg.resizable(False, False)
        dlg.grab_set()
        dlg.transient(self.root)
        dlg.focus_force()
        self.root.update_idletasks()
        rx = self.root.winfo_x() + self.root.winfo_width()  // 2
        ry = self.root.winfo_y() + self.root.winfo_height() // 2
        dlg.geometry(f"500x380+{rx-250}+{ry-190}")

        def lbl(text):
            tk.Label(dlg, text=text, bg=SURFACE, fg=MUTED,
                     font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=18, pady=(10,2))

        def inp(parent=dlg):
            f = tk.Frame(parent, bg=SURFACE2,
                         highlightbackground=BORDER, highlightthickness=1)
            f.pack(fill="x", padx=18)
            e = tk.Entry(f, bg=SURFACE2, fg=TEXT, insertbackground=CYAN,
                         relief="flat", font=FONT, bd=4)
            e.pack(fill="x", padx=4, pady=5)
            return e

        tk.Label(dlg, text="Añadir nuevo comando", bg=SURFACE,
                 fg=TEXT, font=FONT_LG).pack(pady=(16,4), padx=18, anchor="w")

        lbl("Nombre")
        e_name = inp()
        e_name.focus_set()

        lbl("Categoría")
        cat_ids   = [c["id"]    for c in CATEGORIES]
        cat_names = [c["label"].strip() for c in CATEGORIES]
        cat_display = tk.StringVar(value=cat_names[self.current_cat])
        cf = tk.Frame(dlg, bg=SURFACE2, highlightbackground=BORDER, highlightthickness=1)
        cf.pack(fill="x", padx=18)
        om = tk.OptionMenu(cf, cat_display, *cat_names)
        om.config(bg=SURFACE2, fg=TEXT, activebackground=CYAN_DIM,
                  activeforeground=CYAN, relief="flat", font=FONT,
                  bd=0, highlightthickness=0, anchor="w", width=40)
        om["menu"].config(bg=SURFACE2, fg=TEXT, activebackground=CYAN_DIM,
                          activeforeground=CYAN, font=FONT, bd=0)
        om.pack(fill="x", padx=2, pady=2)

        lbl("Descripción  (opcional)")
        e_desc = inp()

        lbl("Comando")
        e_cmd = inp()

        def save():
            n   = e_name.get().strip()
            cmd = e_cmd.get().strip()
            if not n or not cmd:
                messagebox.showwarning("Faltan datos",
                    "El nombre y el comando son obligatorios.", parent=dlg)
                return
            cid = cat_ids[cat_names.index(cat_display.get())]                   if cat_display.get() in cat_names else cat_ids[0]
            self.custom_cmds.append({
                "name": n, "desc": e_desc.get().strip(),
                "cmd": cmd, "cat": cid
            })
            self._save_custom()
            self._select_cat(self.current_cat)
            dlg.destroy()

        dlg.bind("<Return>", lambda e: save())
        dlg.bind("<Escape>", lambda e: dlg.destroy())

        btn_row = tk.Frame(dlg, bg=SURFACE)
        btn_row.pack(fill="x", padx=18, pady=14)
        tk.Button(btn_row, text="Cancelar", bg=SURFACE2, fg=MUTED,
                  relief="flat", bd=0, cursor="hand2", font=FONT,
                  command=dlg.destroy,
                  activebackground=BORDER).pack(side="right", padx=(8,0), ipadx=12, ipady=6)
        tk.Button(btn_row, text="  Guardar  ", bg=CYAN, fg="#000",
                  relief="flat", bd=0, cursor="hand2", font=FONT_B,
                  command=save,
                  activebackground="#0096b4").pack(side="right", ipadx=12, ipady=6)

    def _export_cmds(self):
        from tkinter import filedialog
        all_cmds = {
            "version": "1.0",
            "custom_commands": self.custom_cmds
        }
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json"), ("Todos", "*.*")],
            title="Exportar comandos personalizados",
            initialfile="wincmd_ricma_comandos.json"
        )
        if path:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(all_cmds, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Exportado", f"Comandos exportados a:\n{path}")

    def _import_cmds(self):
        from tkinter import filedialog
        path = filedialog.askopenfilename(
            filetypes=[("JSON", "*.json"), ("Todos", "*.*")],
            title="Importar comandos personalizados"
        )
        if not path:
            return
        try:
            with open(path, encoding='utf-8') as f:
                data = json.load(f)
            imported = data.get("custom_commands", [])
            if not isinstance(imported, list):
                raise ValueError("Formato incorrecto")
            added = 0
            for c in imported:
                if c not in self.custom_cmds:
                    self.custom_cmds.append(c)
                    added += 1
            self._save_custom()
            self._select_cat(self.current_cat)
            messagebox.showinfo("Importado", f"Se importaron {added} comandos nuevos.")
        except Exception as ex:
            messagebox.showerror("Error", f"No se pudo importar:\n{ex}")

    def run(self):
        self.root.mainloop()


# ══════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════
def main():
    _elevate()
    SplashScreen().show()
    app = App()
    app.run()


if __name__ == "__main__":
    main()