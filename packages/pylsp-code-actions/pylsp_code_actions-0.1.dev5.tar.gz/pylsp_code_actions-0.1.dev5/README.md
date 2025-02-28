<!--
 ~ Copyright DB InfraGO AG and contributors
 ~ SPDX-License-Identifier: Apache-2.0
 -->

PyLSP Code Actions
==================

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pylsp-code-actions)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)
![Code QA workflow status](https://github.com/DSD-DBS/pylsp-code-actions/actions/workflows/code-qa.yml/badge.svg)

Handy code actions for python-lsp-server

This is a plugin for `python-lsp-server` which adds a few handy code actions
that I always missed:

- [x] Flip comma or other operand
- [ ] Sort keyword arguments by name
- [ ] Order keyword arguments as in the called function
- [ ] Sort dict literal by keys
- [x] Generate docstring for function/method
- [ ] Add / Remove `Annotated[...]` around a type annotation

Installation
============

Run the following command in the same venv as the server itself:

```bash
pip install pylsp-code-actions
```

If you are using neovim and mason, use:

```vim
:PylspInstall pylsp-code-actions
```

<sub>(I use neovim too btw. I also use Arch btw.)</sub>

To set up a development environment, clone the project and install it in
editable mode, again in the same virtual environment as the server itself:

```sh
git clone https://github.com/DSD-DBS/pylsp-code-actions
cd pylsp-code-actions

source ~/.../pylsp-server-venv/bin/activate  # (replace with the correct path)
pip install -U pip pre-commit
pip install -e .
pre-commit install
git config commit.template .git_commit_template
```

Contributing
============

We'd love to see your bug reports and improvement suggestions! Please take a
look at our [guidelines for contributors](CONTRIBUTING.md) for details.

Licenses
========

This project is compliant with the [REUSE Specification Version
3.0](https://git.fsfe.org/reuse/docs/src/commit/d173a27231a36e1a2a3af07421f5e557ae0fec46/spec.md).

Copyright DB InfraGO AG, licensed under Apache 2.0 (see full text in
[LICENSES/Apache-2.0.txt](LICENSES/Apache-2.0.txt))

Dot-files are licensed under CC0-1.0 (see full text in
[LICENSES/CC0-1.0.txt](LICENSES/CC0-1.0.txt))
