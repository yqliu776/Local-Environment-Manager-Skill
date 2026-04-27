<a id="english"></a>

# Local Environment Manager  Skill

[English](#english) | [中文](#zh-cn)

## English

This Codex skill records local development environment facts as reusable artifacts so later agents can read the snapshot first instead of rediscovering machine details.

### Key Capabilities

- Collect local environment facts from both user-provided hints and automatic detection.
- Generate `references/env.json` as the primary machine-readable snapshot for agents.
- Generate two human-readable documents from `env.json`:
  - `references/environment.en.md`
  - `references/environment.zh-CN.md`
- Provide a local validation script for the skill metadata and workflow.

### Workflow

1. Install or place the skill where Codex can discover it.
2. Initialize the local project environment with `uv sync`.
3. Ask the agent to collect or refresh the environment snapshot.
4. The agent should run `uv run scripts/collect_env.py --render-md` and pass any user-provided hints as script arguments.
5. The script writes `references/env.json`, then renders:
   - `references/environment.en.md`
   - `references/environment.zh-CN.md`
6. Later agents should read `references/env.json` first and only re-collect when the snapshot is stale or the user requests verification.

### How Users Can Provide Or Supplement Environment Information

Users can supplement environment information in direct conversation with the agent. If the user clearly says they have extra environment facts or restrictions to provide, the agent should invoke this skill and pass them as parameters instead of leaving them as unstructured chat context.

Typical user hints include:

- Workspace root
- Preferred global tool manager
- Preferred Python manager
- Preferred shell
- General environment notes
- Local rules
- Protected directories that must not be modified
- Protected files that must not be modified

Examples of user messages the agent should convert into parameters:

- `I have three environment facts to tell you: the workspace root is D:\Workspace, use uv for Python, and do not modify D:\Protected.`
- `Before you continue, record two local rules: do not edit .env files and do not touch the deployment scripts.`
- `Please collect my environment, and note that D:\Secrets and config\prod.yaml are protected.`

Recommended parameter mapping:

- `--workspace-root`
- `--global-manager`
- `--python-manager`
- `--primary-shell`
- `--note`
- `--rule`
- `--protected-path`
- `--protected-file`

### Interactive Prompt Language

When the agent chooses interactive collection instead of fully passing arguments:

- If the user is speaking English, the agent should pass `--language en`, and the script should prompt in English.
- If the user is speaking Chinese, the agent should pass `--language zh`, and the script should prompt in bilingual Chinese + English text.

Recommended examples:

```powershell
uv run scripts/collect_env.py --render-md --language en
uv run scripts/collect_env.py --render-md --language zh
```

For public repositories, generate a redacted snapshot:

```powershell
uv run scripts/collect_env.py --render-md --non-interactive --public
```

`--public` removes user-specific names and absolute local paths from the generated artifacts while keeping the high-level environment summary.

### Suggested Rules To Collect

The agent should actively capture operational boundaries when the user mentions them. Useful rules include:

- directories that must not be modified
- files that must not be modified
- package managers that should or should not be used
- network, proxy, mirror, or certificate requirements
- rules about system PATH, shell profile files, or global installs
- any local safety rule that should remain visible to later agents

### Directory Overview

- `SKILL.md`: skill instructions and trigger description
- `scripts/collect_env.py`: collect environment data and write `env.json`
- `scripts/render_environment_md.py`: render bilingual environment documents from `env.json`
- `scripts/validate_skill.py`: validate the current skill
- `references/env.json`: primary agent-facing environment snapshot
- `references/environment.en.md`: English environment document
- `references/environment.zh-CN.md`: Chinese environment document

### Notes

- Prefer running all skill-local scripts inside the project `uv` virtual environment.
- Regenerate `env.json` and the bilingual markdown documents after environment changes.
- Do not edit generated environment documents by hand; rebuild them from `env.json`.

<a id="zh-cn"></a>

## 本地环境管理

这个 Codex skill 用于把本地开发环境事实沉淀成可复用工件，让后续 agent 优先读取快照，而不是重复探测机器环境。

### 主要能力

- 收集本机环境信息，包括用户补充提示和自动探测结果。
- 生成 `references/env.json`，作为 agent 首选读取的机器可读环境快照。
- 基于 `env.json` 生成两份人类可读文档：
  - `references/environment.en.md`
  - `references/environment.zh-CN.md`
- 提供本地校验脚本，保证 skill 元数据和工作流可用。

### 工作流程

1. 将 skill 安装或放置到 Codex 可发现的位置。
2. 使用 `uv sync` 初始化本项目虚拟环境。
3. 让 agent 执行环境采集或刷新环境快照。
4. agent 应运行 `uv run scripts/collect_env.py --render-md`，并把用户明确提供的环境信息转成脚本参数传入。
5. 脚本会写入 `references/env.json`，再生成：
   - `references/environment.en.md`
   - `references/environment.zh-CN.md`
6. 后续 agent 应先读取 `references/env.json`；只有在快照过期、缺失或用户要求验证时才重新采集。

### 用户如何提示或补充环境信息

用户可以直接在和 agent 的对话中补充环境信息。只要用户明确表示“我有几项环境信息要补充”“我有几条本地规则要告知”“这些目录/文件禁止修改”等，agent 在调用本 skill 时就应把这些信息转成参数传给脚本，而不是只停留在自然语言上下文里。

常见可补充信息包括：

- 工作区根目录
- 首选全局工具管理器
- 首选 Python 管理器
- 首选 Shell
- 一般环境备注
- 本地规则
- 禁止修改的目录
- 禁止修改的文件

用户提示示例：

- `我有三项环境信息要告知：工作区根目录是 D:\Workspace，Python 一律用 uv，不要修改 D:\Protected。`
- `继续之前先记录两条规则：不要编辑 .env 文件，不要动部署脚本。`
- `请采集本机环境，并记住 D:\Secrets 和 config\prod.yaml 是受保护目标。`

建议映射到以下参数：

- `--workspace-root`
- `--global-manager`
- `--python-manager`
- `--primary-shell`
- `--note`
- `--rule`
- `--protected-path`
- `--protected-file`

### 交互式询问语言

如果 agent 选择交互式采集，而不是一次性把参数传完整：

- 当用户使用英文时，agent 应传入 `--language en`，脚本使用英文询问。
- 当用户使用中文时，agent 应传入 `--language zh`，脚本使用中英双语询问。

推荐示例：

```powershell
uv run scripts/collect_env.py --render-md --language en
uv run scripts/collect_env.py --render-md --language zh
```

如果要提交到公开仓库，建议生成脱敏快照：

```powershell
uv run scripts/collect_env.py --render-md --non-interactive --public
```

`--public` 会移除生成结果中的用户名和绝对本机路径，同时保留必要的环境摘要。

### 建议收集的规则项

当用户提到操作边界时，agent 应主动记录。常见规则包括：

- 哪些目录禁止修改
- 哪些文件禁止修改
- 应该或不应该使用哪些包管理器
- 网络、代理、镜像源、证书等要求
- 关于系统 PATH、shell 配置文件、全局安装的限制
- 任何需要让后续 agent 持续遵守的本地安全规则

### 目录说明

- `SKILL.md`: skill 说明和触发逻辑
- `scripts/collect_env.py`: 采集环境信息并生成 `env.json`
- `scripts/render_environment_md.py`: 从 `env.json` 生成双语环境文档
- `scripts/validate_skill.py`: 校验当前 skill
- `references/env.json`: agent 首选读取的环境快照
- `references/environment.en.md`: 英文环境文档
- `references/environment.zh-CN.md`: 中文环境文档

### 注意事项

- 本 skill 的本地脚本应优先在项目内 `uv` 虚拟环境执行。
- 环境发生变化后应重新生成 `env.json` 和双语文档。
- 不要手工编辑生成的环境文档，应从 `env.json` 重建。
