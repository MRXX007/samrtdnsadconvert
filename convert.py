import requests
import re

SOURCE_URL = "https://raw.githubusercontent.com/lingeringsound/10007_auto/master/all"
OUTPUT_FILE = "ad-smartdns.conf"

# 自定义白名单：不拦截
EXCLUDE_KEYWORDS = [
    "umsns"
]

# 本地关键字直接过滤
LOCAL_KEYWORDS = [
    "localhost",
    "ip6-localhost",
    "ip6-loopback",
    "hostname"
]

# 严格匹配纯IP、IPv6
IP_REGEX = re.compile(
    r'^(\d{1,3}\.){3}\d{1,3}$|^[0-9a-fA-F:]+$'
)

def need_exclude(domain):
    d = domain.lower().strip()
    for kw in EXCLUDE_KEYWORDS + LOCAL_KEYWORDS:
        if kw in d:
            return True
    return False

def is_ip_or_ipv6(s):
    return bool(IP_REGEX.match(s.strip()))

def main():
    resp = requests.get(SOURCE_URL, timeout=15)
    lines = resp.text.splitlines()
    out = []

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        
        # 整行有空格 直接丢弃
        if " " in line:
            continue
        
        # 剥离 0.0.0.0 / 127.0.0.1 前缀
        if line.startswith(("0.0.0.0", "127.0.0.1")):
            parts = line.split()
            if len(parts) >= 2:
                line = parts[1]

        # 是IP/IPv6 直接跳过
        if is_ip_or_ipv6(line):
            continue
        
        # 白名单跳过
        if need_exclude(line):
            continue
        
        # 标准格式 无空格
        out.append(f"address /{line}/#")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(out))

if __name__ == "__main__":
    main()
