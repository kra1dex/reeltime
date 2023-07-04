import requests


def get_client_ip(meta_data):
    x_forwarded_for = meta_data['HTTP_X_FORWARDED_FOR']
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = meta_data['REMOTE_ADDR']
    return ip


def get_timezone(meta_data):
    # url = f'http://ip-api.com/json/{get_client_ip(meta_data)}'
    # response = requests.get(url)
    # timezone = response.json()['timezone']
    # return timezone

    return 'Europe/Kyiv'
