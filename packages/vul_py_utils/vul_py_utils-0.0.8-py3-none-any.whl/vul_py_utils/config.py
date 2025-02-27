"""
    This file contains all the Environments-DefaultValue used in the project.
"""

# GPU Multi-processing
try:
    import torch
    CUDA_WORLD_SIZE = {
        "key": "CUDA_WORLD_SIZE",
        "default": torch.cuda.device_count(),
    }
except Exception as e:
    CUDA_WORLD_SIZE = {
        "key": "CUDA_WORLD_SIZE",
        "default": 1,
    }

# Redis
USE_REDIS = {
    "key": "USE_REDIS",
    "default": False,
}

REDIS_LOCATION = {
    "key": "REDIS_LOCATION",
    "default": "redis://localhost:6379",
}

REDIS_CLUSTER = {
    "key": "REDIS_CLUSTER",
    "default": "",
}

REDIS_TIME_TO_LIVE = {
    "key": "REDIS_TIME_TO_LIVE",
    "default": 24 * 60 * 60, # 1 day
}

# Android 
ANDROID_FIREBASE_CREDENTIAL_PATH = {
    "key": "ANDROID_FIREBASE_CREDENTIAL_PATH",
    "default": "/certs/ai-service-android.json",
}

ANDROID_PUBSUB_PROJECT_ID = {
    "key": "ANDROID_PROJECT_ID",
    "default": "text-to-animation-android",
}

ANDROID_STORAGE_BUCKET = {
    "key": "ANDROID_STORAGE_BUCKET",
    "default": "android-ani-staging-results",

}
# IOS
IOS_FIREBASE_CREDENTIAL_PATH = {
    "key": "IOS_FIREBASE_CREDENTIAL_PATH",
    "default": "/certs/ai-service-ios.json",
}

IOS_PUBSUB_PROJECT_ID = {
    "key": "IOS_PROJECT_ID",
    "default": "animationai-ios",
}

IOS_STORAGE_BUCKET = {
    "key": "IOS_STORAGE_BUCKET",
    "default": "ani-staging-results",
}
# Same for both IOS and Android
PUBSUB_SUBSCRIPTION_ID = {
    "key": "SUBSCRIPTION_ID",
    "default": "animation-beautify-dev-sub",
}

PUBSUB_TOPIC_ID = {
    "key": "TOPIC_ID",
    "default": "animation-beautify-dev",
}

NUM_MESSAGES = {
    "key": "NUM_MESSAGES",
    "default": 1,
}

# Security
JWT_SECRET = {
    "key": "JWT_SECRET",
    "default": "ahihidongoc:3",
}

ALGORITHM = {
    "key": "ALGORITHM",
    "default": "HS256",
}