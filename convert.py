import requests
import re

SOURCE_URL = "https://raw.githubusercontent.com/lingeringsound/10007_auto/master/all"
OUTPUT_FILE = "ad-smartdns.conf"

# 白名单：放行不拦截
EXCLUDE_KEYWORDS = [
    "umeng",
    "umsns",
    "123yunpan",
    "123yp",
    "yunpan.123"
]

# 要过滤的本地关键字
LOCAL_KEYWORDS = [
    "localhost",
    "ip6-localhost",
    "ip6-loopback",
    "hostname"
]

# 匹配纯IP
IP_REGEX = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$|^[0-9a-fA-F:]+$')

# 匹配合法域名
DOMAIN_REGEX = re.compile(r'^[a-zA-Z0-9_-]+\.[a-zA-Z0-9._-]+$')

def need_exclude(domain):
    d = domain.lower().strip()
    for kw in EXCLUDE_KEYWORDS + LOCAL_KEYWORDS:
        if kw in d:
            return True
    return False

def is_ip(s):
    return bool(IP_REGEX.match(s.strip()))

def is_valid_domain(s):
    return bool(DOMAIN_REGEX.match(s.strip()))

def main():
    resp = requests.get(SOURCE_URL, timeout=15)
    lines = resp.text.splitlines()
    out = []

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # 拆分：不管前面是0.0.0.0还是IP 域名，只拿最后一截当域名
        parts = line.split()
        domain = parts[-1]

        # 是IP直接跳过
        if is_ip(domain):
            continue

        # 不是合法域名跳过
        if not is_valid_domain(domain):
            continue

        # 白名单跳过
        if need_exclude(domain):
            continue

        # 标准格式，无空格
        out.append(f"address /{domain}/#")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(out))

if __name__ == "__main__":
    main()
