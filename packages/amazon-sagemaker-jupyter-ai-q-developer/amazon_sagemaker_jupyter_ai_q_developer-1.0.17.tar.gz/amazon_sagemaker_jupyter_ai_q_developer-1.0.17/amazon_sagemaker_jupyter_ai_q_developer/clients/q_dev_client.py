import logging
from abc import ABC, abstractmethod
from functools import partial

from amazon_sagemaker_jupyter_ai_q_developer.clients.base_client import (
    BaseClient,
)
from botocore import UNSIGNED
from sagemaker_jupyterlab_extension_common.util.environment import Environment

CW_PROD_ENDPOINT = "https://codewhisperer.us-east-1.amazonaws.com"
logging.basicConfig(format="%(levelname)s: %(message)s")


class QDevClient(ABC, BaseClient):
    def __init__(self):
        self._client = None

    @abstractmethod
    def call_chat_api(
        self, prompt, q_dev_profile_arn, conversation_id=None, customization_arn=None
    ):
        pass


class QDevSSOClient(QDevClient):
    def __init__(self, opt_out):
        super().__init__()
        client = QDevSSOClient.get_client(
            service_name="bearer",
            endpoint_url=CW_PROD_ENDPOINT,
            api_version="2023-11-27",
            region_name=CW_PROD_ENDPOINT.split(".")[1],
            signature_version=UNSIGNED,
        )
        partial_add_header = partial(QDevSSOClient.add_header, opt_out=opt_out)
        client.meta.events.register("before-sign.*.*", partial_add_header)
        self._client = client

    def call_chat_api(
        self, prompt, q_dev_profile_arn, conversation_id=None, customization_arn=None
    ):
        data = {
            "currentMessage": {"userInputMessage": {"content": f"{prompt}"}},
            "chatTriggerType": "MANUAL",
        }

        # add customizationArn key when there is selected customization
        if customization_arn:
            data["customizationArn"] = customization_arn

        if conversation_id and len(conversation_id):
            data["conversationId"] = conversation_id

        response = self._client.generate_assistant_response(
            conversationState=data, profileArn=q_dev_profile_arn
        )
        event_stream = response["generateAssistantResponseResponse"]

        return {
            "conversationId": response.get("conversationId", None),
            "eventStream": event_stream,
            "requestId": response.get("ResponseMetadata", None).get("RequestId", ""),
        }


class QDevIAMClient(QDevClient):
    def __init__(self, opt_out):
        super().__init__()
        logging.info("Initializing QDevIAMClient...")
        client = QDevIAMClient.get_client(
            service_name="qdeveloperstreaming",
            endpoint_url=CW_PROD_ENDPOINT,
            region_name=CW_PROD_ENDPOINT.split(".")[1],
            api_version="2024-06-11",
        )
        self._client = client
        # no headers are needed because this is sigv4 based free tier

    def call_chat_api(
        self, prompt, q_dev_profile_arn, conversation_id=None, customization_arn=None
    ):
        data = {
            "chatTriggerType": "MANUAL",
            "currentMessage": {
                "userInputMessage": {"content": f"{prompt}", "userInputMessageContext": {}}
            },
        }
        if conversation_id and len(conversation_id):
            data["conversationId"] = conversation_id

        # we don not use q_dev_profile_arn
        response = self._client.send_message(conversationState=data)
        response_stream = response["sendMessageResponse"]
        metadata = {}
        for event in response_stream:
            if "messageMetadataEvent" in event:
                metadata = event["messageMetadataEvent"]
                break

        return {
            "conversationId": metadata.get("conversationId", None),
            "eventStream": response_stream,
            "requestId": response.get("ResponseMetadata", None).get("RequestId", ""),
        }


class QDevChatClientFactory:
    _clients = {
        Environment.STUDIO_SSO: QDevSSOClient,
        Environment.MD_IDC: QDevSSOClient,
        Environment.STUDIO_IAM: QDevIAMClient,
        Environment.MD_IAM: QDevIAMClient,
    }

    @classmethod
    def get_client(cls, environment, opt_out):
        logging.info(f"Getting client creator for ${environment}")
        creator = cls._clients.get(environment)
        if not creator:
            raise ValueError(environment)
        return creator(opt_out=opt_out)
