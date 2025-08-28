def get_recommended_recipes(age, gender):
    # Dummy implementation for demonstration purposes
    # Database query from here
    if age < 5:
        return ["Mashed Pumpkin", "Rice Porridge"]
    elif gender == "female":
        return ["Salad Bowl", "Fruit Smoothie"]
    else:
        return ["Grilled Chicken", "Veggie Soup"]
