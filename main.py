"""This is a project which uses boredapi.com in order to display activity suggestions for when a user is bored.
There are a number of filters that can be used to search through the results, however the api pulls random
results each time. This project requires NO api key. For the best experience it is recommended that you use your own
computer terminal or change pycharm settings, to emulate the terminal."""

import requests
import time
import os

# requests module primarily used for importing the GET api method, and for changing API responses into json formatting.

# Time module used for adding a time delay between when the next piece of text is printed out,
# so that the user has time to read the data that has been provided.

# os module used to get os data so the program can interact with the computer/terminal. I have used this
# module so that I can clear the terminal screen when the menu options are loaded or when a user selects one of the
# options so that it is easier to read. I have used it to check which device the user is running the program on,
# and it will provide the corresponding commands as a result. I have imported it using pycharm.


# global variable used to keep track of all results shown.
previousActivities = []


# provides the end and beginning codes for changing terminal text color.
def colorCodes():
    colors = {
        'colorStart': "\033[",
        'colorEnd': "\033[0m",
        'boldStart': "\033[1m",
        'boldEnd': "\033[0m"
    }
    return colors


def startAgainFunction(userInput, methodType):
    if userInput.lower() == "y" or userInput.lower() == "yes":
        clear()
        if methodType == 1:
            return chooseRandomActivity()
        elif methodType == 3:
            return searchByCategory()
        elif methodType == 4:
            return searchByNumberOfParticipants()
        elif methodType == 5:
            return searchByDifficulty()
    elif userInput.lower() == "n" or userInput.lower() == "no":
        clear()
        menuOptions()
    else:
        clear()
        print("You have entered an incorrect value")
        print("Loading menu...")
        time.sleep(2)
        clear()
        menuOptions()


def writeFinalResults(previousActivities):
    userName = input("What is your name? ")
    file = open('allActivities.txt', 'w')
    file.write(f"Results for: {userName}\n")
    file.write("Activity ideas for when you're bored: \n")
    file.write("------------------------------------------ \n")
    file.write("\n")
    count = 0
    for previousActivity in previousActivities:
        count += 1
        file.write(f"Activity {count}: {previousActivity['activity']}\n")
        category = previousActivity['type'].capitalize()
        file.write(f"Category: {category}\n")
        file.write(f"Number of participants required: {previousActivity['participants']}\n")
        file.write(f"Difficulty Score: {(previousActivity['accessibility'] * 10)}/10\n")
        if previousActivity['price'] == 0.0:
            file.write("Cost of activity: FREE \n")
        else:
            file.write(f"Cost of activity: {(previousActivity['price'] * 10)}/10\n")
        if previousActivity['link'] != '':
            file.write(f"Link to related resources: {previousActivity['link']}\n")
        file.write("\n")
    file.close()


def formatPreviousResults(previousActivities):
    colors = colorCodes()
    for currentActivity in previousActivities:
        print(f"Activity: {currentActivity['activity']}")
        category = currentActivity['type'].capitalize()
        print(f"Category: {category}")
        print(f"Number of participants required: {currentActivity['participants']}")
        print(f"Difficulty Score: {(currentActivity['accessibility'] * 10)}/10")
        if currentActivity['link'] != '':
            print(f"Link to related resources: {currentActivity['link']}")
        if currentActivity['price'] == 0.0:
            print("Cost of activity: FREE ")
        else:
            print(f"Cost of activity: {(currentActivity['price'] * 10)}/10\n")
        print(colors['colorStart'] + "33m--------------------------------------------------------------  " + colors[
            'colorEnd'])


# base url link which can be used in other functions through concatenating to add 'filters'
def urlLink():
    baseUrl = "http://www.boredapi.com/api/activity?"
    return (baseUrl)


# Clear function from: https://www.tutorialspoint.com/how-to-clear-python-shell
def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


# formats the users results so that each key value is formatted in an easier to read format.
def formatResults(response):
    colors = colorCodes()
    responseFormatted = (response.json())
    print(f"Activity: {responseFormatted['activity']}")
    category = responseFormatted['type'].capitalize()
    print(f"Category: {category}")
    print(f"Number of participants required: {responseFormatted['participants']}")
    print(f"Difficulty Score: {(responseFormatted['accessibility'] * 10)}/10")
    if responseFormatted['price'] == 0.0:
        print("Cost of activity: FREE ")
    else:
        print(f"Cost of activity: {(responseFormatted['price'] * 10)}/10")
    if responseFormatted['link'] != '':
        print(f"Link to related resources: {responseFormatted['link']}")

    print(colors['colorStart'] + "36m--------------------------------------------------------------  " + colors[
        'colorEnd'])


# Displays all menu options (1-7), allows user to quit the program.
def menuOptions():
    colors = colorCodes()
    print(colors['colorStart'] + "36mACTIVITY RECOMMENDATION SERVICE" + colors['colorEnd'])
    print("~ MENU OPTIONS ~")
    print("1: Find a random activity")
    print("2: Search by category")
    print("3: Search by number of participants")
    print("4: Search by difficulty of the activity")
    print("5: View previous activity results")
    print("6: View previous activity results file")
    print("7: Exit")

    userOption = input("Select an option 1-7: ")

    if userOption == "1":
        chooseRandomActivity()
    elif userOption == "2":
        searchByCategory()
    elif userOption == "3":
        searchByNumberOfParticipants()
    elif userOption == "4":
        searchByDifficulty()
    elif userOption == "5":
        fileOrNotFile = False
        viewPreviousActivities(previousActivities, fileOrNotFile)
    elif userOption == "6":
        fileOrNotFile = True
        viewPreviousActivities(previousActivities, fileOrNotFile)
    elif userOption == "7":
        print("Thank you using our service, goodbye.")
        time.sleep(2)
        exit()
    else:
        clear()
        print("You have entered an incorrect value")
        print("Loading menu...")
        time.sleep(2)
        clear()
        menuOptions()


# Runs the base API call to provide a random activity.
def chooseRandomActivity():
    clear()
    colors = colorCodes()
    print(colors['colorStart'] + "32mHere is a random Activity for you to do: " + colors['colorEnd'])
    url = urlLink()
    response = requests.get(url)
    print(colors['colorStart'] + "36m--------------------------------------------------------------  " + colors[
        'colorEnd'])
    formatResults(response)  # formats the response from the api
    previousActivities.append(response.json())  # appends results to previousActivities list.
    time.sleep(2)
    startAgain = input("Would you like to see another random activity? y/n ")
    startAgainFunction(startAgain, 1)


# Used to determine if there are any previous activities to display. Uses an if statement to determine whether to call
# the file creation function or the function used to print results in terminal
def viewPreviousActivities(previousActivities, fileOrNotFile):
    colors = colorCodes()
    if len(previousActivities) == 0:
        clear()
        print("You have no previous searches")
        print("Start searching to view previous results")
        time.sleep(5)
        clear()
        menuOptions()

    else:
        if not fileOrNotFile:
            clear()
            print("Here are your previous activity results: ")
            print(colors['colorStart'] + "33m--------------------------------------------------------------  " + colors[
                'colorEnd'])

            resultsList = []
            for i in range(len(previousActivities)):
                if previousActivities[i] not in resultsList:
                    resultsList.append(previousActivities[i])

            formatPreviousResults(resultsList)
            time.sleep(5)
            startAgain = input(
                "Would you like to keep looking y/n ")  # extends time delay so user can keep checking the results

            while startAgain.lower() == "y" or startAgain.lower() == "yes":
                time.sleep(5)
                startAgain = input("Would you like to keep looking y/n ")
            else:
                clear()
                menuOptions()
        else:
            clear()
            resultsList = []
            for i in range(len(previousActivities)):
                if previousActivities[i] not in resultsList:
                    resultsList.append(previousActivities[i])
            writeFinalResults(resultsList)
            print(colors['colorStart'] + "33m--------------------------------------------------------------  " +
                  colors[
                      'colorEnd'])
            print("Your results have been saved in allActivities.txt ")
            print(colors['colorStart'] + "33m--------------------------------------------------------------  " +
                  colors[
                      'colorEnd'])
            time.sleep(5)
            clear()
            menuOptions()


def searchByCategory():
    clear()
    colors = colorCodes()
    url = urlLink()
    categoriesOfActivities = ["education", "recreational", "social", "diy", "charity", "cooking", "relaxation", "music",
                              "busywork"]
    print(colors['colorStart'] + "36mTypes of activities" + colors['colorEnd'])
    for i in categoriesOfActivities:
        print(f"- {i.capitalize()}")
    userCategory = input("Which category would you like to search? ")
    userCategory = userCategory.lower()
    clear()
    numberOfResults = int(input("How many results would you like to see? 1-10 "))
    print(colors['colorStart'] + "36m--------------------------------------------------------------  " + colors[
        'colorEnd'])

    if 1 <= numberOfResults <= 10:
        resultsList = []
        numberOfResultsShown = 0
        if userCategory.lower() in categoriesOfActivities:
            for i in range(numberOfResults):
                response = requests.get(f"{url}type={userCategory}")
                if response.json() not in resultsList:
                    resultsList.append(response.json())
                    formatResults(response)
                    previousActivities.append(response.json())
                    numberOfResultsShown += 1
        if numberOfResults != numberOfResultsShown:
            print(f"Sorry only {numberOfResultsShown} activities were shown:")
        elif numberOfResults == numberOfResultsShown:
            print(f"Number of results shown: {numberOfResults}")
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

    startAgainFunction(startAgain, 3)


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
        resultsList = []
        numberOfResultsShown = 0
        for i in range(numberOfResults):
            response = requests.get(f"{url}accessibility={userDifficulty}")
            if response.json() not in resultsList:
                resultsList.append(response.json())
                formatResults(response)
                previousActivities.append(response.json())
                numberOfResultsShown += 1
    if numberOfResults != numberOfResultsShown:
        print(f"Sorry only {numberOfResultsShown} activities were shown:")
    elif numberOfResults == numberOfResultsShown:
        print(f"Number of results shown: {numberOfResults}")
    else:
        print("Sorry the value you have entered is not between 1 and 10, please try again")
        time.sleep(2)
        searchByDifficulty()

    startAgain = input("Would you like to check a different difficulty rating? y/n ")

    startAgainFunction(startAgain, 5)


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
        else:
            print(f"Number of results shown: {numberOfResults}")

        startAgain = input("Would you like to check a different number of Participants? y/n ")

        startAgainFunction(startAgain, 4)


menuOptions()
