# -*- coding: utf-8 -*-
"""纯 Python 生成 docx（不依赖 lxml/python-docx），解析 Markdown 转 Word。"""
import re, zipfile, os, html

MD_PATH = r"D:\codearts_huawei\project_files\silver-guard\项目说明文档.md"
DOCX_PATH = r"D:\codearts_huawei\project_files\silver-guard\项目说明文档.docx"

# ---------- Markdown 解析 ----------
def parse_md(text):
    lines = text.replace("\r\n", "\n").split("\n")
    blocks = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        # 代码块
        if line.strip().startswith("```"):
            code_lines = []
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1
            blocks.append(("code", "\n".join(code_lines)))
            continue
        # 分隔线
        if re.match(r'^-{3,}$', line.strip()):
            blocks.append(("hr", None))
            i += 1
            continue
        # 标题
        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m:
            level = len(m.group(1))
            blocks.append(("h", level, m.group(2).strip()))
            i += 1
            continue
        # 表格
        if "|" in line and i + 1 < n and re.match(r'^[\s|:-]+$', lines[i+1]):
            table_lines = [line]
            i += 2
            while i < n and "|" in lines[i] and lines[i].strip():
                table_lines.append(lines[i])
                i += 1
            rows = []
            for tl in table_lines:
                cells = [c.strip() for c in tl.split("|")]
                cells = [c for c in cells if c != ""]
                rows.append(cells)
            blocks.append(("table", rows))
            continue
        # 引用
        if line.strip().startswith(">"):
            quote_lines = []
            while i < n and lines[i].strip().startswith(">"):
                quote_lines.append(lines[i].strip()[1:].strip())
                i += 1
            blocks.append(("quote", "\n".join(quote_lines)))
            continue
        # 无序列表
        if re.match(r'^[\s]*[-*+]\s+', line):
            list_items = []
            while i < n and re.match(r'^[\s]*[-*+]\s+', lines[i]):
                item = re.sub(r'^[\s]*[-*+]\s+', '', lines[i])
                list_items.append(item.strip())
                i += 1
            blocks.append(("ul", list_items))
            continue
        # 有序列表
        if re.match(r'^[\s]*\d+\.\s+', line):
            list_items = []
            while i < n and re.match(r'^[\s]*\d+\.\s+', lines[i]):
                item = re.sub(r'^[\s]*\d+\.\s+', '', lines[i])
                list_items.append(item.strip())
                i += 1
            blocks.append(("ol", list_items))
            continue
        # 空行
        if line.strip() == "":
            i += 1
            continue
        # 普通段落
        para_lines = [line]
        i += 1
        while i < n and lines[i].strip() != "" and not lines[i].strip().startswith(("#", "```", "-", "*", ">")) and "|" not in lines[i]:
            para_lines.append(lines[i])
            i += 1
        blocks.append(("p", " ".join(para_lines).strip()))
    return blocks

# ---------- 内联格式 ----------
def inline(text):
    """处理 **粗体**、`代码`、[链接](url)"""
    # 转义 XML
    text = html.escape(text)
    # 粗体
    text = re.sub(r'\*\*(.+?)\*\*', r'<w:b/><w:t xml:space="preserve">\1</w:t><w:b/>', text)
    # 行内代码
    text = re.sub(r'`(.+?)`', r'<w:rPr><w:rStyle w:val="CodeChar"/></w:rPr><w:t xml:space="preserve">\1</w:t>', text)
    return text

def run(text, bold=False, size=None, color=None):
    rpr = ""
    if bold:
        rpr += "<w:b/>"
    if size:
        rpr += f'<w:sz w:val="{size}"/>'
    if color:
        rpr += f'<w:color w:val="{color}"/>'
    rpr_xml = f"<w:rPr>{rpr}</w:rPr>" if rpr else ""
    return f'<w:r>{rpr_xml}<w:t xml:space="preserve">{html.escape(text)}</w:t></w:r>'

def para(text, style=None, align=None):
    ppr = ""
    if style:
        ppr += f'<w:pStyle w:val="{style}"/>'
    if align:
        ppr += f'<w:jc w:val="{align}"/>'
    ppr_xml = f"<w:pPr>{ppr}</w:pPr>" if ppr else ""
    return f'<w:p>{ppr_xml}{text}</w:p>'

# ---------- 生成 document.xml ----------
def build_document_xml(blocks):
    body = []
    for b in blocks:
        if b[0] == "h":
            _, level, text = b
            style = f"Heading{min(level, 4)}"
            body.append(para(run(text, bold=True), style=style))
        elif b[0] == "p":
            _, text = b
            # 处理粗体
            parts = re.split(r'(\*\*.+?\*\*)', text)
            runs = []
            for p in parts:
                if p.startswith("**") and p.endswith("**"):
                    runs.append(run(p[2:-2], bold=True))
                elif p:
                    runs.append(run(p))
            body.append(para("".join(runs)))
        elif b[0] == "ul":
            _, items = b
            for item in items:
                parts = re.split(r'(\*\*.+?\*\*)', item)
                runs = [run("• ", bold=True)]
                for p in parts:
                    if p.startswith("**") and p.endswith("**"):
                        runs.append(run(p[2:-2], bold=True))
                    elif p:
                        runs.append(run(p))
                body.append(para("".join(runs)))
        elif b[0] == "ol":
            _, items = b
            for idx, item in enumerate(items, 1):
                parts = re.split(r'(\*\*.+?\*\*)', item)
                runs = [run(f"{idx}. ", bold=True)]
                for p in parts:
                    if p.startswith("**") and p.endswith("**"):
                        runs.append(run(p[2:-2], bold=True))
                    elif p:
                        runs.append(run(p))
                body.append(para("".join(runs)))
        elif b[0] == "table":
            _, rows = b
            # 表格
            tbl = ['<w:tbl><w:tblPr><w:tblW w:w="5000" w:type="pct"/><w:tblBorders>']
            for edge in ["top", "left", "bottom", "right", "insideH", "insideV"]:
                tbl.append(f'<w:{edge} w:val="single" w:sz="4" w:color="D4A574"/>')
            tbl.append('</w:tblBorders></w:tblPr>')
            for ri, row in enumerate(rows):
                tbl.append('<w:tr>')
                for cell in row:
                    shading = '<w:shd w:val="clear" w:fill="FFF7ED"/>' if ri == 0 else ""
                    cell_runs = []
                    parts = re.split(r'(\*\*.+?\*\*)', cell)
                    for p in parts:
                        if p.startswith("**") and p.endswith("**"):
                            cell_runs.append(run(p[2:-2], bold=True, size=20 if ri == 0 else None))
                        elif p:
                            cell_runs.append(run(p, size=20 if ri == 0 else None))
                    tbl.append(f'<w:tc><w:tcPr><w:tcW w:w="0" w:type="auto"/>{shading}</w:tcPr>{para("".join(cell_runs))}</w:tc>')
                tbl.append('</w:tr>')
            tbl.append('</w:tbl>')
            body.append("".join(tbl))
            body.append(para(""))
        elif b[0] == "code":
            _, code = b
            for cl in code.split("\n"):
                body.append(para(run(cl, size=18), style="Code"))
        elif b[0] == "quote":
            _, text = b
            body.append(para(run(text, color="6B7280"), style="Quote"))
        elif b[0] == "hr":
            body.append('<w:p><w:pPr><w:pBdr><w:bottom w:val="single" w:sz="6" w:color="FED7AA"/></w:pBdr></w:pPr></w:p>')
    return "".join(body)

# ---------- docx 模板 ----------
CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''

RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

DOC_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''

STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Microsoft YaHei" w:eastAsia="Microsoft YaHei" w:hAnsi="Microsoft YaHei"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:rPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:pPr><w:spacing w:before="360" w:after="120"/></w:pPr><w:rPr><w:b/><w:color w:val="EA580C"/><w:sz w:val="36"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:pPr><w:spacing w:before="280" w:after="100"/></w:pPr><w:rPr><w:b/><w:color w:val="F97316"/><w:sz w:val="30"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:pPr><w:spacing w:before="240" w:after="80"/></w:pPr><w:rPr><w:b/><w:color w:val="C2410C"/><w:sz w:val="26"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading4"><w:name w:val="heading 4"/><w:pPr><w:spacing w:before="200" w:after="60"/></w:pPr><w:rPr><w:b/><w:color w:val="9A3412"/><w:sz w:val="24"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Code"><w:name w:val="Code"/><w:pPr><w:shd w:val="clear" w:fill="F5F5F5"/><w:spacing w:after="0"/></w:pPr><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:sz w:val="18"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Quote"><w:name w:val="Quote"/><w:pPr><w:ind w:left="480"/></w:pPr></w:style>
</w:styles>'''

def make_docx(md_text, out_path):
    blocks = parse_md(md_text)
    body = build_document_xml(blocks)
    document_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:body>{body}<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr></w:body>
</w:document>'''
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", RELS)
        z.writestr("word/_rels/document.xml.rels", DOC_RELS)
        z.writestr("word/styles.xml", STYLES)
        z.writestr("word/document.xml", document_xml)
    return out_path

if __name__ == "__main__":
    with open(MD_PATH, "r", encoding="utf-8") as f:
        md = f.read()
    p = make_docx(md, DOCX_PATH)
    print(f"OK: {p} ({os.path.getsize(p)} bytes)")
