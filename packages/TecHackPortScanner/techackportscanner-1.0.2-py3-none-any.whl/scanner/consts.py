"""
Módulo de constantes para o projeto.

Este módulo contém fingerprints de sistemas operacionais baseados em TTL e tamanho da janela,
bem como serviços conhecidos e suas portas padrão.
"""

# Fingerprints de Sistemas Operacionais (baseados em TTL e Tamanho da Janela)
OS_FINGERPRINTS = {
    (64, 5840): "Linux",
    (64, 14600): "Linux",
    (128, 8192): "Windows",
    (128, 65535): "Windows",
    (255, 4128): "Cisco",
    (255, 8760): "Solaris",
    (255, 16384): "FreeBSD/OpenBSD"
}

# Serviços conhecidos e suas portas padrão (https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers)
KNOWN_SERVICES = {
    "ftp": 21,
    "ssh": 22,
    "telnet": 23,
    "smtp": 25,
    "dns": 53,
    "dhcp": 67,
    "http": 80,
    "pop3": 110,
    "ntp": 123,
    "imap": 143,
    "snmp": 161,
    "ldap": 389,
    "https": 443,
    "smb": 445,
    "syslog": 514,
    "ftps": 989,
    "imaps": 993,
    "mysql": 3306,
    "rdp": 3389,
    "postgresql": 5432,
    "vnc": 5900,
    "redis": 6379,
    "mongodb": 27017,
    "cassandra": 9042,
    "minecraft": 25565,
    "minecraft_bedrock": 19132,
    "oracle_db": 1521,
    "mssql": 1433,
    "elastic_search": 9200,
    "kafka": 9092,
    "zookeeper": 2181
}
