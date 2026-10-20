"""
generate_perfect_pdf.py
Builds an exact 11-page publication-grade PDF technical report for Smart Network Packet Sniffer v2.
Each page is calibrated to standard A4 printable dimensions with custom running headers and footers.
"""

import os
import subprocess
import sys

HTML_FILE = r"c:\Smart-Packet-Sniffer_v1\report_document.html"
PDF_FILE = r"c:\Smart-Packet-Sniffer_v1\Smart_Packet_Sniffer_Project_Report.pdf"

html_content = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Smart Network Packet Sniffer v2 - Comprehensive Technical Report</title>
<style>
  @page {
    size: A4 portrait;
    margin: 14mm 14mm 14mm 14mm;
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
    line-height: 1.5;
    font-size: 10pt;
    margin: 0;
    padding: 0;
  }

  /* Page Wrapper - Exactly 1 physical A4 page per section */
  .page {
    page-break-after: always;
    break-after: page;
    height: 268mm;
    max-height: 268mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
    position: relative;
    padding-bottom: 2mm;
  }

  .page-content {
    flex: 1 1 auto;
    overflow: hidden;
  }

  .page-footer {
    flex: 0 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid #cbd5e1;
    padding-top: 5px;
    font-size: 8pt;
    color: #64748b;
    margin-top: 6px;
  }
  .page-footer .report-tag {
    font-weight: 600;
    color: #334155;
  }
  .page-footer .page-number {
    font-weight: 700;
    color: #2563eb;
  }

  /* Headings */
  h1 {
    font-size: 16pt;
    font-weight: 800;
    color: #0f172a;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 6px;
    margin-top: 4px;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
  }
  h1 .chapter-num {
    background: #1e3a8a;
    color: #ffffff;
    font-size: 10pt;
    font-weight: 700;
    padding: 2px 9px;
    border-radius: 4px;
    margin-right: 10px;
  }

  h2 {
    font-size: 12pt;
    font-weight: 700;
    color: #1e293b;
    margin-top: 14px;
    margin-bottom: 6px;
  }

  h3 {
    font-size: 10.5pt;
    font-weight: 600;
    color: #334155;
    margin-top: 10px;
    margin-bottom: 4px;
  }

  p {
    margin-top: 0;
    margin-bottom: 8px;
    text-align: justify;
    line-height: 1.48;
  }

  ul, ol {
    margin-top: 0;
    margin-bottom: 8px;
    padding-left: 20px;
  }
  li {
    margin-bottom: 4px;
    line-height: 1.45;
  }

  /* Callouts */
  .callout {
    padding: 10px 14px;
    border-radius: 6px;
    margin: 10px 0;
    font-size: 9pt;
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
  .callout-title {
    font-weight: 700;
    margin-bottom: 3px;
    font-size: 9.5pt;
  }

  /* Tables */
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
    font-size: 8.5pt;
  }
  th {
    background-color: #0f172a;
    color: #ffffff;
    font-weight: 600;
    text-align: left;
    padding: 6px 10px;
    border: 1px solid #0f172a;
  }
  td {
    padding: 5px 10px;
    border: 1px solid #e2e8f0;
    vertical-align: top;
  }
  tr:nth-child(even) td {
    background-color: #f8fafc;
  }

  /* Code & Formulas */
  pre {
    background: #0f172a;
    color: #f1f5f9;
    padding: 10px 14px;
    border-radius: 6px;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 8pt;
    margin: 8px 0;
    line-height: 1.4;
  }
  code {
    font-family: "Consolas", "Courier New", monospace;
    background: #f1f5f9;
    color: #0f172a;
    padding: 1px 4px;
    border-radius: 3px;
    font-size: 8.5pt;
  }
  pre code {
    background: transparent;
    color: inherit;
    padding: 0;
  }

  .formula-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 8px 12px;
    margin: 6px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .formula-name {
    font-weight: 700;
    color: #1e3a8a;
    font-size: 9pt;
  }
  .formula-math {
    font-family: "Consolas", monospace;
    background: #ffffff;
    border: 1px solid #cbd5e1;
    padding: 3px 8px;
    border-radius: 4px;
    font-weight: 600;
    color: #0f172a;
    font-size: 8.5pt;
  }

  /* Metric Cards */
  .metrics-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin: 10px 0;
  }
  .metric-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 8px 10px;
    text-align: center;
  }
  .metric-value {
    font-size: 15pt;
    font-weight: 800;
    color: #1e3a8a;
    margin-bottom: 2px;
  }
  .metric-label {
    font-size: 7.5pt;
    text-transform: uppercase;
    font-weight: 600;
    color: #64748b;
  }

  /* Badges */
  .badge {
    display: inline-block;
    padding: 2px 7px;
    border-radius: 10px;
    font-size: 7pt;
    font-weight: 700;
    text-transform: uppercase;
  }
  .badge-tcp { background: #dbeafe; color: #1e40af; }
  .badge-udp { background: #fef3c7; color: #92400e; }
  .badge-icmp { background: #fee2e2; color: #991b1b; }
  .badge-arp { background: #e0e7ff; color: #3730a3; }

  /* Table of Contents Box */
  .toc-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 14px 18px;
    margin-top: 10px;
  }
  .toc-row {
    display: flex;
    justify-content: space-between;
    padding: 5px 0;
    border-bottom: 1px dotted #cbd5e1;
    font-size: 9pt;
  }
  .toc-row:last-child {
    border-bottom: none;
  }
  .toc-chapter {
    font-weight: 700;
    color: #1e293b;
  }
  .toc-dots {
    color: #64748b;
  }
  .toc-pnum {
    font-weight: 700;
    color: #2563eb;
  }
</style>
</head>
<body>

<!-- ==================== PAGE 1: COVER PAGE ==================== -->
<div class="page" style="border-top: 8px solid #1e3a8a; padding: 25px 15px 10px 15px;">
  <div class="page-content" style="display: flex; flex-direction: column; justify-content: space-between;">
    <div>
      <div style="display: inline-block; padding: 5px 14px; background: #e0e7ff; color: #3730a3; font-weight: 700; font-size: 8.5pt; text-transform: uppercase; letter-spacing: 1.5px; border-radius: 20px; margin-bottom: 20px;">
        Engineering &amp; Technical Project Report
      </div>
      <h1 style="font-size: 26pt; font-weight: 800; color: #0f172a; line-height: 1.2; margin: 0 0 12px 0; border: none; padding: 0;">
        SMART NETWORK PACKET SNIFFER v2
      </h1>
      <div style="font-size: 13pt; color: #475569; font-weight: 400; line-height: 1.4; margin-bottom: 20px;">
        Real-Time Traffic Analysis, Multi-Layer Protocol Dissection, Heuristic Anomaly Detection &amp; Telemetry Reporting System
      </div>
      <div style="width: 70px; height: 4px; background: #2563eb; margin-bottom: 24px;"></div>
      <p style="color: #475569; font-size: 10pt; line-height: 1.6; max-width: 95%;">
        A high-performance, modular Python network inspection framework designed for wire-speed packet capture,
        deep protocol decapsulation across Layers 2 through 7, real-time statistical bandwidth calculation,
        rule-based security anomaly alerting, and resilient session auditing on modern Windows architectures.
      </p>
    </div>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 18px; margin: 20px 0;">
      <div>
        <div style="font-size: 8pt; text-transform: uppercase; letter-spacing: 0.8px; color: #64748b; font-weight: 600;">Project Domain</div>
        <div style="font-size: 10pt; font-weight: 700; color: #0f172a;">Computer Networks &amp; Cybersecurity</div>
      </div>
      <div>
        <div style="font-size: 8pt; text-transform: uppercase; letter-spacing: 0.8px; color: #64748b; font-weight: 600;">Core Implementation</div>
        <div style="font-size: 10pt; font-weight: 700; color: #0f172a;">Python 3.12, Scapy 2.7.0, Npcap Engine</div>
      </div>
      <div>
        <div style="font-size: 8pt; text-transform: uppercase; letter-spacing: 0.8px; color: #64748b; font-weight: 600;">Operating Platform</div>
        <div style="font-size: 10pt; font-weight: 700; color: #0f172a;">Microsoft Windows (x64 Architecture)</div>
      </div>
      <div>
        <div style="font-size: 8pt; text-transform: uppercase; letter-spacing: 0.8px; color: #64748b; font-weight: 600;">Document Specification</div>
        <div style="font-size: 10pt; font-weight: 700; color: #0f172a;">v2.1 Comprehensive Architecture Report</div>
      </div>
      <div>
        <div style="font-size: 8pt; text-transform: uppercase; letter-spacing: 0.8px; color: #64748b; font-weight: 600;">System Modules</div>
        <div style="font-size: 10pt; font-weight: 700; color: #0f172a;">Capture, Dissection, Analytics, Logger, Report, CLI</div>
      </div>
      <div>
        <div style="font-size: 8pt; text-transform: uppercase; letter-spacing: 0.8px; color: #64748b; font-weight: 600;">Telemetry Outputs</div>
        <div style="font-size: 10pt; font-weight: 700; color: #0f172a;">Structured CSV Logs &amp; Archival TXT Summaries</div>
      </div>
    </div>

    <div style="display: flex; justify-content: space-between; border-top: 1px solid #e2e8f0; padding-top: 14px; font-size: 8.5pt; color: #64748b;">
      <div>Smart Packet Sniffer Development Team</div>
      <div>October 2026</div>
      <div>Confidential &amp; Academic Project Material</div>
    </div>
  </div>
  <div class="page-footer">
    <span class="report-tag">Smart Network Packet Sniffer v2 • Project Report</span>
    <span class="page-number">Page 1 of 11</span>
  </div>
</div>

<!-- ==================== PAGE 2: EXECUTIVE SUMMARY ==================== -->
<div class="page">
  <div class="page-content">
    <h1><span class="chapter-num">00</span>Executive Summary &amp; Abstract</h1>
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
      and ARP traffic without dropped frames under moderate to high network loads.
    </p>

    <h2>Key Technical Milestones Achieved</h2>
    <ul>
      <li><strong>Asynchronous GIL-Responsive Micro-Batching:</strong> Implements a 0.5-second polling window that resolves the notorious Scapy Windows GIL-locking issue, enabling instantaneous <code>Ctrl+C</code> signal termination even on completely idle network adapters.</li>
      <li><strong>Full-Stack Multi-Layer Protocol Dissection:</strong> Safely parses raw frames across Layer 2 (Ethernet, ARP), Layer 3 (IPv4, IPv6), Layer 4 (TCP with complete bitmask flag decoding, UDP, ICMP with RFC-compliant code mappings), and Layer 7 (well-known service heuristics).</li>
      <li><strong>Stateful Real-Time Analytics Engine:</strong> Continuously measures throughput (Packets/sec, Bytes/sec, Kilobits/sec), payload distribution metrics, and endpoint talker rankings (source and destination IPs).</li>
      <li><strong>Rule-Based Security Anomaly Detection:</strong> Evaluates traffic heuristics to flag TCP SYN flooding attempts, horizontal port scans (distinct port sweeping per host), and cleartext credentials transmitted over unencrypted legacy protocols (HTTP, Telnet, FTP).</li>
      <li><strong>Resilient Concurrent CSV Logging:</strong> Employs auto-recovering file I/O with automatic lock detection and alternative filename redirection when target log files are opened in external applications such as Microsoft Excel.</li>
    </ul>

    <div class="callout callout-info" style="margin-top: 14px;">
      <div class="callout-title">Operational Summary</div>
      The system combines interactive terminal monitoring with dual-tier telemetry persistence. In empirical testing,
      the engine successfully processed over 2,500 frames without memory degradation while autonomously generating forensic audit trails.
    </div>
  </div>
  <div class="page-footer">
    <span class="report-tag">Smart Network Packet Sniffer v2 • Project Report</span>
    <span class="page-number">Page 2 of 11</span>
  </div>
</div>

<!-- ==================== PAGE 3: TABLE OF CONTENTS & SYSTEM SPECIFICATIONS ==================== -->
<div class="page">
  <div class="page-content">
    <h1><span class="chapter-num">00</span>Table of Contents &amp; Specifications</h1>

    <div class="toc-box">
      <div class="toc-row">
        <span class="toc-chapter">Chapter 1: Introduction, Problem Statement &amp; Objectives</span>
        <span class="toc-dots">...........................................................................</span>
        <span class="toc-pnum">Page 4</span>
      </div>
      <div class="toc-row">
        <span class="toc-chapter">Chapter 2: System Architecture &amp; Modular Pipeline Design</span>
        <span class="toc-dots">...........................................................................</span>
        <span class="toc-pnum">Page 5</span>
      </div>
      <div class="toc-row">
        <span class="toc-chapter">Chapter 3: Packet Dissection &amp; Multi-Layer Protocol Handling</span>
        <span class="toc-dots">...........................................................................</span>
        <span class="toc-pnum">Page 6</span>
      </div>
      <div class="toc-row">
        <span class="toc-chapter">Chapter 4: Real-Time Analytics &amp; Threat Anomaly Detection</span>
        <span class="toc-dots">...........................................................................</span>
        <span class="toc-pnum">Page 7</span>
      </div>
      <div class="toc-row">
        <span class="toc-chapter">Chapter 5: Concurrency, Fault Tolerance &amp; Logging Resilience</span>
        <span class="toc-dots">...........................................................................</span>
        <span class="toc-pnum">Page 8</span>
      </div>
      <div class="toc-row">
        <span class="toc-chapter">Chapter 6: Empirical Verification, Benchmarking &amp; Test Results</span>
        <span class="toc-dots">...........................................................................</span>
        <span class="toc-pnum">Page 9</span>
      </div>
      <div class="toc-row">
        <span class="toc-chapter">Chapter 7: Security Privileges, Ethical Boundaries &amp; Deployment</span>
        <span class="toc-dots">...........................................................................</span>
        <span class="toc-pnum">Page 10</span>
      </div>
      <div class="toc-row">
        <span class="toc-chapter">Chapter 8: Conclusion, Future Roadmap &amp; References</span>
        <span class="toc-dots">...........................................................................</span>
        <span class="toc-pnum">Page 11</span>
      </div>
    </div>

    <h2>System Environment &amp; Hardware Specifications</h2>
    <table>
      <thead>
        <tr>
          <th style="width: 30%;">Component / Parameter</th>
          <th style="width: 35%;">Specification / Version</th>
          <th>Operational Role in System</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Runtime Interpreter</strong></td>
          <td>Python 3.12.x (64-bit)</td>
          <td>Execution environment, standard library collections, and CLI runtime.</td>
        </tr>
        <tr>
          <td><strong>Core Packet Engine</strong></td>
          <td>Scapy 2.7.0</td>
          <td>Network frame decapsulation, BPF filter parsing, and raw socket bindings.</td>
        </tr>
        <tr>
          <td><strong>Kernel Capture Driver</strong></td>
          <td>Npcap 1.7x+ (WinPcap API Mode)</td>
          <td>Low-level kernel NDIS filter driver capturing raw frames off NIC buffers.</td>
        </tr>
        <tr>
          <td><strong>Operating System</strong></td>
          <td>Microsoft Windows 11 / 10 (x64)</td>
          <td>Host OS; requires administrative privilege escalation for raw socket access.</td>
        </tr>
        <tr>
          <td><strong>Network Adapters</strong></td>
          <td>802.11ac Wi-Fi / Gigabit Ethernet</td>
          <td>Physical hardware interfaces monitored in promiscuous capture mode.</td>
        </tr>
        <tr>
          <td><strong>Storage System</strong></td>
          <td>NTFS / Local SSD</td>
          <td>Append-only CSV log repository (<code>logs/</code>) and report storage (<code>reports/</code>).</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="page-footer">
    <span class="report-tag">Smart Network Packet Sniffer v2 • Project Report</span>
    <span class="page-number">Page 3 of 11</span>
  </div>
</div>

<!-- ==================== PAGE 4: CHAPTER 1 ==================== -->
<div class="page">
  <div class="page-content">
    <h1><span class="chapter-num">01</span>Introduction &amp; Theoretical Background</h1>

    <h2>1.1 Problem Statement &amp; Motivations</h2>
    <p>
      In contemporary computer networks, raw packet data provides the absolute ground truth for all system communications.
      Diagnosing intermittent network bottlenecks, verifying firewall policies, and investigating security breaches all depend
      upon packet-level visibility. However, existing packet inspection tools present distinct operational challenges:
    </p>
    <ul>
      <li><strong>Excessive Resource Demands:</strong> GUI-based sniffers like Wireshark carry substantial memory footprints that complicate remote headless deployment and rapid CLI triage.</li>
      <li><strong>Information Overload:</strong> Unprocessed capture outputs inundate analysts with hexadecimal payloads without summarizing endpoint conversations or immediate security threats.</li>
      <li><strong>Windows Platform Concurrency Deadlocks:</strong> On Windows platforms, Python-based sniffers frequently deadlock the Global Interpreter Lock (GIL) inside native C drivers, preventing clean termination via <code>Ctrl+C</code>.</li>
      <li><strong>File Sharing Violations:</strong> Opening active CSV telemetry logs in analytical suites like Microsoft Excel triggers exclusive OS file locks, causing unhandled exceptions in standard sniffers.</li>
    </ul>

    <h2>1.2 System Objectives</h2>
    <p>
      The primary objective of <strong>Smart Network Packet Sniffer v2</strong> is to deliver a robust, modular, and resilient
      packet inspection engine tailored for Windows environments, featuring:
    </p>
    <ol>
      <li><strong>Automated Adapter Enumeration:</strong> Intelligently querying host routing tables to present active adapters with default gateway auto-detection.</li>
      <li><strong>Multi-Layer Protocol Decapsulation:</strong> Dissecting Layer 2 through Layer 7 protocol headers in real-time.</li>
      <li><strong>Stateful Traffic Analytics:</strong> Tracking throughput velocity (PPS, BPS, Kbps) and endpoint rankings.</li>
      <li><strong>Heuristic Security Anomaly Detection:</strong> Detecting TCP SYN flood patterns, port sweeps, and cleartext transmissions.</li>
      <li><strong>Resilient Concurrent Storage:</strong> Streaming logs with automatic file-lock recovery and generating formatted post-capture reports.</li>
    </ol>

    <h2>1.3 Scope &amp; Target Applications</h2>
    <p>
      Designed for network administrators, cybersecurity analysts, and academic researchers, the tool serves as a lightweight
      forensic monitor across local corporate LANs, testing laboratories, and cloud edge nodes.
    </p>
  </div>
  <div class="page-footer">
    <span class="report-tag">Smart Network Packet Sniffer v2 • Project Report</span>
    <span class="page-number">Page 4 of 11</span>
  </div>
</div>

<!-- ==================== PAGE 5: CHAPTER 2 ==================== -->
<div class="page">
  <div class="page-content">
    <h1><span class="chapter-num">02</span>System Architecture &amp; Component Design</h1>

    <h2>2.1 End-to-End Pipeline Architecture</h2>
    <p>
      The architecture follows a decoupled ingestion-dissection-analytics pipeline, ensuring that packet capture timing remains
      unaffected by disk I/O latency or terminal rendering overhead.
    </p>

    <!-- Architecture Diagram SVG -->
    <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; padding: 10px; margin: 8px 0; text-align: center;">
      <svg width="100%" height="150" viewBox="0 0 740 150" xmlns="http://www.w3.org/2000/svg">
        <rect x="5" y="5" width="730" height="140" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.2"/>
        
        <!-- Box 1 -->
        <rect x="20" y="25" width="125" height="100" rx="5" fill="#1e3a8a"/>
        <text x="82" y="50" fill="#ffffff" font-size="10" font-weight="bold" text-anchor="middle">INGESTION</text>
        <text x="82" y="70" fill="#93c5fd" font-size="8.5" text-anchor="middle">packet_capture.py</text>
        <text x="82" y="90" fill="#ffffff" font-size="7.5" text-anchor="middle">• Npcap Driver</text>
        <text x="82" y="105" fill="#ffffff" font-size="7.5" text-anchor="middle">• 0.5s Micro-Batch</text>

        <path d="M 145 75 L 185 75" stroke="#2563eb" stroke-width="2.5" fill="none"/>

        <!-- Box 2 -->
        <rect x="185" y="25" width="135" height="100" rx="5" fill="#0f766e"/>
        <text x="252" y="50" fill="#ffffff" font-size="10" font-weight="bold" text-anchor="middle">DISSECTION</text>
        <text x="252" y="70" fill="#99f6e4" font-size="8.5" text-anchor="middle">analyzer.py</text>
        <text x="252" y="90" fill="#ffffff" font-size="7.5" text-anchor="middle">• Eth / ARP / IP</text>
        <text x="252" y="105" fill="#ffffff" font-size="7.5" text-anchor="middle">• TCP / UDP / ICMP</text>

        <path d="M 320 75 L 360 75" stroke="#2563eb" stroke-width="2.5" fill="none"/>

        <!-- Box 3 -->
        <rect x="360" y="25" width="145" height="100" rx="5" fill="#4338ca"/>
        <text x="432" y="50" fill="#ffffff" font-size="10" font-weight="bold" text-anchor="middle">ANALYTICS</text>
        <text x="432" y="70" fill="#c7d2fe" font-size="8.5" text-anchor="middle">traffic_analyzer.py</text>
        <text x="432" y="90" fill="#ffffff" font-size="7.5" text-anchor="middle">• TrafficStats State</text>
        <text x="432" y="105" fill="#ffffff" font-size="7.5" text-anchor="middle">• Heuristic Threat Rules</text>

        <path d="M 505 55 L 545 40" stroke="#2563eb" stroke-width="2" fill="none"/>
        <path d="M 505 75 L 545 75" stroke="#2563eb" stroke-width="2" fill="none"/>
        <path d="M 505 95 L 545 110" stroke="#2563eb" stroke-width="2" fill="none"/>

        <!-- Outputs -->
        <rect x="545" y="20" width="170" height="30" rx="4" fill="#0284c7"/>
        <text x="630" y="38" fill="#ffffff" font-size="8" font-weight="bold" text-anchor="middle">CLI Terminal Cards (Real-Time)</text>

        <rect x="545" y="60" width="170" height="30" rx="4" fill="#16a34a"/>
        <text x="630" y="78" fill="#ffffff" font-size="8" font-weight="bold" text-anchor="middle">Resilient CSV Logs (logger.py)</text>

        <rect x="545" y="100" width="170" height="30" rx="4" fill="#d97706"/>
        <text x="630" y="118" fill="#ffffff" font-size="8" font-weight="bold" text-anchor="middle">Summary TXT Report (report.py)</text>
      </svg>
      <div style="font-size: 7.5pt; color: #64748b; margin-top: 4px; font-weight: 600;">Figure 2.1: End-to-End Processing Architecture of Smart Network Packet Sniffer v2</div>
    </div>

    <h2>2.2 Functional Module Breakdown</h2>
    <table>
      <thead>
        <tr>
          <th style="width: 20%;">Module</th>
          <th style="width: 25%;">Primary Functions / Classes</th>
          <th>Core Architectural Functionality</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>packet_capture.py</strong></td>
          <td><code>get_available_interfaces()</code><br><code>start_capture()</code></td>
          <td>Interfaces with Npcap driver, enumerates network adapters, applies BPF filters, and runs 0.5s micro-batch sniffing.</td>
        </tr>
        <tr>
          <td><strong>analyzer.py</strong></td>
          <td><code>analyze_packet()</code><br><code>decode_tcp_flags()</code></td>
          <td>Dissects raw Scapy frames into structured dictionaries. Translates TCP flags, ICMP RFC codes, and Layer 7 ports.</td>
        </tr>
        <tr>
          <td><strong>traffic_analyzer.py</strong></td>
          <td><code>TrafficStats</code> class<br><code>add_packet()</code></td>
          <td>Stateful engine maintaining packet/byte counters, computing rates (pps, bps, kbps), and executing anomaly rules.</td>
        </tr>
        <tr>
          <td><strong>logger.py</strong></td>
          <td><code>SessionLogger</code> class<br><code>log_packet()</code></td>
          <td>Streams parsed packets into CSV files with automatic fallback redirection upon detecting file-lock errors.</td>
        </tr>
        <tr>
          <td><strong>report.py</strong></td>
          <td><code>generate_report()</code><br><code>get_previous_reports()</code></td>
          <td>Compiles final analytics into a structured text report saved in <code>reports/</code> and allows terminal browsing.</td>
        </tr>
        <tr>
          <td><strong>main.py</strong></td>
          <td><code>main()</code> loop<br><code>run_packet_sniffer()</code></td>
          <td>Interactive CLI interface handling user input validation, terminal card formatting, and capture orchestration.</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="page-footer">
    <span class="report-tag">Smart Network Packet Sniffer v2 • Project Report</span>
    <span class="page-number">Page 5 of 11</span>
  </div>
</div>

<!-- ==================== PAGE 6: CHAPTER 3 ==================== -->
<div class="page">
  <div class="page-content">
    <h1><span class="chapter-num">03</span>Packet Dissection &amp; Protocol Handling</h1>

    <h2>3.1 Multi-Layer Protocol Decapsulation</h2>
    <p>
      The packet dissection engine in <code>analyzer.py</code> strips headers sequentially across the OSI stack:
    </p>
    <ul>
      <li><strong>Data Link Layer (Layer 2):</strong> Decodes Ethernet frames and Address Resolution Protocol (ARP). Distinguishes ARP Requests (Opcode 1: "Who has IP? Tell Source") from ARP Replies (Opcode 2: "IP is at MAC"). Preserves raw EtherType identifiers for non-IP traffic.</li>
      <li><strong>Network Layer (Layer 3):</strong> Handles both IPv4 and IPv6 packets, extracting source and destination IP addresses, payload lengths, and timestamps while maintaining accurate IP vs. Non-IP metrics.</li>
      <li><strong>Transport Layer (Layer 4):</strong> Segregates traffic into TCP, UDP, and ICMP. Decodes TCP sequence numbers and flags, maps UDP ports, and parses ICMP types/codes according to RFC specifications.</li>
      <li><strong>Application Layer Heuristics (Layer 7):</strong> Maps port pairs to well-known protocols including HTTP (80), HTTPS (443), DNS (53), SSH (22), Telnet (23), DHCP (67/68), RDP (3389), and SQL databases (3306, 5432).</li>
    </ul>

    <h2>3.2 TCP Flag Bitmask Decoding Table</h2>
    <table>
      <thead>
        <tr>
          <th style="width: 12%;">Flag Code</th>
          <th style="width: 14%;">Flag Name</th>
          <th style="width: 14%;">Bitmask Hex</th>
          <th>Protocol Role &amp; Anomaly Detection Relevance</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><code>S</code></td>
          <td><strong>SYN</strong></td>
          <td>0x02</td>
          <td>Synchronize sequence numbers. Initiates TCP 3-way handshake; monitored for SYN floods.</td>
        </tr>
        <tr>
          <td><code>A</code></td>
          <td><strong>ACK</strong></td>
          <td>0x10</td>
          <td>Acknowledgment field valid. Asserted on all packets following initial handshake initiation.</td>
        </tr>
        <tr>
          <td><code>F</code></td>
          <td><strong>FIN</strong></td>
          <td>0x01</td>
          <td>Finished. Sender requests graceful connection teardown.</td>
        </tr>
        <tr>
          <td><code>R</code></td>
          <td><strong>RST</strong></td>
          <td>0x04</td>
          <td>Reset. Abrupt connection termination or rejection of closed port requests.</td>
        </tr>
        <tr>
          <td><code>P</code></td>
          <td><strong>PSH</strong></td>
          <td>0x08</td>
          <td>Push function. Requests receiver to forward buffered data immediately to application.</td>
        </tr>
        <tr>
          <td><code>U</code></td>
          <td><strong>URG</strong></td>
          <td>0x20</td>
          <td>Urgent pointer valid. Marks prioritized out-of-band data stream.</td>
        </tr>
      </tbody>
    </table>

    <h2>3.3 ICMP RFC Diagnostic Translation</h2>
    <p>
      Rather than displaying numeric integers, ICMP packets are translated into descriptive diagnostic messages:
      Type 0 (Echo Reply), Type 8 (Echo Request), and Type 3 (Destination Unreachable) with corresponding sub-codes:
      Code 0 (Net Unreachable), Code 1 (Host Unreachable), Code 3 (Port Unreachable), and Code 4 (Fragmentation Needed).
    </p>
  </div>
  <div class="page-footer">
    <span class="report-tag">Smart Network Packet Sniffer v2 • Project Report</span>
    <span class="page-number">Page 6 of 11</span>
  </div>
</div>

<!-- ==================== PAGE 7: CHAPTER 4 ==================== -->
<div class="page">
  <div class="page-content">
    <h1><span class="chapter-num">04</span>Real-Time Analytics &amp; Threat Detection</h1>

    <h2>4.1 Bandwidth &amp; Velocity Velocity Metrics</h2>
    <p>
      The <code>TrafficStats</code> class computes real-time network throughput using stateful accumulators:
    </p>

    <div class="formula-card">
      <span class="formula-name">Packet Velocity (Packets per Second)</span>
      <span class="formula-math">PPS = Total_Packets / &Delta;t</span>
    </div>
    <div class="formula-card">
      <span class="formula-name">Byte Throughput (Bytes per Second)</span>
      <span class="formula-math">BPS = Total_Bytes / &Delta;t</span>
    </div>
    <div class="formula-card">
      <span class="formula-name">Network Bandwidth (Kilobits per Second)</span>
      <span class="formula-math">Kbps = (Total_Bytes &times; 8) / (&Delta;t &times; 1000)</span>
    </div>
    <p style="font-size: 8pt; color: #64748b; margin-top: 2px;">
      * Where &Delta;t is the elapsed capture duration in seconds: &Delta;t = max(t_end - t_start, 0.001).
    </p>

    <h2>4.2 Rule-Based Threat Detection Heuristics</h2>
    <p>
      To maintain wire-speed processing without machine learning latency, the sniffer evaluates three deterministic threat detection rules:
    </p>

    <div class="callout callout-warning">
      <div class="callout-title">Threat Rule 1: TCP SYN Flood &amp; Half-Open Scan Detection</div>
      <p style="margin: 0;">
        Tracks all packets where <code>SYN</code> is asserted while <code>ACK</code> is absent. An alert triggers if total lone SYN
        packets exceed 15 and comprise over 40% of all TCP traffic, or if any individual host emits &ge; 10 lone SYN packets.
        <br><code>Trigger: (SYN_Total &ge; 15 AND (SYN_Total / TCP_Total) &gt; 0.40) OR (Max_Host_SYN &ge; 10)</code>
      </p>
    </div>

    <div class="callout callout-warning">
      <div class="callout-title">Threat Rule 2: Horizontal Port Sweep / Scanning Detection</div>
      <p style="margin: 0;">
        Maintains an in-memory set of unique destination ports targeted by each distinct source IP:
        <code>Port_Map[Source_IP] = {Port_1, Port_2, ...}</code>. If the set cardinality <code>|Port_Map[Source_IP]| &ge; 8</code>,
        the system flags the host as an active port scanner.
      </p>
    </div>

    <div class="callout callout-warning">
      <div class="callout-title">Threat Rule 3: Cleartext Insecure Protocol Usage</div>
      <p style="margin: 0;">
        Monitors for unencrypted protocols that transmit plaintext credentials across the wire, including HTTP (Port 80),
        Telnet (Port 23), and FTP Control (Port 21). Specific communicating endpoint pairs are logged in the security summary.
      </p>
    </div>
  </div>
  <div class="page-footer">
    <span class="report-tag">Smart Network Packet Sniffer v2 • Project Report</span>
    <span class="page-number">Page 7 of 11</span>
  </div>
</div>

<!-- ==================== PAGE 8: CHAPTER 5 ==================== -->
<div class="page">
  <div class="page-content">
    <h1><span class="chapter-num">05</span>Concurrency, Fault Tolerance &amp; Resilience</h1>

    <h2>5.1 Resolving the Windows Scapy GIL Lock Issue</h2>
    <p>
      On Windows, invoking <code>sniff(count=N)</code> enters the native C Npcap driver. When network traffic is quiet or idle,
      the process blocks inside C code without releasing Python's Global Interpreter Lock (GIL). As a result, the Python runtime
      cannot process Windows signals or keyboard interrupts (<code>Ctrl+C</code>), causing the sniffer to appear frozen.
    </p>
    <p>
      To resolve this, <code>packet_capture.py</code> implements a responsive <strong>Micro-Batching Architecture</strong>:
    </p>

    <pre><code>def start_capture(callback, iface=None, packet_filter="", count=0):
    # Executes micro-batches with a 0.5-second timeout window
    while captured_count < count:
        remaining = count - captured_count
        sniff(
            prn=counting_callback,
            filter=packet_filter,
            count=remaining,
            store=False,
            timeout=0.5   # Regains Python GIL every 500ms to catch Ctrl+C
        )</code></pre>

    <h2>5.2 Dynamic File-Lock Detection &amp; Auto-Recovery</h2>
    <p>
      During network investigations, analysts frequently open the active CSV file in spreadsheet viewers (e.g., Microsoft Excel).
      On Windows, Excel places an exclusive <code>FILE_SHARE_READ</code> lock on the file. Standard Python scripts encounter an unhandled
      <code>PermissionError</code> and terminate immediately.
    </p>
    <p>
      <code>logger.py</code> implements an adaptive <strong>File-Lock Redirection Protocol</strong>. When a write operation raises
      a permission error, the logger catches the exception, prints a non-intrusive warning, and automatically diverts subsequent
      packet rows into an alternate timestamped file (<code>session_ID_alt_TIMESTAMP.csv</code>), preventing any data loss.
    </p>

    <h2>5.3 Network Adapter Discovery &amp; Gateway Heuristics</h2>
    <p>
      The system queries Scapy's <code>conf.ifaces</code> routing table, filters out non-functional virtual WAN miniports,
      flags isolated virtual adapters (Hyper-V / WSL), and highlights the primary active gateway adapter with an intuitive
      <code>[Recommended]</code> tag for seamless user onboarding.
    </p>
  </div>
  <div class="page-footer">
    <span class="report-tag">Smart Network Packet Sniffer v2 • Project Report</span>
    <span class="page-number">Page 8 of 11</span>
  </div>
</div>

<!-- ==================== PAGE 9: CHAPTER 6 ==================== -->
<div class="page">
  <div class="page-content">
    <h1><span class="chapter-num">06</span>Empirical Verification &amp; Test Results</h1>

    <h2>6.1 Real Network Benchmark Analysis</h2>
    <p>
      The system was evaluated against real live network traffic on an 802.11ac Wi-Fi production interface.
      The benchmark captured <strong>2,500 continuous packets</strong> over an observation window of <strong>222.10 seconds</strong>
      (Session ID: <code>20260908_120458</code>). Below are the empirical metrics recorded by the analytics engine:
    </p>

    <div class="metrics-grid">
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
        <div class="metric-label">Throughput (Packets / Sec)</div>
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
    <table>
      <thead>
        <tr>
          <th>Protocol</th>
          <th>Packet Count</th>
          <th>Percentage</th>
          <th>Observed Traffic Types &amp; Primary Services</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><span class="badge badge-tcp">TCP</span></td>
          <td><strong>2,021</strong></td>
          <td><strong>80.8 %</strong></td>
          <td>HTTPS (Port 443 TLS/SSL), Cleartext HTTP (Port 80)</td>
        </tr>
        <tr>
          <td><span class="badge badge-udp">UDP</span></td>
          <td><strong>444</strong></td>
          <td><strong>17.8 %</strong></td>
          <td>DNS Name Resolution (Port 53), Local mDNS / SSDP discovery</td>
        </tr>
        <tr>
          <td><span class="badge badge-arp">ARP</span></td>
          <td><strong>33</strong></td>
          <td><strong>1.3 %</strong></td>
          <td>20 ARP Requests, 13 ARP Replies (Default Gateway resolution)</td>
        </tr>
        <tr>
          <td><span class="badge badge-icmp">ICMP</span></td>
          <td><strong>2</strong></td>
          <td><strong>0.1 %</strong></td>
          <td>Diagnostic Echo Request / Reply pings</td>
        </tr>
        <tr>
          <td><strong>Total Frames</strong></td>
          <td><strong>2,500</strong></td>
          <td><strong>100.0 %</strong></td>
          <td>2,467 IP Frames (98.7%) / 33 Non-IP Frames (1.3%)</td>
        </tr>
      </tbody>
    </table>

    <h2>6.3 Verified Threat Anomaly Alerts</h2>
    <div class="callout callout-warning">
      <div class="callout-title">Automated Alerts Triggered in Benchmark Session:</div>
      <ul style="margin: 0; padding-left: 18px;">
        <li><strong>High SYN Burst Detected:</strong> Host <code>10.108.17.127</code> generated 43 single SYN packets during connection handshakes.</li>
        <li><strong>Port Sweep Reconnaissance Detected:</strong> Remote host <code>10.108.17.247</code> systematically probed 24 distinct destination ports.</li>
        <li><strong>Cleartext Insecure Protocol Usage:</strong> 65 unencrypted HTTP packets detected between <code>10.108.17.127</code> and external web hosts.</li>
      </ul>
    </div>
  </div>
  <div class="page-footer">
    <span class="report-tag">Smart Network Packet Sniffer v2 • Project Report</span>
    <span class="page-number">Page 9 of 11</span>
  </div>
</div>

<!-- ==================== PAGE 10: CHAPTER 7 ==================== -->
<div class="page">
  <div class="page-content">
    <h1><span class="chapter-num">07</span>Security, Ethical Boundaries &amp; Deployment</h1>

    <h2>7.1 Ethical Boundaries &amp; Promiscuous Mode Legality</h2>
    <p>
      Packet sniffing technology is inherently dual-use. Operating network interfaces in promiscuous mode allows an adapter
      to capture all unicast, multicast, and broadcast frames passing through the shared medium, regardless of destination MAC addresses.
    </p>
    <ul>
      <li><strong>Authorization Requirement:</strong> This framework must only be deployed on networks where explicit written authorization has been obtained, or within controlled laboratory educational environments.</li>
      <li><strong>Data Privacy Considerations:</strong> Unencrypted network frames frequently expose sensitive credentials, URLs, and cookies. Generated log files stored in <code>logs/</code> must be protected using strict operating system file permissions.</li>
    </ul>

    <h2>7.2 Windows Security Privileges &amp; Driver Setup</h2>
    <ol>
      <li><strong>Npcap Driver Installation:</strong> Windows requires the Npcap kernel driver. When installing, ensure <em>"Install Npcap in WinPcap API-compatible Mode"</em> is checked.</li>
      <li><strong>Administrator Escalation:</strong> Launch PowerShell or Command Prompt via <em>"Run as Administrator"</em>. Non-elevated accounts cannot access Npcap device handles (<code>\Device\NPF_{...}</code>).</li>
    </ol>

    <h2>7.3 Step-by-Step CLI Execution Guide</h2>
    <pre><code># Step 1: Open PowerShell as Administrator and navigate to the project directory
cd c:\Smart-Packet-Sniffer_v1

# Step 2: Launch the interactive CLI controller using the Windows Python launcher
py main.py

# Step 3: Select [1] to Start Packet Capture
# Step 4: Choose network interface (Default is auto-detected active adapter)
# Step 5: Select capture mode (Fixed packet count or Continuous Ctrl+C)
# Step 6: Select protocol filter (All Traffic, TCP, UDP, ICMP, ARP, or Custom BPF)</code></pre>
  </div>
  <div class="page-footer">
    <span class="report-tag">Smart Network Packet Sniffer v2 • Project Report</span>
    <span class="page-number">Page 10 of 11</span>
  </div>
</div>

<!-- ==================== PAGE 11: CHAPTER 8 ==================== -->
<div class="page">
  <div class="page-content">
    <h1><span class="chapter-num">08</span>Conclusion, Future Roadmap &amp; References</h1>

    <h2>8.1 Project Conclusion</h2>
    <p>
      The <strong>Smart Network Packet Sniffer v2</strong> successfully provides a lightweight, modular, and resilient network
      telemetry framework. By coupling Scapy's packet decapsulation capabilities with 0.5-second micro-batching, stateful traffic analytics,
      and dynamic file-lock recovery, the software achieves high operational stability, immediate signal responsiveness,
      and automated security alerting without external GUI dependencies.
    </p>

    <h2>8.2 Future Roadmap</h2>
    <ul>
      <li><strong>Native PCAP/PCAPNG Serialization:</strong> Adding direct binary PCAP recording to enable seamless imports into external analysis platforms like Wireshark and Zeek.</li>
      <li><strong>WebSocket Real-Time Web Dashboard:</strong> Integrating a lightweight Flask/FastAPI service to broadcast live packet streams and interactive bandwidth graphs to modern web browsers.</li>
      <li><strong>Machine Learning Anomaly Detection:</strong> Incorporating unsupervised Isolation Forest models for automated zero-day volumetric anomaly and DNS tunneling detection.</li>
      <li><strong>High-Throughput Multiprocessing:</strong> Splitting packet ingestion and analytical computation across Python <code>multiprocessing</code> worker pools for 10Gbps enterprise networks.</li>
    </ul>

    <h2>8.3 Standards &amp; RFC References</h2>
    <ol style="font-size: 8pt; line-height: 1.45;">
      <li>RFC 791: <em>Internet Protocol (IPv4) Specification</em>, Internet Engineering Task Force (IETF).</li>
      <li>RFC 793: <em>Transmission Control Protocol (TCP) Specification</em>, IETF.</li>
      <li>RFC 768: <em>User Datagram Protocol (UDP) Specification</em>, IETF.</li>
      <li>RFC 792: <em>Internet Control Message Protocol (ICMP) Specification</em>, IETF.</li>
      <li>RFC 826: <em>An Ethernet Address Resolution Protocol (ARP)</em>, IETF.</li>
      <li>Biman et al., <em>Scapy: Packet Manipulation and Analysis Library Documentation</em>, SecDev, 2024.</li>
      <li>Insecure.Org, <em>Npcap: Windows Packet Capture Library Architecture &amp; API Reference</em>, 2024.</li>
    </ol>
  </div>
  <div class="page-footer">
    <span class="report-tag">Smart Network Packet Sniffer v2 • Project Report</span>
    <span class="page-number">Page 11 of 11</span>
  </div>
</div>

</body>
</html>
"""

def main():
    print("[*] Writing calibrated 11-page HTML report document...")
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
        print("[!] Headless browser not found.")
        sys.exit(1)

    print(f"[*] Compiling publication-grade PDF using: {browser_bin}")
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
        print(f"[SUCCESS] Calibrated Project Report PDF generated successfully!")
        print(f"         Location : {PDF_FILE}")
        print(f"         Size     : {size_kb:.2f} KB")
    else:
        print(f"[ERROR] Failed to generate PDF: {res.stderr}")
        sys.exit(1)

if __name__ == "__main__":
    main()
