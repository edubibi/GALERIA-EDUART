# 📘 GÚIA RÁPIDA: Cómo añadir obras a tu Web

Tu página web es "dinámica": lee la lista de cuadros un archivo y los pinta automáticamente.
Para añadir o quitar cuadros, **no necesitas saber programación**, solo seguir estos 3 pasos.

---

## PASO 1: La Imagen 📸
Guarda la foto de tu nueva obra en la carpeta **`assets`** de tu proyecto.
*   Ejemplo: `mi_obra_maestra.jpg`

## PASO 2: El Registro 📝
Abre el archivo **`js/data.js`**. Verás una lista de "bloques" parecida a esta:

```javascript
    {
        id: "obra1",
        title: "Atardecer Dorado",
        category: "Naturaleza",
        src: "assets/sample1.jpg", 
        description: "Óleo sobre lienzo, 2024",
        size: "100x80cm",
        price: "Consultar"
    },
```

## PASO 3: Copiar y Pegar 📋
1.  **Copia** todo el bloque (desde el `{` hasta el `},`).
2.  **Pégalo** justo debajo (antes del final `];`).
3.  **Cambia los datos** por los de tu nueva obra:

```javascript
    {
        id: "obra_nueva",                 // Un nombre único (sin espacios)
        title: "Mi Nueva Obra",           // El título que se ve
        category: "Abstracto",            // La categoría para agruparla
        src: "assets/mi_obra_maestra.jpg",// <--- ¡El nombre de tu archivo!
        description: "Acrílico, 2025",
        size: "50x50cm",
        price: "200€"
    },
```

✅ **¡LISTO!**
Guarda el archivo (`Ctrl + S`).
Al recargar tu web, la nueva obra aparecerá en **Inicio**, **Galería** y **Colecciones** automáticamente.

---

## 🎨 CÓMO UNIR LAS OBRAS A UN "ESTILO"
No tienes que "crear" los estilos o botones. **Se crean solos**.

1.  En el campo `category` de tu obra, escribe el nombre del estilo.
    *   Ejemplo: `category: "Paisaje Urbano",`
2.  Automáticamente, en la página de **Colecciones**, aparecerá un botón llamado "Paisaje Urbano".
3.  Si pones el mismo nombre en 5 obras, esas 5 obras saldrán al pulsar ese botón.

¡Así de fácil! Solo inventa un nombre y úsalo en tus obras.


---

## 💡 TRUCO PRO: Usar el Generador Automático
Para no escribir el código a mano (Paso 2 y 3), hemos creado una herramienta secreta.
1. Abre el archivo **`admin.html`** en tu navegador.
2. Rellena los datos en el formulario.
3. Dale a **"Generar Código"** y pégalo en `data.js`.
¡Mucho más rápido y sin errores!

---

## 🌍 CÓMO ACTUALIZAR TU WEB EN INTERNET
Cuando hagas cambios en tu ordenador (añadir obras, cambiar textos...), tu hermana NO los verá automáticamente. Tienes que "subir" los cambios.

**Pasos para actualizar:**
1. Entra en **[Netlify Drop](https://app.netlify.com/drop)**.
2. Coge tu carpeta **`photo_catalog_portable`** entera y **arrástrala** al recuadro de la web.
3. Espera a que ponga "Complete".
4. ¡Listo! El enlace de siempre ya mostrará lo nuevo.
