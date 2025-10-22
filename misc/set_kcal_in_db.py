import json
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from database.models import Products  # noqa: E402

async def import_products():
    values = await Products.all()
    if values:
        print('База не данных пуста')
    else:    
        json_path = os.path.join(project_root, 'parsed_products.json')
        
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        for item in data:
                bgu = item["bgu"].split(',')
                protein = float(bgu[0])
                fat = float(bgu[1])
                carbs = float(bgu[2])
                kcal = float(item['kcal'])
                name = item['name']
                
                await Products.create(
                    name=name.lower(),
                    protein=protein,
                    fat=fat, 
                    carbs=carbs,
                    kcal=kcal
                )
        print('Данные успешно импортированы')
                
        
