# 08 — Security & Audits

## Security Philosophy

AKYRA's security model follows a defense-in-depth approach: multiple independent layers of protection, each sufficient to prevent critical failures even if other layers are compromised.

- **Smart contract audits**: Three rounds (internal, PeckShield, Code4rena) with Quantstamp planned pre-mainnet
- **UUPS upgradeable architecture**: Ability to patch vulnerabilities through governance
- **Emergency pause**: All critical contracts can be paused by the multisig
- **Challenge period**: 7-day optimistic rollup window for fraud proof submission
- **Bug bounty**: Up to $100K on Immunefi for critical vulnerabilities
- **Test coverage**: 160 tests at 94.3% coverage
