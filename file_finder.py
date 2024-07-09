import requests
import threading
import signal
import sys
from bs4 import BeautifulSoup

class py:
    def __init__(self):
        signal.signal(signal.SIGINT, self.exit)
        self.lista = set()
        self.lock = threading.Lock()  
    def exit(self,sig,frame):
        print(f"\nExiting...")
        sys.exit(0)
    def main(self, url):
        with self.lock:
            if url in self.lista:
                return
            self.lista.add(url)

        try:
            if url[-1]!='/':
                url=url+'/'
            response = requests.get(url)
            response.raise_for_status()  
        except requests.RequestException:
            return

        soup = BeautifulSoup(response.content, 'html.parser')
        anchor_tags = soup.find_all('a')
        
        threads = []
        for tag in anchor_tags:
            href = tag.get('href')
            if href and not href.startswith('?') and not href.endswith('/'):
                print(url + href)
            if href and href.endswith('/') and not href.startswith('?') and href != '/':
                path = url + href
                if path not in self.lista:
                    thread = threading.Thread(target=self.main, args=(path,))
                    thread.start()
                    threads.append(thread)
    
        for thread in threads:
            thread.join() 

if __name__ == '__main__':
    main = py()
    main.main(input("Enter target: "))
