import json
import os

import redis


class ConversationMemory:

    def __init__(self):

        redis_url = os.getenv(
            "REDIS_URL",
            "redis://localhost:6379/0"
        )

        self.client = redis.Redis.from_url(
            redis_url,
            decode_responses=True
        )

        self.max_messages = int(
            os.getenv(
                "REDIS_MAX_MESSAGES",
                "20"
            )
        )

        self.ttl_seconds = int(
            os.getenv(
                "REDIS_TTL_SECONDS",
                "86400"
            )
        )


    def _key(
        self,
        conversation_id
    ):

        return (
            f"conversation:"
            f"{conversation_id}:messages"
        )


    def get_history(
        self,
        conversation_id
    ):

        key = self._key(
            conversation_id
        )

        messages = self.client.lrange(
            key,
            0,
            self.max_messages - 1
        )

        return [
            json.loads(message)
            for message in messages
        ]


    def add_message(
        self,
        conversation_id,
        role,
        content
    ):

        key = self._key(
            conversation_id
        )

        message = json.dumps(
            {
                "role": role,
                "content": content
            },
            ensure_ascii=False
        )

        self.client.rpush(
            key,
            message
        )

        self.client.ltrim(
            key,
            -self.max_messages,
            -1
        )

        self.client.expire(
            key,
            self.ttl_seconds
        )


    def restore(
        self,
        conversation_id,
        messages
    ):

        self.clear(
            conversation_id
        )

        for message in messages:

            self.add_message(
                conversation_id,
                message["role"],
                message["content"]
            )


    def clear(
        self,
        conversation_id
    ):

        self.client.delete(
            self._key(
                conversation_id
            )
        )