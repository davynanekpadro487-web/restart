import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aurea.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

c = Client(HTTP_HOST='127.0.0.1')
c.force_login(User.objects.first())
response = c.get('/defi/6/')
content = response.content.decode('utf-8')
match = re.search(r'<h3[^>]*>.*?Spiritualit.*?</h3>', content, re.DOTALL | re.IGNORECASE)
if match:
    print("Found H3:", match.group(0))
else:
    print('Not found')
