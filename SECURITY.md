# Security Policy

## Supported Versions

This project is currently in pre-release (v0.x). Security fixes are applied to the
`main` branch only.

| Version | Supported |
|---|---|
| 0.x (main) | ✅ |
| older branches | ❌ |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub Issues.**

To report a vulnerability:

1. Open a [GitHub Security Advisory](https://github.com/zavrocKk/zav-sandbox/security/advisories/new)
   (private channel — GitHub account required).
2. Describe the vulnerability: what it is, how to reproduce it, potential impact.
3. You will receive a response within 5 business days.

We follow responsible disclosure principles: we will acknowledge receipt, keep you
informed of progress, and credit you in the fix unless you prefer to remain anonymous.

## Scope

This project is a **100% Markdown framework** with no runtime server, no external
dependencies, and no user data processing. The attack surface is limited to:

- **Agent hooks** (`agents/hooks/`) — shell scripts that run with VS Code permissions.
  They are **opt-in and disabled by default**. Enable only after reviewing the scripts.
- **Prompt injection** — malicious content in files read by the AI agent during a
  session could attempt to override framework instructions.

## Security Design Principles

- No secrets in plain text — `<REDACTED>` or vault references only.
- Destructive commands require explicit user confirmation (enforced via the
  `security-guard` hook when enabled).
- All agent hooks are read-only inspectors — they never execute the commands they scan.
- External skills/resources require explicit user authorization before access.
- The framework itself contains no credentials, API keys, or production data.
