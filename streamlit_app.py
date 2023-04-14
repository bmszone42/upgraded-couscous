# import streamlit as st
# import requests
# from bs4 import BeautifulSoup

# # Set default numbers
# default_numbers = [9, 36, 41, 44, 59]
# default_bonus_number = 4

# # Create inputs for user to enter numbers
# number1 = st.number_input("Enter first number", min_value=1, max_value=69, value=default_numbers[0])
# number2 = st.number_input("Enter second number", min_value=1, max_value=69, value=default_numbers[1])
# number3 = st.number_input("Enter third number", min_value=1, max_value=69, value=default_numbers[2])
# number4 = st.number_input("Enter fourth number", min_value=1, max_value=69, value=default_numbers[3])
# number5 = st.number_input("Enter fifth number", min_value=1, max_value=69, value=default_numbers[4])
# bonus_number = st.number_input("Enter bonus number", min_value=1, max_value=26, value=default_bonus_number)

# # Get results from website
# url = 'https://www.powerball.com/previous-results?gc=powerball'
# params = {
#     'game': 'powerball',
#     'p': '',
#     'pn': '',
#     'pp': ''
# }

# response = requests.get(url, params=params)

# # Parse the HTML code using BeautifulSoup
# soup = BeautifulSoup(response.content, 'html.parser')

# # Find all the divs that contain the winning numbers and their parent divs
# winning_divs = soup.select('div.game-ball-group')

# # Extract the winning numbers from each winning div
# winning_numbers = []
# for div in winning_divs:
#     numbers = div.select('div.white-balls.item-powerball')
#     powerball = div.select('div.powerball.item-powerball')
#     winning_numbers.append([int(n.text) for n in numbers] + [int(p.text) for p in powerball])

# # Print the winning numbers
# st.write("The winning numbers are:")
# for numbers in winning_numbers:
#     st.write(numbers)

# # Check if user's numbers match winning numbers
# matches = []
# if number1 in winning_numbers:
#     matches.append(number1)
# if number2 in winning_numbers:
#     matches.append(number2)
# if number3 in winning_numbers:
#     matches.append(number3)
# if number4 in winning_numbers:
#     matches.append(number4)
# if number5 in winning_numbers:
#     matches.append(number5)

# # Display results
# st.write(f"You entered the numbers {number1}, {number2}, {number3}, {number4}, {number5}, and {bonus_number}")
# st.write(f"The winning numbers are {winning_numbers} and the bonus number is {bonus_number}")
# if len(matches) == 0:
#     st.write("Sorry, you did not win any prizes.")
# elif len(matches) == 1:
#     st.write(f"Congratulations! You matched 1 number ({matches[0]}) and won a prize.")
# else:
#     st.write(f"Congratulations! You matched {len(matches)} numbers ({matches}) and won a prize.")
# if bonus_number in winning_numbers:
#     st.write("You also matched the bonus number and won an additional prize!")

import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Set default numbers
default_numbers = [9, 36, 41, 44, 59]
default_bonus_number = 4

# Create inputs for user to enter numbers
number1 = st.number_input("Enter first number", min_value=1, max_value=69, value=default_numbers[0])
number2 = st.number_input("Enter second number", min_value=1, max_value=69, value=default_numbers[1])
number3 = st.number_input("Enter third number", min_value=1, max_value=69, value=default_numbers[2])
number4 = st.number_input("Enter fourth number", min_value=1, max_value=69, value=default_numbers[3])
number5 = st.number_input("Enter fifth number", min_value=1, max_value=69, value=default_numbers[4])
bonus_number = st.number_input("Enter bonus number", min_value=1, max_value=26, value=default_bonus_number)

# Get results from website
url = 'https://www.powerball.com/previous-results?gc=powerball'
params = {
    'game': 'powerball',
    'p': '',
    'pn': '',
    'pp': ''
}

response = requests.get(url, params=params)

# Parse the HTML code using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the divs that contain the winning numbers, their parent divs and the drawing dates
winning_data = soup.select('div.game-ball-group-container')

# Extract the winning numbers and dates from each winning div
winning_numbers = []
drawing_dates = []
for data in winning_data:
    date = data.select_one('div.draw-date').text.strip()
    numbers = data.select('div.white-balls.item-powerball')
    powerball = data.select('div.powerball.item-powerball')
    winning_numbers.append([int(n.text) for n in numbers] + [int(p.text) for p in powerball])
    drawing_dates.append(date)

# Create a DataFrame with the winning numbers and dates
winning_df = pd.DataFrame({'Date': drawing_dates, 'Winning Numbers': winning_numbers})

# Display the winning numbers in a DataFrame
st.write("The winning numbers are:")
st.write(winning_df)

# Define user_numbers
user_numbers = [number1, number2, number3, number4, number5]

# Display results
st.write(f"You entered the numbers {number1}, {number2}, {number3}, {number4}, {number5}, and {bonus_number}")

for i, numbers in enumerate(winning_numbers):
    # Check if the user matched the winning numbers
    matches = set(user_numbers).intersection(numbers[:-1])  # Exclude the last number (powerball)
    matched_bonus = bonus_number == numbers[-1]  # Check if the bonus number matches the powerball

    # Display the number of matches and bonus number match
    if len(matches) == 0 and not matched_bonus:
        st.write(f"For the drawing date {drawing_dates[i]}, you did not win any prizes.")
    else:
        result = f"For the drawing date {drawing_dates[i]}, you matched {len(matches)} numbers ({', '.join(map(str, matches))})"
        if matched_bonus:
            result += f" and the bonus number ({bonus

