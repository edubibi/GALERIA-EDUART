import os
import re

html_files = [
    'index.html', 'colecciones.html', 'sobre-mi.html', 'contacto.html', 
    'carrito.html', 'compra.html', 'condiciones.html', 'galeria.html',
    'muestrario_estilos.html', 'catalogo_completo.html'
]

footer_html = '''<footer class="site-footer" style="text-align: center; padding: 2rem; background-color: var(--bg-color, #fafafa); color: var(--text-color, #333); border-top: 1px solid #eaeaea; margin-top: 4rem;">
    <p style="margin-bottom: 0.5rem; font-size: 0.9rem;">&copy; e.ramirez 2026. Todos los derechos reservados.</p>
    <a href="condiciones.html" style="color: inherit; text-decoration: underline; font-size: 0.85rem;">Términos y Condiciones</a>
</footer>'''

for file_name in html_files:
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if it already has a footer
        if '<footer' in content:
            # Replace existing footer
            content = re.sub(r'<footer.*?</footer>', footer_html, content, flags=re.DOTALL)
        else:
            # Inject before </body>
            content = content.replace('</body>', f'{footer_html}\n</body>')
            
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated {file_name}')
    else:
        print(f'File {file_name} not found')
