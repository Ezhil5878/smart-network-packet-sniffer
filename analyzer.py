"""
analyzer.py - Packet Dissection & Protocol Analysis Module
Smart Network Packet Sniffer v2
"""

from datetime import datetime
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.inet6 import IPv6
from scapy.layers.l2 import ARP, Ether


# Static dictionary for well-known transport layer ports (Common Service Mapping)
COMMON_SERVICES = {
    20: "FTP-Data",
    21: "FTP-Control",
    22: "SSH",
    23: "Telnet (Insecure)",
    25: "SMTP",
    53: "DNS",
    67: "DHCP-Server",
    68: "DHCP-Client",
    80: "HTTP (Cleartext)",
    110: "POP3",
    123: "NTP",
    143: "IMAP",
    161: "SNMP",
    162: "SNMP-Trap",
    443: "HTTPS",
    445: "SMB",
    587: "SMTP-Submission",
    993: "IMAPS",
    995: "POP3S",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    8080: "HTTP-Proxy",
    8443: "HTTPS-Alt"
}

# TCP Flag bit mapping
TCP_FLAG_MAP = {
    "F": "FIN",
    "S": "SYN",
    "R": "RST",
    "P": "PSH",
    "A": "ACK",
    "U": "URG",
    "E": "ECE",
    "C": "CWR"
}

# ICMP Type mapping
ICMP_TYPE_MAP = {
    0: "Echo Reply (Pong)",
    3: "Destination Unreachable",
    4: "Source Quench",
    5: "Redirect",
    8: "Echo Request (Ping)",
    9: "Router Advertisement",
    10: "Router Solicitation",
    11: "Time Exceeded (TTL Expired)",
    12: "Parameter Problem",
    13: "Timestamp Request",
    14: "Timestamp Reply"
}

# ICMP Destination Unreachable Code mapping
ICMP_UNREACHABLE_CODES = {
    0: "Net Unreachable",
    1: "Host Unreachable",
    2: "Protocol Unreachable",
    3: "Port Unreachable",
    4: "Fragmentation Needed",
    5: "Source Route Failed"
}


def get_service_name(src_port, dst_port):
    """
    Resolve common service name based on standard port numbers.
    Clearly designated as Common Service Mapping (heuristic based on port).
    """
    if isinstance(dst_port, int) and dst_port in COMMON_SERVICES:
        return COMMON_SERVICES[dst_port]
    if isinstance(src_port, int) and src_port in COMMON_SERVICES:
        return COMMON_SERVICES[src_port]
    return "Other / Dynamic"


def decode_tcp_flags(flags):
    """
    Convert Scapy TCP flags into a human-readable string (e.g. 'SYN, ACK').
    """
    if not flags:
        return "None"
    
    flag_str = str(flags)
    active_flags = [TCP_FLAG_MAP[char] for char in flag_str if char in TCP_FLAG_MAP]
    
    return ", ".join(active_flags) if active_flags else flag_str


def decode_icmp_info(packet):
    """
    Extract ICMP type, code, and human-readable description.
    """
    try:
        icmp_layer = packet[ICMP]
        itype = icmp_layer.type
        icode = icmp_layer.code
        
        type_name = ICMP_TYPE_MAP.get(itype, f"Type {itype}")
        
        if itype == 3 and icode in ICMP_UNREACHABLE_CODES:
            code_desc = ICMP_UNREACHABLE_CODES[icode]
            return f"{type_name} ({code_desc}, Code {icode})"
        
        return f"{type_name} (Code {icode})"
    except Exception:
        return "ICMP Packet"


def analyze_packet(packet):
    """
    Dissects a raw Scapy packet into a structured dictionary.
    Handles IPv4, IPv6, ARP, and non-IP link layer frames safely.
    """
    packet_length = len(packet)
    raw_time = getattr(packet, 'time', None)
    
    if raw_time:
        try:
            pkt_datetime = datetime.fromtimestamp(float(raw_time))
        except Exception:
            pkt_datetime = datetime.now()
    else:
        pkt_datetime = datetime.now()
        
    date_str = pkt_datetime.strftime("%Y-%m-%d")
    time_str = pkt_datetime.strftime("%H:%M:%S")

    # Defaults
    packet_type = "Non-IP"
    source_ip = "N/A"
    destination_ip = "N/A"
    source_port = "-"
    destination_port = "-"
    protocol = "Other"
    tcp_flags = "-"
    icmp_info = "-"
    service = "N/A"

    # 1. Handle IPv4 Packets
    if IP in packet:
        packet_type = "IPv4"
        source_ip = packet[IP].src
        destination_ip = packet[IP].dst
        
        if TCP in packet:
            protocol = "TCP"
            source_port = packet[TCP].sport
            destination_port = packet[TCP].dport
            tcp_flags = decode_tcp_flags(packet[TCP].flags)
            service = get_service_name(source_port, destination_port)
            
        elif UDP in packet:
            protocol = "UDP"
            source_port = packet[UDP].sport
            destination_port = packet[UDP].dport
            service = get_service_name(source_port, destination_port)
            
        elif ICMP in packet:
            protocol = "ICMP"
            icmp_info = decode_icmp_info(packet)
            service = "ICMP"
            
        else:
            protocol = "IPv4-Other"
            service = f"IP Proto {packet[IP].proto}"

    # 2. Handle IPv6 Packets
    elif IPv6 in packet:
        packet_type = "IPv6"
        source_ip = packet[IPv6].src
        destination_ip = packet[IPv6].dst
        
        if TCP in packet:
            protocol = "TCP"
            source_port = packet[TCP].sport
            destination_port = packet[TCP].dport
            tcp_flags = decode_tcp_flags(packet[TCP].flags)
            service = get_service_name(source_port, destination_port)
        elif UDP in packet:
            protocol = "UDP"
            source_port = packet[UDP].sport
            destination_port = packet[UDP].dport
            service = get_service_name(source_port, destination_port)
        else:
            protocol = "IPv6-Other"
            service = "IPv6"

    # 3. Handle ARP Packets
    elif ARP in packet:
        packet_type = "ARP"
        source_ip = packet[ARP].psrc
        destination_ip = packet[ARP].pdst
        protocol = "ARP"
        op_code = packet[ARP].op
        if op_code == 1:
            service = "ARP Request"
            icmp_info = f"Who has {packet[ARP].pdst}? Tell {packet[ARP].psrc}"
        elif op_code == 2:
            service = "ARP Reply"
            icmp_info = f"{packet[ARP].psrc} is at {packet[ARP].hwsrc}"
        else:
            service = f"ARP Op {op_code}"

    # 4. Handle other Layer 2 frames (e.g. raw Ethernet / LLDP / STP)
    elif Ether in packet:
        packet_type = "Non-IP (Ethernet)"
        source_ip = packet[Ether].src
        destination_ip = packet[Ether].dst
        protocol = "Ethernet"
        service = f"Type 0x{packet[Ether].type:04x}"

    return {
        "date": date_str,
        "time": time_str,
        "raw_time": float(raw_time) if raw_time else pkt_datetime.timestamp(),
        "packet_type": packet_type,
        "source_ip": source_ip,
        "destination_ip": destination_ip,
        "source_port": source_port,
        "destination_port": destination_port,
        "protocol": protocol,
        "tcp_flags": tcp_flags,
        "icmp_info": icmp_info,
        "service": service,
        "packet_length": packet_length
    }