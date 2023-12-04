def get_api_key():
    with open('API_KEY.txt', 'r') as file:
        return file.read().strip()
