def text_meal(name, list_user_products):
    weight = 0
    calories = 0
    proteins = 0
    fats = 0
    carbohydrates = 0
    text = (f'Приём пищи: {name}\n'
            f'\n')
    for tuple_product in enumerate(list_user_products, start=1):
        text += (f"{tuple_product[0]}) {tuple_product[1]['name_product']}\n"
                 f"Вес: {tuple_product[1]['weight_product']}\n"
                 f"Калории: {tuple_product[1]['calories']}\n"
                 f"Б: {tuple_product[1]['proteins']} Ж: {tuple_product[1]['fats']} У: {tuple_product[1]['carbohydrates']}\n"
                 f"\n")
        weight += tuple_product[1]['weight_product']
        calories += tuple_product[1]['calories']
        proteins += tuple_product[1]['proteins']
        fats += tuple_product[1]['fats']
        carbohydrates += tuple_product[1]['carbohydrates']
    text += (f'Итог:\n'
             f'Общий вес: {weight}\n'
             f'Калории: {calories}\n'
             f'Б: {proteins} Ж: {fats} У: {carbohydrates}')
    return text