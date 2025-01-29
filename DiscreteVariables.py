import random

def choose_car():
    cars = ["Sedan", "SUV", "Hatchback","Convertible","Truck"]

    probabilities = [0.3, 0.2, 0.25, 0.15, 0.1]

    selected_car = random.choices(cars, weights=probabilities, k=1)[0]

    return selected_car

for _ in range(5):
    print(f"chosen car:{choose_car()}")