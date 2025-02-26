from google.cloud import firestore # pylint: disable=import-error,no-name-in-module

from datetime import datetime, timezone
from typing import Annotated, List, Union
from firebase_admin import credentials, messaging, storage, firestore, initialize_app

from ..redis.keys import TaskStatus


class FirebaseClient:
    """ This class is used to interact with Firebase """

    def __init__(self, key_path: str, storage_bucket: str = "", app_name: str = "app"):
        firebase_cred = credentials.Certificate(key_path)
        if storage_bucket is None:
            firebase_app = initialize_app(
                credential=firebase_cred, name=app_name)
        else:
            firebase_app = initialize_app(credential=firebase_cred, options={
                                          "storageBucket": storage_bucket}, name=app_name)
        self.app = firebase_app
        self.db: firestore.Client = firestore.client(app=firebase_app)
        self.bucket = storage.bucket(app=firebase_app)

    def send_fcm_notification(self, device_tokens: List[str], data: dict, title: str = "Task Done", body: str = "Your task is ready", click_action: str = "") -> Union[None, List[dict[str, any]]]:
        """Send Firebase Cloud Messaging (FCM) Notification to device_tokens 

        Args:
            device_tokens (List[str]): List of device tokens
            data (dict): Data to send to device_tokens
            title (str, optional): Title of notification. Defaults to "Task Done".
            body (str, optional): Body of notification. Defaults to "Your task is ready".
            click_action (str, optional): Click action of notification. Defaults to "".
        
        Returns:
            Union[None, List[dict[str, any]]]: None if no error, otherwise return list of failed cases
        """
        message = messaging.MulticastMessage(data=data,
                                             notification=messaging.Notification(
                                                 title=title, body=body),
                                             tokens=device_tokens, 
                                             android=messaging.AndroidConfig(notification=messaging.AndroidNotification(click_action=click_action)))
        response: messaging.BatchResponse = messaging.send_multicast(
            app=self.app, multicast_message=message)
        if response.failure_count > 0:
            failed_cases = self.__record_fcm_error(device_tokens, response)
            return failed_cases
    
    def set_document(self, collection: str, document: str, data: dict) -> None:
        """ Set a Document to Firestore

        Args:
            collection (str): collection name
            document (str): document_id
            data (dict)
        """
        doc_ref: firestore.DocumentReference = self.db.collection(collection).document(document)
        doc_ref.set(data)
    
    def set_sub_document(self, collection: str, document: str, sub_collection: str, sub_document: str, data: dict) -> None:
        """ Set a Document inside another Collection-Document to Firestore. Example: Processes/{user_id}/ArtWork/{task_id}

        Args:
            collection (str):
            document (str):
            sub_collection (str):
            sub_document (str):
            data (dict):
        """
        doc_ref: firestore.DocumentReference = self.db.collection(collection).document(document).collection(sub_collection).document(sub_document)
        doc_ref.set(data)
        
    def get_document(self, collection: str, document: str) -> Annotated[dict, None]:
        """ Get a Document from Firestore

        Args:
            collection (str):
            document (str):

        Returns:
            Annotated[dict, None]:
        """
        doc_ref: firestore.DocumentReference = self.db.collection(collection).document(document)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return None
        
    def get_all_document_by_collection(self, collection: str):
        """ Get all Document existsed in a collection on Firestore

        Args:
            collection (str):

        Returns:
            Iterator of DocumentSnapshot
        """
        snap_ref = self.db.collection(collection).stream()
        return snap_ref
        
    def get_sub_document(self, collection: str, document: str, sub_collection: str, sub_document: str) -> Annotated[dict, None]:
        """ Get a Document inside another Collection-Document from Firestore. Example: Processes/{user_id}/ArtWork/{task_id}

        Args:
            collection (str): 
            document (str): 
            sub_collection (str): 
            sub_document (str): 

        Returns:
            Annotated[dict, None]: Document data in dict format
        """
        doc_ref: firestore.DocumentReference = self.db.collection(collection).document(document).collection(sub_collection).document(sub_document)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return None
        
    def get_all_document_by_sub_collection(self, collection: str, document: str, sub_collection: str):
        """ Get all Document existsed in a sub collection inside a collection on Firestore. Example: Processes/{user_id}/ArtWork

        Args:
            collection (str):
            document (str):

        Returns:
            Iterator of DocumentSnapshot
        """
        snap_ref = self.db.collection(collection).document(document).collection(sub_collection).stream()
        return snap_ref
        
    def update_document(self, collection: str, document: str, data: dict) -> None:
        """ Update a Document to Firestore

        Args:
            collection (str):
            document (str):
            data (dict):
        """
        doc_ref: firestore.DocumentReference = self.db.collection(collection).document(document)
        doc_ref.update(data)
        
    def update_sub_document(self, collection: str, document: str, sub_collection: str, sub_document: str, data: dict) -> None:
        """ Update a Document inside another Collection-Document to Firestore. Example: Processes/{user_id}/ArtWork/{task_id}

        Args:
            collection (str): 
            document (str): 
            sub_collection (str): 
            sub_document (str): 
            data (dict): 
        """
        doc_ref: firestore.DocumentReference = self.db.collection(collection).document(document).collection(sub_collection).document(sub_document)
        doc_ref.update(data)

    def __record_fcm_error(self, tokens: List[str], response: messaging.BatchResponse) -> List[dict[str, any]]:
        """ Log FCM Error

        Args:
            tokens (List[str]): list of tokens
            response (messaging.BatchResponse): response from FCM

        Returns:
            List[str]: include list of tokens that caused failures
        """
        failed_cases = []
        for idx, resp in enumerate(response.responses):
            resp: messaging.SendResponse
            if not resp.success:
                print("[FCM Token] Error is", resp.exception)
                # The order of responses corresponds to the order of the registration tokens
                detail = {
                    "token": tokens[idx],
                    "error": resp.exception
                }
                failed_cases.append(detail)
        return failed_cases


class FirebaseClientWithTask(FirebaseClient):
    """ This class is used to interact with Firebase and Task
    """
    def __init__(self, key_path: str, storage_bucket: str = "", app_name: str = "app", task_collection: str = "Processes", task_sub_collection: str = "ArtWork"):
        """ The init stage of FirebaseWithTask requires key_path, task_collection and task_sub_collection. 
            The task_collection and task_sub_collection are used to store task information on Firestore
            The hierarchy of Firestore is: TaskCollection/{user_id}/TaskSubCollection/{task_id}

        Args:
            key_path (str): path to crendential key file
            storage_bucket (str, optional): name of Google Cloud Bucket. Defaults to "".
            app_name (str, optional): Defaults to "app".
            task_collection (str, optional): collection name for task. Defaults to "Processes".
            task_sub_collection (str, optional): collection name for sub document of task. Defaults to "ArtWork".
        """
        super().__init__(key_path, storage_bucket, app_name)
        self.task_collection = task_collection
        self.task_sub_collection = task_sub_collection
    
    def pend_task(self, task_id: str, user_id: str, task_data: dict) -> None:
        """ Init Task information on Firestore

        Args:
            task_id (str)
            user_id (str)
            task_data (dict)
        """
        self.__init_task_to_firestore(task_id=task_id, status=TaskStatus.pending.value, user_id=user_id, task_data=task_data)

    def start_process_task(self, task_id: str, user_id: str) -> None:
        """ Update task's status -> in_process on Firestore

        Args:
            task_id (str): 
            user_id (str): 
        """
        self.__update_task_to_firestore(task_id, user_id, {"status": TaskStatus.in_process.value})

    def failed_task(self, task_id: str, user_id: str) -> None:
        """ Update task's status -> failed on Firestore

        Args:
            task_id (str): 
            user_id (str): 
        """
        self.__update_task_to_firestore(task_id, user_id, task_data={"status": TaskStatus.failed.value})

    def cancel_process_task(self, task_id: str, user_id: str) -> None:
        """ Update task's status -> cancelled on Firestore

        Args:
            task_id (str): 
            user_id (str): 
        """
        self.__update_task_to_firestore(task_id, user_id, task_data={"status": TaskStatus.cancelled.value})

    def done_task(self, device_tokens: List[str], user_id: str, task_id: str, file_data: bytes = b'', file_extension: str = ".mp4" ) -> str:
        """ Update task's status -> done on Firestore and push result to Google Cloud Storage

        Args:
            device_tokens (List[str]): list of device tokens
            user_id (str):
            task_id (str):
            file_data (bytes, optional): byte data of the task result. Defaults to b''.
            file_extension (str, optional): file format of the task result. Defaults to ".mp4".
            
        Returns:
            str: public url of file
        """
        result_url = self.__push_result_to_google_cloud(task_id, user_id, file_data=file_data, file_extension=file_extension)
        self.__update_task_to_firestore(task_id, user_id, task_data={"status": TaskStatus.done.value, 
                                                                     "result_url": result_url,})
        print(f"Firebase finished task {task_id} {TaskStatus.done.value}")
        self.send_fcm_notification(device_tokens, data={"task_id": task_id, "result_url": result_url})
        return result_url

    def get_task(self, user_id: str, task_id: str) -> Annotated[dict, None]:
        """ Get Task Information from Firestore

        Args:
            user_id (str):
            task_id (str):

        Returns:
            Annotated[dict, None]: if task exists, return task information, otherwise return None
        """
        return self.get_sub_document(collection=self.task_collection, document=user_id, sub_collection=self.task_sub_collection, sub_document=task_id)

    def get_all_task(self, user_id: str) -> List[dict]: 
        """ Get all Task Information from Firestore which is not failed or cancelled

        Args:
            user_id (str)

        Returns:
            List[dict]: a list of task information
        """
        snap_ref = self.get_all_document_by_sub_collection(collection=self.task_collection, document=user_id, sub_collection=self.task_sub_collection)
        all_task = []
        for doc in snap_ref:
            doc: firestore.DocumentSnapshot
            doc.to_dict()
            if doc.to_dict()["status"] in [TaskStatus.done.value, TaskStatus.pending.value, TaskStatus.in_process.value]:
                # Only get task that is done, pending or in_process
                # Ignore task that is failed or cancelled
                doc_dict = doc.to_dict()
                doc_dict["id"] = doc.id
                all_task.append(doc_dict)
        return all_task

    def __init_task_to_firestore(self,task_id: str, status: int, user_id: str, task_data: dict) -> None:
        """ Init Task to Firestore

        Args:
            task_id (str): 
            status (int): 
            user_id (str): 
            task_data (dict): 
        """
        data = {**task_data, 
                "status": status,}
        self.set_sub_document(collection=self.task_collection, document=user_id, sub_collection=self.task_sub_collection, sub_document=task_id, data=data)

    def __update_task_to_firestore(self, task_id: str, user_id: str, task_data: dict = {}) -> None:
        """ Update Task to Firestore

        Args:
            task_id (str): 
            user_id (str): 
            task_data (dict, optional): Defaults to {}.
        """
        data = {**task_data,
                "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d%H:%M:%S")}
        self.update_sub_document(collection=self.task_collection, document=user_id, sub_collection=self.task_sub_collection, sub_document=task_id, data=data)

    def __push_result_to_google_cloud(self, task_id: str, user_id: str, file_data: bytes, file_extension: str = "mp4") -> str:
        """ Push result to Google Cloud Storage

        Args:
            task_id (str): 
            user_id (str): 
            file_data (bytes): the bytes of file, this file could be mp4 or gif or any file type
            file_extension (str, optional): Defaults to "mp4".

        Returns:
            str: public url of file
        """
        blob = self.bucket.blob(f"{user_id}/{task_id}/{task_id}.{file_extension}")
        blob.upload_from_string(file_data)
        blob.make_public()
        return blob.public_url
