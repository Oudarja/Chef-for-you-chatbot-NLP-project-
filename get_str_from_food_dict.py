def get_str_from_food_dict(food_dict:dict):
    return ", ".join([f"{int(value)} {key}" for key,value in food_dict.items()])

