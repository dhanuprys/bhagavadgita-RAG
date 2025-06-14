import json

def json_dumps_hindi(data_list):
    return json.dumps(
        data_list,
        ensure_ascii=False,
        indent=4
    )
    
def json_load(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
    
raw_data = json_load('data/raw/verse.json')
level_2_fine = json_load('data/2-fine-translated_manual_ai/verses.json')

for verse in level_2_fine:
    found = False
    for raw_verse in raw_data:
        if raw_verse['id'] == verse['id']:
            verse['verse_number'] = raw_verse['verse_number']
            found = True
            break
        
    if not found:
        raise KeyError('Not found!', verse) 
    
with open('data/3-fine-verse_number/verses.json', 'w') as f:
    f.write(json_dumps_hindi(level_2_fine))