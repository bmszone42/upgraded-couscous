import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Set default numbers
default_numbers = [9, 36, 41, 44, 59]
default_bonus_number = 4

# Create inputs for user to enter numbers
number1 = st.sidebar.number_input("Enter first number", min_value=1, max_value=69, value=default_numbers[0])
number2 = st.sidebar.number_input("Enter second number", min_value=1, max_value=69, value=default_numbers[1])
number3 = st.sidebar.number_input("Enter third number", min_value=1, max_value=69, value=default_numbers[2])
number4 = st.sidebar.number_input("Enter fourth number", min_value=1, max_value=69, value=default_numbers[3])
number5 = st.sidebar.number_input("Enter fifth number", min_value=1, max_value=69, value=default_numbers[4])
bonus_number = st.sidebar.number_input("Enter bonus number", min_value=1, max_value=26, value=default_bonus_number)

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
winning_data = soup.select('#searchNumbersResults > div.d-flex.gap-3.flex-column > a')

# Extract the winning numbers and dates from each winning div
winning_numbers = []
drawing_dates = []
for data in winning_data:
    date = data.select_one('div > div > div:nth-child(1) > div > h5').text.strip()
    numbers = data.select('div.white-balls.item-powerball')
    powerball = data.select('div.powerball.item-powerball')
    winning_numbers.append([int(n.text) for n in numbers] + [int(p.text) for p in powerball])
    drawing_dates.append(date)

# Create a DataFrame with the winning numbers and dates
winning_df = pd.DataFrame({'Date': drawing_dates, 'Winning Numbers': winning_numbers})

# Display the winning numbers in a DataFrame
st.write("The winning numbers are:")
st.write(winning_df)
# st.write("The winning numbers are:")
# for numbers in winning_numbers:
#    st.write(numbers)

# Define user_numbers
user_numbers = [number1, number2, number3, number4, number5]
# Display results
st.write(f"You entered the numbers {number1}, {number2}, {number3}, {number4}, {number5}, and {bonus_number}")

winning_dates = []
for i, numbers in enumerate(winning_numbers):
    # Check if the user matched the winning numbers
    matches = set(user_numbers).intersection(numbers[:-1])  # Exclude the last number (powerball)
    matched_bonus = bonus_number == numbers[-1]  # Check if the bonus number matches the powerball

    # If the user has matched any numbers or the bonus number, add the drawing date to the winning_dates list
    if len(matches) > 0 or matched_bonus:
        winning_dates.append(drawing_dates[i])

if len(winning_dates) == 0:
    st.write("No winners.")
else:
    st.write("You won on the following drawing dates:")
    for date in winning_dates:
        st.write(date)

