# backend/apps/accounts/views.py

import os
from django.shortcuts import render
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    # 환경 변수로부터 사이트 도메인을 가져와서 callback URL 생성
    # 로컬: http://localhost, 프로덕션: https://life-learn.site
    # console.cloud.google.com/에 승인된 리디렉션 URI로 등록되어 있어야 함
    @property
    def callback_url(self):
        site_domain = os.environ.get('SITE_DOMAIN', 'http://localhost')
        return f"{site_domain}/api/v1/accounts/google/login/callback/" 
    