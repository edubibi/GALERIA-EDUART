import json
import os

METADATA_FILE = "metadata.json"

descriptions_33minigestpoetic = {
    "amor_y_perdida": {
        "title": "Amor Y Pérdida",
        "description": "Una poderosa alegoría visual que representa la unión y la fractura. Dos manos entrelazadas formadas por raíces se alzan sobre un corazón agrietado, simbolizando la dualidad entre el afecto y el dolor.",
        "tech_info": "Estilo MINIGESTPOETIC: Arte conceptual de corte gestual y poético. Utiliza una paleta restringida y un lenguaje simbólico para explorar temas existenciales. El contraste entre el vacío y la forma busca generar una respuesta emocional."
    },
    "el_eterno_suspiro_del_tiempo": {
        "title": "El Eterno Suspiro Del Tiempo",
        "description": "Un árbol de luz que emerge de un tocón ancestral, conectado por un haz de energía pura en el centro de un vórtice oscuro. Reflexiona sobre la continuidad de la memoria más allá de la existencia física.",
        "tech_info": "Estilo MINIGESTPOETIC: Arte conceptual de corte gestual y poético. Utiliza una paleta restringida y un lenguaje simbólico para explorar temas existenciales. El contraste entre el vacío y la forma busca generar una respuesta emocional."
    },
    "el_ojo_del_cazador": {
        "title": "El Ojo Del Cazador",
        "description": "Una mirada penetrante que emerge de las sombras, capturando la esencia de la vigilancia y el instinto. Invita a cuestionar quién es el observador y quién el observado en el ciclo de la vida.",
        "tech_info": "Estilo MINIGESTPOETIC: Arte conceptual de corte gestual y poético. Utiliza una paleta restringida y un lenguaje simbólico para explorar temas existenciales. El contraste entre el vacío y la forma busca generar una respuesta emocional."
    },
    "el_primer_suspiro_del_cielo": {
        "title": "El Primer Suspiro Del Cielo",
        "description": "Un punto de luz central que irradia energía en un firmamento de partículas cósmicas. Representa el nacimiento de una idea o el origen de un nuevo mundo en una explosión de fuerza elemental.",
        "tech_info": "Estilo MINIGESTPOETIC: Arte conceptual de corte gestual y poético. Utiliza una paleta restringida y un lenguaje simbólico para explorar temas existenciales. El contraste entre el vacío y la forma busca generar una respuesta emocional."
    },
    "golpe_de_una_gota_en_el_oceano": {
        "title": "Gota En El Océano",
        "description": "La caligrafía del alma se funde con el movimiento del agua. Trazos gestuales que evocan palabras perdidas en el flujo del tiempo, recordándonos que cada pequeña acción genera ondas en la inmensidad.",
        "tech_info": "Estilo MINIGESTPOETIC: Arte conceptual de corte gestual y poético. Utiliza una paleta restringida y un lenguaje simbólico para explorar temas existenciales. El contraste entre el vacío y la forma busca generar una respuesta emocional."
    },
    "la_arquitectura_respira": {
        "title": "La Arquitectura Respira",
        "description": "Una torre estilizada que se eleva hacia un cielo turbulento, actuando como un faro de conciencia. Sugiere la resistencia de la voluntad humana frente al caos orgánico del infinito.",
        "tech_info": "Estilo MINIGESTPOETIC: Arte conceptual de corte gestual y poético. Utiliza una paleta restringida y un lenguaje simbólico para explorar temas existenciales. El contraste entre el vacío y la forma busca generar una respuesta emocional."
    },
    "suspiro_cosmico_del_ser": {
        "title": "Suspiro Cósmico Del Ser",
        "description": "Un cerebro formado por constelaciones de estrellas y redes neuronales celestes que flotan sobre nubes. Explora la conexión íntima entre el pensamiento humano y el tejido del universo.",
        "tech_info": "Estilo MINIGESTPOETIC: Arte conceptual de corte gestual y poético. Utiliza una paleta restringida y un lenguaje simbólico para explorar temas existenciales. El contraste entre el vacío y la forma busca generar una respuesta emocional."
    }
}

descriptions_28espatac = {
    "arrozales_de_yuanyang_en_yunnan": {
        "title": "Arrozales De Yunnan",
        "description": "Los arrozales en terraza de Yunnan descienden por la montaña como espejos de colores. La luz crea un mosaico vibrante de ocres y verdes bajo un cielo de nubes bajas.",
        "tech_info": "Estilo ESPATAC (China): Técnica de espátula y óleo texturizado para capturar la majestuosidad de Asia. El uso del color y el relieve busca transmitir la vibración espiritual y la escala monumental."
    },
    "el_parque_nacional_de_zhāngjiājiè": {
        "title": "Zhāngjiājiè (Montañas Avatar)",
        "description": "Los pilares de cuarcita de Zhangjiajie se elevan entre la niebla. La luz dorada destaca las crestas rocosas y la vegetación resiliente que corona estas montañas legendarias.",
        "tech_info": "Estilo ESPATAC (China): Técnica de espátula y óleo texturizado para capturar la majestuosidad de Asia. El uso del color y el relieve busca transmitir la vibración espiritual y la escala monumental."
    },
    "gran_buda_de_leshan": {
        "title": "Gran Buda De Leshan",
        "description": "El imponente rostro del Buda gigante excavado en la roca roja, rodeado de vegetación exuberante. Captura la serenidad monumental de este tesoro histórico sobre el río.",
        "tech_info": "Estilo ESPATAC (China): Técnica de espátula y óleo texturizado para capturar la majestuosidad de Asia. El uso del color y el relieve busca transmitir la vibración espiritual y la escala monumental."
    },
    "los_guerreros_de_xi’an": {
        "title": "Guerreros De Xi'An",
        "description": "Las infinitas hileras del ejército de terracota en su foso sagrado. La pincelada dinámica resalta la individualidad de cada guerrero y la solemnidad de este entierro imperial.",
        "tech_info": "Estilo ESPATAC (China): Técnica de espátula y óleo texturizado para capturar la majestuosidad de Asia. El uso del color y el relieve busca transmitir la vibración espiritual y la escala monumental."
    },
    "zhouzhuang": {
        "title": "Pueblo Del Agua Zhouzhuang",
        "description": "Un canal tranquilo en Zhouzhuang con sauces llorones que acarician la superficie. Un pabellón tradicional se refleja en el agua, evocando una paz milenaria.",
        "tech_info": "Estilo ESPATAC (China): Técnica de espátula y óleo texturizado para capturar la majestuosidad de Asia. El uso del color y el relieve busca transmitir la vibración espiritual y la escala monumental."
    }
}

def apply_descriptions_v2():
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    count = 0
    # Apply 33MINIGESTPOETIC
    for key, info in descriptions_33minigestpoetic.items():
        if key in data:
            data[key]["title"] = info["title"]
            data[key]["description"] = info["description"]
            data[key]["tech_info"] = info["tech_info"]
            count += 1
            print(f"Updated: {key}")

    # Apply 28ESPATAC
    for key, info in descriptions_28espatac.items():
        if key in data:
            data[key]["title"] = info["title"]
            data[key]["description"] = info["description"]
            data[key]["tech_info"] = info["tech_info"]
            count += 1
            print(f"Updated: {key}")

    if count > 0:
        with open(METADATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"\nSUCCESS: Applied descriptions to {count} additional items.")
    else:
        print("No items found to update.")

if __name__ == "__main__":
    apply_descriptions_v2()
