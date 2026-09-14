from pydantic_settings import BaseSettings


class RabbitMQSettings(BaseSettings):
    RABBITMQ_HOST: str
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str

    @property
    def rabbitmq_uri(self) -> str:
        return f'amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}@{self.RABBITMQ_HOST}/'
