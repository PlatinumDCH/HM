import pika

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='hello')

message = b'Hello World!!'
channel.basic_publish(exchange='', routing_key='hello', body=message)

print(f" [x] Sent '{message}'")
connection.close()

'''
1.импортировать библиотеку  pika для взаимодействия с RabbitMQ
2.настроить учетные данные для подключение к RabbitMQ ( имя пользователя . пароль) 
3.установить соединение с RabbitMQ сервером, используя учетные данные и 
параметры подключения ( хост, порт)
4. создать канал для взаимодействия с RabbitMQ
5.объявить очередь с именем hello ( если она не существует, она будет создана )
6.создать сообщение в виде байт строки
7.опубликовать сообщение в очередь hello через канал
8.вывести сообщение о том, что сообщение было отправлено
9.закрыть соединение с RabbitMQ

'''