import random
from math import gcd

def phi(p, q):
    return (p - 1) * (q - 1)
def mod_inverse(e, phi_n):
    return pow(e, -1, phi_n)
# Función para generar un número aleatorio e que sea primo relativo con phi(n)
def generate_e(p, q):
    phi_n = phi(p, q)
    while True:
        e = random.randint(2, phi_n - 1)
        if gcd(e, phi_n) == 1:
            return e
def encrypt_message(M, e, n):
    return pow(M, e) % n
def decrypt_message(C, d, n):
    return pow(C, d) % n
def text_to_numbers(text):
    return [ord(char) - ord('A') + 1 for char in text.upper()]
def numbers_to_text(numbers):
    return ''.join([chr(num + ord('A') - 1) for num in numbers])

def generate_public_key(p,q):
    # Llave publica (e,d)
    e = generate_e(p,q)
    phi_n = phi(p,q)
    d = mod_inverse(e, phi_n)
    public_key = [e, d]
    return public_key

def generate_private_key(p,q):
    # Llave privada (d,n)
    n = p * q



# Mensaje de texto
message = "Nomomon"

# Convertir el mensaje de texto a números
M = text_to_numbers(message)
# Generar números primos p y q
# p = random.randint(10, 100)
# q = random.randint(10, 100)
# n = p * q
# print("n =", n)
# # Tiene que ser mayor a 1 y menor a phi_n
# e = generate_e(p, q)
# print("e =", e)
# phi_n = phi(p, q)
# d = mod_inverse(e, phi_n)
# print("d =", d)
# Cifrar el mensaje completo
# ------------------------------------------
# Llave publica (e,d)
# Llave privada (d,n)

# Erik:
# Llave publica = (2641, 1177)
# Llave privada = (1177, 3071)

# Cajero:
# cifrar (m^e mod n)
# descifrar (enc^d mod n)
# print("Cifrado con llave de Erik:")
# encrypted_numbers = [encrypt_message(m, 2641, 3071) for m in M]
# decrypted_numbers = [decrypt_message(enc, 1177, 3071) for enc in encrypted_numbers]
# decrypted_message = numbers_to_text(decrypted_numbers)
# print("Mensaje descifrado con Erik:", decrypted_message)