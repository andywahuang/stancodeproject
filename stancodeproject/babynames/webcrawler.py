"""
File: webcrawler.py
Name: Andy Huang
--------------------------
This file collects more data from
https://www.ssa.gov/oact/babynames/decades/names2010s.html
https://www.ssa.gov/oact/babynames/decades/names2000s.html
https://www.ssa.gov/oact/babynames/decades/names1990s.html
Please print the number of top200 male and female on Console
You should see:
---------------------------
2010s
Male Number: 10900879
Female Number: 7946050
---------------------------
2000s
Male Number: 12977993
Female Number: 9209211
---------------------------
1990s
Male Number: 14146310
Female Number: 10644506
"""

import requests
from bs4 import BeautifulSoup


def main():
    for year in ['2010s', '2000s', '1990s']:
        print('---------------------------')
        print(year)
        url = 'https://www.ssa.gov/oact/babynames/decades/names'+year+'.html'
        
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, features="html.parser")

        # ----- Write your code below this line ----- #

        tags = soup.find_all('tbody')
        male = 0
        female = 0
        for tag in tags:
            numbers = tag.text.split('\n')[1:401]  # a list with only rank and name+count
            for number in numbers:
                if len(number.split()) == 4:  # remove rank
                    count_male = int(number.split()[1].split(',')[0]) * 1000 + int(number.split()[1].split(',')[1])
                    count_female = int(number.split()[3].split(',')[0]) * 1000 + int(number.split()[3].split(',')[1])
                    male += count_male
                    female += count_female
        print(f'Male Number: {male}')
        print(f'Female Number: {female}')


if __name__ == '__main__':
    main()
