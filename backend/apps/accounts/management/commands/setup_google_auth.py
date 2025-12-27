import os
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

class Command(BaseCommand):
    help = 'Setup Google SocialApp configuration from environment variables'

    def handle(self, *args, **options):
        client_id = os.environ.get('GOOGLE_CLIENT_ID')
        secret_key = os.environ.get('GOOGLE_SECRET_KEY')

        if not client_id or not secret_key:
            self.stdout.write(self.style.WARNING('GOOGLE_CLIENT_ID or GOOGLE_SECRET_KEY not found in environment variables.'))
            return

        # 1. Site 설정 (ID=1 기본 사이트)
        # 환경 변수로부터 도메인 가져오기 (기본값: localhost)
        site_domain = os.environ.get('SITE_DOMAIN', 'http://localhost').replace('http://', '').replace('https://', '')

        site, created = Site.objects.get_or_create(
            id=1,
            defaults={'domain': site_domain, 'name': site_domain}
        )
        # 도메인이 환경 변수와 다르면 업데이트
        if site.domain != site_domain or site.name != site_domain:
            site.domain = site_domain
            site.name = site_domain
            site.save()
            self.stdout.write(self.style.SUCCESS(f'Updated Site domain to: {site_domain}'))

        # 2. SocialApp 설정
        app, created = SocialApp.objects.update_or_create(
            provider='google',
            defaults={
                'name': 'Google Login',
                'client_id': client_id,
                'secret': secret_key,
            }
        )
        
        # Site 연결 확인
        if not app.sites.filter(id=site.id).exists():
            app.sites.add(site)

        if created:
            self.stdout.write(self.style.SUCCESS(f'Successfully created SocialApp: {app.name}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Successfully updated SocialApp: {app.name}'))
