from resolver import DNSResolver

def main():
    resolver = DNSResolver()

    while True:
        domain = input("\nEnter domain name (or 'exit'): ")

        if domain.lower() == "exit":
            break

        ip = resolver.resolve(domain)

        if ip:
            print(f"\n Final IP Address: {ip}")
        else:
            print("\n Resolution failed.")


if __name__ == "__main__":
    main()

