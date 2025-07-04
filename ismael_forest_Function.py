
if __name__ == "__main__":
    cars = ['Toyota','Benz','Kia','Honda','Ferrari','Lexus']
    with open("file.txt","r+") as file:
       list(map(file.write,(item + '\n' for item in cars)))
    with(open("file.txt","r+") as file):
        print(file.read())