import socket

with open("history_data.txt", "r") as f:
    data = f.readlines()

domain_names = set()
for url in data:
    final_url = urlparse(url).netloc
    final_url = final_url.split(":")[0]
    domain_names.add(final_url)

ip_set = set()
for domain in domain_names:
    try:
        ip_addr = socket.gethostbyname(domain)
        ip_set.add(ip_addr)
    except:
        print(domain)
