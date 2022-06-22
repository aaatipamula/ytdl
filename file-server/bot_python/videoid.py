import random
import base64

print(base64.urlsafe_b64encode(str(random.choice(range(1, 999999))).encode('utf-8')).decode('utf-8'))
