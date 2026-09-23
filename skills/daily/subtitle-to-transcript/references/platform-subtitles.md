# 在线视频字幕选择与下载

本说明只用于视频 URL；本地 SRT 直接进入主流程。

## 选择顺序

先运行 `yt-dlp --list-subs "<视频URL>"`，分别检查人工字幕和自动字幕区。列表不显示播放器针对当前用户设置的个人默认项；按下面规则选择一个最合适的轨道。下载指定的人工轨道时用 `--write-subs`，自动轨道用 `--write-auto-subs`。如果轨道类型不清楚，先试人工字幕，再试自动字幕。

- **YouTube：**省略 `--sub-langs` 使用 yt-dlp 默认语言选择（当前默认为英语）。默认轨道不可用时，优先选列表中的 `en`，没有时选第一条 `en.*` 英语轨道。列表若显示自动字幕，即使末尾同时写着 `has no subtitles`，仍按自动字幕轨道尝试下载；这条提示不能单独证明没有字幕。
- **Bilibili：**先选列表中第一条非 `danmaku` 人工字幕；没有人工字幕时选第一条非弹幕自动字幕，并使用其实际语言代码。默认轨道不可用时，回退到一条中文轨道，候选代码包括 `zh.*`、`ai-zh`。多条候选时只选一条，不合并多种语言。字幕列表可以显示 `danmaku` 供排除；所有下载命令都用 `--sub-langs "<实际语言代码>,-danmaku"` 排除弹幕。

## 下载

将 `<输出目录>` 替换为主流程确定的目录，将 `<语言参数>` 替换为选定轨道的语言参数。YouTube 默认选择时省略语言参数；Bilibili 或显式回退时使用准确的列表代码，例如 `--sub-langs "ai-zh,-danmaku"`。

```bash
yt-dlp --skip-download --write-subs \
  <语言参数> \
  --sub-format "srt/best" --convert-subs srt \
  -P "<输出目录>" -o "%(title)s.%(ext)s" "<视频URL>"
```

如果所选自动轨道未生成 SRT，将 `--write-subs` 替换为 `--write-auto-subs` 后重试。若所选人工轨道不可用，则改试自动轨道；若默认字幕仍未获取，再按平台规则回退到英语或中文。每次尝试只选择一条轨道。`--skip-download` 只取字幕，不下载视频；`--convert-subs srt` 请求将可转换格式保存为 SRT。

若列表中没有可用字幕，或下载命令失败，报告 yt-dlp 的具体结果并停止；不要把视频内容当作已取得的字幕。遇到登录或访问限制时，转到 [`platform-auth.md`](platform-auth.md)。

参考：[yt-dlp CLI 选项](https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/options.py)、[yt-dlp 字幕选择逻辑](https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/YoutubeDL.py)。
