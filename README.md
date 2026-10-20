# Smart Network Packet Sniffer

**Real-Time Traffic Analysis and Protocol Monitoring System**

A Python-based command-line project that uses Scapy to capture and inspect network packets, display packet details, summarize observed traffic, and save session output for later review.

## Project Objectives

- Capture packets from a selected network interface.
- Display packet information such as protocol, source/destination addresses, ports when available, and packet length.
- Summarize observed traffic and protocol distribution.
- Save packet/session information to CSV logs and text reports.
- Demonstrate basic rule-based traffic indicators where supported by the implementation.

## Technologies

- Python 3.12
- Scapy
- Npcap on Windows (may be required for packet capture)

## Project Files

- `main.py` — command-line entry point
- `packet_capture.py` — packet capture and interface selection
- `analyzer.py` — packet field analysis
- `traffic_analyzer.py` — traffic statistics and rule-based indicators
- `logger.py` — CSV logging
- `report.py` — text report generation and report browsing
- `generate_pdf_report.py` and `generate_perfect_pdf.py` — report-generation scripts, if used in the current workflow
- `Smart_Packet_Sniffer_Project_Report.pdf` — project report
- `screenshots/` — add screenshots of the running application here

## Requirements

- Windows
- Python 3.12 or a compatible Python 3 version
- Scapy
- Npcap installed and configured if required by your Windows capture setup

## Installation

1. Install Python from [python.org](https://www.python.org/).
2. Install Npcap from [npcap.com](https://npcap.com/) if needed for packet capture.
3. Open Command Prompt in the project directory.
4. Install Python dependencies:

   ```bash
   py -m pip install -r requirements.txt
   ```

## Run the Application

Open Command Prompt in the project folder and run:

```bash
py main.py
```

Follow the on-screen menu to select a network interface, capture mode, and supported protocol filter. The application may require running Command Prompt with suitable permissions.

## Output

Depending on the options and features available in the version you run, the application can save session CSV logs in `logs/` and text reports in `reports/`. Check the paths printed by the application.

## Screenshots

Add screenshots of the application's menu, packet output, and traffic summary to the `screenshots/` folder. If using GitHub's web interface, you can upload the images into this folder.

## Important Usage Note

Only capture traffic on networks and devices you own or are explicitly authorized to monitor. Packet captures and logs can contain sensitive information; review and sanitize them before sharing.

## Limitations

- The tool can only observe traffic available to the selected network interface.
- Port-to-service labels are indicative and do not guarantee the actual application protocol.
- Rule-based warnings are heuristic indicators and are not proof of malicious activity.

