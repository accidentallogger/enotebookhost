from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class InviteTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, email, timestamp):
        # Use email and timestamp to generate a hash value for the token
        return urlsafe_base64_encode(force_bytes(email)) + str(
            timestamp
        )  # Convert timestamp to string for hash value


invite_token_generator = InviteTokenGenerator()
