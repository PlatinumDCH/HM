import os
import sys

import pika#[1]


def main():
    credentials = pika.PlainCredentials('guest', 'guest') #[2]
    #connection
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))#[3]
    channel = connection.channel()#[4]
    # объявить очередь
    channel.queue_declare(queue='hello')#[5]

    # определить callback функцию
    def callback(ch, method, properties, body):#[6]
        print(f" [x] Received {body.decode()}")#[6.1]

    # Сообщить RabbitMQ, что callback будет использоваться для обработки сообщений
    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)#[7]
    # Начать обработку сообщений#
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()#[8]


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

'''
1. Импортировать библиотеку pika для взаимодействия с RabbitMQ
2. Настроить учетные данные для подключения к RabbitMQ (имя пользователя и пароль)
3. Установить соединение с RabbitMQ сервером, используя учетные данные и параметры подключения (хост и порт)
4. Создать канал для взаимодействия с RabbitMQ
5. Объявить очередь с именем 'hello' (если она не существует, она будет создана)
6. Определить callback функцию, которая будет вызываться, когда сообщение будет получено из очереди
    6.1. Вывести полученное сообщение
7. Сообщить RabbitMQ, что callback функция будет использоваться для обработки сообщений из очереди 'hello'
8. Начать обработку сообщений (будет работать до тех пор, пока не будет прервано вручную)

'''