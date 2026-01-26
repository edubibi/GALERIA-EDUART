import json

def update_variants():
    with open('metadata.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Update 12cristal_cubico_001
    if "12cristal_cubico_001" in data:
        print("Updating 12cristal_cubico_001...")
        data["12cristal_cubico_001"]["description"] = "Técnica: Aunque está en este bloque, es la pieza puente. Usa la base del cubismo pero con las grietas del estilo cristal.\nVisual: La luz es mucho más suave y los bordes menos afilados que en la versión pura de CUBESSE."
        data["12cristal_cubico_001"]["tech_info"] = "Ver descripción detallada."

    # Update 02cubesse_stilo_013
    if "02cubesse_stilo_013" in data:
        print("Updating 02cubesse_stilo_013...")
        data["02cubesse_stilo_013"]["description"] = "Técnica: Es la pieza más equilibrada. El jarrón tiene una curvatura sugerida mediante 12 o 14 planos verticales de luz.\nVisual: La mesa se funde con el suelo en un degradado de polígonos marrones, eliminando la línea del horizonte."
        data["02cubesse_stilo_013"]["tech_info"] = "Ver descripción detallada."

    with open('metadata.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print("Variants updated.")

if __name__ == "__main__":
    update_variants()
