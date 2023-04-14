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
soup = BeautifulSoup(response.content, 'html.parser')

# Get the most recent winning numbers
winning_numbers_div = soup.find_all('div', {'class': 'item-powerball'})
winning_numbers = [int(number.text) for number in winning_numbers_div[:5]]
bonus_div = soup.find('div', {'class': 'powerball item-powerball'})
if bonus_div:
    bonus = int(bonus_div.text)
else:
    bonus = None

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
st.write(soup.prettify())

st.write(f"You entered the numbers {number1}, {number2}, {number3}, {number4}, {number5}, and {bonus_number}")
st.write(f"The winning numbers are {winning_numbers} and the bonus number is {bonus}")
if len(matches) == 0:
    st.write("Sorry, you did not win any prizes.")
elif len(matches) == 1:
    st.write(f"Congratulations! You matched 1 number ({matches[0]}) and won a prize.")
else:
    st.write(f"Congratulations! You matched {len(matches)} numbers ({matches}) and won a prize.")
if bonus_number == bonus:
    st.write("You also matched the bonus number and won an additional prize!")

   
