import streamlit as st
import requests
from bs4 import BeautifulSoup

# Set default numbers
default_numbers = [9, 36, 41, 44, 59]
default_bonus_number = 4

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
winning_divs = soup.select('div.col-12.col-lg-4')

# Extract the winning numbers and dates from each winning div
results = []
for div in winning_divs:
    numbers = div.select('div.white-balls.item-powerball')
    powerball = div.select('div.powerball.item-powerball')
    winning_numbers = [int(n.text) for n in numbers] + [int(p.text) for p in powerball]
    date = div.select_one('h5.card-title').text.strip()
    results.append((date, winning_numbers))

# Print the winning numbers and dates
st.write("Powerball Winning Numbers and Dates:")
for date, numbers in results:
    st.write(f"{date}: {numbers}")
