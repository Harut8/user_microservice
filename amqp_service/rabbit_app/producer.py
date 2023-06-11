# import pika
# from service.parser import ParseEnv
#
# class Producer:
#     def __init__(self, queue):
#         self.conn = pika.BlockingConnection(
#             pika.URLParameters(f'amqp://{id}:{password}@{host}:{port}'),
#         )
#         self.channel = self.conn.channel()
#         self.channel.queue_declare(queue=queue)
#
#     def produce(self, exchange: str, routing_key: str, body: str) -> None:
#         self.channel.basic_publish(
#             exchange=exchange,
#             routing_key=routing_key,
#             body=body,
#         )
#         self.conn.close()