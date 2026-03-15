# openai-codex-multi-oauth

用于管理和排查 OpenClaw 中多个 OpenAI Codex OAuth 配置的 skill。

## 覆盖内容

- 多个 `openai-codex` OAuth 登录
- 相同邮箱但不同账号 / workspace 的处理
- profile 分配与选择
- soft-pin 自动切换语义
- 损坏 token 的恢复
- auth profile 持久化
- `/status` 与 usage 不一致的排查

## 仓库结构

- `SKILL.md` — skill 主说明
- `references/runtime-files.md` — 关键文件位置与分层说明
- `references/workflows.md` — 标准排障流程与回滚点
- `scripts/summarize_codex_profiles.py` — 快速检查脚本

## 快速开始

```bash
python3 scripts/summarize_codex_profiles.py
python3 scripts/summarize_codex_profiles.py --agent main --json
python3 scripts/summarize_codex_profiles.py --session-key 'agent:main:<channel>:<scope>:<id>'
```

这里的 session key 需要替换成你自己 `sessions.json` 里的真实值，不要默认写死 Telegram。

## 打包

可使用 OpenClaw 自带的 skill 打包脚本生成 `.skill` 文件。

## 说明

这个仓库应保持通用、可发布。不要把本机特例、密钥或本地事故记录直接放进仓库。
