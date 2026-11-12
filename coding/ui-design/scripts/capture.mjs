#!/usr/bin/env node
/**
 * Optional screenshot capture using the free, open-source Playwright package.
 * This utility never installs dependencies or launches remote services.
 * Use local project dependencies: npm install -D playwright && npx playwright install chromium
 * Or use a browser/screenshot capability already provided by your agent.
 *
 * Usage: node scripts/capture.mjs --url http://127.0.0.1:3000 --output ./evidence/desktop.png --width 1440 --height 900
 */
import { writeFile, mkdir } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { createRequire } from 'node:module';

const HELP = `免费 Playwright 截图工具（需提前安装本地 playwright 与 Chromium）

用法：
 node scripts/capture.mjs --url http://127.0.0.1:3000 --output ./evidence/desktop.png [选项]

选项：
 --url URL             目标页面（仅支持 http://、https:// 或 file://）
 --output FILE         输出 PNG 文件路径
 --width INT           视口宽度，默认 1440
 --height INT          视口高度，默认 900
 --full-page           捕获全页；默认只截当前视口
 --wait-for SELECTOR   等待指定 CSS 元素可见；不任意休眠
 --timeout INT         等待上限，默认 15000ms（1000–120000）
 --device-scale INT    截图像素比，默认 1（1–3）
 --help                显示帮助

注意：脚本只负责客观取证，不声称截图已被看过，也不自动评判页面。
`; 

function parse(args) {
  const out = { width:1440, height:900, timeout:15000, deviceScale:1, fullPage:false };
  const names = new Set(['--url','--output','--width','--height','--wait-for','--timeout','--device-scale']);
  for(let i=0;i<args.length;i++) {
    const key=args[i];
    if (key==='--help' || key==='-h') return { help:true };
    if (key==='--full-page') { out.fullPage=true; continue; }
    if (!names.has(key)) throw new Error(`未知参数：${key}`);
    const value=args[++i];
    if (!value || value.startsWith('--')) throw new Error(`${key} 缺少值`);
    switch(key) {
      case '--url': out.url=value; break;
      case '--output': out.output=value; break;
      case '--wait-for': out.waitFor=value; break;
      case '--width': out.width=Number(value); break;
      case '--height': out.height=Number(value); break;
      case '--timeout': out.timeout=Number(value); break;
      case '--device-scale': out.deviceScale=Number(value); break;
    }
  }
  if (!out.url || !out.output) throw new Error('必须指定 --url 和 --output');
  if (!/^https?:\/\//i.test(out.url) && !/^file:\/\//i.test(out.url)) throw new Error('不支持的 URL 方案，仅允许 HTTP(S) 或 file://');
  for(const [name,value,low,high] of [['width',out.width,240,3840],['height',out.height,320,4000],['timeout',out.timeout,1000,120000],['deviceScale',out.deviceScale,1,3]]) {
    if (!Number.isInteger(value) || value<low || value>high) throw new Error(`${name} 必须是 ${low}–${high} 的整数`);
  }
  if (!out.output.toLowerCase().endsWith('.png')) throw new Error('输出文件需要 .png 扩展名');
  return out;
}

async function main() {
  let options;
  try { options=parse(process.argv.slice(2)); }
  catch(err) { console.error(String(err.message)); console.error('运行 --help 查看选项'); process.exitCode=2; return; }
  if(options.help){ console.log(HELP); return; }

  let chromium;
  // Resolve Playwright from the active project first, rather than the Skill's own folder.
  try { ({ chromium } = createRequire(resolve(process.cwd(), 'package.json'))('playwright')); }
  catch {
    try { ({ chromium } = await import('playwright')); }
    catch {
      console.error('没有找到项目或 Skill 可用的 Playwright。请先征得用户同意再安装依赖，或使用宿主浏览器取证。');
      process.exitCode=3; return;
    }
  }
  const browser = await chromium.launch({ headless:true });
  try {
    const page = await browser.newPage({viewport:{width:options.width,height:options.height},deviceScaleFactor:options.deviceScale,reduceMotion:'reduce'});
    await page.goto(options.url, { waitUntil:'domcontentloaded',timeout:options.timeout });
    if(options.waitFor) await page.locator(options.waitFor).first().waitFor({state:'visible',timeout:options.timeout});
    await page.evaluate(async()=>document.fonts?.ready);
    const output=resolve(options.output);
    await mkdir(dirname(output),{recursive:true});
    await page.screenshot({path:output,fullPage:options.fullPage,animations:'disabled'});
    // Do not save tokens that might be present in query/fragment into evidence metadata.
    const safeUrl = new URL(page.url()); safeUrl.search=''; safeUrl.hash='';
    const details={url:safeUrl.toString(),viewport:{width:options.width,height:options.height},deviceScaleFactor:options.deviceScale,fullPage:options.fullPage,selector:options.waitFor||null,output,accessedAt:new Date().toISOString(),claim:'Capture only; visual and interaction review not performed by this tool.'};
    await writeFile(output.replace(/\.png$/i,'.json'),JSON.stringify(details,null,2)+'\n');
    console.log(`截图已保存：${output}`);
    console.log('需由有视觉能力的评审者实际查看截图，截图成功≠视觉评审通过。');
  } finally { await browser.close(); }
}

main().catch((err)=>{console.error(err);process.exitCode=1});
