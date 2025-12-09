# Changelog

All notable changes to Terminal221b will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project scaffold with PAO architecture
- Tiered license verification system (Free/Pro/Enterprise)
- Multi-platform release workflow (Linux, macOS, Windows)
- Docker build with multi-arch support (amd64, arm64)
- Unit tests for license module
- TODO_MVP.md gap analysis document

### Planned
- Core agent system (Analyst, Artist, Engineer, Writer)
- Terminal UI using Textual/Rich
- Solana blockchain integration
- TensorRT-LLM local inference

---

## [0.1.0] - TBD

### Added
- **License System**: Tiered licensing with feature gates
  - Free: 5 runs/day, 1 agent, no blockchain
  - Pro: 100 runs/day, 3 agents, blockchain enabled
  - Enterprise: Unlimited everything
- **Build System**: PyInstaller-based binary generation
- **CI/CD**: GitHub Actions release workflow
- **Documentation**: README, CHANGELOG, TODO_MVP

### Architecture
- `src/agents/` - Multi-agent collaboration system
- `src/tui/` - Terminal user interface
- `src/blockchain/` - Solana integration
- `src/inference/` - Local LLM inference
- `utils/` - Shared utilities including licensing

---

## Version History

| Version | Date | Highlights |
|---------|------|------------|
| 0.1.0 | TBD | Initial release with license system |

---

## Upgrade Guides

### Migrating to v0.1.0

This is the initial release. No migration needed.

### License Key Setup

1. **Free Tier**: No key required
2. **Pro Tier**: Set `LICENSE_KEY=PRO_your_key_here` environment variable
3. **Enterprise**: Contact sales@bakerstreetproject221B.store

---

## Contributors

- **Kiliaan Vanvoorden** - Lead Developer
- **BoozeLee** - GitHub Organization

---

## Links

- **Repository**: https://github.com/Bakery-street-project/Terminal221b
- **Website**: https://bakerstreetproject221B.store
- **Issues**: https://github.com/Bakery-street-project/Terminal221b/issues
- **License**: MIT (code) / Commercial (premium features)
