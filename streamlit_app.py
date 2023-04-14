import requests
from bs4 import BeautifulSoup

number_inputs = [1, 10, 23, 27, 33]
bonus_input = 7

import requests
from bs4 import BeautifulSoup
import streamlit as st

st.set_page_config(page_title="Lottery Checker")

st.title("Lottery Checker")

number_inputs = [1, 10, 23, 27, 33]
bonus_input = 7

number_inputs = st.multiselect("Select your numbers", range(1, 70), number_inputs)
bonus_input = st.selectbox("Select your bonus number", range(1, 27), bonus_input)

url = "https://www.powerball.com/previous-results"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

winning_numbers = []
for i in range(5):
    winning_numbers.append(int(soup.find("div", class_="winning-numbers-red-ball").text))
    soup = soup.find("div", class_="winning-numbers-white-balls")
    winning_numbers.append(int(soup.contents[i].text))

winning_bonus = int(soup.find("div", class_="winning-numbers-red-ball").text)

st.write(f"Your numbers: {number_inputs}")
st.write(f"Winning numbers: {winning_numbers}")
st.write(f"Your bonus number: {bonus_input}")
st.write(f"Winning bonus number: {winning_bonus}")

matches = set(number_inputs).intersection(set(winning_numbers))

if len(matches) == 5:
    st.write("JACKPOT! You have won the grand prize!")
elif len(matches) == 4:
    st.write("Congratulations! You have won $1,000 a week for life!")
elif len(matches) == 3:
    st.write("Congratulations! You have won $20!")
else:
    st.write("Sorry, you did not win this time. Try again!")
