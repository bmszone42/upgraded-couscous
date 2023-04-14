import streamlit as st
import requests
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
html_code = response.content
soup = BeautifulSoup(html_code, 'html.parser')

# Find all the divs that contain the winning numbers and their parent divs
winning_divs = soup.select('div.game-ball-group')

# Extract the winning numbers and dates from each winning div
winning_numbers = []
winning_dates = []
for div in winning_divs:
    date = div.select_one('h2.card-title').text.strip()
    numbers = div.select('div.white-balls.item-powerball')
    powerball = div.select('div.powerball.item-powerball')
    winning_numbers.append([int(n.text) for n in numbers] + [int(p.text) for p in powerball])
    winning_dates.append(date)

# Print the winning numbers and dates
st.write("The winning numbers are:")
for date, numbers in zip(winning_dates, winning_numbers):
    st.write(f"{date}: {numbers}")

# Check if user's numbers match winning numbers
matches = []
if number1 in winning_numbers:
    matches.append(number1)
if number2 in winning_numbers:
    matches.append(number2)
if number3 in winning_numbers:
    matches.append(number3)
if number4 in winning_numbers:
    matches.append(number4)
if number5 in winning_numbers:
    matches.append(number5)

# Display results
st.write(f"You entered the numbers {number1}, {number2}, {number3}, {number4}, {number5}, and {bonus_number}")
st.write(f"The winning numbers are {winning_numbers} and the bonus number is {bonus_number}")
