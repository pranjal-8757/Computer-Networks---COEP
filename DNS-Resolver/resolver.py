import dns.message
import dns.query
import dns.rdatatype
import time
import json
import os

ROOT_SERVER = "198.41.0.4"
CACHE_FILE = "cache.json"


class DNSResolver:
    def __init__(self):
        self.cache = self.load_cache()

    # ---------------- CACHE ----------------

    def load_cache(self):
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_cache(self):
        with open(CACHE_FILE, "w") as f:
            json.dump(self.cache, f, indent=4)

    def get_cached(self, domain):
        if domain in self.cache:
            entry = self.cache[domain]
            if time.time() < entry["expires_at"]:
                print("Cache hit!")
                return entry["ip"]
            else:
                print("Cache expired.")
                del self.cache[domain]
                self.save_cache()
        return None

    def add_to_cache(self, domain, ip, ttl):
        self.cache[domain] = {
            "ip": ip,
            "expires_at": time.time() + ttl
        }
        self.save_cache()

    # ---------------- ITERATIVE RESOLUTION ----------------

    def resolve(self, domain):

        domain = domain.strip().lower().rstrip(".")

        # Check cache
        cached_ip = self.get_cached(domain)
        if cached_ip:
            return cached_ip

        print("Cache miss.")
        print("Starting iterative resolution...")

        return self.iterative_lookup(domain)


    def iterative_lookup(self, domain):

        current_server = ROOT_SERVER
        visited_servers = set()
        max_depth = 25
        depth = 0
        level = "Root Server"

        while depth < max_depth:
            depth += 1

            if current_server in visited_servers:
                print("Loop detected.")
                return None

            visited_servers.add(current_server)

            print(f"➡ Querying {level}: {current_server}")

            try:
                query = dns.message.make_query(domain, dns.rdatatype.A)
                response = dns.query.udp(query, current_server, timeout=5)
            except Exception:
                print("Server timeout.")
                return None

            # ---------------- ANSWER SECTION ----------------
            if response.answer:
                for answer in response.answer:

                    # Handle A record
                    if answer.rdtype == dns.rdatatype.A:
                        for item in answer:
                            ip = item.address
                            ttl = answer.ttl
                            print(f"Found IP: {ip}")
                            self.add_to_cache(domain, ip, ttl)
                            return ip

                    # Handle CNAME
                    if answer.rdtype == dns.rdatatype.CNAME:
                        cname_target = answer[0].target.to_text().rstrip(".")
                        print(f"Following CNAME → {cname_target}")
                        return self.resolve(cname_target)

            # ---------------- ADDITIONAL SECTION ----------------
            if response.additional:
                for additional in response.additional:
                    if additional.rdtype == dns.rdatatype.A:
                        for item in additional:
                            current_server = item.address
                            break
                        break

                level = "Authoritative Server"
                continue

            # ---------------- AUTHORITY SECTION ----------------
            ns_name = None

            if response.authority:
                for authority in response.authority:
                    if authority.rdtype == dns.rdatatype.NS:
                        for item in authority:
                            ns_name = item.target.to_text().rstrip(".")
                            break
                    if ns_name:
                        break

            if ns_name:
                print(f"Resolving NS: {ns_name}")

                ns_ip = self.iterative_lookup(ns_name)

                if ns_ip:
                    current_server = ns_ip
                    level = "TLD/Delegated Server"
                    continue
                else:
                    print("Failed resolving NS.")
                    return None

            print("Resolution failed.")
            return None

        print("Max depth reached.")
        return None

