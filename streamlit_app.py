import requests
from bs4 import BeautifulSoup

# Define the URL of the Powerball winning numbers page
url = 'https://www.powerball.com/numbers/'

# Retrieve the page contents
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract the latest winning numbers
winning_numbers = []
for div in soup.find_all('div', class_='winning-numbers-white-ball'):
    winning_numbers.append(int(div.text))
winning_numbers.append(int(soup.find('div', class_='winning-numbers-red-ball').text))

print('Latest Powerball winning numbers:', winning_numbers)
# Prompt the user to enter their numbers
user_numbers = input('Enter your Powerball numbers (5 white balls between 1 and 69, and 1 red ball between 1 and 26, separated by commas): ')
user_numbers = [int(x) for x in user_numbers.split(',')]

# Check if the user's numbers match the winning numbers
num_correct_white_balls = len(set(user_numbers).intersection(set(winning_numbers[:-1])))
num_correct_red_ball = user_numbers[-1] == winning_numbers[-1]

if num_correct_white_balls == 5 and num_correct_red_ball:
    print('Congratulations! You won the Powerball jackpot!')
else:
    print('Sorry, your numbers did not match the winning numbers.')
