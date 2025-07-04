


def upper_lower(sentence):
    upper_counter = 0
    lower_counter = 0
    for x in sentence:
        if x.islower():
            lower_counter += 1
        elif x.isupper():
            upper_counter +=1
    print("upper,lower",upper_counter,lower_counter)
if __name__ == "__main__":
    upper_lower("I love Oranges and Bananas Desktop and TableCloths")