import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}

__all__ = [BASE_DIR, headers]

