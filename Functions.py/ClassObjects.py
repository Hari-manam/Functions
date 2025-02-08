class car:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
    def display_info(self):
        print(f"car: {self.brand},{self.model}")
# creating objects (instances)
car1= car("tesla", "model s")
car2 = car("toyata", "corolla")
car1.display_info()
car2.display_info()