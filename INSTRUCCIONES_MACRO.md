# 🤖 Guía de Configuración: Tu Robot de Photoshop

## 1. Prepara el Terreno (Solo una vez)
1.  Abre **Photoshop**.
2.  Abre **UNA** de las fotos que quieres retocar (cualquiera sirve de prueba).
3.  Abre el panel de **Acciones** (Menú: *Ventana > Acciones* o `Alt + F9`).

## 2. Crea la "Caja de Herramientas"
1.  En el panel de Acciones, haz clic en el icono de **Carpeta** (📂) abajo del todo.
2.  Ponle de nombre exacto: `MisRobots`
3.  Dale a OK.

## 3. Graba la Acción (¡La parte importante!)
1.  Con la carpeta `MisRobots` seleccionada, haz clic en el icono de **Nueva Acción** (➕).
2.  Ponle de nombre exacto: `BorrarMarca`
3.  Dale a **Grabar** (🔴 Se pondrá el botón rojo).
4.  **AHORA HAZ TU RETOQUE:**
    *   Usa el **Pincel Corrector Puntual** para borrar la marca.
    *   Ve a *Archivo > Guardar* (Ctrl+S).
    *   Ve a *Archivo > Cerrar* (Ctrl+W).
5.  Dale al botón **Stop** (⏹️) en el panel de Acciones para dejar de grabar.

---

## 4. ¡EJECUTA EL ROBOT! 🚀
Ahora que Photoshop ya sabe qué hacer, lánzalo tantas veces como quieras:

1.  En Photoshop, ve al menú: **Archivo > Secuencias de comandos > Explorar...**
2.  Busca y selecciona el archivo: `RobotPhotoshop.jsx`
    *(Está en la carpeta de tu proyecto: `photo_catalog_portable`)*.
3.  Una ventana te pedirá: **"Selecciona la carpeta con las fotos"**.
4.  Elige la carpeta donde tienes las 100/200 fotos.
5.  ¡Siéntate y mira cómo trabaja solo! 😎

> **Nota:** El robot procesará todas las fotos de esa carpeta, una por una.
