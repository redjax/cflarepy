# cflarepy <!-- omit in toc -->

Scripts for the Cloudflare API.

This repository is a [Python monorepo managed by the `uv` project manager](https://docs.astral.sh/uv/concepts/projects/workspaces/). [Libs](./libs) provide core functionality to [packages](./packages/), which can be assembled into [applications](./applications/) for exposing to the user. For example, the [`cli.py`](./cli.py) script at the repository root calls the [`project_cli`](./applications/project-cli/) app to expose entrypoints to the user via CLI.

## Table of Contents <!-- omit in toc -->

- [Setup](#setup)
  - [Requirements](#requirements)
  - [After cloning](#after-cloning)
    - [Dynaconf configurations](#dynaconf-configurations)
    - [With direnv](#with-direnv)
- [Usage](#usage)
  - [App entrypoint](#app-entrypoint)
- [Links](#links)
- [General](#general)
  - [Python packages used in project](#python-packages-used-in-project)
  - [Cloudflare API documentation](#cloudflare-api-documentation)

## Setup

### Requirements

- [Astral `uv`](https://docs.astral.sh/uv)
- (Optional) [Python](https://python.org)
  - The `uv` tool can [manage your Python install for you](https://docs.astral.sh/uv/guides/install-python/), meaning you don't need to install Python for this app, just `uv`!
- (Optional) [Direnv](direnv.net/)
  - This repository provides a [`.envrc`](./.envrc) file for `direnv`.
  - See the [direnv setup instructions](#with-direnv)
- [A Cloudflare account](https://cloudflare.com/sign-up)
- [A Cloudflare API token](https://developers.cloudflare.com/fundamentals/api/get-started/create-token/)

### After cloning

#### Dynaconf configurations

This project uses [Dynaconf](https://dynaconf.com) to manage app configurations. Dynaconf is a powerful configuration loading package; it can load environment variables from the command line, host environment, or [a number of settings files (`.toml` by default)](https://www.dynaconf.com/settings_files/).

To run this app, you need to set up your configurations and edit some values:

- Copy & edit config files
  - In the [config/ directory](./config), iterate through each directory and copy any `settings.toml` to `settings.local.toml`, and any `.secrets.toml` to any `.secrets.local.toml`
  - The `.local.toml` version of each file is for local development and will not be committed to git.
  - This project assumes you're using an API token, not a combination of email + API key.
  - Add your token to [config/cloudflare/.secrets.local.toml](./config/cloudflare/.secrets.toml)'s `CF_API_TOKEN`.
  - Note the `[environment]` tags in these settings files, i.e. `[dev]` and `[prod]`.
  - To set the environment for the project, export an environment variable `ENV_FOR_DYNACONF=[dev, rc, prod]`

#### With direnv

If you have installed `direnv`, this repository includes a [`.envrc` file for direnv](./.envrc). Before allowing the configuration, you need to export a couple of variables. When you run `direnv allow`, it will use the following environment variables to populate the `direnv` environment at a path `./.direnv` (does not exist until you run `direnv allow` the first time).

Exporting environment variables:

- Linux: `export ENV_VAR_NAME=value`
- Windows: `$env:ENV_VAR_NAME=value`

Export the following variables, then run `direnv allow`:

- `DIRENV_ENV=[dev,rc,prod]`
  - Controls the app environment.
  - Sets/overrides your `ENV_FOR_DYNACONF` value
- (Optional) `API_TOKEN=<your Cloudflare API token, if available>`
  - Only required if you do not set `API_EMAIL` and `API_KEY`.
  - This script assumes you're using a [Cloudflare API token](https://developers.cloudflare.com/fundamentals/api/get-started/create-token/), versus an email + API key combination.
  - When a `CF_API_TOKEN` value is present (this is set by `direnv` or the [Cloudflare secrets file](./config/cloudflare/.secrets.toml)), the app will  prefer token authentication, even if you set an email and API key.
- (Optional) `API_EMAIL=<your Cloudflare account email>`
  - Only required if you do not set a value for `API_TOKEN`.
  - The email address for your Cloudflare account.
- (Optional) `API_KEY=<your Cloudflare API key>`
  - Only required if you do not set a value for `API_TOKEN`.
  - The API key you create for this app.

The Direnv environment does not set values for all available configurations. You will still need to [create/edit configuration files](#dynaconf-configurations) for things like the database, logging level, etc.

## Usage

### App entrypoint

You can start various processes using an entrypoint, or write your own scripts in the [scripts/](./scripts/) or [sandbox/](./sandbox/) directories.

- Run `uv run cli.py --help` to start using the CLI.
- Run a [script](./scripts) to run a predefined list of commands.
- Create or run a [sandbox script/app](./sandbox/)

## Links

## General

- [Astral `uv`](https://docs.astral.sh/uv)
- [Direnv](https://direnv.net)

### Python packages used in project

- [Dynaconf Python package](https://dynaconf.com)
- [Cyclopts Python package](https://github.com/BrianPugh/cyclopts)
- [HTTPX Python package](https://www.python-httpx.org)
- [Hishel Python package](hishel.com)

### Cloudflare API documentation

Links to sections of the Cloudflare API documentation.

- [Cloudflare API documentation home](https://developers.cloudflare.com/api)
  - [List WAF packages (for getting custom WAF rules)](https://developers.cloudflare.com/api/resources/firewall/subresources/waf/subresources/packages/methods/list/)
  - [Cloudflare custom  WAF filter rules documentation](https://developers.cloudflare.com/api/resources/filters/)
