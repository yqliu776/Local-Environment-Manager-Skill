# 本地开发环境

此文档面向人类阅读。Agent 应优先读取 `env.json`。

## 快照

- 生成时间: `2026-04-27T16:23:24.306434+00:00`
- 工作区根目录: `E:\VibeCoding`
- 操作系统: `Windows 11`
- Shell: `PowerShell`
- 用户名: `10264`

## 管理约定

- 首选全局工具管理器: `Scoop`
- 首选 Python 管理器: `uv`

## 环境备注

- 优先复用现有全局工具，不要额外引入新的系统级管理器。
- 执行机器级变更前先读取 env.json。

## 规则与受保护目标

- 规则:
- 无
- 禁止修改的目录:
- 无
- 禁止修改的文件:
- 无

## Python

- 默认 Python: `3.12.11`
- 已安装版本:
- `3.8.20`
- `3.10.20`
- `3.12.11`

## PATH

- 首选 Python shim 路径: `C:\Users\10264\.local\bin`
- PATH 前若干项:
- `C:\Users\10264\.codex\tmp\arg0\codex-arg0Dw6PXu`
- `D:\Apps\Scoop\persist\nvm\nodejs\v22.21.1\node_modules\@openai\codex\node_modules\@openai\codex-win32-x64\vendor\x86_64-pc-windows-msvc\path`
- `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8\bin`
- `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8\libnvvp`
- `C:\WINDOWS\system32`
- `C:\WINDOWS`
- `C:\WINDOWS\System32\Wbem`
- `C:\WINDOWS\System32\WindowsPowerShell\v1.0\`
- `C:\WINDOWS\System32\OpenSSH\`
- `C:\Program Files\NVIDIA Corporation\NVIDIA App\NvDLISR`
- `C:\Program Files (x86)\NVIDIA Corporation\PhysX\Common`
- `C:\Program Files\NVIDIA Corporation\Nsight Compute 2025.1.1\`

## WSL

- 已知发行版:
- 无

## Docker Desktop

- WSL 数据根目录: `E:\DockerDesktop\DockerDesktopWSL`

## Agent 提示摘要

- 在做机器级假设之前，请先读取此 `env.json`。
- 机器概况：Windows，PowerShell。优先使用现有全局工具管理器：Scoop。Python 版本管理优先使用 uv。已知 Python 版本：3.8.20, 3.10.20, 3.12.11。PATH 应优先包含 C:\Users\10264\.local\bin，并放在 WindowsApps 之前。
- 优先复用已记录的管理器和工具链，不要随意引入新的全局工具。
- 遵守已记录的禁止修改目录、禁止修改文件和本地规则。
- 只有在请求确实需要最新验证或涉及机器级变更时，才探测真实系统。
- 环境发生变化后要刷新 `env.json`，避免后续 agent 重复发现同样的信息。

## 检测到的工具

- git: git version 2.49.0.windows.1
- uv: uv 0.11.7 (9d177269e 2026-04-15 x86_64-pc-windows-msvc)
- python: C:\Users\10264\.local\bin\python.CMD
- python3.12: Python 3.12.11
- python3.10: Python 3.10.20
- python3.8: Python 3.8.20
- node: v22.21.1
- npm: 11.13.0
- docker: Docker version 29.4.0, build 9d7ad9f
- wsl: WSL 2.5.7.0
- scoop: D:\Apps\Scoop\shims\scoop.CMD
- winget: C:\Users\10264\AppData\Local\Microsoft\WindowsApps\winget.EXE
