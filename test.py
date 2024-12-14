from cryptography.fernet import Fernet
generate_key = Fernet.generate_key() 
print(generate_key)