"""
RabbitMQ Output
-----------------

Uses a `RabbitMQ Queue <https://www.rabbitmq.com/>`_ as a destination for parent
generation messages.

**Plugin name:** ``rabbitmq_out_bulk``

.. list-table::
    :header-rows: 1

    * - Option
      - Value Type
      - Description
    * - ``connection.host``
      - string
      - ``REQUIRED`` RabbitMQ server host
    * - ``connection.user``
      - string
      - ``REQUIRED`` Username
    * - ``connection.password``
      - string
      - ``REQUIRED`` password
    * - ``connection.vhost``
      - string
      - ``REQUIRED`` `Virtual host <https://www.rabbitmq.com/vhosts.html>`_
    * - ``connection.kwargs``
      - dict
      - connection parameter kwargs `pika.conneciton.ConnectionParameters
        <https://pika.readthedocs.io/en/stable/modules/parameters.html#connectionparameters>`_
    * - ``exchange.source_exchange``
      - dict
      - dictionary describing the source exchange. `exchange`_
    * - ``exchange.dest_exchange``
      - dict
      - ``REQUIRED`` The final exchange. This is where the queues will be bound. `exchange`_
    * - ``queues``
      - ``list``
      - ``REQUIRED`` Queue parameters. `queues`_
    * - ``max_cache_size``
      - ``int``
      - Maximum number of messages before cache is emptied.


exchange
^^^^^^^^

The source and dest exchange keys comprise:

.. list-table::
    :header-rows: 1

    * - Option
      - Value Type
      - Description
    * - method
      - string
      - ``REQUIRED`` Exchange name
    * - type
      - string
      - ``REQUIRED`` `Exchange type <https://medium.com/trendyol-tech/rabbitmq-exchange-types-d7e1f51ec825>`_

queues
^^^^^^

List of queue objects. Each queue object comprises:

.. list-table::
    :header-rows: 1

    * - Option
      - Value Type
      - Description
    * - method
      - string
      - ``REQUIRED`` Queue name
    * - kwargs
      - dict
      - kwargs passed to `pika.channel.queue_declare <https://pika.readthedocs.io/en/stable/modules/channel.html#pika.channel.Channel.queue_declare>`_
    * - bind_kwargs
      - dict
      - kwargs passed to `pika.channel.queue_bind <https://pika.readthedocs.io/en/stable/modules/channel.html#pika.channel.Channel.queue_bind>`_
    * - consume_kwargs
      - dict
      - kwargs passed to `pika.channel.Channel.basic_consume <https://pika.readthedocs.io/en/stable/modules/channel.html#pika.channel.Channel.basic_consume>`_

Example Configuration:

    .. code-block:: yaml

        outputs:
            - method: rabbitmq_bulk
              connection:
                host: my-rabbit-server.co.uk
                user: user
                password: '*********'
                vhost: my_virtual_host
                kwargs:
                  heartbeat: 300
              exchange:
                name: mydest-exchange
                type: fanout
                routing_key: asset
              cache_max_size: 10
"""

import json

import pika
from pydantic import BaseModel, Field

from stac_generator.core.bulk_output import BulkOutput, BulkOutputConf


class RabbitMQConnection(BaseModel):
    """JSON config model."""

    user: str = Field(
        description="RabbitMQ user.",
    )
    password: str = Field(
        description="RabbitMQ password.",
    )
    host: str = Field(
        description="RabbitMQ host.",
    )
    host: str = Field(
        description="RabbitMQ vhost.",
    )
    kwargs: dict = Field(
        default={},
        description="RabbitMQ additional kwargs.",
    )


class RabbitMQExchange(BaseModel):
    """JSON config model."""

    name: str = Field(
        description="RabbitMQ exchange name.",
    )
    type: str = Field(
        description="RabbitMQ exchange type.",
    )
    routing_key: str = Field(
        default="",
        description="RabbitMQ exchange routing key.",
    )


class RabbitMQConf(BulkOutputConf):
    """RabbitMQ config model."""

    connection: RabbitMQConnection = Field(
        default={},
        description="RabbitMQ connection kwargs.",
    )
    exchange: RabbitMQExchange = Field(
        description="RabbitMQ exchange info.",
    )


class RabbitMQBulkOutput(BulkOutput):
    """
    RabbitMQ Bulk output for sending grouped messages.
    """

    config_class = RabbitMQConf

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create the credentials object
        credentials = pika.PlainCredentials(
            self.conf.connection.user, self.conf.connection.password
        )

        # Start the rabbitMQ connection
        rabbit_connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.conf.connection.host,
                credentials=credentials,
                virtual_host=self.conf.connection.vhost,
                **self.conf.connection.kwargs,
            )
        )

        # Create a new channel
        self.channel = rabbit_connection.channel()
        self.channel.exchange_declare(
            exchange=self.conf.exchange.name,
            exchange_type=self.conf.exchange.type,
        )

    def data_to_cache(self, data: dict) -> None:
        """
        Convert the data into a data to  be stored in cache.

        :param data: data from processor to be output.
        :param kwargs:
        """
        return {
            data["body"][f"{data['surtype']}_id"]: {
                f"{data['surtype']}_id": data["body"][f"{data['surtype']}_id"],
                "uri": data["uri"],
            }
        }

    def export(self, data_list: list):
        """
        Export the data to rabbit.

        :param data: expected data as header dict
        """

        self.channel.basic_publish(
            exchange=self.conf.exchange.name,
            body=json.dumps(data_list),
            routing_key=self.conf.exchange.routing_key,
        )
