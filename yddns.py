from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json
import datetime

LAST_IP_FILE = 'ip.txt' # Файл, в котором хранится последний прописанный IP
LOG_FILE = 'ddns.log'  # Лог
GET_IP_URL = 'https://myexternalip.com/raw' # Aдрес, сообщающий нам IP
DOMAIN = 'myowndomain.xyz' # Домен, записи DNS которого я редактирую 
RECORD_ID = '0000000' # Номер записи
TOKEN = 'AAAAAAAAAABBBBBB' # Токен от яндекса


# Считываем текущий IP адрес
# Можно добавить ещё проверку, что мы получили именно IP, а не что-то ещё.
ip = urlopen(GET_IP_URL).read().decode().strip()

# Считываем из файла IP, который был записан в DNS последний раз.
# Можно, конечно это не делать, но я считаю, что нехорошо нагружать Яндекс лишними операциями.
try:
    last_ip = open(LAST_IP_FILE, mode='tr').read().strip()
except FileNotFoundError:
    last_ip = ""

# Если старый IP и текущий не совпадают, будем обновлять запись
if last_ip != ip:

    # Готовим POST-запрос
    url = 'https://pddimp.yandex.ru/api2/admin/dns/edit'
    post_fields = {
        'domain': DOMAIN,      
        'record_id': RECORD_ID, 
        'content': ip,
        'token': TOKEN
        }    

    request = Request(url, urlencode(post_fields).encode())
    data = urlopen(request).read().decode()
    json = json.loads(data)

    # Ожидаем, что всё в порядке
    assert json['success']=='ok', json

    # Сохраняем IP в файл
    print(ip, file=open(LAST_IP_FILE, mode='tw'))

    # Пишем об изменении в лог
    d=datetime.datetime.now()
    print(d.strftime("%Y-%m-%d %H:%M:%S"), ip, file=open(LOG_FILE, mode='ta'))
    
