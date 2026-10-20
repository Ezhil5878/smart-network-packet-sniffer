"""
main.py - Interactive CLI Controller & Main Application Entry Point
Smart Network Packet Sniffer with Real-Time Traffic Analysis & Protocol Monitoring System
"""

import sys
from datetime import datetime
from packet_capture import get_available_interfaces, start_capture
from analyzer import analyze_packet
from traffic_analyzer import TrafficStats
from logger import SessionLogger
from report import generate_report, get_previous_reports, read_report


def print_banner():
    """Display the main application banner."""
    print("=" * 65)
    print("           SMART NETWORK PACKET SNIFFER v2")
    print("   REAL-TIME TRAFFIC ANALYSIS & PROTOCOL MONITORING SYSTEM")
    print("=" * 65)


def get_validated_choice(prompt_text, min_val, max_val, default_val=None):
    """
    Prompt the user for an integer choice within [min_val, max_val] with input validation.
    """
    while True:
        try:
            raw_input = input(prompt_text).strip()
            if not raw_input and default_val is not None:
                return default_val
            val = int(raw_input)
            if min_val <= val <= max_val:
                return val
            print(f"[!] Invalid selection. Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("[!] Invalid input. Please enter a numeric value.")


def select_network_interface():
    """
    Display available network interfaces and let the user select one.
    """
    print("\n--- Network Interface Selection ---")
    ifaces, rec_idx = get_available_interfaces()

    for item in ifaces:
        idx = item["display_idx"]
        rec_tag = " (Recommended)" if idx == rec_idx else ""
        print(f"  {idx}. {item['name']:<30} [IP: {item['ip']}] {item['description']}{rec_tag}")

    prompt = f"\nSelect Interface [1-{len(ifaces)}] (Default {rec_idx}): "
    choice = get_validated_choice(prompt, 1, len(ifaces), default_val=rec_idx)

    selected = ifaces[choice - 1]
    print(f"[+] Selected Interface: {selected['name']} ({selected['ip']})")
    return selected["scapy_iface"], selected["name"]


def select_capture_configuration():
    """
    Select capture mode (fixed count vs continuous) and packet filter.
    """
    # 1. Capture Mode
    print("\n--- Choose Capture Mode ---")
    print("  1. Fixed Packet Count")
    print("  2. Continuous Capture (Manual Stop with Ctrl+C)")

    mode_choice = get_validated_choice("\nEnter choice [1-2] (Default 1): ", 1, 2, default_val=1)

    if mode_choice == 1:
        while True:
            try:
                count_input = input("Enter number of packets to capture [1-10000] (Default 20): ").strip()
                if not count_input:
                    count = 20
                    break
                count = int(count_input)
                if count > 0:
                    break
                print("[!] Packet count must be greater than zero.")
            except ValueError:
                print("[!] Invalid input. Please enter a positive integer.")
        capture_mode_str = f"Fixed ({count} packets)"
    else:
        count = 0  # 0 indicates continuous capture in Scapy
        capture_mode_str = "Continuous (Stop with Ctrl+C)"

    # 2. Protocol Filter
    print("\n--- Choose Protocol Filter ---")
    print("  1. All Packets (No Filter)")
    print("  2. TCP Packets Only")
    print("  3. UDP Packets Only")
    print("  4. ICMP Packets Only")
    print("  5. ARP Packets Only")
    print("  6. Custom BPF Filter Expression")

    filter_choice = get_validated_choice("\nEnter choice [1-6] (Default 1): ", 1, 6, default_val=1)

    if filter_choice == 1:
        bpf_filter = ""
        filter_name = "All Traffic"
    elif filter_choice == 2:
        bpf_filter = "tcp"
        filter_name = "TCP Only"
    elif filter_choice == 3:
        bpf_filter = "udp"
        filter_name = "UDP Only"
    elif filter_choice == 4:
        bpf_filter = "icmp"
        filter_name = "ICMP Only"
    elif filter_choice == 5:
        bpf_filter = "arp"
        filter_name = "ARP Only"
    else:
        bpf_filter = input("Enter BPF filter string (e.g. 'port 80 or port 443'): ").strip()
        filter_name = f"Custom ({bpf_filter})" if bpf_filter else "All Traffic"

    return count, capture_mode_str, bpf_filter, filter_name


def print_packet_card(packet_no, data):
    """
    Print a neat, readable card for each captured packet in real-time.
    """
    proto = data.get("protocol", "Other")
    src_ip = data.get("source_ip", "-")
    dst_ip = data.get("destination_ip", "-")
    src_port = data.get("source_port", "-")
    dst_port = data.get("destination_port", "-")
    length = data.get("packet_length", 0)
    time_str = data.get("time", "")
    service = data.get("service", "N/A")
    pkt_type = data.get("packet_type", "IP")

    print("-" * 65)
    print(f"PACKET #{packet_no:<5} | Time: {time_str} | Type: {pkt_type}")
    print("-" * 65)
    
    if src_port != "-" and dst_port != "-":
        print(f"Source      : {src_ip:<20} (Port: {src_port})")
        print(f"Destination : {dst_ip:<20} (Port: {dst_port})")
    else:
        print(f"Source      : {src_ip}")
        print(f"Destination : {dst_ip}")

    print(f"Protocol    : {proto}")

    if proto == "TCP":
        print(f"TCP Flags   : {data.get('tcp_flags', 'None')}")
    elif proto == "ICMP":
        print(f"ICMP Info   : {data.get('icmp_info', '-')}")
    elif proto == "ARP":
        print(f"ARP Info    : {data.get('icmp_info', '-')}")

    print(f"Service     : {service} (Common Service Mapping)")
    print(f"Length      : {length} Bytes")
    print("-" * 65)
    print()


def run_packet_sniffer():
    """
    Orchestrates an interactive packet capture session.
    """
    # 1. Interface Selection
    scapy_iface, iface_name = select_network_interface()

    # 2. Configuration Selection
    count, capture_mode_str, bpf_filter, filter_name = select_capture_configuration()

    # 3. Session Initialization
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    stats = TrafficStats(
        session_id=session_id,
        interface_name=iface_name,
        capture_mode=capture_mode_str,
        filter_str=filter_name
    )
    logger = SessionLogger(session_id=session_id)

    print("\n" + "=" * 65)
    print(f"STARTING CAPTURE SESSION : {session_id}")
    print(f"Interface : {iface_name}")
    print(f"Mode      : {capture_mode_str}")
    print(f"Filter    : {filter_name}")
    print("Press Ctrl+C at any time to stop capture gracefully.")
    print("=" * 65 + "\n")

    packet_counter = 0

    def packet_callback(raw_packet):
        nonlocal packet_counter
        try:
            parsed = analyze_packet(raw_packet)
            packet_counter += 1
            parsed["packet_no"] = packet_counter

            # Record in analytics engine
            stats.add_packet(parsed)

            # Record in CSV log
            logger.log_packet(packet_counter, parsed)

            # Live terminal display
            print_packet_card(packet_counter, parsed)

        except Exception as e:
            print(f"[!] Error processing packet: {e}")

    # 4. Start Capture with Graceful Ctrl+C Handling
    try:
        start_capture(
            callback=packet_callback,
            iface=scapy_iface,
            packet_filter=bpf_filter,
            count=count
        )
    except KeyboardInterrupt:
        print("\n\n[!] Capture stopped by user (Ctrl+C).")
    except Exception as e:
        print(f"\n[ERROR] Capture encountered an error: {e}")

    # 5. Finalize Statistics and Generate Report
    stats.finalize()
    summary = stats.get_summary()

    # 6. Display Traffic Summary
    print("\n" + "=" * 65)
    print("                   TRAFFIC SUMMARY & ANALYTICS")
    print("=" * 65)
    print(f"Session ID           : {summary['session_id']}")
    print(f"Capture Duration     : {summary['duration_formatted']}")
    print(f"Total Packets        : {summary['total_packets']}")
    print(f"Total Data           : {summary['total_bytes']:,} Bytes ({summary['total_bytes']/1024:.2f} KB)")
    print(f"Packet Throughput    : {summary['packets_per_second']} pkts/sec")
    print(f"Data Throughput      : {summary['bytes_per_second']} B/s ({summary['kbps']} Kbps)")
    print(f"Average Packet Size  : {summary['avg_packet_size']} Bytes")
    print(f"Min / Max Size       : {summary['min_packet_size']} / {summary['max_packet_size']} Bytes")
    print(f"IP / Non-IP Frames   : {summary['ip_count']} IP / {summary['non_ip_count']} Non-IP")
    print("-" * 65)
    print("PROTOCOL DISTRIBUTION:")
    print(f"  TCP   : {summary['tcp_count']:<6} ({summary['tcp_pct']:>5.1f} %)")
    print(f"  UDP   : {summary['udp_count']:<6} ({summary['udp_pct']:>5.1f} %)")
    print(f"  ICMP  : {summary['icmp_count']:<6} ({summary['icmp_pct']:>5.1f} %)")
    print(f"  ARP   : {summary['arp_count']:<6} ({summary['arp_pct']:>5.1f} %)")
    print(f"  Other : {summary['other_count']:<6} ({summary['other_pct']:>5.1f} %)")
    print("-" * 65)
    print("TOP SOURCE IP ADDRESSES:")
    if summary["top_source_ips"]:
        for ip, cnt, bcnt in summary["top_source_ips"]:
            print(f"  - {ip:<25} : {cnt:>5} pkts ({bcnt:>8,} B)")
    else:
        print("  - None")

    print("-" * 65)
    print("BASIC RULE-BASED TRAFFIC ANOMALY DETECTION:")
    print(f"Anomaly Status : {summary['anomaly_status']}")
    if summary["anomalies"]:
        for item in summary["anomalies"]:
            print(f"  [!] {item}")
    else:
        print("  [+] No rule-based anomalies detected.")

    print("=" * 65)

    # 7. Generate File Outputs
    report_file = generate_report(summary)
    log_file = logger.get_log_filepath()

    print(f"\n[+] Packet log saved to : {log_file}")
    print(f"[+] Traffic report saved to: {report_file}")
    print("=" * 65 + "\n")


def view_previous_reports_menu():
    """
    Display previously generated reports and allow the user to view one.
    """
    reports = get_previous_reports()
    if not reports:
        print("\n[!] No previous reports found in 'reports/' folder.\n")
        return

    print("\n--- Available Traffic Reports ---")
    for i, r_path in enumerate(reports, start=1):
        print(f"  {i}. {r_path}")

    print(f"  {len(reports) + 1}. Back to Main Menu")

    prompt = f"\nSelect report to view [1-{len(reports) + 1}]: "
    choice = get_validated_choice(prompt, 1, len(reports) + 1)

    if choice == len(reports) + 1:
        return

    selected_report = reports[choice - 1]
    content = read_report(selected_report)
    print("\n" + content + "\n")


def main():
    """Main application loop."""
    while True:
        print_banner()
        print("1. Start Packet Capture")
        print("2. View Previous Report")
        print("3. Exit")

        choice = get_validated_choice("\nEnter your choice [1-3]: ", 1, 3)

        if choice == 1:
            run_packet_sniffer()
        elif choice == 2:
            view_previous_reports_menu()
        elif choice == 3:
            print("\nExiting Smart Network Packet Sniffer. Goodbye!\n")
            sys.exit(0)


if __name__ == "__main__":
    main()