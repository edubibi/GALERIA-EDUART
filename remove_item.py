import json

def remove_item(item_id):
    try:
        with open('metadata.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if item_id in data:
            del data[item_id]
            print(f"Removed {item_id} from metadata.")
            
            with open('metadata.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        else:
            print(f"Item {item_id} not found in metadata.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    remove_item("02cubesse_stilo_006")
