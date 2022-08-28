import requests
import json
from playwright.sync_api import sync_playwright

def get_tor_session():
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    return session

from stem import Signal
from stem.control import Controller

# signal TOR for a new connection
def renew_connection():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password="luposki")
        controller.signal(Signal.NEWNYM)
def initPlay(time,qtd, url):    
    for i in range(qtd):
        session = get_tor_session()
        renew_connection()
        response = session.get("https://ipinfo.io/json")
        
        result = json.loads(response.text)

        locale = f"\n ip: {result['ip']} \n region: {result['region']} \n timezone: {result['timezone']}"
        print(locale)
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url)
            print(f"- {page.title()}")
            page.wait_for_timeout(time)
            browser.close()
            print("\n end...")
            

initPlay(200000, 20,"https://www.youtube.com/watch?v=ogoIxkPjRts&list=RDme_BhryXKZ8&index=2")








#print(result)

