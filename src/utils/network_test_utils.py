import subprocess
import re

def run_ping(host: str = "8.8.8.8", count: int = 10):
    """
    Verilen host’a ping atar, avg RTT (ms) ve packet loss (%) döner.
    """
    try:
        proc = subprocess.run(
            ["ping", "-c", str(count), host],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=20
        )
        out = proc.stdout
        loss = re.search(r"(\d+)% packet loss", out)
        rtt = re.search(r"rtt min/avg/max/mdev = [\d\.]+/([\d\.]+)/", out)
        return (rtt.group(1) if rtt else "N/A",
                loss.group(1) if loss else "N/A")
    except Exception:
        return ("N/A", "N/A")

def run_iperf(host: str = "127.0.0.1", duration: int = 5):
    """
    iperf3 ile host’a band genişliği testi yapar, 'XX Mbits/sec' döner.
    """
    try:
        proc = subprocess.run(
            ["iperf3", "-c", host, "-t", str(duration)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=duration + 5
        )
        out = proc.stdout.splitlines()
        for line in reversed(out):
            if "receiver" in line:
                parts = line.split()
                return parts[-2] + " " + parts[-1]
        return "N/A"
    except Exception:
        return "N/A"
