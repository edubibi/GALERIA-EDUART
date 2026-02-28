import json
import os

METADATA_FILE = "metadata.json"

descriptions_31olenatur = {
    "acantilado_escocia": {
        "title": "Faro en el Acantilado Escocés",
        "description": "Un faro solitario en lo alto de un imponente acantilado escocés, desafiando la inmensidad del océano. La luz del atardecer tiñe las nubes de naranja y fuego, mientras los rayos del faro perforan la bruma que envuelve la costa.",
        "tech_info": "Estilo OLEO NATUR: Técnica de pincelada digital con acabado de óleo tradicional (impasto). Los colores vibrantes y la textura marcada buscan capturar la esencia de la luz y el movimiento en paisajes icónicos."
    },
    "arc_du_triumph": {
        "title": "Arc De Triomphe París",
        "description": "El majestuoso Arco del Triunfo de París en una escena vibrante de la ciudad. El estilo impasto resalta la textura de la piedra histórica y el dinamismo de los coches y peatones que circulan bajo un cielo azul despejado.",
        "tech_info": "Estilo OLEO NATUR: Técnica de pincelada digital con acabado de óleo tradicional (impasto). Los colores vibrantes y la textura marcada buscan capturar la esencia de la luz y el movimiento en paisajes icónicos."
    },
    "coliseum_de_roma": {
        "title": "Coliseo De Roma",
        "description": "El Coliseo de Roma reconstruido mediante pinceladas gruesas y enérgicas. La luz del sol mediterráneo esculpe las arquerías milenarias, contrastando con un cielo de nubes algodonosas que parecen girar alrededor de la historia viva.",
        "tech_info": "Estilo OLEO NATUR: Técnica de pincelada digital con acabado de óleo tradicional (impasto). Los colores vibrantes y la textura marcada buscan capturar la esencia de la luz y el movimiento en paisajes icónicos."
    },
    "en_un_dia_en_japon": {
        "title": "Noche En Tokio",
        "description": "Una callejuela de Tokio en una noche lluviosa, iluminada por el neón de los carteles y los reflejos en el asfalto mojado. Los transeúntes con paraguas avanzan bajo un cielo eléctrico, capturando la esencia futurista y melancólica.",
        "tech_info": "Estilo OLEO NATUR: Técnica de pincelada digital con acabado de óleo tradicional (impasto). Los colores vibrantes y la textura marcada buscan capturar la esencia de la luz y el movimiento en paisajes icónicos."
    },
    "estatua_de_la_libertad": {
        "title": "Estatua De La Libertad NY",
        "description": "La Estatua de la Libertad se alza como un faro de esperanza sobre el puerto de Nueva York. El cielo y el agua se funden en un festival de azules y blancos, donde la pincelada expresionista da vida a la icónica silueta.",
        "tech_info": "Estilo OLEO NATUR: Técnica de pincelada digital con acabado de óleo tradicional (impasto). Los colores vibrantes y la textura marcada buscan capturar la esencia de la luz y el movimiento en paisajes icónicos."
    },
    "new_york_bridge_olo": {
        "title": "Puente De Brooklyn NY",
        "description": "El puente de Brooklyn se extiende con su arquitectura de acero y piedra sobre el East River. El skyline de Manhattan asoma al fondo entre nubes texturizadas, en una composición que celebra la ingeniería monumental y la energía urbana.",
        "tech_info": "Estilo OLEO NATUR: Técnica de pincelada digital con acabado de óleo tradicional (impasto). Los colores vibrantes y la textura marcada buscan capturar la esencia de la luz y el movimiento en paisajes icónicos."
    },
    "pareja_en_el_parque": {
        "title": "Paseo Bajo Las Farolas",
        "description": "Una escena romántica bajo la luz de las farolas en un parque nocturno. Una pareja camina de la mano mientras las hojas de los árboles, bañadas en luz dorada, crean una atmósfera íntima y soñadora sobre el camino mojado.",
        "tech_info": "Estilo OLEO NATUR: Técnica de pincelada digital con acabado de óleo tradicional (impasto). Los colores vibrantes y la textura marcada buscan capturar la esencia de la luz y el movimiento en paisajes icónicos."
    },
    "parque_impresion": {
        "title": "Parque Impresionista",
        "description": "Un parque sumergido en la quietud de la noche, donde las farolas proyectan una luz cálida sobre el sendero y los árboles. La técnica de espátula crea una vibración lumínica que transforma el paisaje cotidiano en un sueño.",
        "tech_info": "Estilo OLEO NATUR: Técnica de pincelada digital con acabado de óleo tradicional (impasto). Los colores vibrantes y la textura marcada buscan capturar la esencia de la luz y el movimiento en paisajes icónicos."
    },
    "paseando_por_monmatre": {
        "title": "Lluvia En Montmartre",
        "description": "Una romántica escena en las calles de Montmartre con la Torre Eiffel al fondo. Una pareja camina bajo un paraguas rojo en un día lluvioso, rodeados de edificios clásicos y el reflejo de las luces en el suelo mojado.",
        "tech_info": "Estilo OLEO NATUR: Técnica de pincelada digital con acabado de óleo tradicional (impasto). Los colores vibrantes y la textura marcada buscan capturar la esencia de la luz y el movimiento en paisajes icónicos."
    },
    "torre_eifel": {
        "title": "Atardecer En La Torre Eiffel",
        "description": "La Torre Eiffel preside el Sena al atardecer. La luz cálida del sol poniente ilumina la estructura de hierro y se refleja en las aguas del río, en una vista clásica y evocadora de la Ciudad de la Luz.",
        "tech_info": "Estilo OLEO NATUR: Técnica de pincelada digital con acabado de óleo tradicional (impasto). Los colores vibrantes y la textura marcada buscan capturar la esencia de la luz y el movimiento en paisajes icónicos."
    }
}

descriptions_35paperchin = {
    "admiración": {
        "description": "Una entrañable escena rural donde un hombre contempla a su fiel caballo en un prado verde frente a imponentes montañas nevadas. La técnica de relieve resalta la textura de la hierba y el pelaje del animal.",
        "tech_info": "Estilo PAPERCHIN: Técnica de simulación de relieve y capas de papel aplicada digitalmente. Se enfoca en la profundidad visual y la simplificación de formas para crear escenas con gran impacto táctil."
    },
    "arco_del_triunfo_paperchin": {
        "description": "El Arco del Triunfo de París representado como una maqueta de papel, con un estilo minimalista y limpio. Los árboles y peatones son figuras sencillas que acompañan al icono bajo un cielo azul vibrante.",
        "tech_info": "Estilo PAPERCHIN: Técnica de simulación de relieve y capas de papel aplicada digitalmente. Se enfoca en la profundidad visual y la simplificación de formas para crear escenas con gran impacto táctil."
    },
    "bufalos": {
        "description": "Una manada de búfalos pastando en la pradera americana bajo un cielo inmenso de nubes algodonosas. La pincelada gruesa captura la fuerza bruta de los animales y la vastedad del paisaje del viejo oeste.",
        "tech_info": "Estilo PAPERCHIN: Técnica de simulación de relieve y capas de papel aplicada digitalmente. Se enfoca en la profundidad visual y la simplificación de formas para crear escenas con gran impacto táctil."
    },
    "elefantes": {
        "description": "Imponente retrato de una madre elefante y su cría en la selva. La técnica de capas resalta la rugosidad de la piel y los colmillos, mientras el fondo de vegetación tropical añade profundidad y misterio.",
        "tech_info": "Estilo PAPERCHIN: Técnica de simulación de relieve y capas de papel aplicada digitalmente. Se enfoca en la profundidad visual y la simplificación de formas para crear escenas con gran impacto táctil."
    },
    "en_el_oeste": {
        "description": "Una caravana de pioneros atraviesa la llanura en carretas tiradas por bueyes. Las montañas se vislumbran al fondo bajo un sol abrasador, capturando la epopeya de la colonización y la dureza del camino.",
        "tech_info": "Estilo PAPERCHIN: Técnica de simulación de relieve y capas de papel aplicada digitalmente. Se enfoca en la profundidad visual y la simplificación de formas para crear escenas con gran impacto táctil."
    },
    "monumentos__del_mundo": {
        "description": "Composición fantástica que reúne grandes iconos mundiales como el Big Ben y el Coliseo. El reflejo de las luces doradas en el agua y el cielo crepuscular crean una estampa de ensueño que celebra la herencia cultural.",
        "tech_info": "Estilo PAPERCHIN: Técnica de simulación de relieve y capas de papel aplicada digitalmente. Se enfoca en la profundidad visual y la simplificación de formas para crear escenas con gran impacto táctil."
    }
}

def apply_descriptions():
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    count = 0
    # Apply 31OLENATUR
    for key, info in descriptions_31olenatur.items():
        if key in data:
            data[key]["title"] = info["title"]
            data[key]["description"] = info["description"]
            data[key]["tech_info"] = info["tech_info"]
            count += 1
            print(f"Updated: {key}")

    # Apply 35PAPERCHIN
    for key, info in descriptions_35paperchin.items():
        if key in data:
            data[key]["description"] = info["description"]
            data[key]["tech_info"] = info["tech_info"]
            count += 1
            print(f"Updated: {key}")

    if count > 0:
        with open(METADATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"\nSUCCESS: Applied descriptions to {count} items.")
    else:
        print("No items found to update.")

if __name__ == "__main__":
    apply_descriptions()
