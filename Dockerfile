# Python 3.11 일반 버전 사용
FROM python:3.11

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 및 Java 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    default-jdk \
    && rm -rf /var/lib/apt/lists/*

# requirements.txt 복사
COPY requirements.txt .

# Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 파일 복사
COPY . .

# FastAPI가 사용할 포트 개방
EXPOSE 8000

# FastAPI 실행 명령어
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
