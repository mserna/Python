import datetime

def main():
    # Asks for name as well
    name = input("Please provide me your name: ")
    # Asks user to enter age
    age = int(input("Please enter your age: "))

    new_age = calculate_new_age(age)

    print("Hi " + name + " you will be 100 years old in the year " + str(new_age))


def calculate_new_age(age):
    current_date = datetime.datetime.now()
    current_year = int(current_date.year)
    age_diff = 100 - age
    year_100 = current_year + age_diff
    return year_100


main()
