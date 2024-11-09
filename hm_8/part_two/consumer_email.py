from config.connect import connect_mongo, q_email, disconnect_mogo, connRabbitMQ
from crv.models import Contact
from bson import ObjectId
from mongoengine import DoesNotExist
from crv.sending import send_email_stub


def callback(ch, method, properties, body):
    contact_id = ObjectId(body.decode())
    try:
        contact = Contact.objects.get(id=contact_id)
        if send_email_stub(contact):
            contact.message_sent = True
            contact.save()
            print(f"Email sent and status updated for contact ID: {contact_id}")

    except DoesNotExist:
        print(f"Contact with ID {body.decode()} does not exist.")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def consume():
    channel = connRabbitMQ.channel()
    channel.queue_declare(queue=q_email)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=q_email, on_message_callback=callback)

    print(' [*] Waiting for email messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    disconnect_mogo()
    connect_mongo()
    consume()

