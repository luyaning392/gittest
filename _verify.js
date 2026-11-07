/**
 * 前端内联脚本语法校验基线
 * 用途：抽取 HTML 中每个 <script> 块并用 Node vm.Script 编译，
 *       编译失败即输出错误并非零退出码（防止"解析期失败导致识别入口永久失效"回归）。
 * 用法：node _verify.js [html文件...]  默认检查独立前端入口 index.html
 */
const fs = require("fs");
const vm = require("vm");

const targets = process.argv.slice(2);
const files = targets.length ? targets : ["index.html"];

let failed = false;

for (const f of files) {
  if (!fs.existsSync(f)) {
    console.log("[跳过] 文件不存在: " + f);
    continue;
  }
  const src = fs.readFileSync(f, "utf8");
  const blocks = src.match(/<script\b[^>]*>[\s\S]*?<\/script>/gi) || [];
  console.log("[检查] " + f + " 共 " + blocks.length + " 个 <script> 块");

  blocks.forEach(function (block, i) {
    const inner = block
      .replace(/^<script\b[^>]*>/i, "")
      .replace(/<\/script>\s*$/i, "");
    const lineOffset = src.slice(0, src.indexOf(block)).split(/\r?\n/).length - 1;
    try {
      new vm.Script(inner, { filename: f + "#block" + i });
      console.log("  块 #" + i + " 语法检查通过");
    } catch (e) {
      failed = true;
      const baseLine = lineOffset + (e.lineNumber || 0);
      console.log("  块 #" + i + " 语法错误: " + e.message + " (约第 " + baseLine + " 行)");
    }
  });
}

if (failed) {
  console.log("语法检查失败");
  process.exit(1);
}
console.log("语法检查通过");