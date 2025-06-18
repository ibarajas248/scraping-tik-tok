# TikTok Scraper: Descarga Videos y Comentarios

Este proyecto permite automatizar la descarga de videos desde TikTok y extraer los comentarios de los mismos. Utiliza **Selenium WebDriver** con Google Chrome para simular la navegación y recopilar datos automáticamente.

---

##  Funcionalidades

-  Busca una palabra clave en TikTok.
-  Descarga los primeros 3 videos del resultado de búsqueda.
-  Extrae los comentarios visibles de cada video (realiza scroll automático).
-  Guarda los videos con nombres `video1.mp4`, `video2.mp4`, etc.
-  Exporta todos los comentarios recopilados a un archivo `comentarios_tiktok.xlsx`.

---

## Tecnologías usadas

- Python 3.x
- Selenium
- Pandas
- ChromeDriver

---

## 📁 Estructura de Carpetas

```text
downloads/
├── video1.mp4
├── video2.mp4
├── video3.mp4
└── comentarios_tiktok.xlsx
```

---

## Requisitos

- Python 3.7 o superior
- Google Chrome instalado
- ChromeDriver compatible con tu versión de Chrome

---

##  Instalación de dependencias

```bash
pip install selenium pandas
```

---

##  Ejecución

1. Clona el repositorio o descarga el script.
2. Asegúrate de tener Google Chrome instalado.
3. Ejecuta el script principal:

```bash
python tiktok_scraper.py
```

---

##  Notas adicionales

- La descarga de videos puede depender de que TikTok mantenga visible el botón de "Descargar video" en el menú contextual.
- Este script no requiere login.
- Asegúrate de tener permisos de escritura en la carpeta donde se ejecuta el script para guardar archivos correctamente.
- Dar permisos de descargas automaticas en el navegador emergente.

---


