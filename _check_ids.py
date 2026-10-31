import re

with open(r'D:\codearts_huawei\project_files\silver-guard\index.html', 'r', encoding='utf-8-sig') as f:
    html = f.read()

# 提取所有 id="xxx" 的元素
defined_ids = set(re.findall(r'id="([^"]+)"', html))
# 提取所有 getElementById("xxx") 调用
used_ids = re.findall(r'getElementById\("([^"]+)"\)', html)

print("=== 定义的 ID ===")
for i in sorted(defined_ids):
    print(f"  {i}")

print("\n=== JS 中引用的 ID ===")
missing = []
for i in used_ids:
    if i not in defined_ids:
        missing.append(i)
        print(f"  ❌ {i} -- 不存在!")
    else:
        print(f"  ✓ {i}")

if missing:
    print(f"\n⚠️ 发现 {len(missing)} 个不存在的 ID 引用，会导致运行时错误!")
else:
    print("\n✅ 所有 ID 引用都存在，无运行时错误风险。")
