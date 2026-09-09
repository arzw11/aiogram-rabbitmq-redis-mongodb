from pydantic import Field
from pydantic_settings import BaseSettings


class MongoDBSettings(BaseSettings):
    MONGO_DB_CONNECTION_URI: str
    MONGO_DB_ADMIN_USERNAME: str
    MONGO_DB_ADMIN_PASSWORD: str

    MONGODB_USERS_DATABASE: str = Field(default="users")
    MONGODB_USERS_COLLECTION: str = Field(default="users")
    MONGODB_COUPLES_DATABASE: str = Field(default="couples")
    MONGODB_COUPLES_COLLECTION: str = Field(default="couples")
