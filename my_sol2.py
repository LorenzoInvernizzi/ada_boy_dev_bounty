# pip install parsel
import requests
from parsel import Selector
import sys


"""
Problem 2. bounty: $125 in adaboy

Write a program that takes N as an argument as before and prints the approximate USD value (1 or 2 sig figs, ill know if youre correct) of the adaboy balance in the tuple.

> ./my_soln2.py 13

0x0a3d8365b5160b21fd1e98179b72d6d547487cba 10000
"""

# setup params
page_size = 50
token = "0x1e653794a6849bc8a78be50c4d48981afad6359"
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
}


if __name__ == "__main__":
    try:
        
        # input id holder
        if len(sys.argv) > 1:
            input_id_holder=int(sys.argv[1])
        else:
            print("WARNING: id holder not passed, using 1 as default")
            input_id_holder = 1
        
        page_id = input_id_holder // page_size + 1*(input_id_holder % page_size != 0)
        sel_input_id_holder = input_id_holder - page_size*(input_id_holder // page_size) - 1

        # total supply
        response = requests.get(f"https://bscscan.com/token/{token}d", headers=headers) 
        sel_page = Selector(response.text)
        total_supply = int(
            sel_page.xpath(
                '//*[@id="ContentPlaceHolder1_divSummary"]/div[1]/div[1]/div/div[2]/div[2]/div[2]/span[1]'
            )[0].get().split('</span>')[0].split('>')[-1].replace(',', '')
        )

        # get usd price
        response = requests.get(f"https://api.pancakeswap.info/api/v2/tokens/{token}d", headers=headers) 
        adaboy_usd = float(response.json()['data']['price'])

        # holders
        response = requests.get(
            f"https://bscscan.com/token/generic-tokenholders2?a={token}d&sid=&m=normal&s=100000000000000000000000000000&p={page_id}", 
            headers=headers
        ) 
        
        # extract page holders
        sel = Selector(response.text)
        list_holders = []
        for row in sel.css('tr'):
            # percentage is on 5th column -> poor resolution
            balance = row.xpath('td[3]/text()').get()
            if balance:  # skip rows with no percentage info
                balance = float(balance.replace(',', ''))

                # addres is on 2nd column under <a>f node
                # we can also use `re()` method to only take the token part of the url
                addr = row.xpath('.//@href').get().split('token/')[1].split('a=')[1]
                list_holders.append((addr, balance/total_supply, balance, balance*adaboy_usd))

        requested_holder = list_holders[sel_input_id_holder]
        print(requested_holder[0], requested_holder[3])
        
        # TO BE COMPLETED

    except Exception as e:
        print(e)
        print('>>>> HELP: You might be asking a non existing holder. Otherwise contact Lorentzo92 for support <<<<<')
