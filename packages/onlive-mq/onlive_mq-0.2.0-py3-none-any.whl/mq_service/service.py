import asyncio
import json
import traceback
import uuid

import aio_pika

MAX_CONCURRENT_TASKS = 5
MAX_PREFETCH_COUNT = 5

class MqService:
    def __init__(self, rabbit_url=None):
        self.connection = None
        self.semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)
        self.rabbit_url = rabbit_url

    async def connect(self):
        try:
            if not self.rabbit_url:
                print("RabbitMQ URI not found in the app settings")
                raise ValueError("RabbitMQ URI not found in the app settings")

            # Connect to RabbitMQ using the URL from the config or a default value
            self.connection = await aio_pika.connect_robust(
                url=self.rabbit_url,
                heartbeat=60
            )
            print("Connected to RabbitMQ")

        except Exception as e:
            print(f"Error connecting to RabbitMQ: {e}")
            raise e

    async def create_exchange(self, channel, exchange_name, exchange_type=aio_pika.ExchangeType.DIRECT):
        # Declare an exchange
        return await channel.declare_exchange(
            exchange_name,
            exchange_type
        )

    async def create_channel(self):
        # Create a channel
        return await self.connection.channel()

    async def create_queue(self, channel, queue_name, durable=True, arguments=None):
        # Declare a queue
        return await channel.declare_queue(queue_name, durable=durable, arguments=arguments)

    async def bind_queue(self, exchange, queue, routing_key):
        # Bind the queue to the exchange with a routing key
        await queue.bind(exchange, routing_key)

    async def publish(self, exchange, message, routing_key):
        await exchange.publish(
            aio_pika.Message(body=message.encode()),
            routing_key=routing_key
        )

    async def create_reply_to_exchange(self, channel):
        # Declare an exchange
        return await channel.declare_exchange(
            "reply_to",
            aio_pika.ExchangeType.DIRECT
        )

    async def reply_to(self, queue_name, message, correlation_id=None, headers=None, error=False):
        try:
            channel = await self.connection.channel()
            reply_to_exchange = await self.create_reply_to_exchange(channel)
            queue = await channel.declare_queue(
                queue_name,
                durable=True,
                passive=True,
                arguments={
                    'x-expires': 5000
                } if queue_name.endswith('.reply') else None
            )
            await queue.bind(reply_to_exchange, queue_name)

            json_encode_result = json.dumps(message)

            if error:
                if headers:
                    headers['x-error-response'] = "true"
                else:
                    headers = {'x-error-response': "true"}

            pika_message = aio_pika.Message(
                body=json_encode_result.encode(),
                correlation_id=correlation_id,
                headers=headers if headers else {}
            )
            
            print(f"Replying message: {pika_message} to queue: {queue_name}")
            await reply_to_exchange.publish(pika_message, routing_key=queue_name, mandatory=True)

        except Exception as e:
            print(f"Error replying message: {e}")

    async def consume(self, queue, callback):
        # Start consuming messages with the provided callback
        await queue.consume(callback, no_ack=False)

    async def stop(self):
        # Close the channel and connection properly
        if self.connection:
            await self.connection.close()

    async def process_message(self, message: aio_pika.IncomingMessage, msgHandler):
        async with self.semaphore:
            try:
                # Verify if the message has already been processed
                if message.processed:
                    print(f"Message already processed: {message}")
                    return  # Exit the function if the message has already been processed
                result = None

                print(
                    f"Received message: {message.body.decode()} with full message {message}")
                # Check if the callback is a coroutine
                if asyncio.iscoroutinefunction(msgHandler):
                    result = await msgHandler(message.body.decode())
                else:
                    result = msgHandler(message.body.decode())

                await message.ack()
                print(f"Acknowledged message sent to queue: {message.routing_key}")
                if result:
                    print(f"Message processed with result: {result}")
                    if message.reply_to:
                        headers = getattr(message, "headers", None)
                        if headers and isinstance(headers, dict):
                            print(
                                f"Headers included in the reply: {headers}")
                        else:
                            headers = None
                        await self.reply_to(message.reply_to, result, message.correlation_id, headers=headers)

            except Exception as e:
                print(f"Error processing message: {e}")
                print(f"Traceback: {traceback.format_exc()}")
                await message.nack(requeue=False)
                if message.reply_to:
                    headers = getattr(message, "headers", None)
                    if headers and isinstance(headers, dict):
                        print(
                            f"Headers included in the reply: {headers}")
                    else:
                        headers = None
                        metadata = {}
                    try:
                        metadata = json.loads(message.body.decode()).get("metadata", {})
                    except json.JSONDecodeError as json_error:
                        print(f"Error decoding metadata JSON: {json_error}")
                    await self.reply_to(message.reply_to, {"error": str(e), "metadata": metadata}, message.correlation_id, error=True, headers=headers)

    async def consume_on(self, queue_name, msgHandler):
        try:
            await self.connect()
            channel = await self.connection.channel()
            await channel.set_qos(prefetch_count=MAX_PREFETCH_COUNT) 
            exchange = await self.create_exchange(channel, queue_name)
            queue = await self.create_queue(channel, queue_name)
            await self.bind_queue(exchange, queue, queue_name)
            await self.consume(
                queue,
                lambda message: asyncio.create_task(
                    self.process_message(message, msgHandler))
            )

        except Exception as e:
            print(f"Error consuming from {queue_name} tasks: {e}")

    async def rpc_call(self, exchange, message, routing_key, timeout=5):
        # Create a temporary exclusive queue for the RPC response
        channel = await self.connection.channel()
        temp_queue = await channel.declare_queue('', exclusive=True)
        correlation_id = str(uuid.uuid4())
        response_future = asyncio.get_event_loop().create_future()

        async def on_response(msg: aio_pika.IncomingMessage):
            if msg.correlation_id == correlation_id and not response_future.done():
                response_future.set_result(msg.body.decode())

        await temp_queue.consume(on_response, no_ack=True)

        pika_message = aio_pika.Message(
            body=message.encode(),
            reply_to=temp_queue.name,
            correlation_id=correlation_id
        )
        await exchange.publish(pika_message, routing_key=routing_key)
        try:
            return await asyncio.wait_for(response_future, timeout)
        except asyncio.TimeoutError:
            raise TimeoutError("RPC call timed out")

