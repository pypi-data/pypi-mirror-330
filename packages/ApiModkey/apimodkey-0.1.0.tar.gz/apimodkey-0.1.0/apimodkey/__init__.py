import requests

def api_request(api_key, method, **kwargs):
    url = 'https://modkey.space/api/v1/action'
    data = {
        'method': method,
        'api_key': api_key,
    }
    data.update(kwargs)

    try:
        response = requests.post(url, data=data)
        if response.ok:
            result = response.json()
            print("Ответ от API:", result)  # Выводим полный ответ для отладки
            if result.get('status'):  # Используем get(), чтобы избежать KeyError
                return True, result['data']  # Возвращаем саму data, а не msg
            else:
                return False, result.get('message', 'Error without message')  # Учитываем сообщение
        else:
            print(response.text)
            return False, 'Server error'
    except requests.RequestException as e:
        print(e)
        return False, f'Request failed: {str(e)}'

def create_key(api_key, days, devices, key_type):
    status, msg = api_request(
        api_key=api_key,
        method='create-key',
        days=days,
        devices=devices,
        type=key_type
    )
    if status:
        print('Ключ успешно создан!')
        print(f'Ваш ключ: {msg["key"]}')
        return f"Ключ успешно создан!\nВаш ключ: {msg['key']}"  # Возвращаем строку с результатом
    else:
        print(f'Ошибка: {msg}')
        return f"Ошибка при создании ключа: {msg}"  # Возвращаем строку с ошибкой

def edit_key_status(api_key, key, new_status):
    status, msg = api_request(
        api_key=api_key,
        method='edit-key-status',
        key=key,
        type=new_status
    )
    
    if status:
        print('Статус ключа успешно изменен!')
        print(f'Старый статус: {msg["old_status"]}')  # Просто выводим строку
        print(f'Новый статус: {msg["new_status"]}')
    else:
        print(f'Ошибка: {msg}')
