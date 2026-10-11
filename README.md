# 🐼 Pandoraga Ω — Full Adaptation Chess Engine

**An experimental Python chess engine exploring search algorithms, position evaluation and adaptive playing strategies.**

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Experimental-orange.svg)]()

Pandoraga Ω is an open-source chess-engine project built around Python. Its goal is to combine chess search, position evaluation, time management and persistent data to experiment with different playing strategies.

> ♟️ **Project goal:** build, test and improve a chess engine with an accessible Python codebase.

## ✨ Features

- **Chess search:** Negamax and alpha-beta pruning, where implemented.
- **Search improvements:** iterative deepening and additional search optimizations, where implemented.
- **Position evaluation:** evaluate chess positions using the engine's evaluation logic.
- **Adaptive experiments:** explore changes in playing strategies and opponent-related data.
- **Persistent memory:** JSON-based storage for supported saved data.
- **Time management:** configurable or automatic search time, depending on the implementation.
- **Graphical interface:** Tkinter interface, if supported by the current version.
- **Python-first design:** intended to be approachable for developers learning about chess engines.

Feature availability depends on the exact version of the source code. See the implementation and release notes for details.

## 🚀 Getting started

### Requirements

- Python 3.10+
- Tkinter, if using the graphical interface
- No external packages are required if the current version uses Python's standard library exclusively.

### Run on Windows

1. Download or clone this repository.
2. Open a terminal in the project directory.
3. Run:

```bash
python Pandoraga.py
```

If your installation uses the Python launcher, try:

```bash
py Pandoraga.py
```

### Run on Linux

```bash
python3 Pandoraga.py
```

**Note:** Tkinter availability depends on your Python installation and operating system.

## 🧠 How it works

Chess engines generally combine three major components:

1. **Move search** — explore possible continuations of a position.
2. **Position evaluation** — estimate which side has the advantage.
3. **Search control** — manage depth, time and computational resources.

Pandoraga Ω is a project for experimenting with these components. Its actual playing strength depends on the implemented algorithms, testing and hardware.

## 📁 Project structure

```text
Pandoraga-Full-Adaptation-Omega/
├── Pandoraga.py
├── README.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
├── docs/
└── .github/
    └── workflows/
```

The exact structure may change between releases.

## 🧪 Testing and limitations

Pandoraga Ω is an experimental project. Before relying on a release, verify:

- Legal move handling and special chess rules.
- Checkmate, stalemate and draw detection.
- Search stability and time limits.
- Memory usage and performance on different devices.
- Correct saving and loading of persistent data.

No official Elo rating, tournament result or guaranteed playing strength is claimed without reproducible benchmarks.

## 🗺️ Roadmap

- [ ] Expand automated chess-rule tests.
- [ ] Benchmark playing strength against reference engines.
- [ ] Improve search efficiency and time management.
- [ ] Document the evaluation function and adaptive mechanisms.
- [ ] Improve compatibility and usability on more devices.

## 🤝 Contributing

Contributions are welcome!

You can help by:

- Reporting reproducible bugs.
- Improving documentation.
- Adding tests for chess rules.
- Optimizing search performance.
- Sharing benchmark results and improvement ideas.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a pull request.

## 🔐 Security

Please see [SECURITY.md](SECURITY.md) for guidance on reporting security-related issues.

## 📄 License

This project is distributed under the license specified in the [`LICENSE`](LICENSE) file.

## ⭐ Support the project

If you find Pandoraga Ω interesting:

- ⭐ Star the repository.
- 🐛 Report bugs with reproducible examples.
- 💡 Suggest improvements.
- 🔧 Contribute code or documentation.

## 📞 Discussions & Questions

Have questions or want to discuss features? Check out the [Discussions](https://github.com/ongleo022-tech/PandoragaAI/discussions) tab!

---

**Built with Python and a passion for chess. 🐼♟️**
