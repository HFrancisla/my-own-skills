#!/usr/bin/env python3
"""Generate a self-contained, dependency-free HTML comparison page.

Usage:
    python3 make_comparison.py --manifest /path/to/variants.json --output /path/to/compare.html

The generated page has NO network dependencies. It can embed user-supplied
HTTP(S) previews, but does not fetch or upload anything by itself.
"""
from __future__ import annotations

import argparse
import html
import json
import os
from pathlib import Path
from urllib.parse import quote, urlparse


def normalize_src(source: str, manifest_dir: Path, output_dir: Path | None = None) -> str:
    """Allow HTTP(S) URLs and local paths; disallow script/data URLs."""
    if not isinstance(source, str) or not source.strip():
        raise ValueError("Each variant requires a nonempty src")
    source = source.strip()
    parsed = urlparse(source)
    if parsed.scheme in ("https", "http"):
        if not parsed.netloc:
            raise ValueError(f"Invalid HTTP(S) address: {source}")
        return source
    if parsed.scheme or source.startswith("//"):
        raise ValueError(f"Unsupported scheme: {source} (use relative path or http/https)")
    path = (manifest_dir / source).resolve()
    if not path.is_file():
        raise ValueError(f"Local preview file does not exist: {path}")
    if output_dir is not None:
        # Keep generated HTML portable after moving the entire folder/ZIP.
        try:
            relative = os.path.relpath(path, output_dir)
            return quote(Path(relative).as_posix(), safe="/.-_")
        except ValueError:  # Different drives on Windows.
            pass
    return path.as_uri()


def load_manifest(path: Path, output_dir: Path | None = None) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Manifest must be a JSON object")
    variants = data.get("variants")
    if not isinstance(variants, list) or len(variants) < 2 or len(variants) > 8:
        raise ValueError("Manifest variants must contain 2–8 items")
    cleaned = []
    for i, item in enumerate(variants, 1):
        if not isinstance(item, dict):
            raise ValueError(f"Variant {i} must be an object")
        kind = item.get("kind", "iframe")
        if kind not in ("iframe", "image"):
            raise ValueError(f"Variant {i}: kind must be iframe or image")
        name = item.get("name")
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"Variant {i}: name required")
        notes = item.get("notes", "")
        if not isinstance(notes, str):
            raise ValueError(f"Variant {i}: notes must be text")
        cleaned.append({
            "name": name.strip(), "notes": notes,
            "kind": kind, "src": normalize_src(item.get("src"), path.parent, output_dir)
        })
    return {
        "title": str(data.get("title") or "UI 方向对比"),
        "subtitle": str(data.get("subtitle") or "使用相同内容和视口进行比较。"),
        "variants": cleaned,
    }


def render_page(data: dict) -> str:
    # Encode data for a JS literal without allowing user-provided text to end a script tag.
    encoded = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    title = html.escape(data["title"])
    template = r'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>__TITLE__ · UI 方向比较</title>
<style>
:root{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;color-scheme:light;background:#f3f5f7;color:#17202b}
*{box-sizing:border-box}body{margin:0}.top{background:#fff;border-bottom:1px solid #d8dfe6;padding:20px clamp(16px,3vw,42px)}h1{font-size:clamp(20px,2.5vw,28px);margin:0 0 6px}p{margin:0;color:#53616e;line-height:1.5}
.controls{display:flex;align-items:center;flex-wrap:wrap;gap:12px;padding:16px clamp(16px,3vw,42px)}.group{display:flex;gap:5px;background:#e6eaf0;border-radius:8px;padding:4px}
button{border:0;border-radius:6px;padding:8px 13px;background:transparent;color:#17202b;font:inherit;cursor:pointer}button[aria-pressed="true"]{background:#fff;box-shadow:0 1px 3px #8693a04a;font-weight:700}button:focus-visible,a:focus-visible{outline:3px solid #265ed5;outline-offset:3px}
.cards{display:grid;grid-template-columns:repeat(var(--cols,2),minmax(0,1fr));gap:16px;padding:0 clamp(16px,3vw,42px) 36px}.card{background:#fff;border:1px solid #d4dbe4;border-radius:12px;min-width:0;overflow:hidden}.meta{padding:16px;border-bottom:1px solid #e2e7ed;display:flex;flex-direction:column;gap:7px}h2{font-size:17px;margin:0}.meta p{font-size:13px;min-height:20px}.preview-wrap{overflow:auto;background:#e8edf2;padding:12px;display:flex;justify-content:center;min-height:320px}
.preview{width:100%;height:640px;background:white;border:1px solid #bec9d5;border-radius:6px;object-fit:contain}.cards.mobile .preview{width:min(100%,390px);height:760px;flex-shrink:0}.cards.mobile .preview-wrap{align-items:flex-start}.card[hidden]{display:none}.choice{align-self:flex-start;border:1px solid #c5d0de;background:#eaf1fa;font-size:13px}.choice:hover{background:#dce9fc}.note{padding:0 3vw 25px;font-size:13px;color:#53616e}
@media(max-width:850px){.cards{grid-template-columns:minmax(0,1fr)}.preview{height:550px}}@media(prefers-reduced-motion:reduce){*,*:before,*:after{scroll-behavior:auto!important;animation:none!important}}
</style>
</head>
<body>
<header class="top"><h1 id="heading"></h1><p id="subtitle"></p></header>
<div class="controls">
  <span>目标视口：</span><div class="group" role="group" aria-label="目标视口">
    <button type="button" data-size="desktop" aria-pressed="true">桌面（自适应）</button>
    <button type="button" data-size="mobile" aria-pressed="false">手机（390px）</button>
  </div>
  <span>展示：</span><div class="group" role="group" aria-label="显示方案">
    <button type="button" data-show="all" aria-pressed="true">并排</button>
    <button type="button" data-show="one" aria-pressed="false">聚焦单个</button>
  </div>
  <label for="variantSelect">选定方向：</label><select id="variantSelect" aria-label="选择要聚焦的方案"></select>
  <button type="button" id="copySelection" title="复制选中方向与理由">复制所选方向</button><span id="copyStatus" role="status" aria-live="polite"></span>
</div>
<main class="cards" id="cards" aria-label="设计方向对比"></main>
<p class="note">每张卡可「选择此方向」；Alt + ← / → 切换。预览仅用于比较视觉和布局；本地 file:// 环境可能限制 iframe 中的部分脚本。该工具不上传内容，也不代替真实的交互验收。</p>
<script>
const data=__DATA__;
const cards=document.getElementById('cards');
const selector=document.getElementById('variantSelect');
let selected=0,show='all',size='desktop';
document.title=data.title+' · UI 方向比较';
document.getElementById('heading').textContent=data.title;
document.getElementById('subtitle').textContent=data.subtitle;
for(let i=0;i<data.variants.length;i++){
  const v=data.variants[i];
  const opt=document.createElement('option');opt.value=String(i);opt.textContent=v.name;selector.append(opt);
  const card=document.createElement('section');card.className='card';
  const meta=document.createElement('header');meta.className='meta';
  const heading=document.createElement('h2');heading.textContent=v.name;
  const note=document.createElement('p');note.textContent=v.notes;
  const link=document.createElement('a');link.href=v.src;link.target='_blank';link.rel='noopener noreferrer';link.textContent='打开原始预览';
  const choose=document.createElement('button'); choose.type='button'; choose.className='choice';choose.textContent='选择此方向';
  choose.addEventListener('click',()=>{selected=i;show='one';refresh();});
  meta.append(heading,note,link,choose);
  const frame=document.createElement('div');frame.className='preview-wrap';
  let media;
  if(v.kind==='image'){
    media=document.createElement('img');media.alt=v.name+' 设计截图';media.loading='lazy';
  }else{
    media=document.createElement('iframe');media.title=v.name+' 页面预览';media.loading='lazy';
  }
  media.className='preview';media.src=v.src;frame.append(media);
  card.append(meta,frame);cards.append(card);
}
function refresh(){
  cards.classList.toggle('mobile',size==='mobile');
  cards.style.setProperty('--cols',String(show==='one'?1:Math.min(3,data.variants.length)));
  [...cards.children].forEach((card,i)=>card.hidden=show==='one'&&i!==selected);
  document.querySelectorAll('[data-size]').forEach(btn=>btn.setAttribute('aria-pressed',String(btn.dataset.size===size)));
  document.querySelectorAll('[data-show]').forEach(btn=>btn.setAttribute('aria-pressed',String(btn.dataset.show===show)));
  selector.disabled=false;selector.value=String(selected);
}
document.querySelectorAll('[data-size]').forEach(btn=>btn.addEventListener('click',()=>{size=btn.dataset.size;refresh()}));
document.querySelectorAll('[data-show]').forEach(btn=>btn.addEventListener('click',()=>{show=btn.dataset.show;refresh()}));
selector.addEventListener('change',()=>{selected=Number(selector.value);show='one';refresh()});
const copyStatus=document.getElementById('copyStatus');
document.getElementById('copySelection').addEventListener('click',async()=>{
  const v=data.variants[selected];const summary='选中设计方向：'+v.name+'\n设计依据：'+v.notes;
  try{await navigator.clipboard.writeText(summary);copyStatus.textContent='已复制';}
  catch{copyStatus.textContent='无法写入剪贴板，请手动复制：'+summary;}
});
document.addEventListener('keydown',e=>{
  if(!e.altKey || !['ArrowLeft','ArrowRight'].includes(e.key) || /INPUT|TEXTAREA|SELECT/.test(document.activeElement?.tagName||''))return;
  e.preventDefault();selected=(selected+(e.key==='ArrowRight'?1:-1)+data.variants.length)%data.variants.length;show='one';refresh();
});
refresh();
</script>
</body>
</html>
'''
    return template.replace("__TITLE__", title).replace("__DATA__", encoded)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path, help="JSON manifest file")
    parser.add_argument("--output", required=True, type=Path, help="Output comparison HTML")
    args = parser.parse_args()
    manifest = args.manifest.resolve()
    output = args.output.resolve()
    data = load_manifest(manifest, output.parent)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_page(data), encoding="utf-8")
    print(f"Created: {output} ({len(data['variants'])} variants)")


if __name__ == "__main__":
    main()
