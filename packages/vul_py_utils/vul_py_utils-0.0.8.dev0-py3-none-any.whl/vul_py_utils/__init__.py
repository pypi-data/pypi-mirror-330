"""
    server_utils is combination of server's related utilities.
    It contains:
    - redis: utilities for redis
        + redis_client: init redis client
        + redis_key: redis task key
        + redis operation: get, set, delete, ...
    - env_getter: utilities for getting environment variables
    - logger: utilities for logging
    - benchmark: utilities for benchmarking runtime
    - configs: configurations to use among the server
    - constant: constants to use among the server
    - firebase: utilities for firebase
        + firebase_client: init firebase client
        + firestore_client: init firestore client
        + google_storage_client: init google storage client
        + firebase operation: upload, download, send FCM notification, edit firestore, ...
    - golang_request: utilities for making request to internal golang server
    - health: 
        + HealthStatus: enum for health status
        + Host simple health check server
    - image: utilities for image processing
    - jwt: utilities for verifying jwt
    - pickle: utilities for compressing and decompressing pickle
    - process_coordinator: utilities for coordinating between different services
        + Publisher/Subscriber: utilities for message queue
        + Firebase: functions for firebase
        + Redis: functions for redis
    - response: utilities for JSON response
"""
