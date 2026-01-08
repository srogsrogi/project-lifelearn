# backend/config/settings/prod.py

from .base import *
import os
from pathlib import Path
from dotenv import load_dotenv
import logging

# Docker 환경에서는 환경변수가 docker-compose의 env_file로 이미 로드됨
# load_dotenv를 사용하면 --env-file 옵션을 덮어쓰므로 제거

DEBUG = False

# ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")
ALLOWED_HOSTS = ["*"]

# Elasticsearch (Docker 환경)
ELASTICSEARCH_URL = os.environ.get("ES_URL", "http://elasticsearch:9200")

# 이메일 설정 (임시: console backend 사용)
# TODO: 실제 프로덕션에서는 SMTP 설정 필요
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set")

# 운영용 PostgreSQL (Docker 환경)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "moduway"),
        "USER": os.environ.get("POSTGRES_USER", "moduway"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "moduway"),
        "HOST": os.environ.get("POSTGRES_HOST", "db"),
        "PORT": int(os.environ.get("POSTGRES_PORT", 5432)),
        "CONN_MAX_AGE": 60,  # 연결 재사용
    }
}

# 로그 디렉토리 생성 (운영 환경: /data/logs)
DATA_DIR = Path("/data")
LOG_DIR = DATA_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# 미디어 파일 (사용자 업로드) 및 정적 파일 경로
MEDIA_ROOT = DATA_DIR / "media"
MEDIA_URL = "/media/"

STATIC_ROOT = DATA_DIR / "static"
STATIC_URL = "/static/"

# Django 로깅: 콘솔 + 파일(7일 보관)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "[{asctime}] {levelname} {name}:{lineno} | {message}", "style": "{"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
        "file_rotating": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": str(LOG_DIR / "django.log"),
            "when": "D",
            "interval": 1,
            "backupCount": 7,
            "encoding": "utf-8",
            "formatter": "verbose",
        },
    },
    "root": {"handlers": ["console", "file_rotating"], "level": "WARNING"},
    "loggers": {
        "django": {"handlers": ["console", "file_rotating"], "level": "WARNING", "propagate": False},
        "django.request": {"handlers": ["console", "file_rotating"], "level": "ERROR", "propagate": False},
    },
}