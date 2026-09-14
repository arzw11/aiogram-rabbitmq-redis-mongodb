from pydantic import Field
from pydantic_settings import BaseSettings


class MongoDBSettings(BaseSettings):
    MONGODB_PORT: int
    MONGODB_HOST: str
    MONGODB_ADMIN_USERNAME: str
    MONGODB_ADMIN_PASSWORD: str

    MONGODB_EXPRESS_PORT: int

    MONGODB_USERS_DATABASE: str = Field(default='users')
    MONGODB_USERS_COLLECTION: str = Field(default='users')
    MONGODB_COUPLES_DATABASE: str = Field(default='couples')
    MONGODB_COUPLES_COLLECTION: str = Field(default='couples')

    @property
    def mongodb_connection_uri(self) -> str:
        return (
            f'mongodb://{self.MONGODB_ADMIN_USERNAME}:'
            f'{self.MONGODB_ADMIN_PASSWORD}@'
            f'{self.MONGODB_HOST}:'
            f'{self.MONGODB_PORT}/'
            f'?authSource=admin'
        )
