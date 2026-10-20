"""
packet_capture.py - Packet Capture Engine Module
Smart Network Packet Sniffer v2
"""

from scapy.all import sniff, conf
from scapy.error import Scapy_Exception


def get_available_interfaces():
    """
    Retrieve and format all active and available network adapters.
    Returns a list of interface dicts with the auto-detected default interface first.
    """
    ifaces_list = []
    
    # 1. Primary Auto-detected Default option
    try:
        def_iface = conf.iface
        def_name = getattr(def_iface, "name", "System Default")
        def_desc = getattr(def_iface, "description", "Primary Active Adapter")
        def_ip = getattr(def_iface, "ip", "Auto-detected")
    except Exception:
        def_name = "System Default"
        def_desc = "Primary Active Adapter"
        def_ip = "Auto-detected"

    ifaces_list.append({
        "display_idx": 1,
        "name": f"Auto-detected Default ({def_name})",
        "description": f"{def_desc} [Recommended]",
        "ip": str(def_ip) if def_ip else "Auto",
        "scapy_iface": None
    })

    # 2. Add specific enumerated adapters
    try:
        raw_ifaces = conf.ifaces
        idx = 2
        for key, iface in raw_ifaces.items():
            name = getattr(iface, "name", str(key))
            desc = getattr(iface, "description", "")
            ip = getattr(iface, "ip", "")
            if not ip and hasattr(iface, "ips") and iface.ips:
                ip = iface.ips[0]
            ip_str = str(ip) if ip else "No IP Assigned"

            # Skip virtual WAN miniports that cannot sniff packets
            if "WAN Miniport" in desc:
                continue

            # Tag virtual interfaces for user clarity
            if "Hyper-V" in desc or "Virtual" in desc or "WSL" in name:
                desc = f"{desc} (Virtual / Isolated)"

            entry = {
                "display_idx": idx,
                "name": name,
                "description": desc,
                "ip": ip_str,
                "scapy_iface": iface
            }
            ifaces_list.append(entry)
            idx += 1

    except Exception:
        pass

    recommended_idx = 1
    return ifaces_list, recommended_idx


def start_capture(callback, iface=None, packet_filter="", count=0, stop_filter=None):
    """
    Start sniffing packets with Scapy.
    Uses timed micro-batches (timeout=0.5s) inside a loop so that on Windows,
    Python regularly regains the GIL and catches Ctrl+C (KeyboardInterrupt) instantly,
    even when capturing on completely idle interfaces with zero incoming packets.
    """
    try:
        if count > 0:
            # Fixed Count Mode with responsive timeout polling
            captured_count = 0

            def counting_callback(pkt):
                nonlocal captured_count
                captured_count += 1
                callback(pkt)

            while captured_count < count:
                remaining = count - captured_count
                sniff_kwargs = {
                    "prn": counting_callback,
                    "filter": packet_filter,
                    "count": remaining,
                    "store": False,
                    "timeout": 0.5
                }
                if iface is not None:
                    sniff_kwargs["iface"] = iface
                if stop_filter is not None:
                    sniff_kwargs["stop_filter"] = stop_filter

                sniff(**sniff_kwargs)
        else:
            # Continuous Capture Mode with responsive timeout polling
            while True:
                sniff_kwargs = {
                    "prn": callback,
                    "filter": packet_filter,
                    "count": 0,
                    "store": False,
                    "timeout": 0.5
                }
                if iface is not None:
                    sniff_kwargs["iface"] = iface
                if stop_filter is not None:
                    sniff_kwargs["stop_filter"] = stop_filter

                sniff(**sniff_kwargs)

    except KeyboardInterrupt:
        # Propagate KeyboardInterrupt cleanly to main.py
        raise KeyboardInterrupt
    except Scapy_Exception as e:
        raise RuntimeError(f"Scapy capture error: {e}")
    except PermissionError:
        raise PermissionError("Administrative privileges required to capture packets on raw sockets.")
    except Exception as e:
        raise RuntimeError(f"Network capture failed: {e}")