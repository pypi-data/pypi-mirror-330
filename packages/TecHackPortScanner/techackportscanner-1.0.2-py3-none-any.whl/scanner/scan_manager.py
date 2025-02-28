"""
Módulo para escanear portas TCP e UDP e detectar o sistema operacional do alvo.
"""

from ssl import create_default_context, OP_NO_TLSv1, OP_NO_TLSv1_1
from socket import socket, AF_INET, SOCK_STREAM
from scapy.all import IP, TCP, sr1, send, UDP, ICMP
from scanner.consts import OS_FINGERPRINTS


def scan_tcp(ip: str, ports: list[int]) -> dict[int, tuple[str, any]]:
    """
    Escaneia portas TCP usando pacotes SYN.

    Args:
        ip (str): O endereço IP do alvo.
        ports (list[int]): Lista de portas a serem escaneadas.

    Returns:
        dict[int, tuple[str, any]]: Um dicionário com o número da porta como chave e uma tupla
                                    contendo o estado da porta ("Open", "Closed", "Filtered") e a resposta.
    """
    results = {}

    for port in ports:
        pkt = IP(dst=ip)/TCP(dport=port, flags="S")
        response = sr1(pkt, timeout=1, verbose=0)

        if response and response.haslayer(TCP):
            # SYN-ACK (0x12) received
            if response.getlayer(TCP).flags == 0x12:
                results[port] = ("Open", response)

                send(IP(dst=ip)/TCP(dport=port, flags="R"), verbose=0)

            # RST-ACK (0x14) received
            elif response.getlayer(TCP).flags == 0x14:
                results[port] = ("Closed", None)
        else:
            results[port] = ("Filtered", None)

    return results


def scan_udp(ip: str, ports: list[int]) -> dict[int, tuple[str, any]]:
    """
    Escaneia portas UDP enviando pacotes e analisando respostas.

    Args:
        ip (str): O endereço IP do alvo.
        ports (list[int]): Lista de portas a serem escaneadas.

    Returns:
        dict[int, tuple[str, any]]: Um dicionário com o número da porta como chave e uma tupla
                                    contendo o estado da porta ("Open", "Closed", "Filtered") e a resposta.
    """
    results = {}

    for port in ports:
        pkt = IP(dst=ip)/UDP(dport=port)
        response = sr1(pkt, timeout=2, verbose=0)

        if response is None:
            results[port] = ("Open/Filtered", None)

        elif response.haslayer(ICMP) and response.getlayer(ICMP).type == 3:
            results[port] = ("Closed", None)

        else:
            results[port] = ("Open", response)

    return results


def detect_os(response : any) -> str:
    """
    Detecta o sistema operacional usando TTL e tamanho da janela TCP.

    Args:
        response: A resposta do pacote.

    Returns:
        str: O sistema operacional detectado ou "Unknown" se não for possível detectar.
    """
    if response is None:
        return "Unknown"

    if response.haslayer(IP):
        ttl = response[IP].ttl
    else:
        ttl = None

    if response.haslayer(TCP):
        window_size = response[TCP].window
    else:
        window_size = None

    return OS_FINGERPRINTS.get((ttl, window_size), "Unknown")


def detect_os_via_banner(ip: str, port: int) -> str:
    """
    Detecta o sistema operacional via banner grabbing.

    Args:
        ip (str): O endereço IP do alvo.
        port (int): A porta do serviço.

    Returns:
        str: O sistema operacional detectado ou "Unknown" se não for possível detectar.
    """
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.settimeout(2)

        context = create_default_context()
        context.options |= OP_NO_TLSv1 | OP_NO_TLSv1_1

        c = context.wrap_socket(s, server_hostname=ip)

        c.connect((ip, port))

        c.send(b"HEAD / HTTP/1.1\r\nHost: " + ip.encode() + b"\r\n\r\n")
        banner = c.recv(1024).decode().strip()
        c.close()

        if "Server" in banner:
            return banner.split("Server: ")[1].split("\r\n")[0]

        if "NTLM" in banner:
            return "Windows"

        return "Unknown"

    except Exception as e:
        return f"Erro ao conectar: {e}"
