import json
import aio_pika 


class RabbitMQClient:
    def __init__(self, RABBITMQ_URL):
        self.RABBITMQ_URL = RABBITMQ_URL
        self.connection = None
        self.channel = None
        self.exchange = None
        self.queue = None


    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.RABBITMQ_URL)
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=10)

        self.exchange = await self.channel.declare_exchange(
            "default_exchange",
            durable=True
        )
    

    async def publish(self, routing_key: str, message: dict):
        if not self.channel or self.channel.close():
           raise RuntimeError("RabbitMQ channel is not initialized")
        
        body = json.dumps(message).encode("utf-8")

        await self.exchange.publish(
            message(
                body=body,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key=routing_key
        )


    async def subscribe(
            self,
            queue_name: str,
            routing_key: str,
            handler
    ):
        queue = await self.channel.declare_queue(
            queue_name,
            durble=True
        )
        await queue.bind(self.exchange, routing_key)
        await queue.consume(handler)

    
    async def close(self):
        if self.channel and not self.channel.is_closed:
            await self.channel.close()
        if self.connection and not self.connection.is_closed:
            await self.connection.close()