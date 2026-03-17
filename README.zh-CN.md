# openai-codex-multi-oauth

用于管理和排查 OpenClaw 中多个 OpenAI Codex OAuth 配置的 skill。

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
