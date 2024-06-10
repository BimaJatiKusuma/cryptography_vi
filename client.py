import socket
import random
import math

prime = set()

def primefiller():
    seive = [True] * 250
    seive[0] = False
    seive[1] = False
    for i in range(2, 250):
        for j in range(i * 2, 250, i):
            seive[j] = False

    for i in range(len(seive)):
        if seive[i]:
            prime.add(i)

def pickrandomprime():
    k = random.randint(0, len(prime) - 1)
    it = iter(prime)
    for _ in range(k):
        next(it)
    ret = next(it)
    prime.remove(ret)
    return ret

def setkeys():
    prime1 = pickrandomprime()
    prime2 = pickrandomprime()

    n = prime1 * prime2
    fi = (prime1 - 1) * (prime2 - 1)

    e = 2
    while True:
        if math.gcd(e, fi) == 1:
            break
        e += 1

    d = 2
    while True:
        if (d * e) % fi == 1:
            break
        d += 1

    return (e, n), (d, n)

def encrypt(message, public_key):
    e, n = public_key
    encrypted_text = 1
    while e > 0:
        encrypted_text *= message
        encrypted_text %= n
        e -= 1
    return encrypted_text

def decrypt(encrypted_text, private_key):
    d, n = private_key
    decrypted = 1
    while d > 0:
        decrypted *= encrypted_text
        decrypted %= n
        d -= 1
    return decrypted

def encoder(message, public_key):
    encoded = []
    for letter in message:
        encoded.append(encrypt(ord(letter), public_key))
    return encoded

def decoder(encoded, private_key):
    s = ''
    for num in encoded:
        s += chr(decrypt(num, private_key))
    return s

if __name__ == "__main__":
    primefiller()
    public_key, private_key = setkeys()

    print(f"Alice's Public Key: {public_key}")
    print(f"Alice's Private Key: {private_key}")

    # Enter Bob's public key manually (in real scenario, this should be done securely)
    # bob_public_key = (ENTER_BOB_PUBLIC_KEY_HERE)
    bob_public_key = (5, 14941)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client.connect(('BOB_IP_ADDRESS', 9999))
    client.connect(('192.168.0.107', 9999))

    while True:
        message = input("Enter message for Bob: ")
        encrypted_message = encoder(message, bob_public_key)
        message_to_send = ','.join(map(str, encrypted_message))
        client.send(message_to_send.encode())
