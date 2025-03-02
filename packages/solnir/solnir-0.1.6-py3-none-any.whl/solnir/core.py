import time
import threading
from datetime import datetime
import inspect
import pika
import json

class Solnir:
    _exit_flag = False
    rabbitmq_host     = "rabbitmq.rabbitmq.svc.cluster.local"
    queue_name        = "log-queue"
    rabbitmq_user     = "user"
    rabbitmq_password = "VOZZdgHu4JGpZ8am"

    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=rabbitmq_host, 
        credentials=credentials,
        heartbeat=600
    ))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name)

    @staticmethod
    def exit():
        Solnir._exit_flag = True
        Solnir.log("Exiting solnir main loop.")

    @staticmethod
    def main(func):
        def wrapper():
            Solnir.log("Starting solnir main loop.")
            while not Solnir._exit_flag:
                func()
            Solnir.log("solnir main loop has stopped.")
        Solnir.connection.close()
        return wrapper

    @staticmethod
    def run(func):
        main_thread = threading.Thread(target=func)
        main_thread.start()
        main_thread.join()

    @staticmethod
    def sleep(t):
        time.sleep(t)

    @staticmethod
    def log(msg):
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

        stack = inspect.stack()
        caller = stack[1]
        caller_name = caller.function
        caller_line = caller.lineno

        message = {"id": "GlSI08PFfUJAcknEW7kxI", "text": f"[INFO-{caller_name}:{caller_line}] ({formatted_time}) {msg}\n"}
        Solnir.send(msg)

    @staticmethod
    def send(msg):
        try:
            Solnir.channel.basic_publish(exchange="", routing_key=Solnir.queue_name, body=json.dumps(msg))
        except:
            Solnir.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=Solnir.rabbitmq_host, 
                credentials=Solnir.credentials,
                heartbeat=600
            ))
            Solnir.channel = Solnir.connection.channel()
            Solnir.channel.queue_declare(queue=Solnir.queue_name)
            Solnir.channel.basic_publish(exchange="", routing_key=Solnir.queue_name, body=json.dumps(msg))