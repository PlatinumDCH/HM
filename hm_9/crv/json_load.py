import json

def save_to_json(data, filename):
    with open(filename,'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)