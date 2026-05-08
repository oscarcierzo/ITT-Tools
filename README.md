# 🛠 IT Tools by Oscarcierzo

> Centro de comandos IT para administradores de sistemas Windows.  
> Más de 200 comandos organizados en 19 categorías, con terminal integrado, favoritos, historial e informes HTML.

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![Windows](https://img.shields.io/badge/Windows-10%2F11-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Stars](https://img.shields.io/github/stars/oscarcierzo/it-tools?style=social)

---

## ✨ Características

- **19 categorías** con +200 comandos nativos de Windows / PowerShell
- **Terminal integrado** con streaming en tiempo real e historial de teclas ↑↓
- **⭐ Favoritos** — marca tus comandos más usados, se guardan automáticamente
- **📋 Historial** — registro de ejecuciones con fecha/hora, exportable a TXT
- **📊 Informe del equipo** — genera un HTML en el escritorio con hostname, IP, CPU, RAM, disco, GPU, licencia y AnyDesk ID
- **🖥 Ejecutar en remoto** — campo ComputerName para lanzar con `Invoke-Command`
- Color verde/rojo en el terminal según resultado del comando

## 📦 Categorías

| | | |
|---|---|---|
| 🖥 Sistema | 💾 Discos | 🌐 Red / Internet |
| 👤 Usuarios | ⚙️ Procesos | 🔧 Boot / Arranque |
| 🗂 Registro | 🔒 Seguridad | 🏢 Active Directory |
| 🖨 Impresoras | 🔄 Windows Update | 🖥 RDP / Remoto |
| 📦 Inventario | 🌍 DNS / Puertos | 🔨 Reparaciones |
| ⚡ Optimización | 🧪 Tests & Diagnóstico | 💡 PowerShell |

## 🚀 Uso rápido

### Requisitos
- Windows 10 / 11
- Python 3.10+ → [python.org](https://python.org)
- CMD o PowerShell como **Administrador**

```cmd
python ittools.py
```

### Compilar a .exe standalone
```cmd
pip install pyinstaller
pyinstaller --onefile --windowed --uac-admin --name "IT-Tools" ittools.py
```
El `.exe` aparece en `dist/`

## 📁 Archivos generados automáticamente
| Archivo | Descripción |
|---|---|
| `favoritos.json` | Comandos marcados como favoritos |
| `historial.json` | Historial de ejecuciones |
| `custom_commands.json` | Comandos personalizados añadidos |
| `informe_YYYYMMDD.html` | Informe del equipo (guardado en el Escritorio) |

## 🤝 Contribuir

1. Fork del repositorio
2. Crea tu rama: `git checkout -b feature/nueva-categoria`
3. Añade tus comandos en `CATEGORIES` dentro de `ittools.py`
4. Pull Request con descripción de los comandos añadidos

## 📄 Licencia

MIT License — libre para uso personal y comercial.  
Si lo usas en tu empresa o lo mejoras, ¡una estrella ⭐ siempre se agradece!

---
*by [Oscarcierzo](https://github.com/oscarcierzo) · 2026*
