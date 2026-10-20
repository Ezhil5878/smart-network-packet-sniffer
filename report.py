"""
report.py - Automated Session Report Generator Module
Smart Network Packet Sniffer v2
"""

import os
from datetime import datetime


def generate_report(summary, reports_dir="reports"):
    """
    Generates a structured, comprehensive plaintext network traffic report
    from the TrafficStats summary dictionary.
    """
    os.makedirs(reports_dir, exist_ok=True)
    session_id = summary.get("session_id", datetime.now().strftime("%Y%m%d_%H%M%S"))
    report_filename = os.path.join(reports_dir, f"report_{session_id}.txt")

    lines = []
    lines.append("=" * 65)
    lines.append("           SMART NETWORK PACKET SNIFFER v2")
    lines.append("     REAL-TIME TRAFFIC ANALYSIS & PROTOCOL REPORT")
    lines.append("=" * 65)
    lines.append("")
    lines.append(f"Session ID       : {session_id}")
    lines.append(f"Start Time       : {summary.get('start_time', 'N/A')}")
    lines.append(f"End Time         : {summary.get('end_time', 'N/A')}")
    lines.append(f"Capture Duration : {summary.get('duration_formatted', 'N/A')}")
    lines.append(f"Network Interface: {summary.get('interface', 'Default')}")
    lines.append(f"Capture Mode     : {summary.get('capture_mode', 'Fixed')}")
    lines.append(f"Protocol Filter  : {summary.get('filter', 'None')}")
    lines.append("")

    lines.append("-" * 65)
    lines.append("1. TRAFFIC SUMMARY")
    lines.append("-" * 65)
    lines.append(f"Total Packets Captured : {summary.get('total_packets', 0):,}")
    lines.append(f"Total Data Transferred : {summary.get('total_bytes', 0):,} Bytes ({summary.get('total_bytes', 0)/1024:.2f} KB)")
    lines.append(f"Packet Throughput Rate : {summary.get('packets_per_second', 0.0):.2f} packets/sec")
    lines.append(f"Data Transfer Rate     : {summary.get('bytes_per_second', 0.0):.2f} Bytes/sec ({summary.get('kbps', 0.0):.2f} Kbps)")
    lines.append(f"Average Packet Length  : {summary.get('avg_packet_size', 0.0):.2f} Bytes")
    lines.append(f"Min / Max Packet Size  : {summary.get('min_packet_size', 0)} / {summary.get('max_packet_size', 0)} Bytes")
    lines.append(f"IP vs Non-IP Frames    : {summary.get('ip_count', 0)} IP / {summary.get('non_ip_count', 0)} Non-IP")
    lines.append("")

    lines.append("-" * 65)
    lines.append("2. PROTOCOL DISTRIBUTION")
    lines.append("-" * 65)
    total = summary.get('total_packets', 0)
    lines.append(f"  * TCP Packets        : {summary.get('tcp_count', 0):<6} ({summary.get('tcp_pct', 0.0):>5.1f} %)")
    lines.append(f"  * UDP Packets        : {summary.get('udp_count', 0):<6} ({summary.get('udp_pct', 0.0):>5.1f} %)")
    lines.append(f"  * ICMP Packets       : {summary.get('icmp_count', 0):<6} ({summary.get('icmp_pct', 0.0):>5.1f} %)")
    lines.append(f"  * ARP Packets        : {summary.get('arp_count', 0):<6} ({summary.get('arp_pct', 0.0):>5.1f} %)")
    lines.append(f"  * Other Packets      : {summary.get('other_count', 0):<6} ({summary.get('other_pct', 0.0):>5.1f} %)")
    lines.append("")

    lines.append("-" * 65)
    lines.append("3. TOP COMMUNICATING ENDPOINTS (TOP TALKERS)")
    lines.append("-" * 65)
    
    top_src = summary.get("top_source_ips", [])
    lines.append("Top Source IP Addresses:")
    if top_src:
        for ip, count, bcount in top_src:
            lines.append(f"  - {ip:<25} : {count:>5} packets ({bcount:>8,} Bytes)")
    else:
        lines.append("  - None recorded")
    lines.append("")

    top_dst = summary.get("top_dest_ips", [])
    lines.append("Top Destination IP Addresses:")
    if top_dst:
        for ip, count, bcount in top_dst:
            lines.append(f"  - {ip:<25} : {count:>5} packets ({bcount:>8,} Bytes)")
    else:
        lines.append("  - None recorded")
    lines.append("")

    top_srv = summary.get("top_services", [])
    lines.append("Top Identified Services (Common Service Mapping):")
    if top_srv:
        for srv, count in top_srv:
            lines.append(f"  - {srv:<25} : {count:>5} packets")
    else:
        lines.append("  - None identified")
    lines.append("")

    lines.append("-" * 65)
    lines.append("4. BASIC RULE-BASED TRAFFIC ANOMALY DETECTION")
    lines.append("-" * 65)
    anomaly_status = summary.get("anomaly_status", "NORMAL")
    lines.append(f"Anomaly Status : {anomaly_status}")
    lines.append("")
    
    anomalies = summary.get("anomalies", [])
    if anomalies:
        lines.append("Detected Issues / Alerts:")
        for issue in anomalies:
            lines.append(f"  [!] {issue}")
    else:
        lines.append("No rule-based anomalies detected during this capture session.")
        lines.append("Traffic pattern appears consistent with normal network operations.")
    lines.append("")

    lines.append("=" * 65)
    lines.append("                       END OF REPORT")
    lines.append("=" * 65)

    content = "\n".join(lines)

    try:
        with open(report_filename, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        print(f"[ERROR] Failed to write report file '{report_filename}': {e}")

    return report_filename


def get_previous_reports(reports_dir="reports"):
    """
    Returns a sorted list of previously generated report filenames (newest first).
    """
    if not os.path.exists(reports_dir):
        return []
    
    files = [
        f for f in os.listdir(reports_dir)
        if f.startswith("report_") and f.endswith(".txt")
    ]
    files.sort(reverse=True)
    return [os.path.join(reports_dir, f) for f in files]


def read_report(filepath):
    """
    Safely reads and returns the plaintext contents of a report file.
    """
    if not os.path.exists(filepath):
        return f"File '{filepath}' not found."
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading report '{filepath}': {e}"