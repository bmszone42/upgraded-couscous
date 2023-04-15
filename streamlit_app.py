import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup

title = "<h1 style='text-align: center; font-family: Arial, sans-serif; color: blue;'>Lottery Checker -- Let's Check Our Numbers</h1>"
st.markdown(title, unsafe_allow_html=True)


def create_html_table(dataframe):
    table_html = '<table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">'
    table_html += "<tr><th>Date</th><th>Winning Numbers</th></tr>"
    
    for index, row in dataframe.iterrows():
        table_html += "<tr>"
        table_html += f"<td style='text-align: center;'>{row['Date']}</td>"
        table_html += "<td style='text-align: center;'>"
        
        for num in row['Winning Numbers'][:-1]:  # Main numbers
            table_html += f"<span style='padding: 5px; display: inline-block; margin-right: 3px;'>{num}</span>"
        
        # Powerball number in red
        table_html += f"<span style='padding: 5px; display: inline-block; margin-right: 3px; color: red;'>{row['Winning Numbers'][-1]}</span>"
        
        table_html += "</td></tr>"
    
    table_html += "</table><br><br>"
    return table_html

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

# Display the winning numbers in an HTML table
st.write("The winning numbers are:")
st.markdown(create_html_table(winning_df), unsafe_allow_html=True)

# Define user_numbers
user_numbers = [number1, number2, number3, number4, number5]
# Display results
#st.write(f"You entered the numbers {number1}, {number2}, {number3}, {number4}, {number5}, and {bonus_number}")
entered_numbers = f"You entered the numbers <strong>{number1}</strong>, <strong>{number2}</strong>, <strong>{number3}</strong>, <strong>{number4}</strong>, <strong>{number5}</strong>, and <span style='color: red;'><strong>{bonus_number}</strong></span>"
st.markdown(entered_numbers, unsafe_allow_html=True)

def calculate_prize(matched_numbers, matched_bonus):
    if matched_numbers == 5 and matched_bonus:
        return "Jackpot"
    elif matched_numbers == 5:
        return "$1,000,000"
    elif matched_numbers == 4 and matched_bonus:
        return "$50,000"
    elif matched_numbers == 4:
        return "$100"
    elif matched_numbers == 3 and matched_bonus:
        return "$100"
    elif matched_numbers == 3:
        return "$7"
    elif matched_numbers == 2 and matched_bonus:
        return "$7"
    elif matched_numbers == 1 and matched_bonus:
        return "$4"
    elif matched_numbers == 0 and matched_bonus:
        return "$4"
    else:
        return "No prize"

winning_dates = []
for i, numbers in enumerate(winning_numbers):
    # Check if the user matched the winning numbers
    matches = set(user_numbers).intersection(numbers[:-1])  # Exclude the last number (powerball)
    matched_bonus = bonus_number == numbers[-1]  # Check if the bonus number matches the powerball

    # If the user has matched any numbers or the bonus number, add the drawing date to the winning_dates list
    if len(matches) > 0 or matched_bonus:
        prize = calculate_prize(len(matches), matched_bonus)
        winning_dates.append((drawing_dates[i], prize))

if len(winning_dates) == 0:
    st.write("No winners.")
else:
    st.write("You got at least one number on the following drawing dates:")
    for date, prize in winning_dates:
        st.write(f"{date}: {prize}")

