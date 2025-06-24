

if __name__ == '__main__':
    cars = ["Honda","Toyota", "Mercedes","Ferrari","Nissan","Hyundai"]
    cars.append("Mercedes")
    print(cars.index("Ferrari"))
    print(cars[2])
    cars.remove("Honda")
    print(cars)
    cars.reverse()