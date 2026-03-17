# openai-codex-multi-oauth

用于管理和排查 OpenClaw 中多个 OpenAI Codex OAuth 配置的 skill。

## 人能直接关心的内容

这个仓库不是只给写代码的人看的，也适合 OpenClaw 的实际使用者 / 运维者看。

它主要帮你搞清楚这些问题：

- 当前聊天到底在用哪个 Codex profile
- 这个聊天是不是有自己单独 pin 住的 profile override
- 遇到 rate limit 之后 OpenClaw 有没有自动切换 profile
- `/status` 里的 usage 到底是不是你预期的那个 profile
- 为什么两个 profile 看起来很像，但其实应该分开

## 常见的用户侧命令 / 入口

下面这些是现实部署里很常见的入口；有的是 OpenClaw 内建，有的是某个部署自己加的 helper：

- `/status` —— 看当前聊天的模型、profile 语义和 usage 摘要
- `/codex_profile` —— 某些部署里会有，用来查看或切换当前聊天的 Codex profile
- `/codex_usage` —— 某些部署里会有，用来比较多个 profile 的 live usage

注意：`/codex_profile` 和 `/codex_usage` 不是每个 OpenClaw 安装都天然自带的。这份 skill 也会说明怎样正确实现和排查它们。

## 覆盖内容

- 多个 `openai-codex` OAuth 登录
- 相同邮箱但不同账号 / workspace 的处理
- profile 分配与选择
- auth order 与 session override 的排查
- helper / router 切换链路排查
- `/status` 与 usage 不一致的诊断
- 按 profile 直接拉取 live usage
- 同一 team workspace 下不同成员 usage 的排查
- 损坏 token 的恢复

## 支持的形态

它主要覆盖两类常见形态：

1. **原生 auth store 形态**
   - 多个 `openai-codex:*` profile 直接存在 `auth-profiles.json` 中
2. **外部 router 形态**
   - 另外维护一份 Codex OAuth profile 仓库，再由 helper/router 把选中的 profile 复制到运行时 active slot

这里提供的是可迁移的排查模式；路径、helper 名称和 router 细节请按你的实际部署调整。

## 仓库结构

- `openai-codex-multi-oauth/` — 真正的 skill 目录
- `openai-codex-multi-oauth/SKILL.md` — skill 主说明
- `openai-codex-multi-oauth/references/` — 参考资料
- `openai-codex-multi-oauth/scripts/` — 辅助脚本

## 典型使用场景

### 1）我想先看有哪些 profile

```bash
python3 scripts/summarize_codex_profiles.py
```

### 2）我想直接比较两个 profile 的 live usage

```bash
python3 scripts/codex_usage_report.py --profile secondary --profile tertiary
```

### 3）我觉得 `/status` 里显示的 profile 不对

这份 skill 会引导你检查：

- auth order
- session `authProfileOverride`
- active-slot routing
- usage 查询到底是 soft preference 还是 hard pin

### 4）我怀疑 OpenClaw 在 rate limit 之后自动切了 profile

这份 skill 会帮你区分：

- 用户手动选的是谁
- 当前聊天偏好的是谁
- runtime 在 failover 之后真正用的是谁

## 快速开始

```bash
cd openai-codex-multi-oauth
python3 scripts/summarize_codex_profiles.py
python3 scripts/summarize_codex_profiles.py --agent main --json
python3 scripts/summarize_codex_profiles.py --session-key 'agent:main:<channel>:<scope>:<id>'
python3 scripts/codex_usage_report.py
python3 scripts/codex_usage_report.py --profile secondary --profile tertiary
```

如果你的环境是外部 router 形态，可以按需传入路径：

```bash
python3 scripts/summarize_codex_profiles.py \
  --repo-path ~/.openclaw/codex-oauth-profiles.json \
  --helper-path ~/.openclaw/codex_profile \
  --router-path /path/to/workspace/scripts/codex_oauth_router.py
```

这里的 session key 需要替换成你自己 `sessions.json` 里的真实值。不同 channel、不同部署的 key 结构可能不同。

如果两个 profile 看起来像是同一份 usage，先比对 `user_id`、`account_id` 和 reset time，再判断是不是后端把额度合并了；同一个 team workspace 并不自动等于同一份 per-user usage bucket。

## 打包

打包时请从 skill 子目录执行，而不是从仓库根目录执行。

## 说明

仓库内容尽量保持在可复用的工作流、示例和诊断方法上；本地事故记录、密钥和一次性的机器补丁建议放在别处。
