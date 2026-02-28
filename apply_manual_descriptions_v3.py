import json
import os

METADATA_FILE = "metadata.json"

descriptions_29espatac_mat = {
    "altamar_espatac-mat": {
        "title": "Remolcador en Altamar",
        "description": "Un robusto remolcador desafía el embate de las olas en un mar picado. La obra destaca por una técnica de espátula extremadamente matérica, donde bloques de color azul, gris y blanco construyen una sensación de fuerza y dinamismo oceánico.",
        "tech_info": "Óleo con espátula sobre lienzo. Serie ESPATAC-MAT: Enfoque en la textura física y la simplificación de formas mediante planos cromáticos rectangulares."
    },
    "el_parthenon_en_la_niebla_dorada": {
        "title": "El Partenón: Niebla de Oro",
        "description": "La icónica Acrópolis de Atenas emerge de una atmósfera onírica bañada en tonos sepia y dorados. La textura pesada imita la rugosidad del mármol antiguo y el paso de los milenios, creando un puente entre la historia y el sueño.",
        "tech_info": "Giclée retocado con textura manual. Serie ESPATAC-MAT: Técnica que enfatiza la tridimensionalidad de las ruinas clásicas."
    },
    "lago_batur_bali": {
        "title": "Templo en el Lago Batur",
        "description": "Una vista panorámica de la arquitectura balinesa tradicional frente al volcán Batur. La obra utiliza pinceladas rectangulares a modo de mosaico para representar la exuberante vegetación y los reflejos en el agua.",
        "tech_info": "Técnica mixta 'Mosaico Matérico'. Serie ESPATAC-MAT: Representación geométrica de paisajes naturales y sagrados."
    },
    "pueblo_costero_de_santorini": {
        "title": "Santorini: Laberinto Blanco",
        "description": "Las cúpulas azules y la arquitectura escalonada de Santorini se presentan en una composición de alto relieve. La técnica resalta la blancura cegadora de las casas sobre los acantilados de roca volcánica.",
        "tech_info": "Pintura acrílica de alta viscosidad. Serie ESPATAC-MAT: Enfoque en el volumen arquitectónico y el contraste cromático de las islas griegas."
    },
    "templo_en_la_colina esp": {
        "title": "El Refugio de los Dioses",
        "description": "Un antiguo templo se erige solitario sobre una formación rocosa. La paleta de tonos tierra y la textura escarpada evocan la soledad y la resistencia de los monumentos olvidados por el tiempo.",
        "tech_info": "Óleo sobre lienzo con carga matérica. Serie ESPATAC-MAT: Exploración de la simbiosis entre naturaleza y arquitectura antigua."
    },
    "templo_ulun_danu_bali": {
        "title": "Ulun Danu: Atardecer Sagrado",
        "description": "Las pagodas flotantes del templo Ulun Danu Beratan se reflejan en las aguas quietas durante el crepúsculo. La luz dorada se filtra a través de capas de textura que aportan profundidad y espiritualidad a la escena.",
        "tech_info": "Pintura con espátula y veladuras. Serie ESPATAC-MAT: Captura de la serenidad asiática mediante relieve táctil."
    }
}

descriptions_30olonatur_color = {
    "côte de granit rose de francia": {
        "title": "Costa de Granito Rosa",
        "description": "Un atardecer vibrante en la costa de Bretaña, donde las formaciones de granito rosa contrastan con un mar turquesa. Salpicaduras de pintura amarilla y roja aportan una energía expresionista y espontánea.",
        "tech_info": "Óleo impresionista con técnica de salpicado. Serie OLONATUR-COLOR: Paisajes naturales capturados con una paleta cromática intensa y libre."
    },
    "mont saint-michel francia": {
        "title": "La Abadía del Monte",
        "description": "El Mont Saint-Michel se alza como una fortaleza entre reflejos acuosos. La obra juega con la luz de Normandía, utilizando rojos y amarillos audaces para romper la sobriedad del cielo nublado.",
        "tech_info": "Óleo sobre lienzo. Serie OLONATUR-COLOR: Reinterpretación colorista de monumentos históricos franceses."
    },
    "paris cerca de notrdame": {
        "title": "Otoño en Notre Dame",
        "description": "Una vista de la catedral de París enmarcada por árboles en pleno estallido otoñal. La textura densa de las hojas y sus reflejos en el Sena crean un torbellino de color y nostalgia urbana.",
        "tech_info": "Pintura expresionista con espátula. Serie OLONATUR-COLOR: Captura de la atmósfera estacional en entornos urbanos icónicos."
    },
    "pont en royans de francia": {
        "title": "Las Casas Colgantes de Royans",
        "description": "Las pintorescas fachadas que parecen flotar sobre el río en Isère. La técnica libre y los colores saturados resaltan la vertiginosa verticalidad y el encanto rústico de este enclave.",
        "tech_info": "Técnica mixta sobre papel. Serie OLONATUR-COLOR: Estudio del color y la forma en la arquitectura vernácula francesa."
    },
    "colmar_francia": {
        "title": "Anochecer en Colmar",
        "description": "Los canales de la 'Pequeña Venecia' se iluminan al caer el sol. Las casas de entramado de madera se reflejan en el agua, creando una escena de cuento de hadas llena de luz cálida y sombras vibrantes.",
        "tech_info": "Óleo con matices luminiscentes. Serie OLONATUR-COLOR: Representación de la calidez nocturna en pueblos medievales."
    },
    "paseo_por_bulevares": {
        "title": "El Caminante Solitario",
        "description": "Una figura con chaqueta bicolor cruza un bulevar otoñal. La composición destaca por la explosión de rojos y dorados en los árboles y el dinamismo de la ciudad reflejada en el suelo mojado.",
        "tech_info": "Pintura expresionista. Serie OLONATUR-COLOR: Narrativa urbana centrada en el color y el movimiento estacional."
    }
}

descriptions_34expterico = {
    "expterico manchas": {
        "title": "Energía Primordial",
        "description": "Una explosión abstracta de pigmento donde el rosa, el naranja y el azul luchan por el espacio. Líneas negras dinámicas serpentean sobre la superficie, sugiriendo un flujo de energía vital incontrolable.",
        "tech_info": "Abstracción gestual profunda. Serie EXPTERICO: Exploración de las emociones puras a través de la mancha y el gesto automático."
    },
    "face": {
        "title": "Psique Fragmentada",
        "description": "Retrato masculino de rasgos marcados, reconstruido mediante planos de color crema, tostado y violeta. La mirada introspectiva y el uso audaz del relieve revelan la complejidad del pensamiento humano.",
        "tech_info": "Retrato contemporáneo matérico. Serie EXPTERICO: Humanismo abstracto enfocado en la arquitectura del rostro."
    },
    "manchas": {
        "title": "Genesis Cromática",
        "description": "Densa acumulación de materia pictórica en tonos oscuros y cálidos. La obra invita a la exploración táctil del óleo, representando la creación de un universo a partir del caos del color.",
        "tech_info": "Impasto extremo. Serie EXPTERICO: El color como entidad física y emocional autónoma."
    },
    "san francisco expterico": {
        "title": "Golden Gate: Vórtice Cósmico",
        "description": "El puente de San Francisco envuelto en un cielo psicodélico de espirales vibrantes. La ciudad se funde con el cosmos en un torbellino de color que desafía la realidad física del paisaje.",
        "tech_info": "Paisaje visionario. Serie EXPTERICO: Integración del paisaje urbano en visiones dinámicas y celestiales."
    },
    "tranvia": {
        "title": "El Pulso de la Ciudad",
        "description": "Un tranvía icónico atraviesa una atmósfera eléctrica de colores cálidos. El vehículo se convierte en un símbolo de estabilidad en medio de un torbellino de luz y pinceladas audaces.",
        "tech_info": "Expresionismo urbano dinámico. Serie EXPTERICO: Fusión de elementos cotidianos con atmósferas oníricas."
    }
}

def apply_descriptions_v3():
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    count = 0
    all_dicts = [descriptions_29espatac_mat, descriptions_30olonatur_color, descriptions_34expterico]
    
    for desc_dict in all_dicts:
        for key, info in desc_dict.items():
            # Standardize key (metadata uses lowercase for filenames)
            std_key = key.lower()
            if std_key in data:
                data[std_key]["title"] = info["title"]
                data[std_key]["description"] = info["description"]
                data[std_key]["tech_info"] = info["tech_info"]
                count += 1
                print(f"Updated: {std_key}")
            else:
                # Try with underscores or exact match if key had spaces
                print(f"WARNING: Key '{std_key}' not found in metadata.")

    if count > 0:
        with open(METADATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"\nSUCCESS: Applied descriptions to {count} additional items.")
    else:
        print("No items found to update.")

if __name__ == "__main__":
    apply_descriptions_v3()
