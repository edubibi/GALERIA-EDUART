# Guía de Integración Web

Tienes tu aplicación lista en la carpeta `photo_catalog_portable`. Aquí tienes 3 formas de integrarla en tu web actual:

## Opción 1: Carpeta Independiente (Recomendada)
La forma más limpia y profesional.
1. Accede a tu hosting (cPanel, FTP, etc.).
2. Sube **toda la carpeta** `photo_catalog_portable` a la raíz de tu sitio web (generalmente `public_html`).
3. Renombra la carpeta si quieres, por ejemplo a `catalogo`.
4. Tu app será accesible inmediatamente en: `www.tuweb.com/catalogo`

## Opción 2: Insertar en una página existente (Iframe)
Si quieres que el catálogo aparezca "dentro" de una de tus páginas (ej. en la sección de Servicios).
1. Sube la carpeta igual que en la Opción 1.
2. En tu página web, pega este código donde quieras que aparezca el catálogo:

```html
<iframe src="https://tuweb.com/catalogo/index.html" 
        width="100%" 
        height="800px" 
        style="border:none; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
</iframe>
```

## Opción 3: WordPress
Si usas WordPress, lo más fácil es usar la **Opción 2** o un plugin de "File Manager".
1. Usa un plugin de administrador de archivos para subir la carpeta `catalogo` dentro de `wp-content` o en la raíz.
2. Crea una nueva página en WordPress.
3. Usa un bloque de "HTML Personalizado" y pega el código del Iframe de arriba.

---
**Nota Importante**: Recuerda que la configuración (Logo, textos) se guarda en el navegador del usuario. Si quieres que el Logo salga por defecto para *todos* tus clientes, deberías editar el `index.html` con la ruta de tu logo antes de subirlo, o subirlo tú primero y configurarlo en tu navegador (pero eso solo se guardará para ti). 

*Si deseas que el logo y textos vengan pre-configurados fijos en el código para todos los visitantes, avísame y te ayudo a "quemarlos" en el archivo antes de subirlo.*
