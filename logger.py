"""
logger.py - Session-Based CSV Logging Module
Smart Network Packet Sniffer v2
"""

import csv
import os
from datetime import datetime


CSV_HEADERS = [
    "Packet No",
    "Date",
    "Time",
    "Packet Type",
    "Source IP",
    "Source Port",
    "Destination IP",
    "Destination Port",
    "Protocol",
    "TCP Flags",
    "ICMP Info",
    "Common Service Mapping",
    "Packet Length (Bytes)"
]


class SessionLogger:
    """
    Manages session-based CSV logging with automatic file-lock detection
    and graceful fallback path redirection.
    """

    def __init__(self, session_id=None, logs_dir="logs"):
        self.logs_dir = logs_dir
        os.makedirs(self.logs_dir, exist_ok=True)

        if not session_id:
            session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_id = session_id

        self.filename = os.path.join(self.logs_dir, f"session_{self.session_id}.csv")
        self.fallback_active = False
        self.lock_warning_displayed = False
        self.initialize_file()

    def initialize_file(self):
        """
        Create the CSV file with headers. Handles file permission / lock errors.
        """
        target_file = self.filename
        try:
            with open(target_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(CSV_HEADERS)
        except PermissionError:
            self.fallback_active = True
            self.filename = os.path.join(self.logs_dir, f"session_{self.session_id}_alt.csv")
            print(f"\n[WARNING] Primary log file '{target_file}' is locked (e.g. open in Excel).")
            print(f"[!] Falling back to safe log file: '{self.filename}'\n")
            with open(self.filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(CSV_HEADERS)

    def log_packet(self, packet_no, data):
        """
        Appends a single packet record to the session CSV file.
        Resilient against file locking during active capture.
        """
        row = [
            packet_no,
            data.get("date", ""),
            data.get("time", ""),
            data.get("packet_type", "Unknown"),
            data.get("source_ip", "-"),
            data.get("source_port", "-"),
            data.get("destination_ip", "-"),
            data.get("destination_port", "-"),
            data.get("protocol", "Other"),
            data.get("tcp_flags", "-"),
            data.get("icmp_info", "-"),
            data.get("service", "N/A"),
            data.get("packet_length", 0)
        ]

        try:
            with open(self.filename, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(row)
        except PermissionError:
            if not self.lock_warning_displayed:
                alt_name = os.path.join(self.logs_dir, f"session_{self.session_id}_alt_{datetime.now().strftime('%H%M%S')}.csv")
                print(f"\n[WARNING] CSV log file '{self.filename}' is locked by another program (e.g. Excel).")
                print(f"[!] Redirecting active capture log to: '{alt_name}'\n")
                self.filename = alt_name
                self.lock_warning_displayed = True
                try:
                    with open(self.filename, "w", newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow(CSV_HEADERS)
                        writer.writerow(row)
                except Exception as e:
                    print(f"[ERROR] Failed to write fallback log: {e}")
            else:
                try:
                    with open(self.filename, "a", newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow(row)
                except Exception:
                    pass
        except Exception as e:
            print(f"[ERROR] Logging error: {e}")

    def get_log_filepath(self):
        return self.filename