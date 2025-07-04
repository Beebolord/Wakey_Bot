

if __name__ == '__main__':
    cars = ["Honda","Toyota", "Mercedes","Ferrari","Nissan","Hyundai"]
    print(cars)
    cars[len(cars) - 1] = "Kia"
    print(cars)
    cars[1] = "Chevrolet"
    print(cars)
    cars.sort(reverse=True)
    print(cars)
    cars = []
    print(cars)