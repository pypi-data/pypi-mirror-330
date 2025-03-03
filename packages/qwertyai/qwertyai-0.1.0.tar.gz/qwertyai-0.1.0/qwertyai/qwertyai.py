import requests


class QwertyAI:
    def __init__(self, base_url: str):
        """Инициализация клиента для работы с API нейросети."""
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}

    def send_request(self, endpoint: str, payload: dict):
        """Отправка запроса к API."""
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()

    def generate_text(self, prompt: str, model: str = "free-gpt", max_tokens: int = 100):
        """Генерация текста с использованием бесплатной модели AI."""
        payload = {"model": model, "prompt": prompt, "max_tokens": max_tokens}
        return self.send_request("completions", payload)

    def analyze_sentiment(self, text: str):
        """Анализ тональности текста."""
        payload = {"text": text}
        return self.send_request("sentiment", payload)
