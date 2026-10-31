import re

with open(r'D:\codearts_huawei\project_files\silver-guard\index.html', 'r', encoding='utf-8-sig') as f:
    html = f.read()

# 提取所有 script 内容
scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
for i, s in enumerate(scripts):
    parens = s.count('(') - s.count(')')
    braces = s.count('{') - s.count('}')
    brackets = s.count('[') - s.count(']')
    print(f'Script {i}: parens={parens} braces={braces} brackets={brackets} len={len(s)}')

# 检查 HTML 标签
print(f'<div={html.count("<div")} </div>={html.count("</div>")}')
print(f'<script={html.count("<script")} </script>={html.count("</script>")}')

# 检查是否有中文标点在 JS 中
# 提取最后一个 script（主逻辑）
if scripts:
    main = scripts[-1]
    # 检查中文逗号、中文括号
    cn_comma = main.count('\uff0c')  # ，
    cn_paren_l = main.count('\uff08')  # （
    cn_paren_r = main.count('\uff09')  # ）
    cn_bracket_l = main.count('\u3010')  # 【
    cn_bracket_r = main.count('\u3011')  # 】
    print(f'Chinese commas in JS: {cn_comma}')
    print(f'Chinese parens in JS: ({cn_paren_l}, {cn_paren_r})')
    
    # 写入临时 js 文件用 node 检查
    with open(r'D:\codearts_huawei\project_files\silver-guard\_check.js', 'w', encoding='utf-8') as f:
        f.write(main)
    print('Wrote _check.js for node syntax check')
