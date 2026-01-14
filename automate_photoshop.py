import os
import time
import win32com.client

# ================= CONFIGURACIÓN =================
# 📂 1. LA CARPETA DONDE ESTÁN TUS FOTOS
CARPETA_FOTOS = r"C:\FOTOS_PARA_RETOQUE"  # <--- ¡CAMBIA ESTO POR TU RUTA!

# 🎬 2. EL NOMBRE DE TU ACCIÓN Y SET (Tal como lo grabaste)
NOMBRE_ACCION = "BorrarMarca"
NOMBRE_SET = "MisRobots"

# 🖼️ 3. TIPOS DE ARCHIVO A PROCESAR
EXTENSIONES_VALIDAS = ('.jpg', '.jpeg', '.png', '.tif', '.tiff')
# =================================================

def procesar_fotos():
    # Verificar que la carpeta existe
    if not os.path.isdir(CARPETA_FOTOS):
        print(f"❌ ERROR: La carpeta no existe: {CARPETA_FOTOS}")
        print("👉 Abre este script y edita la variable CARPETA_FOTOS al principio.")
        return

    print(f"🚀 Iniciando Robot de Photoshop...")
    print(f"📂 Carpeta: {CARPETA_FOTOS}")
    print(f"🎬 Acción a ejecutar: '{NOMBRE_ACCION}' del set '{NOMBRE_SET}'")
    
    try:
        # Conectar con Photoshop
        app = win32com.client.Dispatch("Photoshop.Application")
        app.Visible = True # Opcional: ver lo que pasa
        
        # Obtener lista de archivos
        archivos = [f for f in os.listdir(CARPETA_FOTOS) if f.lower().endswith(EXTENSIONES_VALIDAS)]
        total = len(archivos)
        
        if total == 0:
            print("⚠️ No se encontraron imágenes en la carpeta.")
            return

        print(f"📸 Se encontraron {total} fotos. Empezando en 3 segundos...")
        time.sleep(3)

        for i, nombre_archivo in enumerate(archivos):
            ruta_completa = os.path.join(CARPETA_FOTOS, nombre_archivo)
            
            print(f"[{i+1}/{total}] Procesando: {nombre_archivo} ...")
            
            try:
                # 1. Abrir imagen
                doc = app.Open(ruta_completa)
                
                # 2. Ejecutar Acción
                # DoAction(ActionName, SetName)
                app.DoAction(NOMBRE_ACCION, NOMBRE_SET)
                
                # 3. La acción ya debería incluir "Guardar" y "Cerrar" si se grabó bien.
                # Pero por seguridad, si el documento sigue abierto, lo cerramos guardando.
                # Si la acción YA cerró el documento, esto dará error, así que lo manejamos.
                try:
                    if app.Documents.Count > 0:
                        # Si sigue abierto, guardamos y cerramos nosotros
                        doc.Close(1) # 1 = SaveChanges.Yes
                except:
                    # Probablemente el documento ya se cerró por la acción, todo bien.
                    pass
                    
            except Exception as e:
                print(f"⚠️ Error procesando {nombre_archivo}: {e}")
                continue

        print("\n✅ ¡LISTO! Proceso terminado.")

    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO AL CONECTAR CON PHOTOSHOP: {e}")
        print("Asegúrate de que Photoshop está abierto y que instalaste pywin32 (pip install pywin32)")

if __name__ == "__main__":
    procesar_fotos()
    input("\nPresiona ENTER para salir...")
