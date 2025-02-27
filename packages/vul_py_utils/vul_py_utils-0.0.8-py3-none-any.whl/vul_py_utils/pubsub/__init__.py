"""
    This module is used to publish messages to pub/sub
"""
from google.cloud import pubsub_v1

from ..pickle import pickle


class PubSub():
    """
    The PubSub class is used to publish messages to pub/sub
    You must provide a service account file, project id, topic, and subscription id to authenticate
    """
    def __init__(self, service_account_path: str, project_id: str, topic: str, subscription_id: str) -> None:
        """_summary_

        Args:
            service_account_path (str): path to service account file
            project_id (str): Google Cloud project ID
            topic (str): Google Cloud Pub/Sub topic
            subscription_id (str): Google Cloud Pub/Sub subscription ID
        """
        self.project_id = project_id
        self.publisher = pubsub_v1.PublisherClient.from_service_account_file(service_account_path)
        self.service_account_path = service_account_path
        # Topic
        self.topic = topic
        # SubscriptionID
        self.subscription_id = subscription_id

    def get_topic_by_filter(self, filter: str = "") -> str:
        """_summary_

        Args:
            filter (str, optional): this field is used to filter topic. Defaults to "". Example usage: if filter == "anime" then return "anime-topic".

        Returns:
            str: _description_
        """
        return self.publisher.topic_path(self.project_id, self.topic)

    def publish(self, id: str, data: dict, is_premium: bool = False) -> str:
        """_summary_

        Args:
            id (str): task id
            data (dict): any data you want to send. WARNING: the larger the data, the more cost. 
            is_premium (bool, optional): flag if User is premium. Defaults to False.

        Returns:
            str: returns the result of the action MessagePublish 
        """
        topic_path = self.get_topic_by_filter()
        high_priority_attributes = {"priority": "high" if is_premium else "low"}

        data["id"] = id
        # When you publish a message, the client returns a future.
        future = self.publisher.publish(topic_path, pickle.compress(data), **high_priority_attributes)
        print("Published message ID {} to topic {}.".format(future.result(), topic_path))
        return future.result()
