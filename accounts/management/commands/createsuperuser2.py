# myapp/management/commands/createsuperuser.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

class Command(BaseCommand):
    help = 'Create a superuser with custom prompts for username and email'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Username for the superuser')
        parser.add_argument('--email', type=str, help='Email address for the superuser')

    def handle(self, *args, **options):
        """
        Overriding the handle method to add prompts for username and email.
        """
        User = get_user_model()

        # Custom prompt for username
        username = options.get('username')
        if not username:
            username = input("Username: ")

        # Custom prompt for email
        email = options.get('email')
        if not email:
            email = input("Email address: ")

        # Prompt for password
        password = input("Password: ")

        # Create the superuser
        User.objects.create_superuser(username=username, email=email, password=password)

        self.stdout.write(self.style.SUCCESS(f'Successfully created superuser {username}'))
