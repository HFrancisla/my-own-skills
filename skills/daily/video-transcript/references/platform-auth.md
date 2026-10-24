# 登录与访问受限

遇到登录、Cookie、验证码、年龄限制、私有视频、会员专享或反机器人验证时，暂停下载并告诉用户站点和 yt-dlp 的提示。请用户自行登录并完成验证；不索取密码、验证码或 Cookie 内容。

## Cookie 文件

只有用户确认 Cookie 文件已就绪并明确授权本次使用后，才读取或传给 yt-dlp。

- 导出目标站点专用的 Netscape 格式 Cookie 文件，只包含该站点需要的域名。
- 保存到本 skill 的 `auth/` 目录（`<skill目录>/auth/`）：Bilibili 使用 `bilibili.cookies.txt`，YouTube 使用 `youtube.cookies.txt`。
- [`../auth/cookies.example.txt`](../auth/cookies.example.txt) 只展示格式，示例值不可认证；不要手工猜填 Cookie。
- Chrome 可按 [yt-dlp FAQ](https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp) 导出。使用扩展时确认是 `Get cookies.txt LOCALLY`，并只导出当前站点。

用户确认授权后，使用 `--cookies` 参数传入 Cookie 文件，先检查字幕轨道，再下载字幕：

```bash
# 检查轨道
yt-dlp --cookies "<skill目录>/auth/<站点>.cookies.txt" --list-subs "<视频URL>"

# 下载字幕（结合 platform-subtitles.md 的参数）
yt-dlp --cookies "<skill目录>/auth/<站点>.cookies.txt" --skip-download --write-subs \
  <语言参数> \
  --sub-format "srt/best" --convert-subs srt \
  -P "<输出目录>" -o "%(title)s.%(ext)s" "<视频URL>"
```

命令保持 `--skip-download`，并遵循 [`platform-subtitles.md`](platform-subtitles.md) 的语言选择。Cookie 无法读取或访问仍被拒绝时，停止并报告结果，不重复试探或绕过限制。

## 安全与系统环境

所有系统统一使用 `auth/` 下的 Netscape 文件。

- **权限保护**：将权限限制为当前用户可读写，例如 `chmod 600 "<skill目录>/auth/<站点>.cookies.txt"`。
- **防止泄露**：根目录与 `auth/.gitignore` 均已忽略 `*.cookies.txt`；严禁打印、记录或向终端粘贴 Cookie 内容。

## 站点提示

- **Bilibili：**`Subtitles are only available when logged in` 或仅列出 `danmaku` 时，登录可能会解锁普通及 AI 字幕。用户确认授权后重新运行 `--list-subs`，下载时排除 `danmaku`。仍无普通字幕时停止并报告。
- **YouTube：**私人、年龄限制、会员内容及 `Sign in to confirm` 等提示可能需要登录。用户确认授权后使用 `auth/youtube.cookies.txt` 重试。Cookie 无效或验证未通过时停止。避免频繁重复带登录态的请求。

更多说明：[yt-dlp Cookie 参数](https://github.com/yt-dlp/yt-dlp#filesystem-options)、[yt-dlp YouTube Cookie 指引](https://github.com/yt-dlp/yt-dlp/wiki/Extractors#exporting-youtube-cookies)。
