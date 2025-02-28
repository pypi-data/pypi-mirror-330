# ilint - Import LINTer

A tool to enforce dependency rules (via imports) between modules in a project.

## Features

- Enforce dependency rules (imports) between modules
- Support custom layer partitioning
- Chain dependencies (`A > B > C`, `A < B`)
- Layer isolation with walls (`A | B`)
- Mixed dependency rules (`A > B | C`)
- Detailed violation reporting

## Installation

Using pip:
```bash
pip install ilint
```
