"""
Módulo para obter IPs e portas a partir de inputs.
"""

from enum import Enum
from ipaddress import ip_network
from socket import inet_pton, AF_INET, AF_INET6, error
from argparse import Namespace
from scanner.consts import KNOWN_SERVICES


class IPType(Enum):
    """
    Enumeração para representar os tipos de endereços IP.
    """
    IPV4 = "IPv4"
    IPV6 = "IPv6"
    CIDR = "CIDR"
    INVALID = "Invalid"


def args_parser(args: Namespace) -> tuple[IPType, list[str], list[int], bool]:
    """
    Analisa os argumentos fornecidos e retorna o tipo de IP, lista de IPs e lista de portas.

    Args:
        args (Namespace): Os argumentos fornecidos pelo usuário.

    Returns:
        tuple[IPType, list[str], list[int], bool]: Uma tupla contendo o tipo de IP, lista de IPs,
        lista de portas e um booleano indicando se o scan deve ser feito via UDP
    """
    ips, ip_type = __parse_ips(args.ip)

    if ip_type == IPType.INVALID:
        print("Erro: Endereço IP inválido.")
        return ip_type, [], [], False

    ports: list[int] = []

    if args.ports:
        ports.extend(__parse_ports(args.ports))

    if args.service:
        ports.extend(__parse_services(args.service))

    if not ports:
        ports = list(range(1, 65536))
    else:
        ports = sorted(set(ports))

    return ip_type, ips, ports, args.udp


def __parse_ips(ip_input: str) -> tuple[list[str], IPType]:
    """
    Obtém uma lista de IPs a partir de uma entrada de IP ou range de IPs.

    Args:
        ip_input (str): O endereço IP ou range de IPs a ser processado.

    Returns:
        tuple[list[str], IPType]: Uma tupla contendo uma lista de endereços IP e o tipo de IP.
                                  Retorna uma lista vazia se o IP for inválido.
    """
    ip_type = __validate_ip(ip_input)

    match ip_type:
        case IPType.IPV4:
            return [ip_input], ip_type
        case IPType.IPV6:
            return [ip_input], ip_type
        case IPType.CIDR:
            try:
                return [str(ip) for ip in ip_network(ip_input, strict=False)], ip_type
            except Exception:
                return [], IPType.INVALID
        case IPType.INVALID:
            return [], ip_type


def __validate_ip(ip: str) -> IPType:
    """
    Valida se um endereço IP é válido.

    Args:
        ip (str): O endereço IP a ser validado.

    Returns:
        bool: True se o endereço IP for válido (IPv4, IPv6 ou range), False caso contrário.
    """
    # Verifica se é um range de IPs
    if "/" in ip:
        return IPType.CIDR

    try:
        # Verifica se é um IPv4
        inet_pton(AF_INET, ip)
        return IPType.IPV4
    except error:
        pass

    try:
        # Verifica se é um IPv6
        inet_pton(AF_INET6, ip)
        return IPType.IPV6
    except error:
        return IPType.INVALID


def __parse_ports(port_range: str) -> set[int]:
    """
    Converte uma string de intervalo de portas '80,443,22-25' em uma lista de inteiros.

    Args:
        port_range (str): A string contendo portas individuais e/ou intervalos de portas.

    Returns:
        set[int]: Uma lista de números de portas.
    """
    ports = set()

    for part in port_range.split(","):
        if "-" in part:
            try:
                start, end = map(int, part.split("-"))
                ports.update(range(start, end + 1))

            except ValueError:
                print(f"{part} não é um intervalo de portas válido.")

        else:
            try:
                ports.add(int(part))

            except ValueError:
                print(f"{part} não é um número de porta válido.")

    return ports


def __parse_services(service_list: str) -> list[int]:
    """
    Converte uma string de serviços 'http,https,ftp' em uma lista de portas.

    Args:
        service_list (str): A string contendo serviços separados por vírgulas.

    Returns:
        list[int]: Uma lista de números de portas correspondentes aos serviços.
    """

    ports = []

    for service in service_list.split(","):
        service = service.strip()

        if service.lower() in KNOWN_SERVICES:
            service_port = KNOWN_SERVICES[service.lower()]
            ports.append(service_port)

            print(
                f"Procurando pelo serviço {service} na porta {service_port}...")

        else:
            print(f"Erro: Serviço desconhecido '{service}'.")

    return ports
