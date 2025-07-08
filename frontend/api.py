import requests

API_BASE_URL = "http://localhost:8000"


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


def process_results(user_id: str, leagues: list[dict]):
    url = f"{API_BASE_URL}/leagues/process/{user_id}"
    try:
        response = requests.post(url, json=leagues)
        data = response.json()
        return data, None
    except Exception as e:
        return None, str(e)
