import requests

API_BASE_URL = "http://localhost:8000"


def get_user(username):
    """Busca usuário por username"""
    url = f"{API_BASE_URL}/users/{username}"
    try:
        response = requests.post(url)
        if response.ok:
            return response.json(), None
        else:
            return None, f"Status: {response.status_code}"
    except Exception as e:
        return None, str(e)


def get_leagues(user_id):
    """Busca ligas do usuário"""
    url = f"{API_BASE_URL}/leagues/{user_id}"
    try:
        response = requests.get(url)
        if response.ok:
            return response.json(), None
        else:
            return None, f"Status: {response.status_code}"
    except Exception as e:
        return None, str(e)


def get_matches(leagues):
    """Busca partidas das ligas"""
    url = f"{API_BASE_URL}/matches"
    try:
        response = requests.post(url, json=leagues)
        if response.ok:
            return response.json(), None
        else:
            return None, f"Status: {response.status_code}"
    except Exception as e:
        return None, str(e)


def get_rosters(leagues):
    """Busca rosters das ligas"""
    url = f"{API_BASE_URL}/rosters"
    try:
        response = requests.post(url, json=leagues)
        if response.ok:
            return response.json(), None
        else:
            return None, f"Status: {response.status_code}"
    except Exception as e:
        return None, str(e)


def save_leagues(leagues):
    """Salva ligas no banco"""
    url = f"{API_BASE_URL}/leagues"
    try:
        response = requests.post(url, json=leagues)
        if response.ok:
            return True, None
        else:
            return False, f"Status: {response.status_code}"
    except Exception as e:
        return False, str(e)
