# OpenAI Codex Multi OAuth

Manage and debug multiple Codex OAuth profiles in OpenClaw.

这个仓库是给 **OpenClaw 的实际使用者 / 运维者** 看的，不只是给读源码的人看的。

它主要解决的是这些很常见、但很容易搞混的问题：当前聊天到底在用哪个 Codex profile、为什么 usage 看起来不对、OpenClaw 有没有在 rate limit 后自动切 profile、两个 profile 看起来一样到底是后端问题还是本地取错了 token。

## 这个仓库能帮你做什么

如果你想解决下面这些问题，这个仓库就是给你的：

- 在一个 OpenClaw 环境里管理多个 Codex 账号 / 身份
- 搞清楚当前聊天真正使用的是哪个 profile
- 排查 `/status` 里的 usage 为什么和预期不一致
- 直接比较不同 profile 的 live usage
- 判断两个 profile 到底是不是独立的，还是只是“看起来很像”
- 排查 `/codex_profile`、`/codex_usage` 这类 helper 命令
- 理解 rate limit、坏 token、cooldown 之后的自动切换 / failover

## 你在 OpenClaw 里通常会看到什么

不同部署里，常见的人类可见入口通常有这些：

| 入口 | 用途 |
| --- | --- |
| `/status` | 看当前聊天的模型、profile 语义和 usage 摘要 |
| `/codex_profile` | 某些部署里有，用来查看或切换当前聊天的 Codex profile |
| `/codex_usage` | 某些部署里有，用来比较多个 Codex profile 的 live usage |
| 自动 profile 切换 / failover | 遇到 rate limit、token 故障或 cooldown 逻辑时，OpenClaw 可能自动换 profile |

注意：

- `/status` 是正常的 OpenClaw 使用面。
- `/codex_profile` 和 `/codex_usage` 是**常见部署模式**，不是每个安装都天然自带。
- 这个仓库既会解释这些入口怎么用，也会解释它们应该怎样实现才不会误导人。

## 这个仓库回答的典型问题

- “为什么这个聊天突然用了错误的 Codex 账号？”
- “为什么 `/status` 显示的是一个 profile，但 usage 看起来像另一个？”
- “OpenClaw 是不是在 rate limit 之后自动切 profile 了？”
- “这两个 profile 看起来一样，到底是真的共享额度，还是本地代码取错 token 了？”
- “`/codex_profile` 或 `/codex_usage` 应该怎样实现，用户看到的才是对的？”

## 快速开始

### 1）先看当前有哪些 profile

```bash
python3 scripts/summarize_codex_profiles.py
```

### 2）直接比较两个 profile 的 live usage

```bash
python3 scripts/codex_usage_report.py --profile secondary --profile tertiary
```

### 3）导出机器可读状态

```bash
python3 scripts/summarize_codex_profiles.py --agent main --json
```

## 常见使用场景

### 先判断问题属于“选错 profile”“usage 取错”还是“展示错了”

先跑：

```bash
python3 scripts/summarize_codex_profiles.py
python3 scripts/codex_usage_report.py
```

第一个脚本看本地状态、auth order、session override。
第二个脚本直接按每个 profile 的 credential 去拉 live usage。

### 排查 `/status` 里 profile 不对

重点看：

- auth order
- 当前聊天的 `authProfileOverride`
- 如果是 external router 形态，active slot 是怎么同步的
- usage 查询到底是 hard-pin 住了目标 profile，还是只是 soft preference

### 排查“两个 profile 的 usage 看起来一样”

重点比较：

- `user_id`
- `account_id`
- `email`
- reset time

如果 `account_id` 一样但 `user_id` 不一样，那它们很可能只是处在同一个 team workspace，但仍然是不同用户。

## 为什么需要这个仓库

OpenClaw 里跟 Codex profile 相关的状态，通常不止一层：

- 存储的偏好
- auth order
- 某个聊天自己的 override
- runtime 真正使用的 profile
- usage 查询使用的 credential
- UI 最后展示给人的 label

很多看起来“很玄学”的 bug，本质上都是把这几层混在一起了。

这个仓库的目标，就是把这些层次拆开，让它们变得可见、可解释。

## 仓库结构

- `openai-codex-multi-oauth/` —— 真正的 skill 目录
- `openai-codex-multi-oauth/SKILL.md` —— 给 agent 用的主说明
- `openai-codex-multi-oauth/references/` —— 更细的参考资料和工作流
- `openai-codex-multi-oauth/scripts/` —— 可复用的诊断脚本

如果你是人类使用者 / 运维者，先看这个 README。
如果你是把它接进 agent 工作流，去看 `openai-codex-multi-oauth/SKILL.md`。

## 示例命令

```bash
# 看 profile 和最近 session
python3 scripts/summarize_codex_profiles.py

# 看一个指定 profile 的 usage
python3 scripts/codex_usage_report.py --profile tertiary

# 直接比较两个 profile
python3 scripts/codex_usage_report.py --profile quaternary --profile quinary

# 检查某个特定 session key
python3 scripts/summarize_codex_profiles.py --session-key 'agent:main:<channel>:<scope>:<id>'
```

如果你是 external-router 形态，可以按需传路径：

```bash
python3 scripts/summarize_codex_profiles.py \
  --repo-path ~/.openclaw/codex-oauth-profiles.json \
  --helper-path ~/.openclaw/codex_profile \
  --router-path /path/to/workspace/scripts/codex_oauth_router.py
```

## 迁移到自己环境时要注意

- session key 的格式会因 channel 和部署方式不同而不同
- helper 命令名字会因部署不同而不同
- 有些环境直接把所有 profile 放在 auth store 里
- 有些环境会另外维护一份 profile repo，再把选中的 profile 复制到 active slot

这里给的是可迁移的模式，你需要按自己的部署去套。

## 打包

打包时请从 skill 子目录执行，而不是从仓库根目录执行。

## 仓库边界

这个仓库只放可复用的工作流、解释和脚本。
不要把密钥、事故日志、或者一次性的本机补丁放进来。
