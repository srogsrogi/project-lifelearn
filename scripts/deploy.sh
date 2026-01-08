#!/bin/bash

# 에러 발생 시 스크립트 중단
set -e

# 사용법 안내
if [ -z "$1" ]; then
    echo "사용법: ./scripts/deploy.sh <GOOGLE_CLOUD_PROJECT_ID>"
    echo "예시: ./scripts/deploy.sh my-awesome-project"
    exit 1
fi

PROJECT_ID=$1

echo "========================================================"
echo "🚀 배포 시작: 프로젝트 [$PROJECT_ID]"
echo "========================================================"

# 1. Backend 빌드 및 푸시
echo "--------------------------------------------------------"
echo "📦 Backend 이미지 빌드 중..."
docker build -t gcr.io/$PROJECT_ID/lifelearn-backend:latest ./backend

echo "⬆️  Backend 이미지 푸시 중..."
docker push gcr.io/$PROJECT_ID/lifelearn-backend:latest

# 2. Frontend 빌드 및 푸시
echo "--------------------------------------------------------"
echo "📦 Frontend 이미지 빌드 중..."
docker build -t gcr.io/$PROJECT_ID/lifelearn-frontend:latest ./frontend/project-lifelearn

echo "⬆️  Frontend 이미지 푸시 중..."
docker push gcr.io/$PROJECT_ID/lifelearn-frontend:latest

# 3. K8s YAML 파일 이미지 주소 업데이트 (sed 사용)
echo "--------------------------------------------------------"
echo "📝 Kubernetes 설정 파일 이미지 주소 업데이트..."

# 운영체제 확인 (Mac용 sed와 리눅스/윈도우용 sed 호환성 처리)
if [[ "$OSTYPE" == "darwin"* ]]; then
    SED_CMD="sed -i ''"
else
    SED_CMD="sed -i"
fi

# Backend YAML 수정
# 기존 이미지 주소 패턴을 찾아 교체
$SED_CMD "s|image: .*lifelearn-backend.*|image: gcr.io/$PROJECT_ID/lifelearn-backend:latest|g" k8s/05-backend.yaml

# Frontend YAML 수정
$SED_CMD "s|image: .*lifelearn-frontend.*|image: gcr.io/$PROJECT_ID/lifelearn-frontend:latest|g" k8s/06-frontend.yaml

echo "✅ YAML 파일 업데이트 완료"

# 4. GKE 배포
echo "--------------------------------------------------------"
echo "🚀 Kubernetes 클러스터에 배포 적용 중..."
kubectl apply -f k8s/

echo "========================================================"
echo "🎉 배포가 완료되었습니다!"
echo "상태 확인: kubectl get pods -n lifelearn"
echo "서비스 확인: kubectl get svc -n lifelearn"
echo "========================================================"
