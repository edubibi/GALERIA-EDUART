import json
import os

# Define descriptions based on titles
descriptions = {
    "sello_magico_001": "El Acueducto de Segovia es una obra de ingeniería civil romana, la más importante de las construidas en la península ibérica. Se data a principios del siglo II d.C.",
    "sello_magico_002": "El Arco de la Victoria (Moncloa) es un arco de triunfo construido entre 1950 y 1956 para conmemorar la victoria del bando sublevado en la batalla de la Ciudad Universitaria.",
    "sello_magico_003": "Carlos I de España y V del Sacro Imperio Romano Germánico. Una de las figuras más potentes de la historia europea, reinó en todos los dominios españoles y en el Sacro Imperio.",
    "sello_magico_004": "La Catedral de Santiago de Compostela, meta final del Camino de Santiago. Obra maestra del románico, gótico y barroco.",
    "sello_magico_005": "Vista de la fachada del Obradoiro de la Catedral de Santiago, símbolo de la peregrinación cristiana en Europa.",
    "sello_magico_006": "Miguel de Cervantes Saavedra, máxima figura de la literatura española y autor de 'El Ingenioso Hidalgo Don Quijote de la Mancha'.",
    "sello_magico_007": "Conmemoración del Año Santo Jacobeo en Santiago de Compostela.",
    "sello_magico_008": "Sello conmemorativo de la integración y el espíritu de Europa.",
    "sello_magico_009": "Emisión conmemorativa de la Constitución Española de 1978, la norma suprema del ordenamiento jurídico español.",
    "sello_magico_010": "Sello de 1951 conmemorando a Cristóbal Colón y el descubrimiento de América.",
    "sello_magico_011": "Retrato de Cristóbal Colón, navegante y almirante que lideró la expedición que llegó a América en 1492.",
    "sello_magico_012": "El Cid Campeador (Rodrigo Díaz de Vivar), líder militar castellano y héroe nacional de la Reconquista.",
    "sello_magico_013": "Francisco Franco, jefe de Estado durante la dictadura en España (1939-1975).",
    "sello_magico_014": "Representación de Don Quijote de la Mancha, la obra cumbre de la literatura universal.",
    "sello_magico_015": "Fernando II de Aragón, 'El Católico', artífice junto a Isabel de la unidad dinástica de España.",
    "sello_magico_016": "Fernando VII, rey de España. Su reinado estuvo marcado por la Guerra de Independencia y la pérdida de las colonias americanas.",
    "sello_magico_017": "Efigie de Francisco Franco en emisión de 1955.",
    "sello_magico_018": "Isabel la Católica, reina de Castilla. Sello conmemorativo de 1964.",
    "sello_magico_019": "Isabel la Católica y Cervantes, uniendo la historia monárquica con la literaria.",
    "sello_magico_020": "Isabel I de Castilla, 'La Católica', figura clave en la financiación del viaje de Colón y la finalización de la Reconquista.",
    "sello_magico_021": "Juan Carlos I, Rey de España. Sello de 1966 cuando aún era Príncipe de España.",
    "sello_magico_022": "Los Reyes Juan Carlos I y Sofía de Grecia, símbolos de la Transición y la monarquía parlamentaria.",
    "sello_magico_023": "Juan de la Cierva, ingeniero inventor del autogiro, precursor del helicóptero moderno.",
    "sello_magico_024": "Serie dedicada a la Fauna Ibérica, destacando la biodiversidad de la península.",
    "sello_magico_025": "Lope de Vega, el 'Fénix de los Ingenios', uno de los más prolíficos poetas y dramaturgos del Siglo de Oro.",
    "sello_magico_026": "Monasterio de San Lorenzo de El Escorial, residencia histórica de la Familia Real Española y panteón de reyes.",
    "sello_magico_027": "Francisco Pizarro, conquistador del Imperio Inca y fundador de la ciudad de Lima.",
    "sello_magico_028": "Santiago Ramón y Cajal, Premio Nobel de Medicina en 1906, padre de la neurociencia moderna. Emisión de 1955.",
    "sello_magico_029": "Templo Expiatorio de la Sagrada Familia en Barcelona, obra maestra de Antoni Gaudí y máximo exponente del modernismo catalán.",
    "sello_magico_030": "José de San Martín, libertador de Argentina, Chile y Perú. Homenaje a los vínculos con América.",
    "sello_magico_031": "Diego Velázquez, pintor barroco, considerado uno de los máximos exponentes de la pintura española y maestro de la pintura universal.",
    "sello_magico_032": "Autorretrato o detalle de obra de Diego Velázquez. Pintor de cámara de Felipe IV."
}

metadata_path = 'metadata.json'

def update_metadata():
    if not os.path.exists(metadata_path):
        print("Metadata file not found!")
        return

    with open(metadata_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    count = 0
    for key, desc in descriptions.items():
        if key in data:
            data[key]['description'] = desc
            data[key]['price'] = "Colección" # Set generic price/status
            count += 1
        else:
            print(f"Warning: Key {key} not found in metadata.")

    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"Updated {count} items in metadata.json")

if __name__ == "__main__":
    update_metadata()
