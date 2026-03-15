# openai-codex-multi-oauth

用于管理和排查 OpenClaw 中多个 OpenAI Codex OAuth 配置的 skill。

## 仓库结构

- `openai-codex-multi-oauth/` — 真正的 skill 目录
- `openai-codex-multi-oauth/SKILL.md` — skill 主说明
- `openai-codex-multi-oauth/references/` — 参考资料
- `openai-codex-multi-oauth/scripts/` — 辅助脚本

## 覆盖内容

- 多个 `openai-codex` OAuth 登录
- 相同邮箱但不同账号 / workspace 的处理
- profile 分配与选择
- soft-pin 自动切换语义
- 损坏 token 的恢复
- auth profile 持久化
- `/status` 与 usage 不一致的排查

## 快速开始

```bash
cd openai-codex-multi-oauth
python3 scripts/summarize_codex_profiles.py
python3 scripts/summarize_codex_profiles.py --agent main --json
python3 scripts/summarize_codex_profiles.py --session-key 'agent:main:<channel>:<scope>:<id>'
```

这里的 session key 需要替换成你自己 `sessions.json` 里的真实值。当前这套说明和示例**实际只在 Telegram 会话上验证过**；如果你在别的 channel 上使用，请以目标环境中的真实 session key 结构为准。

## 打包

打包时请从 skill 子目录执行，而不是从仓库根目录执行。

## 说明

这个仓库应保持通用、可发布。不要把本机特例、密钥或本地事故记录直接放进仓库。
