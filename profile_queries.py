import os
import django
import sys
from django.test import Client
from django.test.utils import CaptureQueriesContext
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aurea.settings')
django.setup()

from django.contrib.auth.models import User

def profile_views():
    user = User.objects.first()
    if not user:
        print("No users found.")
        return

    client = Client()
    client.force_login(user)

    urls = [
        '/',
        '/programme/',
        '/journal/',
        '/progression/',
        '/profil/',
        '/parametres/',
    ]

    for url in urls:
        with CaptureQueriesContext(connection) as queries:
            response = client.get(url)
            print(f"URL: {url} - Status: {response.status_code} - Queries: {len(queries)}")
            
            from collections import Counter
            q_texts = [q['sql'] for q in queries]
            counts = Counter(q_texts)
            duplicates = {k: v for k, v in counts.items() if v > 1}
            if duplicates:
                print(f"  Duplicate queries:")
                for q, count in duplicates.items():
                    print(f"    - {count}x: {q[:100]}...")

if __name__ == '__main__':
    profile_views()
