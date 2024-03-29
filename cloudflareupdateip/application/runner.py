import os
import requests

from cloudflareupdateip.backend.model import cloudflare_api


def get_my_current_public_ip():
    return requests.get('https://ifconfig.me/ip').text.strip()


class CloudflareUpdater:

    def __init__(self):
        token = os.environ.get('CF_TOKEN')
        self._cloudflare_api = cloudflare_api(token)

        # get domain from environment variable $CURRENT_DOMAIN
        self._domain = os.getenv('CURRENT_DOMAIN')

    @staticmethod
    def get_local_ip():
        current_ip = get_my_current_public_ip()
        print(f"Current Local IP address: {current_ip}")
        return current_ip

    def get_cloudflare_current_ip(self):
        current_ip = self._cloudflare_api.get_current_a_record(self._domain)
        return current_ip

    def update(self, current_ip):
        current_a_record = self._cloudflare_api.get_current_a_record(self._domain)

        if current_a_record != current_ip:
            self._cloudflare_api.update_the_a_record(current_ip, self._domain)
            print(f"Updated {self._domain} to {current_ip}")
        else:
            print(f"{self._domain} is already pointing to {current_ip}")
