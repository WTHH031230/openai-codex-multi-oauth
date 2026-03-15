#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path):
    if not path.exists():
        return None
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def default_paths(state_dir: Path, agent: str):
    return {
        'saved': state_dir / 'codex_profile_id',
        'auth': state_dir / 'agents' / agent / 'agent' / 'auth-profiles.json',
        'sessions': state_dir / 'agents' / agent / 'sessions' / 'sessions.json',
    }


def summarize(state_dir: Path, agent: str, session_key: str | None):
    paths = default_paths(state_dir, agent)
    auth = load_json(paths['auth']) or {}
    sessions = load_json(paths['sessions']) or {}
    profiles = auth.get('profiles') or {}
    order = ((auth.get('order') or {}).get('openai-codex') or [])
    saved_profile = paths['saved'].read_text(encoding='utf-8').strip() if paths['saved'].exists() else None

    codex_profiles: list[dict[str, Any]] = []
    for pid, cred in sorted(profiles.items()):
        if not str(pid).startswith('openai-codex:'):
            continue
        token_state = None
        token = cred.get('access') or cred.get('token')
        if isinstance(token, str):
            if token.startswith('eyJ'):
                token_state = 'jwt-like'
            elif token:
                token_state = 'non-jwt'
        codex_profiles.append({
            'profileId': pid,
            'type': cred.get('type'),
            'accountId': cred.get('accountId'),
            'email': cred.get('email'),
            'expires': cred.get('expires'),
            'tokenState': token_state,
            'lastGood': cred.get('lastGood'),
        })

    session = None
    if session_key:
        entry = sessions.get(session_key)
        if entry:
            session = {
                'key': session_key,
                'modelProvider': entry.get('modelProvider'),
                'model': entry.get('model'),
                'authProfileOverride': entry.get('authProfileOverride'),
                'authProfileOverrideSource': entry.get('authProfileOverrideSource'),
            }

    return {
        'stateDir': str(state_dir),
        'agent': agent,
        'savedProfile': saved_profile,
        'authOrder': order,
        'profiles': codex_profiles,
        'session': session,
        'paths': {k: str(v) for k, v in paths.items()},
    }


def print_human(summary: dict[str, Any]):
    print(f"state_dir: {summary['stateDir']}")
    print(f"agent: {summary['agent']}")
    print(f"saved_profile: {summary['savedProfile'] or '<missing>'}")
    print('auth_order:', ', '.join(summary['authOrder']) if summary['authOrder'] else '<none>')
    print('profiles:')
    if not summary['profiles']:
        print('  <none>')
    for item in summary['profiles']:
        print(
            '  - '
            f"{item['profileId']} | "
            f"type={item['type'] or '-'} | "
            f"accountId={item['accountId'] or '-'} | "
            f"email={item['email'] or '-'} | "
            f"expires={item['expires'] or '-'} | "
            f"token={item['tokenState'] or '-'} | "
            f"lastGood={item['lastGood'] or '-'}"
        )
    if summary['session']:
        s = summary['session']
        print('session:')
        print(f"  key: {s['key']}")
        print(f"  modelProvider: {s['modelProvider'] or '-'}")
        print(f"  model: {s['model'] or '-'}")
        print(f"  authProfileOverride: {s['authProfileOverride'] or '-'}")
        print(f"  authProfileOverrideSource: {s['authProfileOverrideSource'] or '-'}")
    else:
        print('session: <not requested or not found>')


def main():
    parser = argparse.ArgumentParser(description='Summarize OpenClaw openai-codex OAuth profile state.')
    parser.add_argument('--state-dir', default='~/.openclaw', help='OpenClaw state directory (default: ~/.openclaw)')
    parser.add_argument('--agent', default='main', help='Agent id to inspect (default: main)')
    parser.add_argument('--session-key', default=None, help='Optional exact session key from sessions.json')
    parser.add_argument('--json', action='store_true', help='Print JSON instead of human-readable output')
    args = parser.parse_args()

    summary = summarize(Path(args.state_dir).expanduser(), args.agent, args.session_key)
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print_human(summary)


if __name__ == '__main__':
    main()
