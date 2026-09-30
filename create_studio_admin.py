import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

def create_admin():
    User = get_user_model()
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'quorv_admin')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'quorv911@gmail.com')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'QuorvStudio2026!')

    user, created = User.objects.get_or_create(username=username, defaults={'email': email})
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.email = email
    user.save()

    if created:
        print(f"Superuser '{username}' created successfully!")
    else:
        print(f"Superuser '{username}' updated with new credentials.")
    print(f"Login URL: http://127.0.0.1:8000/admin/")
    print(f"Username: {username}")
    print(f"Email: {email}")

if __name__ == '__main__':
    create_admin()
