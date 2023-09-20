# A console app which displays random
import requests
import time
import os

# codes for changing terminal text color.
colorStart = "\033["
colorEnd = "\033[0m"
baseUrl = "http://www.boredapi.com/api/activity?"
previousActivities = []


# Clear function from: https://www.tutorialspoint.com/how-to-clear-python-shell
def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


def formatResults(response):
    responseFormatted = (response.json())
    print(f"Activity: {responseFormatted['activity']}")
    print(f"Category: {responseFormatted['type']}")
    print(f"Number of participants required: {responseFormatted['participants']}")
    if responseFormatted['price'] == 0.0:
        print("Cost of activity: FREE ")
    else:
        print(f"Cost of activity: £{float(responseFormatted['price'])}")
    print(colorStart + "36m--------------------------------------------------------------  " + colorEnd)


def formatPreviousResults(previousActivities):
    for currentActivity in previousActivities:
        print(f"Activity: {currentActivity['activity']}")
        print(f"Category: {currentActivity['type']}")
        print(f"Number of participants required: {currentActivity['participants']}")
        if currentActivity['price'] == 0.0:
            print("Cost of activity: FREE ")
        else:
            print(f"Cost of activity: £{float(currentActivity['price'])}")
        print(colorStart + "33m--------------------------------------------------------------  " + colorEnd)


def viewPreviousActivities(previousActivities):
    if len(previousActivities) == 0:
        clear()
        print("You have no previous searches")
        print("Start searching to view previous results")
        time.sleep(2)
        menuOptions()
    else:
        clear()
        print("Here are your previous activity results: ")
        print(colorStart + "33m--------------------------------------------------------------  " + colorEnd)
        formatPreviousResults(previousActivities)
        time.sleep(5)
        menuOptions()


def searchByCategory():
    categoriesOfActivities = ["education", "recreational", "social", "diy", "charity", "cooking", "relaxation", "music",
                              "busywork"]
    print(colorStart + "36mTypes of activities: " + colorEnd)
    for i in categoriesOfActivities:
        print(f"- {i.capitalize()}")
    userCategory = input("Which category would you like to search? ")
    clear()
    numberOfResults = int(input("How many results would you like to see? 1-10 "))
    print(colorStart + "36m--------------------------------------------------------------  " + colorEnd)

    if 1 <= numberOfResults <= 10:
        if userCategory.lower() in categoriesOfActivities:
            for i in range(numberOfResults):
                response = requests.get(f"{baseUrl}type={userCategory}")
                formatResults(response)
                previousActivities.append(response.json())
        else:
            print("Error, you have typed in an invalid category")
            print("Please try again")
            time.sleep(2)
            searchByCategory()
    else:
        print("Sorry the value you have entered is not between 1 and 10, please try again")
        time.sleep(2)
        searchByCategory()

    startAgain = input("Would you like to check a different category? y/n ")

    if startAgain.lower() == "y" or startAgain.lower() == "yes":
        clear()
        searchByCategory()
    else:
        clear()
        menuOptions()


def menuOptions():
    print(colorStart + "36mACTIVITY RECOMMENDATION SERVICE" + colorEnd)
    print("~ MENU OPTIONS ~")
    print("1: Find a random activity")
    print("2: Search by category")
    print("3: Search by number of participants")
    print("4: Search by total price of activity")
    print("5: View previous activity results")
    print("6: Exit")

    userOption = input("Select an option 1-5: ")

    if userOption == "2":
        searchByCategory()
    elif userOption == "5":
        viewPreviousActivities(previousActivities)
    else:
        print("Goodbye")
        time.sleep(2)
        exit()

        # menuOptions()


menuOptions()
