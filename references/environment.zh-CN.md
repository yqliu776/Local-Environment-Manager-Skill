# 本地开发环境

此文档面向人类阅读。Agent 应优先读取 `env.json`。

## 快照

- 生成时间: `2026-04-28T01:03:13.225755+00:00`
- 工作区根目录: `<workspace-root>`
- 操作系统: `Windows 11`
- Shell: `PowerShell`
- 用户名: `local-user`

## 管理约定

- 首选全局工具管理器: `Winget`
- 首选 Python 管理器: `uv`

## 环境备注

- 无

## 规则与受保护目标

- 规则:
- 无
- 禁止修改的目录:
- 无
- 禁止修改的文件:
- 无

## Python

- 默认 Python: `3.12.8`
- 已安装版本:
- 无

## PATH

- 首选 Python shim 路径: `未知`
- PATH 前若干项:
- `%PROGRAMFILES% (x86)\PowerShell\7`
- `<redacted-path>`
- `<codex-vendor-path>`
- `%PROGRAMFILES% (x86)\Common Files\Oracle\Java\java8path`
- `%PROGRAMFILES% (x86)\Common Files\Oracle\Java\javapath`
- `%SYSTEMROOT%\system32`
- `%SYSTEMROOT%`
- `%SYSTEMROOT%\System32\Wbem`
- `%SYSTEMROOT%\System32\WindowsPowerShell\v1.0\`
- `%SYSTEMROOT%\System32\OpenSSH\`
- `%PROGRAMFILES%\dotnet\`

## WSL

- 已知发行版:
- 无

## Docker Desktop

- WSL 数据根目录: `<docker-desktop-wsl-root>`

## Agent 提示摘要

- 在做机器级假设之前，请先读取此 `env.json`。
- 机器概况：Windows，PowerShell。优先使用现有全局工具管理器：Winget。Python 版本管理优先使用 uv。
- 优先复用已记录的管理器和工具链，不要随意引入新的全局工具。
- 遵守已记录的禁止修改目录、禁止修改文件和本地规则。
- 只有在请求确实需要最新验证或涉及机器级变更时，才探测真实系统。
- 环境发生变化后要刷新 `env.json`，避免后续 agent 重复发现同样的信息。

## 检测到的工具

- git: git version 2.47.1.windows.2
- uv: <redacted-path>
- python: <redacted-path>
- python3.12: <redacted-path>
- python3.8: <redacted-path>
- node: v22.17.0
- npm: 11.11.0
- pnpm: 8.15.4
- docker: Docker version 28.0.1, build 068a01e
- wsl: WSL 2.4.10.0
- winget: %LOCALAPPDATA%\Microsoft\WindowsApps\winget.EXE
