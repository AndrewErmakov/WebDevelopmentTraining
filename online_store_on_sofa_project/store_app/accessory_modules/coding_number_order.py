import random


def encryption_number_order(order_number):
    encryption_key = random.randint(280, 570)
    dict_params = {'encryption_key': encryption_key}
    dict_params['encrypted_order_number'] = order_number + dict_params['encryption_key']
    return dict_params


def decryption_number_order(encrypted_order_num, key):
    decoded_order_number = str(encrypted_order_num - key).zfill(6)
    return decoded_order_number

