<div align="center">
<img src = "static/logo.png" width = "150" height = "150">
<h1>absorb</h1>
<h2>The extensible, feature-rich CLI workspace.</h2>
<br>

> **⚠️ Please update `absorb` to `0.1.2`! All versions below `0.1.2` are not recommended due to security issues in [GitPython](https://security.snyk.io/vuln/SNYK-PYTHON-GITPYTHON-3113858).**

<a href = "https://pypi.org/project/absorb/">
<img src = "https://img.shields.io/pypi/v/absorb.svg">
</a>
<a href = "https://absorb.readthedocs.io">
<img src = "https://readthedocs.org/projects/absorb/badge/?version=latest">
</a>
<a href="https://codecov.io/gh/burntcarrot/absorb">
<img src="https://codecov.io/gh/burntcarrot/absorb/branch/main/graph/badge.svg?token=RYGS24J9AC"/>
</a>
<a href = "https://github.com/burntcarrot/absorb/actions?workflow=Tests">
<img src = "https://github.com/burntcarrot/absorb/workflows/Tests/badge.svg">
</a>
<a href = "https://github.com/burntcarrot/absorb/CODE_OF_CONDUCT.md">
<img src = "https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg">
</a>
<a href = "https://pypi.org/project/absorb/">
<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/absorb?color=%23000fff">
<a href="https://deepsource.io/gh/burntcarrot/absorb/?ref=repository-badge" target="_blank"><img alt="DeepSource" title="DeepSource" src="https://deepsource.io/gh/burntcarrot/absorb.svg/?label=active+issues&show_trend=true"/></a>
<a href="https://deepsource.io/gh/burntcarrot/absorb/?ref=repository-badge" target="_blank"><img alt="DeepSource" title="DeepSource" src="https://deepsource.io/gh/burntcarrot/absorb.svg/?label=resolved+issues&show_trend=true"/></a>
</a>
<br><br>
</div>


![absorb preview](static/absorb-idea.gif)

# why absorb?

- Task management tools are mostly web apps. **Why open a browser, sign up for a service and trust a company which stores your data?**
- **Have full control and flexibility of your data.** Upload your data to Github or backup it using your own preferred method. No lock-ins forever.
- Use the terminal to store your ideas, keep track of tasks, and much more! **No need to open up browsers and set up accounts.**
- absorb is built for the community. Want a feature to be added? Discuss about your ideas in discussions, and we'll try to implement it.
- Is your proposal is out of the scope of the project? Don't worry! You can build your own plugins easily!
-Experiment by creating your own plugins! **Break and build things. Install locally. Add your own dependencies. No need to wait for your PR to get merged.**


Not interested by the possibilities mentioned above?

Give it a try. Maybe you would like it! 😉

# Installation

To install `absorb`, run this command in your terminal:

```
pip install absorb
```

# Usage

`absorb`'s usage looks like:

```
absorb [OPTIONS]
```

`absorb` provides 3 commands:
- `tasks`
- `kanban`
- `idea`

More details can be found in the [documentation.](https://absorb.readthedocs.io)

# Documentation

Documentation is available at [Read the Docs](https://absorb.readthedocs.io).

# Plugins

Check out [absorb-plugins](https://github.com/burntcarrot/absorb-plugins) for sample plugins and a guide on creating plugins from scratch!

# FAQ

- **How do I create plugins?**
  - Check out [absorb-plugins](https://github.com/burntcarrot/absorb-plugins) for sample plugins and a guide on creating plugins from scratch!
- **Why can't I install `absorb` in Python 3.5/3.6?**
  - `absorb` uses [rich](https://github.com/willmcgugan/rich) for displaying content. [rich](https://github.com/willmcgugan/rich) uses [dataclasses](https://docs.python.org/3/library/dataclasses.html), which were introduced in Python 3.7 via [PEP 557](https://www.python.org/dev/peps/pep-0557/).
- **If I uninstall `absorb`, would my data get deleted too?**
  - **No.** absorb doesn't delete the files, so even if you messed up your installation or if you need to uninstall `pip`, you can re-install `absorb` and your data is loaded automatically.
- **How do I create backups?**
  - The "brain" (directory containing all files related to `absorb`) is a `git` repository. You can set up a cron job for uploading your files to GitHub, or even other cloud storage providers.
