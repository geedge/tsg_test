# -*- coding: utf-8 -*-
from datetime import datetime
import requests
import struct
import dns.message
import dns.name

class DohPlayer:
    def send_doh_query(self, traffic_data):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Begin to send doh query for effect verification.", flush=True)
        
        domain = traffic_data["domain"]
        query_type = traffic_data["query_type"]
        doh_server_url = traffic_data["doh_server_url"]
        
        query_id, query_wire = self.create_dns_query(domain, query_type)
        data = query_wire
        headers = {
            "Content-Type": "application/dns-message"
        }
        response = requests.post(doh_server_url, headers=headers, data=data)
        
        response_data = ""
        if response.status_code == 200:
            response_data = dns.message.from_wire(response.content)
            for rrset in response_data.answer:
                for rd in rrset:
                    return f"Type: {dns.rdatatype.to_text(rd.rdtype)}, Rdata: {rd.to_text()}"
        else:
            return f"Error querying DoH server: {response.status_code}"
    
    def create_dns_query(self, domain, qtype):
        query = dns.message.make_query(dns.name.from_text(domain), qtype)
        query_wire = query.to_wire()
        query_id = struct.unpack('!H', query_wire[:2])[0]
        return query_id, query_wire

if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")
    test_data = {
        "traffic": {
            "protocol": "doh",
            "type": "client",
            "domain": "www.google.com", # ipv6.google.com
            "query_type": "A", # AAAA
            # "doh_server_url": "https://dns9.quad9.net/dns-query"
            "doh_server_url": "https://dns.quad9.net/dns-query"
        }
    }
    traffic_data = test_data["traffic"]
    doh_player = DohPlayer()
    results_doh = doh_player.send_doh_query(traffic_data, "ui", False)
    print(results_doh)
