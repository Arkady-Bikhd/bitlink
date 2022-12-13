import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
import argparse


BASE_URL = 'https://api-ssl.bitly.com/v4/'

def main():

    load_dotenv()
    	
    bitly_token = os.getenv("BITLY_TOKEN")    
    headers = {
        'Authorization': f'Bearer {bitly_token}'
    }
    url = create_parcer()
    if is_bitlink(url,headers):
        try:
            total_clicks = count_clicks(url, headers)
            print(f'Количество кликов по ссылке: {total_clicks}')
        except requests.exceptions.HTTPError:
            print('Введена неправильная сокращённая ссылка или неверный токен')
    else:
        try:
            bitlink = shorten_link(url, headers)
            print (f'Битлинк: {bitlink}')
        except requests.exceptions.HTTPError:
            print('Введена неправильная ссылка или неверный токен')

def shorten_link(url, headers):

    url_base = f'{BASE_URL}shorten'
    payload = {'long_url': url}
    response = requests.post(url_base, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['link']

def count_clicks(bitlink, headers):
  
    parsed_link = urlparse(bitlink)
    link = f'{parsed_link.netloc}{parsed_link.path}'
    url = f'{BASE_URL}bitlinks/{link}/clicks/summary'
    url_params = {
                'units': '-1'
                }
    response = requests.get(url, headers=headers, params=url_params)
    response.raise_for_status()
            
    return response.json()['total_clicks']

def is_bitlink(url, headers):
    
    parsed_link = urlparse(url)
    link = f'{parsed_link.netloc}{parsed_link.path}'
    url_link = f'{BASE_URL}bitlinks/{link}'     
    response = requests.get(url_link, headers=headers)
               
    return response.ok   

def create_parcer():

    parcer = argparse.ArgumentParser(
        description='Программа сокращает длинные ссылки и показывает статистику переходов'
    )
    parcer.add_argument('link', help='Введите ссылку')
    args = parcer.parse_args()

    return args.link

if __name__ == '__main__':
   
    main()