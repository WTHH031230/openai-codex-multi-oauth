# openai-codex-multi-oauth

用于管理和排查 OpenClaw 中多个 OpenAI Codex OAuth 配置的 skill。

## 覆盖内容

- 多个 `openai-codex` OAuth 登录
- 相同邮箱但不同账号 / workspace 的处理
- profile 分配与选择
- auth order 与 session override 的排查
- helper / router 切换链路排查
- `/status` 与 usage 不一致的诊断
- 损坏 token 的恢复

## 支持的形态

这个仓库现在按“通用可发布”来维护。

它覆盖两类常见形态：

1. **原生 auth store 形态**
   - 多个 `openai-codex:*` profile 直接存在 `auth-profiles.json` 中
2. **外部 router 形态**
   - 另外维护一份 Codex OAuth profile 仓库，再由 helper/router 把选中的 profile 复制到运行时 active slot

这个 skill **不再假设**固定机器、用户名、workspace 路径，或某个特定 helper 实现。

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
```

如果你的环境是外部 router 形态，可以按需传入路径：

```bash
python3 scripts/summarize_codex_profiles.py \
  --repo-path ~/.openclaw/codex-oauth-profiles.json \
  --helper-path ~/.openclaw/codex_profile \
  --router-path /path/to/workspace/scripts/codex_oauth_router.py
```

这里的 session key 需要替换成你自己 `sessions.json` 里的真实值。不同 channel、不同部署的 key 结构可能不同。

## 打包

打包时请从 skill 子目录执行，而不是从仓库根目录执行。

## 说明

不要把本机特例、密钥或本地事故记录直接放进这个仓库。
