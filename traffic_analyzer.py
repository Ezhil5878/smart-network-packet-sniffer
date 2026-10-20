"""
traffic_analyzer.py - Traffic Analytics & Anomaly Detection Module
Smart Network Packet Sniffer v2
"""

from collections import Counter, defaultdict
from datetime import datetime
import time


class TrafficStats:
    """
    Stateful analytics engine that tracks real-time traffic statistics,
    calculates bandwidth and packet throughput, ranks top communicating endpoints,
    and performs basic rule-based anomaly detection.
    """

    def __init__(self, session_id="N/A", interface_name="Default", capture_mode="Fixed", filter_str="None"):
        self.session_id = session_id
        self.interface_name = interface_name
        self.capture_mode = capture_mode
        self.filter_str = filter_str

        self.start_timestamp = time.time()
        self.start_datetime = datetime.now()
        self.end_timestamp = None
        self.end_datetime = None
        self.duration_seconds = 0.0

        # Core packet and byte counters
        self.total_packets = 0
        self.total_bytes = 0
        self.min_packet_size = None
        self.max_packet_size = None

        # Protocol counters
        self.tcp_count = 0
        self.udp_count = 0
        self.icmp_count = 0
        self.arp_count = 0
        self.other_count = 0
        self.ip_count = 0
        self.non_ip_count = 0

        # Endpoint & Talker tracking
        self.src_ip_pkts = Counter()
        self.src_ip_bytes = Counter()
        self.dst_ip_pkts = Counter()
        self.dst_ip_bytes = Counter()
        self.service_counts = Counter()

        # Heuristic Anomaly Detection State
        self.syn_count = 0
        self.syn_by_ip = Counter()
        self.src_to_dst_ports = defaultdict(set)
        self.insecure_traffic_count = 0
        self.insecure_details = []

    def add_packet(self, data):
        """
        Record a dissected packet dictionary into aggregate statistics.
        """
        self.total_packets += 1
        pkt_len = data.get("packet_length", 0)
        self.total_bytes += pkt_len

        # Min / Max packet size
        if self.min_packet_size is None or pkt_len < self.min_packet_size:
            self.min_packet_size = pkt_len
        if self.max_packet_size is None or pkt_len > self.max_packet_size:
            self.max_packet_size = pkt_len

        # Layer 3 / Protocol classification
        pkt_type = data.get("packet_type", "")
        proto = data.get("protocol", "Other")

        if "IP" in pkt_type and "Non-IP" not in pkt_type:
            self.ip_count += 1
        else:
            self.non_ip_count += 1

        if proto == "TCP":
            self.tcp_count += 1
        elif proto == "UDP":
            self.udp_count += 1
        elif proto == "ICMP":
            self.icmp_count += 1
        elif proto == "ARP":
            self.arp_count += 1
        else:
            self.other_count += 1

        # Endpoint tracking
        src_ip = data.get("source_ip", "N/A")
        dst_ip = data.get("destination_ip", "N/A")
        if src_ip and src_ip != "N/A":
            self.src_ip_pkts[src_ip] += 1
            self.src_ip_bytes[src_ip] += pkt_len
        if dst_ip and dst_ip != "N/A":
            self.dst_ip_pkts[dst_ip] += 1
            self.dst_ip_bytes[dst_ip] += pkt_len

        # Service / Port tracking
        service = data.get("service", "N/A")
        if service and service != "N/A" and service != "Other / Dynamic":
            self.service_counts[service] += 1

        # Anomaly Detection Tracking
        tcp_flags = data.get("tcp_flags", "")
        dst_port = data.get("destination_port", "-")

        # Track SYN flags
        if "SYN" in tcp_flags and "ACK" not in tcp_flags:
            self.syn_count += 1
            if src_ip != "N/A":
                self.syn_by_ip[src_ip] += 1

        # Track Port Probing / Scanning
        if src_ip != "N/A" and isinstance(dst_port, int):
            self.src_to_dst_ports[src_ip].add(dst_port)

        # Track Insecure/Cleartext Protocols
        if service in ["Telnet (Insecure)", "HTTP (Cleartext)", "FTP-Control"]:
            self.insecure_traffic_count += 1
            entry = f"{src_ip} -> {dst_ip} ({service})"
            if entry not in self.insecure_details:
                self.insecure_details.append(entry)

    def finalize(self):
        """
        Finalizes capture timing and prepares consolidated summary metrics.
        """
        self.end_timestamp = time.time()
        self.end_datetime = datetime.now()
        self.duration_seconds = max(self.end_timestamp - self.start_timestamp, 0.001)

    def get_summary(self):
        """
        Compute and return comprehensive dictionary of metrics.
        """
        if not self.end_timestamp:
            self.finalize()

        # Rates
        pps = round(self.total_packets / self.duration_seconds, 2)
        bps = round(self.total_bytes / self.duration_seconds, 2)
        kbps = round((self.total_bytes * 8) / (self.duration_seconds * 1000), 2)
        avg_size = round(self.total_bytes / self.total_packets, 2) if self.total_packets > 0 else 0.0

        # Percentages
        def pct(count):
            return round((count / self.total_packets) * 100, 1) if self.total_packets > 0 else 0.0

        # Top Talkers
        top_src = self.src_ip_pkts.most_common(5)
        top_dst = self.dst_ip_pkts.most_common(5)
        top_services = self.service_counts.most_common(5)

        # Anomaly Analysis (Basic Rule-Based)
        anomalies = []
        
        # Rule 1: High SYN Activity
        if self.syn_count >= 15 and (self.tcp_count > 0 and (self.syn_count / self.tcp_count) > 0.4):
            anomalies.append(f"High SYN activity detected ({self.syn_count} SYN packets, {pct(self.syn_count)}% of TCP traffic). Potential SYN flood probe.")
        for ip, syns in self.syn_by_ip.items():
            if syns >= 10:
                anomalies.append(f"High SYN burst ({syns} SYN packets) originating from host {ip}.")

        # Rule 2: Multiple Destination Ports Contacted (Port Scan Heuristic)
        for ip, ports in self.src_to_dst_ports.items():
            if len(ports) >= 8:
                anomalies.append(f"Potential port scan/sweep: Host {ip} probed {len(ports)} distinct destination ports.")

        # Rule 3: Insecure Cleartext Protocol Alert
        if self.insecure_traffic_count > 0:
            sample_insecure = ", ".join(self.insecure_details[:3])
            anomalies.append(f"Cleartext/Insecure protocol usage observed ({self.insecure_traffic_count} packets): {sample_insecure}")

        anomaly_status = "WARNING" if anomalies else "NORMAL"

        return {
            "session_id": self.session_id,
            "interface": self.interface_name,
            "capture_mode": self.capture_mode,
            "filter": self.filter_str,
            "start_time": self.start_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": self.end_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "duration_formatted": f"{self.duration_seconds:.2f} seconds",
            "duration_seconds": self.duration_seconds,
            "total_packets": self.total_packets,
            "total_bytes": self.total_bytes,
            "avg_packet_size": avg_size,
            "min_packet_size": self.min_packet_size if self.min_packet_size is not None else 0,
            "max_packet_size": self.max_packet_size if self.max_packet_size is not None else 0,
            "packets_per_second": pps,
            "bytes_per_second": bps,
            "kbps": kbps,
            "tcp_count": self.tcp_count,
            "tcp_pct": pct(self.tcp_count),
            "udp_count": self.udp_count,
            "udp_pct": pct(self.udp_count),
            "icmp_count": self.icmp_count,
            "icmp_pct": pct(self.icmp_count),
            "arp_count": self.arp_count,
            "arp_pct": pct(self.arp_count),
            "other_count": self.other_count,
            "other_pct": pct(self.other_count),
            "ip_count": self.ip_count,
            "non_ip_count": self.non_ip_count,
            "top_source_ips": [(ip, count, self.src_ip_bytes[ip]) for ip, count in top_src],
            "top_dest_ips": [(ip, count, self.dst_ip_bytes[ip]) for ip, count in top_dst],
            "top_services": top_services,
            "anomaly_status": anomaly_status,
            "anomalies": anomalies
        }

