"""
2. Задание на закрепление знаний по модулю json. Есть файл orders
в формате JSON с информацией о заказах. Написать скрипт, автоматизирующий
его заполнение данными.

Для этого:
Создать функцию write_order_to_json(), в которую передается
5 параметров — товар (item), количество (quantity), цена (price),
покупатель (buyer), дата (date). Функция должна предусматривать запись
данных в виде словаря в файл orders.json. При записи данных указать
величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json()
с передачей в нее значений каждого параметра.

ПРОШУ ВАС НЕ УДАЛЯТЬ ИСХОДНЫЙ JSON-ФАЙЛ
ПРИМЕР ТОГО, ЧТО ДОЛЖНО ПОЛУЧИТЬСЯ

{
    "orders": [
        {
            "item": "printer",
            "quantity": "10",
            "price": "6700",
            "buyer": "Ivanov I.I.",
            "date": "24.09.2017"
        },
        {
            "item": "scaner",
            "quantity": "20",
            "price": "10000",
            "buyer": "Petrov P.P.",
            "date": "11.01.2018"
        }
    ]
}

вам нужно подгрузить JSON-объект
и достучаться до списка, который и нужно пополнять
а потом сохранять все в файл
"""
import json
import chardet


def write_order_to_json(item, quantity, price, buyer, date):
    """
    Дозапись новых данных в объект файла в JSON формате
    :param item: данные
    :param quantity: данные
    :param price: данные
    :param buyer: данные
    :param date: данные
    """
    with open('orders.json', encoding='utf-8') as file:
        data_file = json.load(file)
    first_el_in_dict = data_file[list(data_file.keys())[0]]
    first_el_in_dict.append({
        'item': item,
        'quantity': quantity,
        'price': price,
        'buyer': buyer,
        'date': date
    })

    with open('orders.json', mode='w', encoding='utf-8') as file:
        json.dump(data_file, file, indent=4, ensure_ascii=False)


write_order_to_json(
    'элемент',
    '29075321614734',
    999999,
    'Инокентий Смактуновский',
    '25.05.1905')
