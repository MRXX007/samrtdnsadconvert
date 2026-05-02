import requests
import re

SOURCE_URL = "https://raw.githubusercontent.com/lingeringsound/10007_auto/master/all"
OUTPUT_FILE = "ad-smartdns.conf"

# 白名单关键词：含这些直接跳过不拦截
EXCLUDE_KEYWORDS = [
    "umsns"
]

# 匹配是否是 IPv4 / IPv6 纯IP
IP_REGEX = re.compile(
    r'^(?:(?:\d{1,3}\.){3}\d{1,3}|[0-9a-fA-F:]+)$'
)

def need_exclude(domain):
    d = domain.lower().strip()
    for kw in EXCLUDE_KEYWORDS:
        if kw in d:
            return True
    return False

def is_ip_address(s):
    s = s.strip()
    return bool(IP_REGEX.match(s))

def main():
    resp = requests.get(SOURCE_URL, timeout=15)
    resp.raise_for_status()
    lines = resp.text.splitlines()

    out = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        
        # 去掉开头 0.0.0.0 / 127.0.0.1 前缀
        if line.startswith("0.0.0.0") or line.startswith("127.0.0.1"):
            parts = line.split()
            if len(parts) >= 2:
                line = parts[1]
        
        # 过滤纯IP、内网、回环地址
        if is_ip_address(line):
            continue
        
        # 过滤本地域名标识
        if any(x in line.lower() for x in ["localhost", "ip6-loopback", "ip6-localhost", "hostname"]):
            continue
        
        # 自定义白名单域名
        if need_exclude(line):
            continue
        
        # 严格标准格式：无多余空格
        out.append(f"address /{line}/#")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(out))

if __name__ == "__main__":
    main()
