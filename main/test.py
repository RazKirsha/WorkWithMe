import os

a = os.environ.get('FP_Django_SecretKey')
b = os.getenv('FP_Django_SecretKey')

print(a)
print(b)