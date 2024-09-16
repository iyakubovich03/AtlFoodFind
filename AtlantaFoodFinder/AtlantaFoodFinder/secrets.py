# Secret management
API_KEY = None

def get_api_key():
    global API_KEY
    if API_KEY == None:
        init_api_key()
    return API_KEY

def init_api_key():
    global API_KEY
    with open("API_KEY", "r") as f:
        API_KEY = f.read()