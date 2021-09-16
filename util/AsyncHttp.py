import threading
import requests


def get_async(url, data=None, callback=None):
    request_async(url, data, get, callback)

def request_async(url, data, method, callback):
    event = threading.Event()
    runner = threading.Thread(target=run,
                              args=(event, url, data, method, callback))
    runner.start()
    while not event.wait(timeout=2.0):
        event.set()
        print("Petición detenida. Tiempo de espera superado")
        callback(None, data)


def run(event, url, data, method, callback):
    event.set()
    result = method(url)
    if callback:
        callback(result, data)


def get(url):
    return requests.get(url)