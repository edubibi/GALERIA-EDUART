import re
import json
import os

DATA_FILE = "js/data.js"

# --- STYLE DICTIONARY ---
STYLES = {
    "00EDUSSE": {
        "visual": "Una composición de surrealismo icónico, caracterizada por la presencia de elementos ingrávidos y una paleta sofisticada de negros profundos y acentos dorados.",
        "tech": "Técnica mixta digital que combina modelado 3D para las estructuras centrales con pintura digital para los detalles atmosféricos. Iluminación global renderizada."
    },
    "01EXP_NEOCIRC": {
        "visual": "Paisajismo onírico que desafía la lógica arquitectónica. Colores vibrantes y saturados construyen ciudades y entornos que parecen sacados de un sueño lúcido.",
        "tech": "Manipulación de perspectiva y 'Digital Collage' avanzado. Uso de capas de ajuste de color selectivo para crear la atmósfera vibrante característica."
    },
    "02CUBESSE stilo": {
        "visual": "Dinamismo geométrico. La imagen se fragmenta en facetas angulares que sugieren movimiento y velocidad, recordando al cubismo analítico pero con limpieza digital.",
        "tech": "Algoritmos de teselación y fragmentación poligonal. Mapeado de texturas sobre formas geométricas planas."
    },
    "03EXPNEOPLUS": {
        "visual": "Una evolución del paisaje clásico hacia una estética hiper-realista y luminosa. Destaca por la claridad atmosférica y la integración de elementos naturales y arquitectónicos.",
        "tech": "Fotocomposición de alto rango dinámico (HDR) procesada con filtros de suavizado y realce de detalles finos."
    },
    "04APLICC": {
        "visual": "Abstracción aplicada con patrones repetitivos y texturas que recuerdan a tejidos o superficies industriales decoradas.",
        "tech": "Generación procedural de patrones y texturizado UV sobre superficies complejas."
    },
    "05PLUMINK": {
        "visual": "La delicadeza de la tinta china fusionada con la precisión vectorial. Trazos fluidos que parecen flotar sobre el papel digital.",
        "tech": "Simulación de fluidos de tinta y pinceles de acuarela digital con control de opacidad y sangrado."
    },
    "06IDE_CLASSIC": {
        "visual": "Un retorno a la estética clásica, con composiciones equilibradas y temas atemporales, reinterpretados con la nitidez del medio digital.",
        "tech": "Pintura digital tradicional (Wacom) emulando técnicas de óleo y barniz."
    },
    "07NEOINK stilo": {
        "visual": "Gráfismo de alto impacto. Líneas negras sólidas definen las formas, con rellenos de color plano o degradados sutiles. Estética cómic/ilustración moderna.",
        "tech": "Inking digital vectorial con coloración cel-shading."
    },
    "08BORACARBON": {
        "visual": "Dramatismo monocromo. Un uso magistral del blanco y negro para evocar soledad, nostalgia o fuerza. El contraste es el protagonista.",
        "tech": "Simulación de carboncillo y grafito. Mapeo de tonos a escala de grises con preservación de grano y textura de papel."
    },
    "09FRACNEO": {
        "visual": "La belleza matemática de la naturaleza. Formas que se repiten a diferentes escalas, creando estructuras orgánicas complejas y fascinantes.",
        "tech": "Geometría fractal generada por algoritmos recursivos. Renderizado de partículas."
    },
    "10OLEOCUBBO": {
        "visual": "La materialidad del óleo llevada al cubismo. Se puede 'sentir' el grosor de la pintura en cada faceta geométrica.",
        "tech": "Simulación de física de fluidos viscosos (Impasto) aplicada sobre una malla geométrica cubista."
    },
    "11URBANSPHERIC": {
        "visual": "La ciudad como organismo vivo. Perspectivas esféricas o distorsionadas que capturan la inmensidad del entorno urbano.",
        "tech": "Proyección panorámica y deformación de lente (Ojo de pez) sobre entornos 3D urbanos."
    },
    "12CRISTAL_CUBICO": {
        "visual": "Transparencia y refracción. El mundo visto a través de un prisma de cristal, descomponiendo la luz y las formas.",
        "tech": "Renderizado de trazado de rayos (Ray Tracing) calculando refracciones complejas y cáusticas."
    },
    "13RECTESSE": {
        "visual": "Rigurosidad ortogonal. Composiciones basadas en líneas rectas y ángulos de 90 grados, transmitiendo orden y estructura.",
        "tech": "Diseño constructivista asistido por rejillas digitales y alineación vectorial perfecta."
    },
    "14TEREXSE": {
        "visual": "Exploración de terrenos y texturas orgánicas complejas. Paisajes que parecen de otro planeta.",
        "tech": "Generación de terrenos procedurales mediante mapas de altura y desplazamiento."
    },
    "15CUBESSEPLUS": {
        "visual": "Cubismo evolucionado con mayor detalle y profundidad de campo. Más complejo que el Cubesse tradicional.",
        "tech": "Modelado low-poly con suavizado selectivo y texturizado PBR (Physically Based Rendering)."
    },
     "16EXPNEO": {
        "visual": "Experimentación neofuturista con luces de neón y atmósferas nocturnas.",
        "tech": "Iluminación volumétrica y efectos de resplandor (Bloom) digitales."
    },
    "17FUZZTESS": {
        "visual": "Bordes difusos y atmósferas de ensueño ('Fuzzy'). La imagen parece emerger de la niebla.",
        "tech": "Filtros de desenfoque gaussiano selectivo y ruido procedural suave."
    },
    "18ABSTRACTO_CONFLUENCIA": {
        "visual": "El punto de encuentro de formas y colores sin referencia figurativa clara. Pura emoción visual.",
        "tech": "Abstracción generativa basada en campos de flujo y mezcla de color aditiva."
    },
    "19FUZZLINE_ABS": {
        "visual": "Líneas vibrantes y difusas que crean formas abstractas en movimiento.",
        "tech": "Trazado de líneas con bordes suavizados y variación de opacidad aleatoria."
    },
    "20BORASSIE": {
        "visual": "Una variante del estilo Bora, quizás introduciendo elementos de color selectivo o mayor suavidad.",
        "tech": "Técnica mixta de grafito digital con lavados de acuarela muy sutiles."
    },
    "21OCE-BURST": {
        "visual": "Explosiones oceánicas. Fluidez, agua, movimiento caótico y energía azul.",
        "tech": "Simulación de fluidos de partículas realistas congelados en un instante de tiempo."
    },
    "22NEO-LUMINA": {
        "visual": "La luz como materia. Composiciones donde la fuente de luz es la protagonista absoluta.",
        "tech": "Motor de renderizado espectral enfocado en la dispersión de la luz."
    },
    "23TRIDIM-BURST": {
        "visual": "Explosiones tridimensionales de objetos y formas que salen del plano.",
        "tech": "Sistemas de partículas 3D con fuerzas de explosión y gravedad simuladas."
    },
    "24BORACARBON MONUMENTOS": {
        "visual": "La monumentalidad arquitectónica en blanco y negro. Solemne, eterno y pétreo.",
        "tech": "Fotogrametría digital procesada en escala de grises de alto contraste."
    },
    "25CAPLIVE": {
        "visual": "Captura de vida. Escenas cotidianas con un toque vibrante y contemporáneo.",
        "tech": "Estilo 'Street Photography' digital con post-procesado de color estilo cine."
    },
    "26CARL_LINE": {
        "visual": "Estilo lineal distintivo, probablemente caracterizado por el trazo continuo o minimalista.",
        "tech": "Dibujo vectorial de línea continua."
    },
    "27LINEVORT": {
        "visual": "Vórtices de líneas que arrastran la mirada hacia el centro o puntos de fuga infinitos.",
        "tech": "Generación de campos vectoriales en espiral."
    },
    "28ESPATAC": {
        "visual": "Mezcla Óptica y vibrante. El azul oscuro, el turquesa y el reflejo amarillo no están mezclados, sino yuxtapuestos, dejando que el ojo cree la vibración. Construcción por Bloques: como teselas de un mosaico.",
        "tech": "Espatulado Puro (Knife Painting) y Heavy Impasto. No se arrastran líneas, se depositan cargas rectangulares de pintura con espátula plana, dejando relieve y la huella de la herramienta."
    },
    "SELLOS_MAGICOS": {
        "visual": "Pequeñas obras de arte contenidas, con estética filatélica o de grabado antiguo.",
        "tech": "Simulación de grabado en metal y texturizado de papel antiguo."
    }
}

DEFAULT_STYLE = {
    "visual": "Una obra singular dentro del catalogo Edusse, explorando la relación entre forma y color.",
    "tech": "Arte digital de alta resolución."
}

# --- KEYWORD NARRATIVES ---
# Dictionary of keywords (lowercase) to narrative snippets
KEYWORDS = {
    "lluvia": "La atmósfera se carga de nostalgia bajo la cortina de agua, sugiriendo un tiempo detenido y una reflexión interior.",
    "new york": "El pulso frenético de la metrópolis se captura en esta pieza, donde el hormigón y los sueños verticales colisionan.",
    "ny": "El pulso frenético de la metrópolis se captura en esta pieza, donde el hormigón y los sueños verticales colisionan.",
    "mujer": "La figura femenina emerge como fuerza central, explorando la identidad y la presencia en un entorno cambiante.",
    "caballo": "La nobleza del animal se traduce en líneas de fuerza y libertad, un símbolo de naturaleza indómita.",
    "bodegon": "Una revisión contemporánea de la naturaleza muerta, donde los objetos cotidianos cobran una nueva vida simbólica.",
    "pueblo": "La memoria de lo rural y la arquitectura vernácula se entrelazan, evocando raíces y pertenencia.",
    "mar": "La inmensidad del océano se convierte en espejo del subconsciente, con sus mareas y su calma tensa.",
    "pesca": "El oficio ancestral y la relación del hombre con el mar se plasman con respeto y luminosidad.",
    "gudarian": "Una entidad protectora que vigila el umbral entre lo tecnológico y lo sagrado.",
    "catedral": "La verticalidad espiritual se encuentra con la ingravidez, creando un templo para la era etérea.",
    "barco": "La travesía y el viaje como metáforas de la existencia, navegando aguas de incertidumbre cromática.",
    "reloj": "El tiempo, implacable y elástico, se descompone en esta pieza, cuestionando la cronología lineal.",
    "toro": "Fuerza bruta y mitología ibérica se sincretizan en una forma poderosa y telúrica.",
    "cisne": "La elegancia fractal se manifiesta en la curva del cuello, un estudio sobre la perfección matemática de la biología.",
    "avestruz": "Lo insólito y lo exótico se dan la mano en una composición que desafía las expectativas con humor y surrealismo.",
    "abuelo": "El peso de la experiencia y las arrugas de la historia se dibujan con respeto y profundidad emocional.",
    "niños": "La inocencia y el juego se capturan como instantes de luz pura en un mundo complejo.",
    "paris": "El romanticismo urbano y la bohemia de antaño reviven bajo una luz nueva.",
    "london": "La niebla y la historia imperial se funden en una atmósfera densa y literaria.",
    "desierto": "La soledad árida revela una belleza desnuda, donde la luz es la única protagonista.",
    "noche": "El misterio nocturno envuelve la escena, revelando lo que la luz del día esconde."
}

# --- SPECIFIC OVERRIDES ---
OVERRIDES = {
    "Hollywood": "Una visión crítica y estética de las viviendas turísticas en la parte sur, contrastando el glamour del nombre con la realidad arquitectónica local.",
    "Avestruz Del Universo Edusse": "El cuerpo del ave funciona como un portal; en su interior se observa una aldea bajo un sol dorado. Representa la libertad y la vigilancia espiritual; el ave no solo vuela por el mundo, sino que lo lleva dentro de sí.",
    "La Vaca Solar Y El Rio De Signos": "Representa la fuerza de la tierra y la civilización. Es la 'Bestia del Mundo' que sostiene el conocimiento y las ciudades sobre su lomo y en sus entrañas, posada sobre un mandala rúnico.",
    "El Guardian Del Circuito Solar": "El mastín actúa como un guardián de mirada profunda y humana. Los símbolos a sus pies refuerzan la idea de un protector de antiguos secretos, contrastando con el río serpenteante que simboliza el paso del tiempo."
}

def generate_narrative(title, category):
    # 1. Check Specific Override
    if title in OVERRIDES:
        return OVERRIDES[title]

    # 2. Check Keywords
    title_lower = title.lower()
    for key, text in KEYWORDS.items():
        if key in title_lower:
            return f"{text} En '{title}', la técnica realza este concepto con una ejecución precisa."

    # 3. Fallback to Style Generic (Standard Option B)
    style = STYLES.get(category, DEFAULT_STYLE)
    return f"{style['visual']} Esta obra, '{title}', es un ejemplo vibrante de la narrativa visual de la colección."

def load_custom_descriptions(file_path):
    custom_map = {}
    current_id = None
    current_tech = ""
    current_visual = ""
    
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} not found.")
        return custom_map

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line in lines:
        line = line.strip()
        if not line: continue
        
        # Match ID line: "Title (filename.jpg):"
        # We need to map filename to ID. ID is usually filename without extension.
        id_match = re.search(r'\((.+?)\):', line)
        if id_match:
            filename = id_match.group(1)
            current_id = os.path.splitext(filename)[0].lower() # "02cubesse_stilo_001"
            continue
            
        if line.startswith("Técnica:"):
            current_tech = line.replace("Técnica:", "").strip()
        elif line.startswith("Visual:"):
            current_visual = line.replace("Visual:", "").strip()
            
        if current_id and current_tech and current_visual:
            custom_map[current_id] = {
                "tech": current_tech,
                "visual": current_visual
            }
            # Reset for next block
            current_id = None
            current_tech = ""
            current_visual = ""
            
    return custom_map

def enrich():
    # Load custom descriptions
    custom_descriptions = load_custom_descriptions("new_descriptions.txt")
    print(f"Loaded {len(custom_descriptions)} custom descriptions.")

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    new_lines = []
    current_category = None
    current_title = ""
    current_id = ""
    
    lines = content.split('\n')
    for line in lines:
        stripped = line.strip()
        
        # Extract Category
        # Matches "category": "Value" or category: "Value"
        cat_match = re.search(r'"?category"?:\s*"([^"]+)"', line)
        if cat_match:
            current_category = cat_match.group(1)
            
        # Extract Title
        title_match = re.search(r'"?title"?:\s*"([^"]+)"', line)
        if title_match:
            current_title = title_match.group(1)

        # Extract ID (Crucial for mapping)
        id_match = re.search(r'"?id"?:\s*"([^"]+)"', line)
        if id_match:
            current_id = id_match.group(1)

        
        # Replace Description
        # Check for "description": or description:
        if re.match(r'"?description"?:\s*', stripped):
            # Priority 1: Custom Map via ID
            if current_id in custom_descriptions:
                desc = custom_descriptions[current_id]["visual"]
                desc_tech = custom_descriptions[current_id]["tech"]
                narrative = f"{desc_tech} {desc}"
                
                # Preserve indent
                # We split by colon to keep left side
                part_before = line.split(':', 1)[0] + ':' 
                new_lines.append(f'{part_before} "{narrative}",')
                continue

            # Priority 2: Overrides by Title
            if current_title and current_title in OVERRIDES:
                narrative = OVERRIDES[current_title]
                part_before = line.split(':', 1)[0] + ':'
                new_lines.append(f'{part_before} "{narrative}",')
                continue
            
            # Priority 3: Keywords or Category Default
            if current_category:
                narrative = generate_narrative(current_title, current_category)
                part_before = line.split(':', 1)[0] + ':'
                new_lines.append(f'{part_before} "{narrative}",')
                continue
        
        # Replace Tech Info
        if re.match(r'"?tech_info"?:\s*', stripped):
            # Priority 1: Custom Map via ID
            if current_id in custom_descriptions:
                 tech_text = custom_descriptions[current_id]["tech"]
                 part_before = line.split(':', 1)[0] + ':'
                 new_lines.append(f'{part_before} "{tech_text}",')
                 continue

            if current_category:
                style = STYLES.get(current_category, DEFAULT_STYLE)
                tech_text = style["tech"]
                part_before = line.split(':', 1)[0] + ':'
                new_lines.append(f'{part_before} "{tech_text}",')
                continue

        # Reset
        if stripped == "}," or stripped == "}":
            current_category = None
            current_title = ""
            current_id = ""

        new_lines.append(line)

    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    
    print("Data enriched with NARRATIVES successfully.")

if __name__ == "__main__":
    enrich()
