"""
scanner package
This package provides functionalities for network scanning and detection.
Modules:
- detector: Contains functions for detecting network services and handling request arguments.
- scan_manager: Provides functions for TCP and UDP scanning, as well as OS detection.
- consts: Defines constants used across the scanner package.
Functions imported:
- detect: Detects network services.
- request_args: Handles request arguments for detection.
- scan_tcp: Performs TCP scanning.
- scan_udp: Performs UDP scanning.
- detect_os: Detects the operating system.
- detect_os_via_banner: Detects the operating system via banner grabbing.
Constants imported:
- KNOWN_SERVICES: A dictionary of known network services.
Version:
- 1.0.0
"""
from scanner.detector import detect, request_args
from scanner.scan_manager import scan_tcp, scan_udp, detect_os, detect_os_via_banner
from scanner.consts import KNOWN_SERVICES

__version__ = "1.0.0"
