# backend/apps/accounts/migrations/0002_setup_google_auth.py

from django.db import migrations
from django.conf import settings

def create_social_app(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    SocialApp = apps.get_model('socialaccount', 'SocialApp')

    # 1. Site 설정
    # 기본으로 생성되는 ID 1번 사이트 생성
    # 환경 변수로부터 도메인 가져오기 (기본값: localhost)
    import os
    site_domain = os.environ.get('SITE_DOMAIN', 'http://localhost').replace('http://', '').replace('https://', '')

    site, created = Site.objects.get_or_create(id=1)
    site.domain = site_domain
    site.name = site_domain
    site.save()

    # 2. SocialApp 설정
    import os
    client_id = os.environ.get('GOOGLE_CLIENT_ID')
    secret_key = os.environ.get('GOOGLE_SECRET_KEY')

    if client_id and secret_key:
        app, created = SocialApp.objects.get_or_create(
            provider='google',
            name='Google Login',
            client_id=client_id,
            secret=secret_key
        )
        app.sites.add(site)

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
        ('sites', '0001_initial'),
        ('socialaccount', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_social_app),
    ]