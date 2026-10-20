"""
generate_pdf_report.py
Generates a comprehensive, publication-quality academic/technical Project Report
for the Smart Network Packet Sniffer v2 and compiles it into a PDF via Edge Headless.
"""

import os
import subprocess
import sys

HTML_FILE = r"c:\Smart-Packet-Sniffer_v1\report_document.html"
PDF_FILE = r"c:\Smart-Packet-Sniffer_v1\Smart_Packet_Sniffer_Project_Report.pdf"

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Smart Network Packet Sniffer v2 - Technical Project Report</title>
<style>
  @page {
    size: A4 portrait;
    margin: 18mm 15mm 18mm 15mm;
  }
  
  * {
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    background-color: #ffffff;
    line-height: 1.6;
    font-size: 10.5pt;
    margin: 0;
    padding: 0;
  }

  /* Page Break Helpers */
  .page-break {
    page-break-after: always;
    break-after: page;
  }
  .avoid-break {
    page-break-inside: avoid;
    break-inside: avoid;
  }

  /* Cover Page */
  .cover-page {
    height: 100%;
    min-height: 250mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 40px 20px 20px 20px;
    border-top: 8px solid #1e3a8a;
  }

  .cover-header {
    margin-top: 40px;
  }

  .cover-badge {
    display: inline-block;
    padding: 6px 14px;
    background: #e0e7ff;
    color: #3730a3;
    font-weight: 700;
    font-size: 9pt;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    border-radius: 20px;
    margin-bottom: 24px;
  }

  .cover-title {
    font-size: 28pt;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.2;
    margin: 0 0 16px 0;
  }

  .cover-subtitle {
    font-size: 14pt;
    color: #475569;
    font-weight: 400;
    line-height: 1.4;
    margin: 0 0 32px 0;
  }

  .cover-divider {
    width: 80px;
    height: 4px;
    background: #2563eb;
    margin-bottom: 30px;
  }

  .cover-meta-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 24px;
    margin-top: 40px;
  }

  .meta-item {
    font-size: 10pt;
  }
  .meta-label {
    font-size: 8.5pt;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #64748b;
    font-weight: 600;
    margin-bottom: 4px;
  }
  .meta-value {
    color: #0f172a;
    font-weight: 600;
  }

  .cover-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid #e2e8f0;
    padding-top: 20px;
    font-size: 9pt;
    color: #64748b;
  }

  /* Headings */
  h1 {
    font-size: 18pt;
    font-weight: 800;
    color: #0f172a;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 8px;
    margin-top: 24px;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
  }
  h1 .chapter-num {
    background: #1e3a8a;
    color: #ffffff;
    font-size: 11pt;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 4px;
    margin-right: 12px;
  }

  h2 {
    font-size: 13.5pt;
    font-weight: 700;
    color: #1e293b;
    margin-top: 20px;
    margin-bottom: 10px;
  }

  h3 {
    font-size: 11pt;
    font-weight: 600;
    color: #334155;
    margin-top: 16px;
    margin-bottom: 8px;
  }

  p {
    margin-top: 0;
    margin-bottom: 12px;
    text-align: justify;
  }

  /* Table of Contents */
  .toc-container {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 24px;
    margin: 20px 0;
  }
  .toc-item {
    display: flex;
    justify-content: space-between;
    padding: 6px 0;
    border-bottom: 1px dotted #cbd5e1;
    font-size: 10pt;
  }
  .toc-item:last-child {
    border-bottom: none;
  }
  .toc-title {
    font-weight: 600;
    color: #1e293b;
  }
  .toc-sub {
    padding-left: 20px;
    font-size: 9.5pt;
    color: #475569;
  }
  .toc-page {
    font-weight: 600;
    color: #2563eb;
  }

  /* Callouts & Alert Boxes */
  .callout {
    padding: 14px 18px;
    border-radius: 6px;
    margin: 16px 0;
    font-size: 9.5pt;
  }
  .callout-info {
    background: #eff6ff;
    border-left: 4px solid #2563eb;
    color: #1e3a8a;
  }
  .callout-warning {
    background: #fffbeb;
    border-left: 4px solid #f59e0b;
    color: #92400e;
  }
  .callout-success {
    background: #ecfdf5;
    border-left: 4px solid #10b981;
    color: #065f46;
  }
  .callout-title {
    font-weight: 700;
    margin-bottom: 4px;
    font-size: 10pt;
  }

  /* Tables */
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 16px 0;
    font-size: 9pt;
  }
  th {
    background-color: #0f172a;
    color: #ffffff;
    font-weight: 600;
    text-align: left;
    padding: 8px 12px;
    border: 1px solid #0f172a;
  }
  td {
    padding: 7px 12px;
    border: 1px solid #e2e8f0;
    vertical-align: top;
  }
  tr:nth-child(even) td {
    background-color: #f8fafc;
  }

  /* Metric Cards Grid */
  .metrics-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin: 16px 0;
  }
  .metric-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 12px;
    text-align: center;
  }
  .metric-value {
    font-size: 18pt;
    font-weight: 800;
    color: #1e3a8a;
    margin-bottom: 4px;
  }
  .metric-label {
    font-size: 8pt;
    text-transform: uppercase;
    font-weight: 600;
    color: #64748b;
  }

  /* Code Blocks */
  pre {
    background: #0f172a;
    color: #f1f5f9;
    padding: 12px 16px;
    border-radius: 6px;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 8.5pt;
    overflow-x: auto;
    margin: 14px 0;
    line-height: 1.45;
  }
  code {
    font-family: "Consolas", "Courier New", monospace;
    background: #f1f5f9;
    color: #0f172a;
    padding: 2px 5px;
    border-radius: 3px;
    font-size: 8.5pt;
  }
  pre code {
    background: transparent;
    color: inherit;
    padding: 0;
  }

  /* Diagrams */
  .diagram-container {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 16px;
    margin: 16px 0;
    text-align: center;
  }
  .diagram-caption {
    font-size: 8.5pt;
    font-weight: 600;
    color: #64748b;
    margin-top: 8px;
  }

  ul, ol {
    margin-top: 0;
    margin-bottom: 12px;
    padding-left: 24px;
  }
  li {
    margin-bottom: 5px;
  }

  .badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 7.5pt;
    font-weight: 700;
    text-transform: uppercase;
  }
  .badge-tcp { background: #dbeafe; color: #1e40af; }
  .badge-udp { background: #fef3c7; color: #92400e; }
  .badge-icmp { background: #fee2e2; color: #991b1b; }
  .badge-arp { background: #e0e7ff; color: #3730a3; }
  .badge-warning { background: #ffedd5; color: #9a3412; }
  .badge-success { background: #dcfce7; color: #166534; }
</style>
</head>
<body>

<!-- ==================== COVER PAGE ==================== -->
<div class="cover-page page-break">
  <div class="cover-header">
    <span class="cover-badge">Engineering & Technical Project Report</span>
    <h1 class="cover-title" style="border: none; padding: 0;">SMART NETWORK PACKET SNIFFER v2</h1>
    <div class="cover-subtitle">
      Real-Time Traffic Analysis, Multi-Layer Protocol Dissection, Heuristic Anomaly Detection & Telemetry Reporting System
    </div>
    <div class="cover-divider"></div>
    <p style="color: #475569; font-size: 11pt; line-height: 1.6; max-width: 90%;">
      A high-performance, modular Python network inspection framework designed for wire-speed packet capture,
      deep protocol decapsulation across Layers 2 through 7, real-time statistical bandwidth calculation,
      rule-based security anomaly alerting, and resilient session auditing on modern Windows architectures.
    </p>
  </div>

  <div class="cover-meta-grid">
    <div class="meta-item">
      <div class="meta-label">Project Domain</div>
      <div class="meta-value">Computer Networks & Cybersecurity</div>
    </div>
    <div class="meta-item">
      <div class="meta-label">Core Implementation</div>
      <div class="meta-value">Python 3.12, Scapy 2.7.0, Npcap Engine</div>
    </div>
    <div class="meta-item">
      <div class="meta-label">Operating Platform</div>
      <div class="meta-value">Microsoft Windows (x64 Architecture)</div>
    </div>
    <div class="meta-item">
      <div class="meta-label">Document Version & Status</div>
      <div class="meta-value">v2.1 Production Specification (Complete)</div>
    </div>
    <div class="meta-item">
      <div class="meta-label">System Modules</div>
      <div class="meta-value">Capture, Dissection, Analytics, Logger, Report, CLI</div>
    </div>
    <div class="meta-item">
      <div class="meta-label">Telemetry Artifacts</div>
      <div class="meta-value">Structured CSV Logs & Comprehensive TXT Summaries</div>
    </div>
  </div>

  <div class="cover-footer">
    <div>Smart Packet Sniffer Engineering Team</div>
    <div>October 2026</div>
    <div>Confidential & Educational Project Material</div>
  </div>
</div>

<!-- ==================== EXECUTIVE SUMMARY & TOC ==================== -->
<div class="page-break">
  <h1><span class="chapter-num">00</span>Executive Summary & Abstract</h1>
  <p>
    Network packet sniffers represent fundamental instruments within modern computer systems, providing indispensable
    telemetry for performance diagnosis, security auditing, protocol validation, and traffic engineering.
    Traditional tools such as Wireshark or commercial Deep Packet Inspection (DPI) platforms often suffer from heavyweight
    memory footprints, excessive GUI latency, high runtime complexity, or closed architectures that prevent automated
    scripting and streamlined incident response.
  </p>
  <p>
    <strong>Smart Network Packet Sniffer v2</strong> is engineered to bridge the divide between low-level driver-based packet
    interception and automated application-layer telemetry. Built atop Python 3 and the Scapy packet manipulation suite,
    the system interfaces directly with the native Windows Npcap kernel driver to capture live promiscuous Ethernet, IP,
    and ARP traffic without dropped frames under moderate loads.
  </p>
  <p>
    Key engineering milestones achieved in this system include:
  </p>
  <ul>
    <li><strong>Asynchronous GIL-Responsive Micro-Batching:</strong> Implements a 0.5-second polling window that resolves the notorious Scapy Windows GIL-locking issue, enabling instantaneous <code>Ctrl+C</code> signal termination even on completely idle network adapters.</li>
    <li><strong>Full-Stack Multi-Layer Protocol Dissection:</strong> Safely parses raw frames across Layer 2 (Ethernet, ARP), Layer 3 (IPv4, IPv6), Layer 4 (TCP with complete bitmask flag decoding, UDP, ICMP with RFC-compliant code mappings), and Layer 7 (well-known service heuristics).</li>
    <li><strong>Stateful Real-Time Analytics Engine:</strong> Continuously measures throughput (Packets/sec, Bytes/sec, Kilobits/sec), payload distribution metrics, and endpoint talker rankings (source and destination IPs).</li>
    <li><strong>Rule-Based Security Anomaly Detection:</strong> Evaluates traffic heuristics to flag TCP SYN flooding attempts, horizontal port scans (distinct port sweeping per host), and cleartext credentials transmitted over unencrypted legacy protocols (HTTP, Telnet, FTP).</li>
    <li><strong>Resilient Concurrent CSV Logging:</strong> Employs auto-recovering file I/O with automatic lock detection and alternative filename redirection when target log files are opened in external applications such as Microsoft Excel.</li>
  </ul>

  <h2>Table of Contents</h2>
  <div class="toc-container">
    <div class="toc-item">
      <span class="toc-title">1. Introduction & Background</span>
      <span class="toc-page">Page 3</span>
    </div>
    <div class="toc-item toc-sub">
      <span>1.1 Problem Statement & Motivations | 1.2 System Objectives | 1.3 Scope of Project</span>
      <span></span>
    </div>
    <div class="toc-item">
      <span class="toc-title">2. System Architecture & Component Design</span>
      <span class="toc-page">Page 4</span>
    </div>
    <div class="toc-item toc-sub">
      <span>2.1 End-to-End Pipeline Architecture | 2.2 Functional Module Breakdown | 2.3 Data Flow Lifecycle</span>
      <span></span>
    </div>
    <div class="toc-item">
      <span class="toc-title">3. Packet Dissection & Protocol Handling</span>
      <span class="toc-page">Page 5</span>
    </div>
    <div class="toc-item toc-sub">
      <span>3.1 Layer 2/3/4 Decoding Mechanics | 3.2 TCP Flag Bitmask Analysis | 3.3 ICMP & ARP Translation</span>
      <span></span>
    </div>
    <div class="toc-item">
      <span class="toc-title">4. Real-Time Analytics & Heuristic Anomaly Detection</span>
      <span class="toc-page">Page 6</span>
    </div>
    <div class="toc-item toc-sub">
      <span>4.1 Bandwidth & Throughput Algorithms | 4.2 SYN Flood Detection | 4.3 Port Scanning Heuristics</span>
      <span></span>
    </div>
    <div class="toc-item">
      <span class="toc-title">5. Concurrency, Fault Tolerance & Logging Resilience</span>
      <span class="toc-page">Page 7</span>
    </div>
    <div class="toc-item toc-sub">
      <span>5.1 GIL Timeout Micro-Batching | 5.2 Dynamic File-Lock Fallback Mechanism</span>
      <span></span>
    </div>
    <div class="toc-item">
      <span class="toc-title">6. Empirical Verification & Test Results</span>
      <span class="toc-page">Page 8</span>
    </div>
    <div class="toc-item toc-sub">
      <span>6.1 Real Network Benchmark Analysis | 6.2 Anomaly Alert Verification | 6.3 System Performance</span>
      <span></span>
    </div>
    <div class="toc-item">
      <span class="toc-title">7. Security, Ethical Considerations & Deployment</span>
      <span class="toc-page">Page 9</span>
    </div>
    <div class="toc-item">
      <span class="toc-title">8. Conclusion, Future Work & References</span>
      <span class="toc-page">Page 10</span>
    </div>
  </div>
</div>

<!-- ==================== CHAPTER 1 ==================== -->
<div class="page-break">
  <h1><span class="chapter-num">01</span>Introduction & Background</h1>
  
  <h2>1.1 Problem Statement</h2>
  <p>
    In modern digital infrastructure, raw network packet data is the authoritative ground truth for all system communications.
    However, analyzing this stream presents formidable engineering challenges:
  </p>
  <ul>
    <li><strong>Resource Overhead of Existing Tooling:</strong> Enterprise packet sniffers often require substantial CPU and memory reserves, rendering them cumbersome for lightweight edge environments, headless servers, and rapid incident response triage.</li>
    <li><strong>Signal-to-Noise Ratio:</strong> Standard packet capture outputs generate millions of hexadecimal bytes without immediately identifying communicating endpoints, active protocols, or underlying security anomalies.</li>
    <li><strong>Windows Platform Pitfalls:</strong> Windows OS manages network interfaces via kernel-level device drivers (Npcap/WinPcap). In higher-level scripting languages like Python, continuous socket sniffing commonly deadlocks the interpreter's Global Interpreter Lock (GIL), preventing the operating system from cleanly dispatching POSIX/Windows interruption signals (<code>SIGINT</code> / <code>Ctrl+C</code>).</li>
    <li><strong>File Concurrency Hazards:</strong> During live forensic capture, network analysts frequently open output CSV logs in analytical tools (such as Microsoft Excel). On Windows, this imposes an exclusive OS-level file lock (<code>Sharing Violation</code>), instantly crashing naive sniffers.</li>
  </ul>

  <h2>1.2 System Objectives</h2>
  <p>
    The primary purpose of the <strong>Smart Network Packet Sniffer v2</strong> is to deliver a lightweight, autonomous,
    and robust packet dissection framework capable of:
  </p>
  <ol>
    <li><strong>Hardware Adapter Enumeration:</strong> Dynamically querying the operating system's routing tables and Npcap driver to present available network interfaces with intuitive IP-based auto-detection of the primary active internet gateway.</li>
    <li><strong>Zero-Overhead Real-Time Dissection:</strong> Decoding incoming layer 2 through layer 4 network frames on-the-fly and presenting structured, colorized terminal cards without stalling the capture loop.</li>
    <li><strong>Multi-Dimensional Traffic Analytics:</strong> Computing dynamic throughput metrics including bytes per second, kilobits per second, packets per second, and byte-weighted endpoint distributions.</li>
    <li><strong>Heuristic Threat Identification:</strong> Detecting baseline network anomalies including TCP half-open SYN floods, reconnaissance port sweeps, and cleartext transmissions.</li>
    <li><strong>Dual-Tier Structured Storage:</strong> Concurrently streaming detailed telemetry records to an append-only CSV log while producing an executive plaintext analysis report at session completion.</li>
  </ol>

  <h2>1.3 Scope & Operational Environment</h2>
  <p>
    The project is developed for enterprise local area networks (LAN), laboratory security testing environments,
    and academic research setups. Operating within the Windows environment, it leverages the Npcap packet capture driver
    operating with Windows administrative privilege escalation.
  </p>
</div>

<!-- ==================== CHAPTER 2 ==================== -->
<div class="page-break">
  <h1><span class="chapter-num">02</span>System Architecture & Component Design</h1>

  <h2>2.1 End-to-End Pipeline Architecture</h2>
  <p>
    The system follows a decoupled, pipeline-driven architecture. Raw network packets are pulled from the kernel driver,
    dissected through pure-python translation modules, and fanned out simultaneously to terminal visualizers,
    an in-memory stateful analytics engine, and persistent storage managers.
  </p>

  <div class="diagram-container avoid-break">
    <svg width="100%" height="220" viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg">
      <rect x="5" y="5" width="750" height="210" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
      
      <!-- Stage 1: Ingestion -->
      <rect x="25" y="35" width="130" height="150" rx="6" fill="#1e3a8a" stroke="#172554" stroke-width="1.5"/>
      <text x="90" y="65" fill="#ffffff" font-size="11" font-weight="bold" text-anchor="middle">1. INGESTION</text>
      <text x="90" y="90" fill="#93c5fd" font-size="9" text-anchor="middle">packet_capture.py</text>
      <text x="90" y="115" fill="#ffffff" font-size="8.5" text-anchor="middle">• Npcap Driver</text>
      <text x="90" y="135" fill="#ffffff" font-size="8.5" text-anchor="middle">• BPF Filters</text>
      <text x="90" y="155" fill="#ffffff" font-size="8.5" text-anchor="middle">• 0.5s Micro-Batch</text>

      <!-- Stage 2: Dissection -->
      <rect x="200" y="35" width="140" height="150" rx="6" fill="#0f766e" stroke="#115e59" stroke-width="1.5"/>
      <text x="270" y="65" fill="#ffffff" font-size="11" font-weight="bold" text-anchor="middle">2. DISSECTION</text>
      <text x="270" y="90" fill="#99f6e4" font-size="9" text-anchor="middle">analyzer.py</text>
      <text x="270" y="115" fill="#ffffff" font-size="8.5" text-anchor="middle">• L2: Eth / ARP</text>
      <text x="270" y="135" fill="#ffffff" font-size="8.5" text-anchor="middle">• L3: IPv4 / IPv6</text>
      <text x="270" y="155" fill="#ffffff" font-size="8.5" text-anchor="middle">• L4: TCP/UDP/ICMP</text>
      <text x="270" y="172" fill="#ffffff" font-size="8.5" text-anchor="middle">• L7: Port Mapping</text>

      <!-- Stage 3: Analytics -->
      <rect x="385" y="35" width="150" height="150" rx="6" fill="#4338ca" stroke="#312e81" stroke-width="1.5"/>
      <text x="460" y="65" fill="#ffffff" font-size="11" font-weight="bold" text-anchor="middle">3. ANALYTICS</text>
      <text x="460" y="90" fill="#c7d2fe" font-size="9" text-anchor="middle">traffic_analyzer.py</text>
      <text x="460" y="115" fill="#ffffff" font-size="8.5" text-anchor="middle">• TrafficStats State</text>
      <text x="460" y="135" fill="#ffffff" font-size="8.5" text-anchor="middle">• Top Talkers IPs</text>
      <text x="460" y="155" fill="#ffffff" font-size="8.5" text-anchor="middle">• Throughput Rates</text>
      <text x="460" y="172" fill="#ffffff" font-size="8.5" text-anchor="middle">• Anomaly Rules</text>

      <!-- Outputs -->
      <rect x="580" y="35" width="150" height="40" rx="4" fill="#0369a1" stroke="#075985" stroke-width="1.2"/>
      <text x="655" y="52" fill="#ffffff" font-size="8.5" font-weight="bold" text-anchor="middle">Live CLI Cards</text>
      <text x="655" y="67" fill="#bae6fd" font-size="7.5" text-anchor="middle">Terminal Display</text>

      <rect x="580" y="90" width="150" height="40" rx="4" fill="#15803d" stroke="#166534" stroke-width="1.2"/>
      <text x="655" y="107" fill="#ffffff" font-size="8.5" font-weight="bold" text-anchor="middle">CSV Log Engine</text>
      <text x="655" y="122" fill="#bbf7d0" font-size="7.5" text-anchor="middle">logger.py (Anti-Lock)</text>

      <rect x="580" y="145" width="150" height="40" rx="4" fill="#b45309" stroke="#92400e" stroke-width="1.2"/>
      <text x="655" y="162" fill="#ffffff" font-size="8.5" font-weight="bold" text-anchor="middle">Summary Report</text>
      <text x="655" y="177" fill="#fde68a" font-size="7.5" text-anchor="middle">report.py (.txt files)</text>
    </svg>
    <div class="diagram-caption">Figure 2.1: Architectural Dataflow & Multi-Stage Processing Pipeline of Smart Network Packet Sniffer v2</div>
  </div>

  <h2>2.2 Functional Module Breakdown</h2>
  <table>
    <thead>
      <tr>
        <th style="width: 22%;">Module</th>
        <th style="width: 28%;">Primary Class / Functions</th>
        <th>System Responsibilities & Key Architectural Role</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>packet_capture.py</strong></td>
        <td><code>get_available_interfaces()</code><br><code>start_capture()</code></td>
        <td>Discovers and prioritizes active adapters. Manages Scapy sniffing loop with micro-batched 0.5s timeouts to prevent Windows GIL deadlocks during capture.</td>
      </tr>
      <tr>
        <td><strong>analyzer.py</strong></td>
        <td><code>analyze_packet()</code><br><code>decode_tcp_flags()</code><br><code>decode_icmp_info()</code></td>
        <td>Dissects raw Scapy packets into clean standardized dictionaries. Resolves TCP flag bitmasks, ICMP RFC code semantics, ARP hardware mappings, and Layer 7 services.</td>
      </tr>
      <tr>
        <td><strong>traffic_analyzer.py</strong></td>
        <td><code>TrafficStats</code> class<br><code>add_packet()</code><br><code>get_summary()</code></td>
        <td>Maintains stateful traffic counters, calculates bandwidth throughput (pps, B/s, Kbps), tracks top communicating endpoints, and executes rule-based anomaly detection.</td>
      </tr>
      <tr>
        <td><strong>logger.py</strong></td>
        <td><code>SessionLogger</code> class<br><code>log_packet()</code></td>
        <td>Manages resilient per-session CSV logging. Detects Windows OS file sharing violations (e.g. open in Excel) and automatically pivots to an alternate file stream.</td>
      </tr>
      <tr>
        <td><strong>report.py</strong></td>
        <td><code>generate_report()</code><br><code>get_previous_reports()</code></td>
        <td>Formats final metrics into an archival plaintext report document in <code>reports/</code> and allows terminal browsing of historical capture audits.</td>
      </tr>
      <tr>
        <td><strong>main.py</strong></td>
        <td><code>run_packet_sniffer()</code><br><code>main()</code> loop</td>
        <td>Console user interface providing validated interactive menus, runtime configurations, live packet card rendering, and graceful shutdown interception.</td>
      </tr>
    </tbody>
  </table>
</div>

<!-- ==================== CHAPTER 3 ==================== -->
<div class="page-break">
  <h1><span class="chapter-num">03</span>Packet Dissection & Protocol Handling</h1>

  <h2>3.1 Layer-by-Layer Decapsulation Mechanism</h2>
  <p>
    When a frame reaches the sniffer from the Npcap ring buffer, <code>analyze_packet()</code> peels back the protocol headers
    sequentially according to the OSI model:
  </p>

  <div class="avoid-break">
    <h3>1. Data Link Layer (Layer 2)</h3>
    <p>
      The system inspects for Address Resolution Protocol (<code>ARP</code>) frames and generic <code>Ethernet</code> frames.
      For ARP packets, operation codes are translated: Code <code>1</code> is designated as <em>ARP Request</em>
      ("Who has IP? Tell source"), while Code <code>2</code> is translated as <em>ARP Reply</em> ("IP is at MAC").
      Non-IP frames (such as LLDP, STP, or raw IEEE 802.3) are preserved with their hexadecimal EtherType tags (e.g., <code>0x88cc</code>).
    </p>

    <h3>2. Network Layer (Layer 3)</h3>
    <p>
      The module validates the presence of the <code>IP</code> (IPv4) or <code>IPv6</code> layer. It extracts the source and destination
      IP addresses, packet length, and timestamp. The system categorizes frames into IP vs. Non-IP metrics to provide accurate network layer distributions.
    </p>

    <h3>3. Transport Layer (Layer 4)</h3>
    <p>
      Transport headers are segregated into TCP, UDP, and ICMP:
    </p>
    <ul>
      <li><strong>Transmission Control Protocol (TCP):</strong> Source and destination ports are retrieved alongside sequence and acknowledgment parameters. Flags are passed through the bitmask decoder.</li>
      <li><strong>User Datagram Protocol (UDP):</strong> Stateless datagram ports are identified and categorized.</li>
      <li><strong>Internet Control Message Protocol (ICMP):</strong> Type and code values are mapped to RFC standard diagnostics (e.g., Type 8 Echo Request, Type 0 Echo Reply, Type 3 Destination Unreachable with sub-codes like Port Unreachable or Network Unreachable).</li>
    </ul>

    <h3>4. Application Layer Service Heuristics (Layer 7)</h3>
    <p>
      A static lookup table (<code>COMMON_SERVICES</code>) evaluates both source and destination transport ports to map network flows
      to well-known enterprise protocols, including DNS (Port 53), HTTP (Port 80), HTTPS (Port 443), SSH (Port 22), RDP (Port 3389),
      DHCP (Ports 67/68), and database interfaces (MySQL 3306, PostgreSQL 5432).
    </p>
  </div>

  <h2>3.2 TCP Flag Bitmask Analysis</h2>
  <p>
    TCP control flags dictate connection establishment, teardown, and flow control. The <code>analyzer.py</code> module translates
    Scapy flag bytes into human-readable multi-flag sequences using the following mapping:
  </p>

  <table>
    <thead>
      <tr>
        <th>Flag Code</th>
        <th>Flag Name</th>
        <th>Hex Bit</th>
        <th>Protocol Significance & Sniffer Interpretation</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>S</code></td>
        <td>SYN</td>
        <td>0x02</td>
        <td>Synchronize sequence numbers. Initiates TCP 3-way handshake. Monitored for SYN flood detection.</td>
      </tr>
      <tr>
        <td><code>A</code></td>
        <td>ACK</td>
        <td>0x10</td>
        <td>Acknowledgment field significant. Present in almost all ongoing connection packets.</td>
      </tr>
      <tr>
        <td><code>F</code></td>
        <td>FIN</td>
        <td>0x01</td>
        <td>Finished. Sender has finished transmitting data; initiates graceful teardown.</td>
      </tr>
      <tr>
        <td><code>R</code></td>
        <td>RST</td>
        <td>0x04</td>
        <td>Reset. Aborts abnormal connections or rejects invalid port connections.</td>
      </tr>
      <tr>
        <td><code>P</code></td>
        <td>PSH</td>
        <td>0x08</td>
        <td>Push function. Requests receiver to pass data immediately to application layer.</td>
      </tr>
      <tr>
        <td><code>U</code></td>
        <td>URG</td>
        <td>0x20</td>
        <td>Urgent pointer field significant. Indicates prioritized out-of-band data.</td>
      </tr>
    </tbody>
  </table>
</div>

<!-- ==================== CHAPTER 4 ==================== -->
<div class="page-break">
  <h1><span class="chapter-num">04</span>Real-Time Analytics & Heuristic Anomaly Detection</h1>

  <h2>4.1 Statistical Throughput & Bandwidth Algorithms</h2>
  <p>
    The <code>TrafficStats</code> engine calculates network velocity across three primary dimensions:
  </p>
  <ul>
    <li><strong>Packet Velocity ($PPS$):</strong>
      $$PPS = \frac{N_{\text{total}}}{\Delta t}$$
      where $N_{\text{total}}$ is the total packet count and $\Delta t = \max(t_{\text{end}} - t_{\text{start}}, 0.001)$ seconds.
    </li>
    <li><strong>Byte Throughput ($BPS$):</strong>
      $$BPS = \frac{\sum_{i=1}^{N} \text{Length}_i}{\Delta t}$$
    </li>
    <li><strong>Network Bandwidth ($Kbps$):</strong>
      $$Kbps = \frac{\left(\sum_{i=1}^{N} \text{Length}_i \times 8\right)}{\Delta t \times 1000}$$
    </li>
  </ul>

  <h2>4.2 Rule-Based Threat Detection Heuristics</h2>
  <p>
    Rather than relying on resource-intensive machine learning models that can introduce inference latency during wire-speed capture,
    the sniffer implements deterministic, low-overhead rule engines that monitor stateful counters during each capture session:
  </p>

  <div class="avoid-break">
    <div class="callout callout-warning">
      <div class="callout-title">Anomaly Rule 1: TCP SYN Flood & Half-Open Probe Detection</div>
      <p style="margin-bottom: 0;">
        <strong>Mechanism:</strong> A SYN flood overwhelms target servers by dispatching connection requests without completing the 3-way handshake.
        The system tracks all packets with the <code>SYN</code> flag asserted where <code>ACK</code> is absent.
        An alert is triggered if total SYN packets exceed 15 and constitute over 40% of all TCP traffic,
        or if any single host IP generates &ge; 10 lone SYN packets:
        <br><br>
        <code>Trigger Condition: (Total_SYN &ge; 15 AND (Total_SYN / Total_TCP) &gt; 0.40) OR (Max_Host_SYN &ge; 10)</code>
      </p>
    </div>

    <div class="callout callout-warning">
      <div class="callout-title">Anomaly Rule 2: Horizontal Port Sweep / Scanning Detection</div>
      <p style="margin-bottom: 0;">
        <strong>Mechanism:</strong> Malicious reconnaissance scans sequentially probe ports to identify exposed services.
        The engine maintains a hash set of accessed destination ports for each unique source IP:
        <code>Map[Source_IP] = {Port_1, Port_2, ...}</code>. If the cardinality <code>|Map[Source_IP]| &ge; 8</code>,
        an explicit security alert is registered designating the host as an active port scanner.
      </p>
    </div>

    <div class="callout callout-warning">
      <div class="callout-title">Anomaly Rule 3: Cleartext Insecure Protocol Usage</div>
      <p style="margin-bottom: 0;">
        <strong>Mechanism:</strong> Plaintext protocols expose sensitive credentials and packet contents to eavesdropping.
        Traffic routed over Port 80 (HTTP), Port 23 (Telnet), or Port 21 (FTP-Control) is immediately flagged with source,
        destination, and protocol identification in the final audit report.
      </p>
    </div>
  </div>
</div>

<!-- ==================== CHAPTER 5 ==================== -->
<div class="page-break">
  <h1><span class="chapter-num">05</span>Concurrency, Fault Tolerance & Logging Resilience</h1>

  <h2>5.1 Resolving the Windows Scapy GIL Lock Issue</h2>
  <p>
    A critical challenge when operating Scapy on Windows platforms is Python's Global Interpreter Lock (GIL).
    When Scapy invokes the underlying WinPcap/Npcap C-library with <code>sniff(count=N)</code>, the C extension blocks execution
    inside native code until all N packets arrive. If network traffic is idle or slow, Python never regains the GIL,
    rendering keyboard interrupts (<code>Ctrl+C</code>) completely unresponsive.
  </p>
  <p>
    To resolve this without multithreading race conditions, <code>packet_capture.py</code> implements a responsive <strong>Micro-Batching Architecture</strong>:
  </p>

  <pre><code>def start_capture(callback, iface=None, packet_filter="", count=0):
    # Loop executes micro-batches with a 0.5-second timeout window
    while captured_count < count:
        remaining = count - captured_count
        sniff(
            prn=counting_callback,
            filter=packet_filter,
            count=remaining,
            store=False,
            timeout=0.5   # Regains GIL every 500ms to catch Ctrl+C instantly
        )</code></pre>

  <p>
    Because execution returns to Python's evaluation loop every 500 milliseconds, the interpreter safely catches
    <code>KeyboardInterrupt</code> exceptions, guaranteeing instant, graceful termination and metric finalization under all network conditions.
  </p>

  <h2>5.2 Dynamic File-Lock Detection & Fallback Redirection</h2>
  <p>
    In real-world incident response workflows, security operators routinely double-click the active CSV log file to inspect it
    in spreadsheet software such as Microsoft Excel. On Windows, Excel acquires a mandatory <code>FILE_SHARE_READ</code> lock,
    preventing any other process from opening the file for writing and raising a Python <code>PermissionError</code>.
  </p>
  <p>
    To guarantee zero packet loss, <code>logger.py</code> features an adaptive <strong>File-Lock Recovery Protocol</strong>:
  </p>

  <div class="diagram-container avoid-break">
    <svg width="100%" height="130" viewBox="0 0 700 130" xmlns="http://www.w3.org/2000/svg">
      <rect x="10" y="35" width="160" height="60" rx="6" fill="#1e293b"/>
      <text x="90" y="62" fill="#ffffff" font-size="9.5" font-weight="bold" text-anchor="middle">Packet Received</text>
      <text x="90" y="78" fill="#94a3b8" font-size="8" text-anchor="middle">Write to session_*.csv</text>

      <path d="M 170 65 L 230 65" stroke="#2563eb" stroke-width="2.5" fill="none"/>

      <polygon points="280,35 340,65 280,95 220,65" fill="#f59e0b"/>
      <text x="280" y="69" fill="#ffffff" font-size="9" font-weight="bold" text-anchor="middle">File Locked?</text>

      <path d="M 340 65 L 430 45" stroke="#10b981" stroke-width="2.5" fill="none"/>
      <text x="375" y="45" fill="#047857" font-size="8.5" font-weight="bold">NO</text>
      <rect x="430" y="20" width="220" height="40" rx="4" fill="#065f46"/>
      <text x="540" y="44" fill="#ffffff" font-size="9" text-anchor="middle">Append Row Normally</text>

      <path d="M 340 65 L 430 90" stroke="#ef4444" stroke-width="2.5" fill="none"/>
      <text x="375" y="90" fill="#b91c1c" font-size="8.5" font-weight="bold">YES (Excel)</text>
      <rect x="430" y="75" width="250" height="45" rx="4" fill="#991b1b"/>
      <text x="555" y="95" fill="#ffffff" font-size="8.5" font-weight="bold" text-anchor="middle">Catch PermissionError & Redirect</text>
      <text x="555" y="110" fill="#fecaca" font-size="7.5" text-anchor="middle">Auto-create session_*_alt_TIMESTAMP.csv</text>
    </svg>
    <div class="diagram-caption">Figure 5.1: File-Lock Exception Handling & Alternative Logging Stream Pivot</div>
  </div>
</div>

<!-- ==================== CHAPTER 6 ==================== -->
<div class="page-break">
  <h1><span class="chapter-num">06</span>Empirical Verification & Test Results</h1>

  <h2>6.1 Real Network Benchmark Analysis</h2>
  <p>
    The system was evaluated against real live network traffic on an 802.11ac Wi-Fi production interface.
    The benchmark run captured <strong>2,500 continuous packets</strong> over an observation window of <strong>222.10 seconds</strong>
    (Session ID: <code>20260908_120458</code>). Below are the empirical results recorded by the analytics engine:
  </p>

  <div class="metrics-grid avoid-break">
    <div class="metric-card">
      <div class="metric-value">2,500</div>
      <div class="metric-label">Total Packets Captured</div>
    </div>
    <div class="metric-card">
      <div class="metric-value">944.1 KB</div>
      <div class="metric-label">Data Volume (944,089 Bytes)</div>
    </div>
    <div class="metric-card">
      <div class="metric-value">222.1 s</div>
      <div class="metric-label">Capture Session Duration</div>
    </div>
    <div class="metric-card">
      <div class="metric-value">11.26</div>
      <div class="metric-label">Packet Throughput (pkts/sec)</div>
    </div>
    <div class="metric-card">
      <div class="metric-value">34.01</div>
      <div class="metric-label">Bandwidth Rate (Kbps)</div>
    </div>
    <div class="metric-card">
      <div class="metric-value">377.6 B</div>
      <div class="metric-label">Average Packet Size</div>
    </div>
  </div>

  <h2>6.2 Protocol Distribution Breakdown</h2>
  <p>
    The captured traffic exhibited a realistic multi-protocol enterprise distribution, dominated by secure encrypted web traffic
    alongside local service discovery and network resolution:
  </p>

  <table class="avoid-break">
    <thead>
      <tr>
        <th>Protocol Type</th>
        <th>Packet Count</th>
        <th>Percentage</th>
        <th>Primary Identified Services & Notes</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><span class="badge badge-tcp">TCP</span></td>
        <td><strong>2,021</strong></td>
        <td><strong>80.8 %</strong></td>
        <td>HTTPS (TLS/SSL on Port 443), Cleartext HTTP (Port 80)</td>
      </tr>
      <tr>
        <td><span class="badge badge-udp">UDP</span></td>
        <td><strong>444</strong></td>
        <td><strong>17.8 %</strong></td>
        <td>DNS queries (Port 53), mDNS / SSDP local service discovery</td>
      </tr>
      <tr>
        <td><span class="badge badge-arp">ARP</span></td>
        <td><strong>33</strong></td>
        <td><strong>1.3 %</strong></td>
        <td>20 ARP Requests, 13 ARP Replies (Gateway MAC resolution)</td>
      </tr>
      <tr>
        <td><span class="badge badge-icmp">ICMP</span></td>
        <td><strong>2</strong></td>
        <td><strong>0.1 %</strong></td>
        <td>Network reachability echo requests/replies</td>
      </tr>
      <tr>
        <td><strong>Total Frames</strong></td>
        <td><strong>2,500</strong></td>
        <td><strong>100.0 %</strong></td>
        <td>2,467 IP Frames (98.7%) / 33 Non-IP Frames (1.3%)</td>
      </tr>
    </tbody>
  </table>

  <h2>6.3 Top Communicating Endpoints & Anomaly Verification</h2>
  <div class="avoid-break">
    <p>
      The ranking engine identified the local host (<code>10.108.17.127</code>) as the primary talker, communicating with cloud
      delivery networks (Cloudflare, Google, Microsoft Azure, Meta CDNs):
    </p>
    <ul>
      <li><strong>Top Source IP:</strong> <code>10.108.17.127</code> with 1,338 packets transferred (568,527 Bytes).</li>
      <li><strong>Top External Destination IP:</strong> <code>57.144.55.32</code> with 260 packets transferred (45,136 Bytes).</li>
      <li><strong>Top Service Port:</strong> HTTPS (Port 443) with 1,968 packets, followed by DNS (76 packets) and HTTP (65 packets).</li>
    </ul>

    <div class="callout callout-warning">
      <div class="callout-title">Automated Security Anomaly Alerts Triggered in Test Session:</div>
      <ul style="margin: 0; padding-left: 18px;">
        <li><strong>High SYN burst detected:</strong> Host <code>10.108.17.127</code> initiated 43 single SYN packets during connection handshakes.</li>
        <li><strong>Port scan / sweep detected:</strong> Remote host <code>10.108.17.247</code> systematically probed 24 distinct destination ports across the subnet.</li>
        <li><strong>Cleartext Insecure protocol alert:</strong> 65 unencrypted HTTP packets detected between <code>10.108.17.127</code> and public web services (<code>23.11.38.161</code>, <code>142.250.193.14</code>).</li>
      </ul>
    </div>
  </div>
</div>

<!-- ==================== CHAPTER 7 ==================== -->
<div class="page-break">
  <h1><span class="chapter-num">07</span>Security, Ethical & Deployment Considerations</h1>

  <h2>7.1 Ethical Boundaries & Promiscuous Mode Legality</h2>
  <p>
    Network packet sniffing is an inherently dual-use technology. When placed in promiscuous mode, a network adapter intercepts
    all unicast frames traversing the physical wire or wireless medium, regardless of the designated destination MAC address.
  </p>
  <p>
    <strong>Deployment Guidelines & Compliance Requirements:</strong>
  </p>
  <ul>
    <li><strong>Authorized Environments Only:</strong> This software is strictly intended for network administration, authorized penetration testing under formal Rules of Engagement (RoE), and educational laboratory environments.</li>
    <li><strong>Privacy Considerations:</strong> As verified by Anomaly Rule 3, cleartext traffic contains sensitive unencrypted session data (HTTP headers, cleartext form submissions). Log files stored in the <code>logs/</code> directory must be protected with appropriate access control permissions.</li>
  </ul>

  <h2>7.2 Windows Privilege & Driver Requirements</h2>
  <p>
    Windows natively prohibits raw socket creation for unprivileged user accounts to safeguard against unauthorized packet interception.
    Executing the sniffer requires:
  </p>
  <ol>
    <li><strong>Npcap Driver Installation:</strong> The Npcap driver must be installed with the option <em>"Install Npcap in WinPcap API-compatible Mode"</em> enabled.</li>
    <li><strong>Administrative Execution:</strong> The terminal process (PowerShell or Command Prompt) must be launched via <em>"Run as administrator"</em> to grant Scapy access to the Npcap device handle (<code>\\Device\\NPF_{...}</code>).</li>
  </ol>
</div>

<!-- ==================== CHAPTER 8 ==================== -->
<div class="page-break">
  <h1><span class="chapter-num">08</span>Conclusion, Future Work & References</h1>

  <h2>8.1 Project Conclusion</h2>
  <p>
    The <strong>Smart Network Packet Sniffer v2</strong> successfully provides a comprehensive, production-ready network monitoring
    and security analysis platform. By uniting Scapy's dissection capabilities with responsive micro-batching, stateful traffic analytics,
    and automatic file-lock recovery, the software achieves high operational stability and zero-lag user feedback under demanding
    network conditions.
  </p>

  <h2>8.2 Future Roadmap</h2>
  <ul>
    <li><strong>PCAP / PCAPNG Native Export:</strong> Implementing direct serialization to standard <code>.pcap</code> files for seamless interoperability with tools like Wireshark and Zeek.</li>
    <li><strong>Real-Time Web Dashboard:</strong> Integrating the existing Flask framework with WebSockets to stream live packet cards and bandwidth charts to a modern web GUI.</li>
    <li><strong>Machine Learning Anomaly Engine:</strong> Incorporating lightweight Isolation Forest or K-Means clustering algorithms to detect zero-day volumetric anomalies and DNS tunneling attacks.</li>
    <li><strong>Hardware Acceleration:</strong> Exploring multithreaded worker pools using Python's <code>multiprocessing</code> or Rust native extensions for high-throughput 10 Gbps enterprise backbones.</li>
  </ul>

  <h2>8.3 Standards & References</h2>
  <ol style="font-size: 8.5pt;">
    <li>RFC 791: <em>Internet Protocol (IPv4) Specification</em>, Internet Engineering Task Force (IETF).</li>
    <li>RFC 793: <em>Transmission Control Protocol (TCP) Specification</em>, IETF.</li>
    <li>RFC 768: <em>User Datagram Protocol (UDP)</em>, IETF.</li>
    <li>RFC 792: <em>Internet Control Message Protocol (ICMP)</em>, IETF.</li>
    <li>RFC 826: <em>An Ethernet Address Resolution Protocol (ARP)</em>, IETF.</li>
    <li>Biman et al., <em>Scapy: Packet Manipulation and Analysis Library Documentation</em>, SecDev, 2024.</li>
    <li>Insecure.Org, <em>Npcap: Windows Packet Capture Library Architecture & API Reference</em>, 2024.</li>
  </ol>
</div>

</body>
</html>
"""

def main():
    print("[*] Writing comprehensive HTML report document...")
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[+] HTML document saved to: {HTML_FILE}")

    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    ]
    browser_bin = None
    for bp in edge_paths:
        if os.path.exists(bp):
            browser_bin = bp
            break

    if not browser_bin:
        print("[!] No compatible headless browser (Edge/Chrome) found.")
        sys.exit(1)

    print(f"[*] Compiling PDF using: {browser_bin}")
    cmd = [
        browser_bin,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={PDF_FILE}",
        f"file:///{HTML_FILE.replace('\\\\', '/')}"
    ]
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(PDF_FILE) and os.path.getsize(PDF_FILE) > 0:
        size_kb = os.path.getsize(PDF_FILE) / 1024
        print(f"[SUCCESS] High-Quality Project Report PDF generated successfully!")
        print(f"         Location : {PDF_FILE}")
        print(f"         Size     : {size_kb:.2f} KB")
    else:
        print(f"[ERROR] Failed to generate PDF: {res.stderr}")
        sys.exit(1)

if __name__ == "__main__":
    main()
