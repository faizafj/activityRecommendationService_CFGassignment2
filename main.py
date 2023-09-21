# A console app which displays random
import requests

import time

'''This is a module (time) used for adding a time delay between when the next piece of text is printed out, 
so that the user has time to read the data that has been provided.
'''

import os

'''This is a module (os) used to get os data so the program can interact with the computer/terminal. I have used this 
module so that I can clear the terminal screen when the menu options are loaded or when a user selects one of the 
options so that it is easier to read. I have used it to check which device the user is running the program on, 
and it will provide the corresponding commands as a result. I have imported it using pycharm.
'''

# global variable used to keep track of all results shown.
previousActivities = []


# provides the end and beginning codes for changing terminal text color.
def colorCodes():
    colors = {
        'colorStart': "\033[",
        'colorEnd': "\033[0m"
    }
    return colors


def urlLink():
    baseUrl = "http://www.boredapi.com/api/activity?"
    return (baseUrl)


# Clear function from: https://www.tutorialspoint.com/how-to-clear-python-shell
def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


# formats the users results so that each key value is formatted in a user friendly way.
def formatResults(response):
    colors = colorCodes()
    responseFormatted = (response.json())
    print(f"Activity: {responseFormatted['activity']}")
    print(f"Category: {responseFormatted['type']}")
    print(f"Number of participants required: {responseFormatted['participants']}")
    if responseFormatted['price'] == 0.0:
        print("Cost of activity: FREE ")
    else:
        print(f"Cost of activity: £{float(responseFormatted['price'])}")
    print(colors['colorStart'] + "36m--------------------------------------------------------------  " + colors[
        'colorEnd'])


# used to format all previous results, uses a different formatting style compared to normal results
def formatPreviousResults(previousActivities):
    colors = colorCodes()
    for currentActivity in previousActivities:
        print(f"Activity: {currentActivity['activity']}")
        print(f"Category: {currentActivity['type']}")
        print(f"Number of participants required: {currentActivity['participants']}")
        if currentActivity['price'] == 0.0:
            print("Cost of activity: FREE ")
        else:
            print(f"Cost of activity: £{float(currentActivity['price'])}")
        print(colors['colorStart'] + "33m--------------------------------------------------------------  " + colors[
            'colorEnd'])


# Displays all menu options, allows user to quit the program too.
def menuOptions():
    colors = colorCodes()
    print(colors['colorStart'] + "36mACTIVITY RECOMMENDATION SERVICE" + colors['colorEnd'])
    print("~ MENU OPTIONS ~")
    print("1: Find a random activity")
    print("2: Search by category")
    print("3: Search by number of participants")
    print("4: Search by difficulty of the activity")
    print("5: View previous activity results")
    print("6: Exit")

    userOption = input("Select an option 1-6: ")

    if userOption == "1":
        chooseRandomActivity()
    elif userOption == "2":
        searchByCategory()
    elif userOption == "3":
        searchByNumberOfParticipants()
    elif userOption == "4":
        searchByDifficulty()
    elif userOption == "5":
        viewPreviousActivities(previousActivities)
    else:
        print("Thank you using our service, goodbye.")
        time.sleep(2)
        exit()


# Runs the base API call to provide a random activity.
def chooseRandomActivity():
    clear()
    colors = colorCodes()
    url = urlLink()
    response = requests.get(url)
    print(colors['colorStart'] + "36m--------------------------------------------------------------  " + colors[
        'colorEnd'])
    formatResults(response)
    previousActivities.append(response.json())
    time.sleep(2)
    startAgain = input("Would you like to see another random activity? y/n ")

    if startAgain.lower() == "y" or startAgain.lower() == "yes":
        clear()
        chooseRandomActivity()
    else:
        clear()
        menuOptions()


# Used to determine if there are any previous activities to display.
def viewPreviousActivities(previousActivities):
    colors = colorCodes()
    if len(previousActivities) == 0:
        clear()
        print("You have no previous searches")
        print("Start searching to view previous results")
        time.sleep(5)

    else:
        clear()
        print("Here are your previous activity results: ")
        print(colors['colorStart'] + "33m--------------------------------------------------------------  " + colors[
            'colorEnd'])

        formatPreviousResults(previousActivities)
        time.sleep(5)
        startAgain = input(
            "Would you like to keep looking y/n ")  # extends time delay so user can keep checking the results

        while startAgain.lower() == "y" or startAgain.lower() == "yes":
            time.sleep(5)
            startAgain = input("Would you like to keep looking y/n ")
        else:
            clear()
            menuOptions()


def searchByCategory():
    colors = colorCodes()
    url = urlLink()
    categoriesOfActivities = ["education", "recreational", "social", "diy", "charity", "cooking", "relaxation", "music",
                              "busywork"]
    print(colors['colorStart'] + "36mTypes of activities" + colors['colorEnd'])
    for i in categoriesOfActivities:
        print(f"- {i.capitalize()}")
    userCategory = input("Which category would you like to search? ")
    clear()
    numberOfResults = int(input("How many results would you like to see? 1-10 "))
    print(colors['colorStart'] + "36m--------------------------------------------------------------  " + colors[
        'colorEnd'])

    if 1 <= numberOfResults <= 10:
        if userCategory.lower() in categoriesOfActivities:
            for i in range(numberOfResults):
                response = requests.get(f"{url}type={userCategory}")
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


def searchByDifficulty():
    colors = colorCodes()
    url = urlLink()
    clear()
    print(colors['colorStart'] + "35m ~ SEARCH BY DIFFICULTY RATING ~" + colors['colorEnd'])
    print("Which difficulty level would you like to search?")
    userDifficulty = int(input("Choose a value between 1 (easy) and 10 (hard): "))

    userDifficulty = userDifficulty / 10
    clear()
    numberOfResults = int(input("How many results would you like to see? 1-10 "))

    print(colors['colorStart'] + "36m--------------------------------------------------------------  " + colors[
        'colorEnd'])

    if 1 <= numberOfResults <= 10:
        for i in range(numberOfResults):
            response = requests.get(f"{url}accessibility={userDifficulty}")
            formatResults(response)
            previousActivities.append(response.json())
    else:
        print("Sorry the value you have entered is not between 1 and 10, please try again")
        time.sleep(2)
        searchByDifficulty()

    startAgain = input("Would you like to check a different difficulty rating? y/n ")
    if startAgain.lower() == "y" or startAgain.lower() == "yes":
        clear()
        searchByDifficulty()
    else:
        clear()
        menuOptions()


def searchByNumberOfParticipants():
    colors = colorCodes()
    url = urlLink()
    clear()
    print(colors['colorStart'] + "35m ~ SEARCH BY NUMBER OF PARTICIPANTS ~" + colors['colorEnd'])
    numberOfParticipants = int(input("How many participants do you have? 1-8 "))
    numberOfResults = int(input("How many results would you like to see? 1-10 "))
    print(colors['colorStart'] + "36m--------------------------------------------------------------  " + colors[
        'colorEnd'])

    if numberOfParticipants == 7 or numberOfParticipants == 6:
        print(f"Sorry we do not have any activities available for {numberOfParticipants} people")
        print("Try again")
        searchByNumberOfParticipants()
    elif numberOfParticipants > 8:
        print(f"Sorry we do not have any activities available for more than 8 people")
        print("Try again with a value less than 8")
        searchByNumberOfParticipants()
    elif numberOfParticipants < 0:
        print("Try again with a value more than 1")
        searchByNumberOfParticipants()
    else:
        if 1 <= numberOfResults <= 10:
            resultsList = []
            numberOfResultsShown = 0

            for i in range(numberOfResults):
                response = requests.get(f"{url}participants={str(numberOfParticipants)}")
                if response.json() not in resultsList:
                    resultsList.append(response.json())
                    formatResults(response)
                    previousActivities.append(response.json())
                    numberOfResultsShown += 1

        if numberOfResults != numberOfResultsShown:
            print(f"Sorry only {numberOfResultsShown} activities were shown:")

        startAgain = input("Would you like to check a different number of Participants? y/n ")

        if startAgain.lower() == "y" or startAgain.lower() == "yes":
            clear()
            searchByNumberOfParticipants()
        else:
            clear()
            menuOptions()


# menuOptions()
searchByDifficulty()

# searchByNumberOfParticipants()
# chooseRandomActivity()
