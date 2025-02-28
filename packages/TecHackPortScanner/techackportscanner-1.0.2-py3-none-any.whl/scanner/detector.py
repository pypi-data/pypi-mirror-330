"""
Módulo para escanear portas TCP/UDP e detectar o sistema operacional e serviços.

Este módulo fornece funcionalidades para escanear portas TCP e UDP em um endereço IP ou range de IPs,
e detectar o sistema operacional e serviços associados às portas abertas.
"""
from argparse import ArgumentParser, Namespace
from scanner.args_parser import IPType, args_parser
from scanner.scan_manager import scan_tcp, scan_udp, detect_os
from scanner.consts import KNOWN_SERVICES


def detect(args: Namespace) -> None:
    """
    Realiza a detecção de portas abertas e do sistema operacional em um endereço IP ou range de IPs.

    Args:
        args (Namespace): Os argumentos fornecidos pelo usuário, incluindo IP, portas e opções de escaneamento.
    """
    ip_type, ips, ports, udp = args_parser(args)

    if ip_type == IPType.INVALID:
        return

    if udp:
        print(f"Escaneando portas UDP em {ports}...")
    else:
        print(f"Escaneando portas TCP em {ports}...")

    for ip in ips:
        print(f"\nEscaneando IP: {ip}")

        if udp:
            results = scan_udp(ip, ports)
        else:
            results = scan_tcp(ip, ports)

        print("\nResultados:")
        print("=" * 50)
        print(f"{'Port':<10}{'Status':<15}{'Serviço':<15}")
        print("=" * 50)

        os_response = None

        for port, (status, response) in results.items():
            service_name = next(
                (s for s, p in KNOWN_SERVICES.items() if p == port), "Unknown")

            print(f"{port:<10}{status:<15}{service_name:<15}")

            if status == "Open" and response:
                os_response = response

        if os_response:
            print("=" * 50)
            print(
                f"\nNo {ip} foi detectado o sistema operacional: {detect_os(os_response)}")


def request_args() -> Namespace:
    """
    Analisa os argumentos da linha de comando fornecidos pelo usuário.

    Returns:
        Namespace: Um objeto Namespace contendo os argumentos fornecidos pelo usuário.
    """
    parser = ArgumentParser(
        description="Advanced TCP/UDP Port Scanner with OS & Service Detection")

    parser.add_argument(
        "ip", type=str, help="Target IP address, IPv6, or range (e.g., '192.168.1.1' or '192.168.1.0/24')")

    parser.add_argument("-p", "--ports", type=str, default="1-1024",
                        help="Port range, e.g., '22,80,443' or '20-25'")

    parser.add_argument("--udp", action="store_true",
                        help="Enable UDP scanning")

    parser.add_argument("--service", type=str,
                        help="Scan a specific service (e.g., ssh, http, rdp)")

    return parser.parse_args()
