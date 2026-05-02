import requests

# 原始规则源
SOURCE_URL = "https://raw.githubusercontent.com/lingeringsound/10007_auto/master/all"
# 输出文件
OUTPUT_FILE = "ad-smartdns.conf"

# 需要排除不拦截的关键词（包含这些域名直接跳过）
EXCLUDE_KEYWORDS = [
    "umsns"
]

def need_exclude(domain):
    d = domain.lower().strip()
    for kw in EXCLUDE_KEYWORDS:
        if kw in d:
            return True
    return False

def main():
    resp = requests.get(SOURCE_URL, timeout=15)
    resp.raise_for_status()
    lines = resp.text.splitlines()

    out = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # 过滤白名单域名
        if need_exclude(line):
            continue
        # 转为 SmartDNS 格式
        out.append(f"address /{line}/ #")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(out))

if __name__ == "__main__":
    main()

