from datetime import datetime as dt

def log(text):
    with open('log.txt', 'a', encoding='utf-8') as f:
        f.write(f'{dt.now().time()}: {text}\n')