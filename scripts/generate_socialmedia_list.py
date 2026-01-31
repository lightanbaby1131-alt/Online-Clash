import os
import requests

URLS = [
    "https://github.com/MetaCubeX/meta-rules-dat/raw/refs/heads/meta/geo/geosite/whatsapp.list",
    "https://github.com/MetaCubeX/meta-rules-dat/raw/refs/heads/meta/geo/geosite/facebook.list",
    "https://github.com/MetaCubeX/meta-rules-dat/raw/refs/heads/meta/geo/geosite/linkedin.list",
    "https://github.com/MetaCubeX/meta-rules-dat/raw/refs/heads/meta/geo/geosite/messenger.list",
    "https://github.com/MetaCubeX/meta-rules-dat/raw/refs/heads/meta/geo/geosite/pinterest.list",
]

def ensure_directories():
    dirs = [
        ".github/tmp",
        "Rule/list"
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

def fetch_and_merge():
    all_lines = set()
    for url in URLS:
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            lines = response.text.splitlines()
            for line in lines:
                line = line.strip()
                # 去掉空行和注释
                if line and not line.startswith("#"):
                    all_lines.add(line)
        except Exception as e:
            print(f"获取 {url} 失败: {e}")
    return sorted(all_lines)

def main():
    ensure_directories()

    merged_lines = fetch_and_merge()

    # 临时文件保存原始合并结果
    tmp_file = os.path.join(".github/tmp", "socialmedia_tmp.txt")
    with open(tmp_file, "w", encoding="utf-8") as f:
        f.write("\n".join(merged_lines))

    # 最终 list 文件（去掉注释和空行）
    list_file = os.path.join("Rule/list", "SocialMedia.list")
    with open(list_file, "w", encoding="utf-8") as f:
        f.write("\n".join(merged_lines))

    print(f"生成完成: {list_file}")

if __name__ == "__main__":
    main()
