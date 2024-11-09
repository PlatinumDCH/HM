from config.connect import connect_mongo,disconnect_mogo, connRabbitMQ
from config.connect import  q_sms, q_email
from crv.create_contacts import create_contact


def main():
    #declare queue
    channel = connRabbitMQ.channel()
    channel.queue_declare(queue=q_email)
    channel.queue_declare(queue=q_sms)

    # Post messages in the queue
    for contact in create_contact():
        message = str(contact.id).encode()
        if contact.preferred_contact_method == 'email':
            queue_name = q_email
        else:
            queue_name = q_sms
        channel.basic_publish(exchange='',routing_key=queue_name,body=message)
        print(f'[x] Sent contact ID "{message.decode()}" to {queue_name} queue')

    connRabbitMQ.close()


if __name__ == '__main__':
    disconnect_mogo()
    connect_mongo()
    main()





