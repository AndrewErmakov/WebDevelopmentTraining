import random


def encryption_number_order(order_number):
    encryption_key = random.randint(280, 570)
    encrypted_order_number = order_number + encryption_key
    return [encrypted_order_number, encryption_key]


def decryption_number_order(encrypted_order_num, key):
    decoded_order_number = str(encrypted_order_num - key).zfill(6)
    return decoded_order_number