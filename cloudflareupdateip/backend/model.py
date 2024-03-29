import CloudFlare


class cloudflare_api:

    def __init__(self, token):
        self._cf = CloudFlare.CloudFlare(token=token)

    # Get the current value of the 'A' record for the given domain
    def get_current_a_record(self, domain):
        try:
            zones = self._cf.zones.get(params={'name': domain})
            if not zones:
                print(f"No zones found for domain {domain}")
                return
            zone_id = zones[0]['id']
        except Exception as e:
            print(f"Error getting zones: {e}")
            return

        try:
            dns_records = self._cf.zones.dns_records.get(zone_id)
        except Exception as e:
            print(f"Error getting DNS records: {e}")
            return

        for record in dns_records:
            if record['name'] == domain and record['type'] == 'A':
                return record['content']
        print(f"No 'A' DNS record found for domain {domain}")
        return None

    def update_the_a_record(self, new_ip, domain, ):

        # Get the zone ID for the given domain
        try:
            zones = self._cf.zones.get(params={'name': domain})
            if not zones:
                print(f"No zones found for domain {domain}")
                return
            zone_id = zones[0]['id']
        except Exception as e:
            print(f"Error getting zones: {e}")
            return

        # Get the DNS records for the zone
        try:
            dns_records = self._cf.zones.dns_records.get(zone_id)
        except Exception as e:
            print(f"Error getting DNS records: {e}")
            return

        # Find the DNS record that matches the given domain and is of type 'A'
        for record in dns_records:
            if record['name'] == domain and record['type'] == 'A':
                dns_record_id = record['id']
                break
        else:
            print(f"No 'A' DNS record found for domain {domain}")
            return

        # Update the DNS record with the new IP address
        try:
            self._cf.zones.dns_records.put(zone_id, dns_record_id, data={
                'name': domain,
                'type': 'A',
                'content': new_ip
            })
            print(f"Updated 'A' DNS record for {domain} to {new_ip}")
        except Exception as e:
            print(f"Error updating DNS record: {e}")
