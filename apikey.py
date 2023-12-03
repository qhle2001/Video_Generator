def get_api_key():
    with open('api_key.txt', 'r') as file:
        return file.read().strip()
