from enum import Enum


class GetCaptureConfigsResponse200ItemTriggerKind(str, Enum):
    EMAIL = "email"
    HTTP = "http"
    KAFKA = "kafka"
    NATS = "nats"
    POSTGRES = "postgres"
    SQS = "sqs"
    WEBHOOK = "webhook"
    WEBSOCKET = "websocket"

    def __str__(self) -> str:
        return str(self.value)
