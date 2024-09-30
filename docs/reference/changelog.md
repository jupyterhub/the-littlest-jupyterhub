(changelog)=

# Changelog

## 2.0

### 2.0.0b1 - 2024-09-30

This release bundles with the latest available software from the JupyterHub
ecosystem.

For instructions on how to make an upgrade, see [](howto-admin-upgrade-tljh).

#### Breaking changes

- JupyterHub 4.\* has been upgraded to >=5.1.0,<6
  - Refer to the [JupyterHub changelog] for details and pay attention to the
    entries for JupyterHub version 5.0.0.
- OAuthenticator 16.0.4 has been upgraded to >=17.0.0,<18
  - If you are using an OAuthenticator based authenticator class
    (GitHubOAuthenticator, GoogleOAuthenticator, ...), refer to the
    [OAuthenticator changelog] for details and pay attention to the entries for
    JupyterHub version 17.0.0.
- LDAPAuthenticator 1.3.2 has been upgraded to >=2.0.0,<3
  - If you are using this authenticator class, refer to the [LDAPAuthenticator
    changelog] for details and pay attention to the entries for
    LDAPAuthenticator version 2.0.0.
- The configured JupyterHub Proxy class `traefik-proxy` and the `traefik` server
  controlled by JupyterHub via the proxy class has been upgraded to a new major
  version, but no breaking change are expected to be noticed for users.

[oauthenticator changelog]: https://oauthenticator.readthedocs.io/en/latest/reference/changelog.html
[ldapauthenticator changelog]: https://github.com/jupyterhub/ldapauthenticator/blob/HEAD/CHANGELOG.md

#### Notable dependencies updated

A TLJH installation provides a Python environment where the software for
JupyterHub itself runs - _the hub environment_, and a Python environment where
the software of users runs - _the user environment_.

If you are installing TLJH for the first time, the user environment will be
setup initially with Python 3.12 and some other packages described in
[tljh/requirements-user-env-extras.txt].

If you are upgrading to this version of TLJH, the bare minimum is changed in the
user environment. The hub environment's dependencies are on the other hand
always upgraded to the latest version within the specified version range defined
in [tljh/requirements-hub-env.txt] and seen below.

[tljh/requirements-user-env-extras.txt]: https://github.com/jupyterhub/the-littlest-jupyterhub/blob/2.0.0b1/tljh/requirements-user-env-extras.txt
[tljh/requirements-hub-env.txt]: https://github.com/jupyterhub/the-littlest-jupyterhub/blob/2.0.0b1/tljh/requirements-hub-env.txt

The changes in the respective environments between TLJH version 1.0.0 and 2.0.0b1
are summarized below.

| Dependency changes in the _hub environment_                                    | Version in 1.0.0 | Version in 2.0.0b1 | Changelog link                                                                           | Note                                                 |
| ------------------------------------------------------------------------------ | ---------------- | ------------------ | ---------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| [jupyterhub](https://github.com/jupyterhub/jupyterhub)                         | >=4.0.2,<5       | >=5.1.0,<6         | [Changelog](https://jupyterhub.readthedocs.io/en/stable/reference/changelog.html)        | Running in the `jupyterhub` systemd service          |
| [traefik](https://github.com/traefik/traefik)                                  | 2.10.1           | 3.1.4              | [Changelog](https://github.com/traefik/traefik/blob/master/CHANGELOG.md)                 | Running in the `traefik` systemd service             |
| [traefik-proxy](https://github.com/jupyterhub/traefik-proxy)                   | >=1.1.0,<2       | 2.\*               | [Changelog](https://jupyterhub-traefik-proxy.readthedocs.io/en/latest/changelog.html)    | Run by jupyterhub, controls `traefik`                |
| [systemdspawner](https://github.com/jupyterhub/systemdspawner)                 | >=1.0.1,<2       | >=1.0.1,<2         | [Changelog](https://github.com/jupyterhub/systemdspawner/blob/master/CHANGELOG.md)       | Run by jupyterhub, controls user servers via systemd |
| [jupyterhub-idle-culler](https://github.com/jupyterhub/jupyterhub-idle-culler) | >=1.2.1,<2       | >=1.4.0,<2         | [Changelog](https://github.com/jupyterhub/jupyterhub-idle-culler/blob/main/CHANGELOG.md) | Run by jupyterhub, stops inactivate servers etc.     |
| [firstuseauthenticator](https://github.com/jupyterhub/firstuseauthenticator)   | >=1.0.0,<2       | 1.1.0,<2           | [Changelog](https://oauthenticator.readthedocs.io/en/latest/reference/changelog.html)    | An optional way to authenticate users                |
| [tmpauthenticator](https://github.com/jupyterhub/tmpauthenticator)             | >=1.0.0,<2       | 1.0.0,<2           | [Changelog](https://github.com/jupyterhub/tmpauthenticator/blob/HEAD/CHANGELOG.md)       | An optional way to authenticate users                |
| [nativeauthenticator](https://github.com/jupyterhub/nativeauthenticator)       | >=1.2.0,<2       | >=1.3.0,<2         | [Changelog](https://github.com/jupyterhub/nativeauthenticator/blob/HEAD/CHANGELOG.md)    | An optional way to authenticate users                |
| [oauthenticator](https://github.com/jupyterhub/oauthenticator)                 | >=16.0.4,<17     | >=17.0.0,<18       | [Changelog](https://oauthenticator.readthedocs.io/en/latest/reference/changelog.html)    | An optional way to authenticate users                |
| [ldapauthenticator](https://github.com/jupyterhub/ldapauthenticator)           | >=1.3.2,<2       | ==2.0.0b2          | [Changelog](https://github.com/jupyterhub/ldapauthenticator/blob/HEAD/CHANGELOG.md)      | An optional way to authenticate users                |
| [pip](https://github.com/pypa/pip)                                             | >=23.1.2         | >=23.1.2           | [Changelog](https://pip.pypa.io/en/stable/news/)                                         | -                                                    |

| Dependency changes in the _user environment_             | Version in 1.0.0 | Version in upgrade to 2.0.0b1 | Version in fresh install of 2.0.0b1 | Changelog link                                                                    | Note                     |
| -------------------------------------------------------- | ---------------- | ----------------------------- | ----------------------------------- | --------------------------------------------------------------------------------- | ------------------------ |
| [jupyterhub](https://github.com/jupyterhub/jupyterhub)   | >=4.0.2,<5       | >=5.1.0,<6                    | >=5.1.0,<6                          | [Changelog](https://jupyterhub.readthedocs.io/en/stable/reference/changelog.html) | Always upgraded.         |
| [pip](https://github.com/pypa/pip)                       | >=23.1.2         | >=23.1.2                      | >=24.2                              | [Changelog](https://pip.pypa.io/en/stable/news/)                                  | Only upgraded if needed. |
| [conda](https://docs.conda.io/projects/conda/en/stable/) | >=4.10.0         | >=4.10.0                      | ==24.7.1                            | [Changelog](https://docs.conda.io/projects/conda/en/stable/release-notes.html)    | Only upgraded if needed. |
| [mamba](https://mamba.readthedocs.io/en/latest/)         | >=0.16.0         | >=0.16.0                      | ==1.5.9                             | [Changelog](https://github.com/mamba-org/mamba/blob/main/CHANGELOG.md)            | Only upgraded if needed. |

#### New features added

- jupyterhub 5 [#989](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/989) ([@minrk](https://github.com/minrk), [@manics](https://github.com/manics))
- Validate tljh specific config [#962](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/962) ([@jrdnbradford](https://github.com/jrdnbradford), [@consideRatio](https://github.com/consideRatio), [@minrk](https://github.com/minrk))
- Add the ability to define conda channels in plugins via `tljh_extra_user_conda_channels` [#942](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/942) ([@yuvipanda](https://github.com/yuvipanda), [@consideRatio](https://github.com/consideRatio))

#### Bugs fixed

- fix `-m` invocation of jupyterhub [#988](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/988) ([@minrk](https://github.com/minrk), [@manics](https://github.com/manics))
- Re-install conda/mamba for every tljh upgrade (doesn't imply upgrade) [#968](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/968) ([@consideRatio](https://github.com/consideRatio), [@minrk](https://github.com/minrk))
- Add missing oauthenticator dependency for AzureADOAuthenticator [#959](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/959) ([@consideRatio](https://github.com/consideRatio))

#### Maintenance and upkeep improvements

- Bump the requirements-user-env-extras.txt lower version bounds [#1002](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/1002) ([@consideRatio](https://github.com/consideRatio))
- Update traefik from 2.10.1 to 3.1.4 [#1001](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/1001) ([@consideRatio](https://github.com/consideRatio))
- Update to install miniforge 24.7.1-2 from 24.7.1-0 [#999](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/999) ([@consideRatio](https://github.com/consideRatio))
- Drop ubuntu 20.04, require py39, traefik-proxy v2, and ldapauthenticator v2 [#998](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/998) ([@consideRatio](https://github.com/consideRatio), [@minrk](https://github.com/minrk))
- consolidate lock file handling [#994](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/994) ([@minrk](https://github.com/minrk), [@consideRatio](https://github.com/consideRatio), [@jrdnbradford](https://github.com/jrdnbradford))
- update oauthenticator to 17 [#992](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/992) ([@minrk](https://github.com/minrk), [@consideRatio](https://github.com/consideRatio))
- Update base user environment to miniforge 24.7.1-0 (Python 3.12) [#990](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/990) ([@minrk](https://github.com/minrk), [@consideRatio](https://github.com/consideRatio))
- Add TLJH config lockfile [#976](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/976) ([@jrdnbradford](https://github.com/jrdnbradford), [@minrk](https://github.com/minrk), [@consideRatio](https://github.com/consideRatio))
- tests: fix to catch test failure earlier when they really happen [#975](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/975) ([@consideRatio](https://github.com/consideRatio), [@minrk](https://github.com/minrk))

#### Documentation improvements

- Added missing details on how to add custom domain from manual HTTPS configuration [#983](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/983) ([@josedaudi](https://github.com/josedaudi), [@yuvipanda](https://github.com/yuvipanda))
- Reword documentation sentence [#970](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/970) ([@davidalber](https://github.com/davidalber), [@consideRatio](https://github.com/consideRatio))
- Fix typo and replace word [#969](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/969) ([@davidalber](https://github.com/davidalber), [@consideRatio](https://github.com/consideRatio))
- Fix URL syntax in nativeauth.md [#949](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/949) ([@pdebuyl](https://github.com/pdebuyl), [@minrk](https://github.com/minrk))
- adapt install documentation for new /lab default interface [#935](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/935) ([@schwebke](https://github.com/schwebke), [@minrk](https://github.com/minrk))

#### Continuous integration improvements

- ci: cache pip only when no container is used [#997](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/997) ([@consideRatio](https://github.com/consideRatio))
- ci: run unit tests in ubuntu-24.04 github actions environment as well [#993](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/993) ([@consideRatio](https://github.com/consideRatio))
- ci: add tests for debian 12 and ubuntu 24.04 [#967](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/967) ([@consideRatio](https://github.com/consideRatio))
- build(deps): bump actions/cache from 3 to 4 [#961](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/961) ([@consideRatio](https://github.com/consideRatio))
- build(deps): bump codecov/codecov-action from 3 to 4 [#960](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/960) ([@consideRatio](https://github.com/consideRatio))
- build(deps): bump actions/setup-python from 4 to 5 [#958](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/958) ([@consideRatio](https://github.com/consideRatio))
- build(deps): bump actions/checkout from 3 to 4 [#943](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/943) ([@consideRatio](https://github.com/consideRatio))

#### Contributors to this release

The following people contributed discussions, new ideas, code and documentation contributions, and review.
See [our definition of contributors](https://github-activity.readthedocs.io/en/latest/#how-does-this-tool-define-contributions-in-the-reports).

([GitHub contributors page for this release](https://github.com/jupyterhub/the-littlest-jupyterhub/graphs/contributors?from=2023-08-11&to=2024-09-30&type=c))

@consideRatio ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3AconsideRatio+updated%3A2023-08-11..2024-09-30&type=Issues)) | @davidalber ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Adavidalber+updated%3A2023-08-11..2024-09-30&type=Issues)) | @josedaudi ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Ajosedaudi+updated%3A2023-08-11..2024-09-30&type=Issues)) | @jrdnbradford ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Ajrdnbradford+updated%3A2023-08-11..2024-09-30&type=Issues)) | @kiliansinger ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Akiliansinger+updated%3A2023-08-11..2024-09-30&type=Issues)) | @manics ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Amanics+updated%3A2023-08-11..2024-09-30&type=Issues)) | @minrk ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Aminrk+updated%3A2023-08-11..2024-09-30&type=Issues)) | @MridulS ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3AMridulS+updated%3A2023-08-11..2024-09-30&type=Issues)) | @pdebuyl ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Apdebuyl+updated%3A2023-08-11..2024-09-30&type=Issues)) | @schwebke ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Aschwebke+updated%3A2023-08-11..2024-09-30&type=Issues)) | @yuvipanda ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Ayuvipanda+updated%3A2023-08-11..2024-09-30&type=Issues))

## 1.0

### 1.0.0 - 2023-08-11

This release bundles with the latest available software from the JupyterHub
ecosystem.

The TLJH project now has tests to verify upgrades of installations between
releases and procedures with automation to make releases. Going onwards, TLJH
installations of version 0.2.0 and later are meant to be easy to upgrade.

For instructions on how to make an upgrade, see [](howto-admin-upgrade-tljh).

#### Breaking changes

- JupyterHub 1.\* has been upgraded to >=4.0.2,<5
  - This upgrade requires user servers to be restarted if they were running
    during the upgrade.
  - Refer to the [JupyterHub changelog] for details where you pay attention to
    the entries for JupyterHub version 2.0.0, 3.0.0, and 4.0.0.
- Several JupyterHub Authenticators has been upgraded a major version, inspect
  the changelog for the authenticator class your installation makes use of. For
  links to the changelogs, see the section below.
- The configured JupyterHub Proxy class `traefik-proxy` and the `traefik` server
  controlled by JupyterHub via the proxy class has been upgraded to a new major
  version, but no breaking change are expected to be noticed for users of this
  distribution.
- The configured JupyterHub Spawner class `jupyterhub-systemdspawner` has been
  upgraded to a new major version, but no breaking change are expected to be
  noticed for users of this distribution.
- User servers now launch into `/lab` by default, to revert this a JupyterHub
  admin user can do `sudo tljh-config set user_environment.default_app classic`
  or set the JupyterHub config `c.Spawner.default_url` directly.

[jupyterhub changelog]: https://jupyterhub.readthedocs.io/en/stable/changelog.html

#### Notable dependencies updated

A TLJH installation provides a Python environment where the software for
JupyterHub itself runs - _the hub environment_, and a Python environment where the
software of users runs - _the user environment_.

If you are installing TLJH for the first time, the user environment will be
setup initially with Python 3.10 and some other packages described in
[tljh/requirements-user-env-extras.txt].

If you are upgrading to this version of TLJH, the bare minimum is changed in the
user environment. The hub environment's dependencies are on the other hand
always upgraded to the latest version within the specified version range defined
in [tljh/requirements-hub-env.txt] and seen below.

[tljh/requirements-user-env-extras.txt]: https://github.com/jupyterhub/the-littlest-jupyterhub/blob/1.0.0/tljh/requirements-user-env-extras.txt
[tljh/requirements-hub-env.txt]: https://github.com/jupyterhub/the-littlest-jupyterhub/blob/1.0.0/tljh/requirements-hub-env.txt

The changes in the respective environments between TLJH version 0.2.0 and 1.0.0
are summarized below.

| Dependency changes in the _hub environment_                                    | Version in 0.2.0 | Version in 1.0.0 | Changelog link                                                                           | Note                                                 |
| ------------------------------------------------------------------------------ | ---------------- | ---------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| [jupyterhub](https://github.com/jupyterhub/jupyterhub)                         | 1.\*             | >=4.0.2,<5       | [Changelog](https://jupyterhub.readthedocs.io/en/stable/reference/changelog.html)        | Running in the `jupyterhub` systemd service          |
| [traefik](https://github.com/traefik/traefik)                                  | 1.7.33           | 2.10.1           | [Changelog](https://github.com/traefik/traefik/blob/master/CHANGELOG.md)                 | Running in the `traefik` systemd service             |
| [traefik-proxy](https://github.com/jupyterhub/traefik-proxy)                   | 0.3.\*           | >=1.1.0,<2       | [Changelog](https://jupyterhub-traefik-proxy.readthedocs.io/en/latest/changelog.html)    | Run by jupyterhub, controls `traefik`                |
| [systemdspawner](https://github.com/jupyterhub/systemdspawner)                 | 0.16.\*          | >=1.0.1,<2       | [Changelog](https://github.com/jupyterhub/systemdspawner/blob/master/CHANGELOG.md)       | Run by jupyterhub, controls user servers via systemd |
| [jupyterhub-idle-culler](https://github.com/jupyterhub/jupyterhub-idle-culler) | 1.\*             | >=1.2.1,<2       | [Changelog](https://github.com/jupyterhub/jupyterhub-idle-culler/blob/main/CHANGELOG.md) | Run by jupyterhub, stops inactivate servers etc.     |
| [firstuseauthenticator](https://github.com/jupyterhub/firstuseauthenticator)   | 1.\*             | >=1.0.0,<2       | [Changelog](https://oauthenticator.readthedocs.io/en/latest/reference/changelog.html)    | An optional way to authenticate users                |
| [tmpauthenticator](https://github.com/jupyterhub/tmpauthenticator)             | 0.6.\*           | >=1.0.0,<2       | [Changelog](https://github.com/jupyterhub/tmpauthenticator/blob/HEAD/CHANGELOG.md)       | An optional way to authenticate users                |
| [nativeauthenticator](https://github.com/jupyterhub/nativeauthenticator)       | 1.\*             | >=1.2.0,<2       | [Changelog](https://github.com/jupyterhub/nativeauthenticator/blob/HEAD/CHANGELOG.md)    | An optional way to authenticate users                |
| [oauthenticator](https://github.com/jupyterhub/oauthenticator)                 | 14.\*            | >=16.0.4,<17     | [Changelog](https://oauthenticator.readthedocs.io/en/latest/reference/changelog.html)    | An optional way to authenticate users                |
| [ldapauthenticator](https://github.com/jupyterhub/ldapauthenticator)           | 1.\*             | >=1.3.2,<2       | [Changelog](https://github.com/jupyterhub/ldapauthenticator/blob/HEAD/CHANGELOG.md)      | An optional way to authenticate users                |
| [pip](https://github.com/pypa/pip)                                             | 21.3.\*          | >=23.1.2         | [Changelog](https://pip.pypa.io/en/stable/news/)                                         | -                                                    |

| Dependency changes in the _user environment_             | Version in 0.2.0 | Version in 1.0.0 | Changelog link                                                                    | Note                     |
| -------------------------------------------------------- | ---------------- | ---------------- | --------------------------------------------------------------------------------- | ------------------------ |
| [jupyterhub](https://github.com/jupyterhub/jupyterhub)   | 1.\*             | >=4.0.2,<5       | [Changelog](https://jupyterhub.readthedocs.io/en/stable/reference/changelog.html) | Always upgraded.         |
| [pip](https://github.com/pypa/pip)                       | \*               | >=23.1.2         | [Changelog](https://pip.pypa.io/en/stable/news/)                                  | Only upgraded if needed. |
| [conda](https://docs.conda.io/projects/conda/en/stable/) | 0.16.0           | >=0.16.0         | [Changelog](https://docs.conda.io/projects/conda/en/stable/release-notes.html)    | Only upgraded if needed. |
| [mamba](https://mamba.readthedocs.io/en/latest/)         | 4.10.3           | >=4.10.0         | [Changelog](https://github.com/mamba-org/mamba/blob/main/CHANGELOG.md)            | Only upgraded if needed. |

#### New features added

- Add http[s].address config to control where traefik listens [#905](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/905) ([@nsurleraux-railnova](https://github.com/nsurleraux-railnova), [@minrk](https://github.com/minrk))
- Add support for debian >=10 to bootstrap.py [#800](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/800) ([@jochym](https://github.com/jochym), [@minrk](https://github.com/minrk), [@consideRatio](https://github.com/consideRatio), [@manics](https://github.com/manics), [@yuvipanda](https://github.com/yuvipanda))

#### Enhancements made

- added `remove_named_servers` setting for jupyterhub-idle-culler [#881](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/881) ([@consideRatio](https://github.com/consideRatio))
- Traefik v2, TraefikProxy v1 [#861](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/861) ([@minrk](https://github.com/minrk), [@consideRatio](https://github.com/consideRatio), [@MridulS](https://github.com/MridulS))

#### Maintenance and upkeep improvements

- Update Notebook, JupyterLab, Jupyter Resource Usage [#928](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/928) ([@jtpio](https://github.com/jtpio), [@consideRatio](https://github.com/consideRatio))
- Launch into `/lab` by default by changing TLJH config's default value [#775](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/775) ([@raybellwaves](https://github.com/raybellwaves), [@consideRatio](https://github.com/consideRatio), [@GeorgianaElena](https://github.com/GeorgianaElena), [@minrk](https://github.com/minrk), [@manics](https://github.com/manics))
- breaking: update oauthenticator from 15.1.0 to >=16.0.2,<17, make tljh auth docs link out [#924](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/924) ([@consideRatio](https://github.com/consideRatio), [@manics](https://github.com/manics), [@minrk](https://github.com/minrk))
- test refactor: add comment about python/conda/mamba [#921](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/921) ([@consideRatio](https://github.com/consideRatio))
- --force-reinstall old conda to ensure it's working before we try to install conda packages [#920](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/920) ([@minrk](https://github.com/minrk), [@consideRatio](https://github.com/consideRatio))
- test refactor: put bootstrap tests in an isolated job, save ~3 min in each of the integration test jobs [#919](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/919) ([@consideRatio](https://github.com/consideRatio), [@minrk](https://github.com/minrk))
- maint: refactor tests, fix upgrade tests (now correctly failing) [#916](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/916) ([@consideRatio](https://github.com/consideRatio), [@minrk](https://github.com/minrk))
- Update systemdspawner from version 0.17.\* to >=1.0.1,<2 [#915](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/915) ([@consideRatio](https://github.com/consideRatio), [@minrk](https://github.com/minrk), [@manics](https://github.com/manics))
- Fix recently introduced failure to upper bound systemdspawner [#914](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/914) ([@consideRatio](https://github.com/consideRatio), [@minrk](https://github.com/minrk))
- Stop bundling jupyterhub-configurator which has been disabled by default [#912](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/912) ([@consideRatio](https://github.com/consideRatio), [@GeorgianaElena](https://github.com/GeorgianaElena), [@yuvipanda](https://github.com/yuvipanda))
- Update nativeauthenticator, tmpauthenticator, and jupyterhub-configurator [#900](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/900) ([@consideRatio](https://github.com/consideRatio), [@minrk](https://github.com/minrk))
- ensure hub env is on $PATH in jupyterhub service [#895](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/895) ([@minrk](https://github.com/minrk), [@consideRatio](https://github.com/consideRatio), [@manics](https://github.com/manics))
- pre-commit: add isort and autoflake [#893](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/893) ([@consideRatio](https://github.com/consideRatio), [@minrk](https://github.com/minrk))
- Upgrade pip in hub env from 21.3 to to 23.1 when bootstrap script runs [#892](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/892) ([@consideRatio](https://github.com/consideRatio), [@minrk](https://github.com/minrk))
- pre-commit.ci configured to update pre-commit hooks on a monthly basis [#891](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/891) ([@consideRatio](https://github.com/consideRatio))
- Only upgrade jupyterhub in user env when upgrading tljh, ensure pip>=23.1.2 in user env [#890](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/890) ([@consideRatio](https://github.com/consideRatio), [@manics](https://github.com/manics), [@minrk](https://github.com/minrk))
- add integration test for hub version [#886](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/886) ([@minrk](https://github.com/minrk), [@consideRatio](https://github.com/consideRatio))
- update: jupyterhub 4 [#880](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/880) ([@consideRatio](https://github.com/consideRatio), [@minrk](https://github.com/minrk))
- maint: add upgrade test from main branch, latest release, and 0.2.0 [#876](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/876) ([@consideRatio](https://github.com/consideRatio), [@minrk](https://github.com/minrk))
- dependabot: monthly updates of github actions [#871](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/871) ([@consideRatio](https://github.com/consideRatio))
- maint: remove deprecated nteract-on-jupyter [#869](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/869) ([@consideRatio](https://github.com/consideRatio), [@yuvipanda](https://github.com/yuvipanda))
- avoid registering duplicate log handlers [#862](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/862) ([@minrk](https://github.com/minrk), [@consideRatio](https://github.com/consideRatio))
- bump version to 1.0.0.dev0 [#859](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/859) ([@minrk](https://github.com/minrk), [@manics](https://github.com/manics))
- Update base user environment to mambaforge 23.1.0-1 (Python 3.10) [#858](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/858) ([@minrk](https://github.com/minrk), [@consideRatio](https://github.com/consideRatio), [@manics](https://github.com/manics))
- require ubuntu 20.04, test on debian 11, require Python 3.8 [#856](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/856) ([@minrk](https://github.com/minrk), [@consideRatio](https://github.com/consideRatio), [@manics](https://github.com/manics))
- update: jupyterhub 3, oauthenticator 15, systemdspawner 0.17 (user env: ipywidgets 8) [#842](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/842) ([@yuvipanda](https://github.com/yuvipanda), [@manics](https://github.com/manics), [@consideRatio](https://github.com/consideRatio), [@minrk](https://github.com/minrk))
- Release 0.2.0 (JupyterHub 1.\*) [#838](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/838) ([@manics](https://github.com/manics), [@minrk](https://github.com/minrk))

#### Documentation improvements

- docs: add docs about environments and upgrades [#932](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/932) ([@consideRatio](https://github.com/consideRatio), [@minrk](https://github.com/minrk))
- Add `JupyterLab` setting overrides docs [#922](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/922) ([@jrdnbradford](https://github.com/jrdnbradford), [@consideRatio](https://github.com/consideRatio))
- Quote `pwd` to prevent error if dir has spaces [#917](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/917) ([@jrdnbradford](https://github.com/jrdnbradford), [@consideRatio](https://github.com/consideRatio))
- Google Cloud troubleshooting and configuration updates [#906](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/906) ([@jrdnbradford](https://github.com/jrdnbradford), [@consideRatio](https://github.com/consideRatio))
- Add user env doc files [#902](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/902) ([@jrdnbradford](https://github.com/jrdnbradford), [@consideRatio](https://github.com/consideRatio))
- Update Google auth docs [#898](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/898) ([@jrdnbradford](https://github.com/jrdnbradford), [@consideRatio](https://github.com/consideRatio))
- docs: disable navigation with arrow keys [#896](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/896) ([@MridulS](https://github.com/MridulS), [@consideRatio](https://github.com/consideRatio))
- docs(awscognito): add custom claims example [#887](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/887) ([@consideRatio](https://github.com/consideRatio))
- Docs: Update DigitalOcean install instructions with new screenshot for "user data" [#883](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/883) ([@audiodude](https://github.com/audiodude), [@consideRatio](https://github.com/consideRatio))
- Typo : username -> admin-user-name [#879](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/879) ([@Rom1deTroyes](https://github.com/Rom1deTroyes), [@consideRatio](https://github.com/consideRatio))
- docs: fix readme badge for tests [#878](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/878) ([@consideRatio](https://github.com/consideRatio))
- docs: fix remaining issues following rst to myst transition [#870](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/870) ([@consideRatio](https://github.com/consideRatio))
- docs: transition from rst to myst markdown using rst2myst [#863](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/863) ([@minrk](https://github.com/minrk), [@consideRatio](https://github.com/consideRatio), [@jrdnbradford](https://github.com/jrdnbradford))
- Typo in user-environment.rst [#849](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/849) ([@jawiv](https://github.com/jawiv), [@minrk](https://github.com/minrk))
- Recommend Ubuntu 22.04 in docs [#843](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/843) ([@adonm](https://github.com/adonm), [@consideRatio](https://github.com/consideRatio))

#### Contributors to this release

The following people contributed discussions, new ideas, code and documentation contributions, and review.
See [our definition of contributors](https://github-activity.readthedocs.io/en/latest/#how-does-this-tool-define-contributions-in-the-reports).

([GitHub contributors page for this release](https://github.com/jupyterhub/the-littlest-jupyterhub/graphs/contributors?from=2023-02-27&to=2023-08-11&type=c))

@adonm ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Aadonm+updated%3A2023-02-27..2023-08-11&type=Issues)) | @audiodude ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Aaudiodude+updated%3A2023-02-27..2023-08-11&type=Issues)) | @choldgraf ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Acholdgraf+updated%3A2023-02-27..2023-08-11&type=Issues)) | @consideRatio ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3AconsideRatio+updated%3A2023-02-27..2023-08-11&type=Issues)) | @eingemaischt ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Aeingemaischt+updated%3A2023-02-27..2023-08-11&type=Issues)) | @GeorgianaElena ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3AGeorgianaElena+updated%3A2023-02-27..2023-08-11&type=Issues)) | @Hannnsen ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3AHannnsen+updated%3A2023-02-27..2023-08-11&type=Issues)) | @jawiv ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Ajawiv+updated%3A2023-02-27..2023-08-11&type=Issues)) | @jochym ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Ajochym+updated%3A2023-02-27..2023-08-11&type=Issues)) | @jrdnbradford ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Ajrdnbradford+updated%3A2023-02-27..2023-08-11&type=Issues)) | @jtpio ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Ajtpio+updated%3A2023-02-27..2023-08-11&type=Issues)) | @kevmk04 ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Akevmk04+updated%3A2023-02-27..2023-08-11&type=Issues)) | @manics ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Amanics+updated%3A2023-02-27..2023-08-11&type=Issues)) | @minrk ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Aminrk+updated%3A2023-02-27..2023-08-11&type=Issues)) | @MridulS ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3AMridulS+updated%3A2023-02-27..2023-08-11&type=Issues)) | @nsurleraux-railnova ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Ansurleraux-railnova+updated%3A2023-02-27..2023-08-11&type=Issues)) | @raybellwaves ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Araybellwaves+updated%3A2023-02-27..2023-08-11&type=Issues)) | @Rom1deTroyes ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3ARom1deTroyes+updated%3A2023-02-27..2023-08-11&type=Issues)) | @wjcapehart ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Awjcapehart+updated%3A2023-02-27..2023-08-11&type=Issues)) | @yuvipanda ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Ayuvipanda+updated%3A2023-02-27..2023-08-11&type=Issues))

## 0.2.0

### 0.2.0 - 2023-02-27

([full changelog](https://github.com/jupyterhub/the-littlest-jupyterhub/compare/4a74ad17a1a19f6378efe12a01ba634ed90f1e03...0.2.0))

#### Merged PRs

- Fix broken CI [#851](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/851) ([@pnasrat](https://github.com/pnasrat))
- Ensure SQLAlchemy 1.x used for hub [#848](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/848) ([@pnasrat](https://github.com/pnasrat))
- docs: update sphinx configuration, add opengraph and rediraffe, fix a warning [#840](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/840) ([@consideRatio](https://github.com/consideRatio))
- ci: fix deprecation of set-output in github workflows [#837](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/837) ([@consideRatio](https://github.com/consideRatio))
- Fix typo with --show-progress-page argument in example [#835](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/835) ([@luong-komorebi](https://github.com/luong-komorebi))
- ci: add dependabot for github actions and bump them now [#831](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/831) ([@consideRatio](https://github.com/consideRatio))
- docs: reference nbgitpullers docs to fix outdated tljh docs [#826](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/826) ([@rdmolony](https://github.com/rdmolony))
- Update precommit [#820](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/820) ([@manics](https://github.com/manics))
- bootstrap script accepts a version [#819](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/819) ([@manics](https://github.com/manics))
- ci: run int. and unit tests on 22.04 LTS + py3.10 [#817](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/817) ([@MridulS](https://github.com/MridulS))
- clarify direction of information in idle-culler [#816](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/816) ([@minrk](https://github.com/minrk))
- Update progress_page_favicon_url link [#811](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/811) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Bump systemdspawner version [#810](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/810) ([@yuvipanda](https://github.com/yuvipanda))
- github workflow: echo $BOOTSTRAP_PIP_SPEC [#801](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/801) ([@manics](https://github.com/manics))
- ENH: add logging if user-requirements-txt-url found [#796](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/796) ([@raybellwaves](https://github.com/raybellwaves))
- extra logger.info [#789](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/789) ([@raybellwaves](https://github.com/raybellwaves))
- DOC: update sudo tljh-config --help demo [#785](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/785) ([@raybellwaves](https://github.com/raybellwaves))
- DOC: add tljh-db plugin to list [#782](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/782) ([@raybellwaves](https://github.com/raybellwaves))
- DOC: move link to contributing/plugin higher [#781](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/781) ([@raybellwaves](https://github.com/raybellwaves))
- DOC: update info on AWS get system log [#772](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/772) ([@raybellwaves](https://github.com/raybellwaves))
- DOC: hyperlink there [#768](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/768) ([@raybellwaves](https://github.com/raybellwaves))
- updating 'plugin' documentation [#764](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/764) ([@oisinBates](https://github.com/oisinBates))
- pre-commit: apply black formatting (and prettier on one yaml file) [#755](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/755) ([@consideRatio](https://github.com/consideRatio))
- pre-commit: remove requirements-txt-fixer [#754](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/754) ([@consideRatio](https://github.com/consideRatio))
- Update firstuseauthenticator to 1.0.0 [#749](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/749) ([@consideRatio](https://github.com/consideRatio))
- Add .pre-commit-config [#748](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/748) ([@consideRatio](https://github.com/consideRatio))
- Small fixes for flake8 and other smaller pre-commit tools [#747](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/747) ([@consideRatio](https://github.com/consideRatio))
- remove addressed FIXMEs in update_auth [#745](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/745) ([@minrk](https://github.com/minrk))
- Remove MockConfigurer [#744](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/744) ([@minrk](https://github.com/minrk))
- docs: require sphinx>=2, otherwise error follows [#743](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/743) ([@consideRatio](https://github.com/consideRatio))
- docs: fix how-to sections table of content section [#742](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/742) ([@consideRatio](https://github.com/consideRatio))
- Modernize docs Makefile with sphinx-autobuild [#741](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/741) ([@consideRatio](https://github.com/consideRatio))
- update awscognito docs to use GenericOAuthenticator [#729](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/729) ([@minrk](https://github.com/minrk))
- Apply TLJH auth config with less assumptions [#721](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/721) ([@consideRatio](https://github.com/consideRatio))
- Bump to recent versions, and make bootstrap.py update to those when run [#719](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/719) ([@consideRatio](https://github.com/consideRatio))
- docs: fix language regarding master [#718](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/718) ([@consideRatio](https://github.com/consideRatio))
- Don't open file twice when downloading conda [#717](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/717) ([@yuvipanda](https://github.com/yuvipanda))
- Try setting min. req to 1GB of RAM [#716](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/716) ([@yuvipanda](https://github.com/yuvipanda))
- Refactor bootstrap.py script for readability [#715](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/715) ([@consideRatio](https://github.com/consideRatio))
- Remove template in root folder - a mistakenly committed file [#713](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/713) ([@consideRatio](https://github.com/consideRatio))
- ci: add .readthedocs.yaml [#712](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/712) ([@consideRatio](https://github.com/consideRatio))
- Revision of our GitHub Workflows and README.rst to README.md [#710](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/710) ([@consideRatio](https://github.com/consideRatio))
- Bump nbgitpuller version [#704](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/704) ([@yuvipanda](https://github.com/yuvipanda))
- Bump notebook from 6.3.0 to 6.4.1 in /tljh [#703](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/703) ([@dependabot](https://github.com/dependabot))
- Switch to Mamba [#697](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/697) ([@manics](https://github.com/manics))
- Reflect the fact that AWS free tier is not enough [#696](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/696) ([@Guillaume-Garrigos](https://github.com/Guillaume-Garrigos))
- Bump hub and notebook versions [#688](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/688) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- bump nativeauthenticator version to avoid critical bug [#683](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/683) ([@ibayer](https://github.com/ibayer))
- Add "Users Lists" example [#682](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/682) ([@jeanmarcalkazzi](https://github.com/jeanmarcalkazzi))
- Add missing configurator config [#680](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/680) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Add support for installing TLJH on Arm64 systems and bump traefik (1.7.18 -> 1.7.33) [#679](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/679) ([@cdibble](https://github.com/cdibble))
- Revert "Revert "Switch integration and upgrade tests from CircleCI to GitHub actions"" [#678](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/678) ([@yuvipanda](https://github.com/yuvipanda))
- Revert "Switch integration and upgrade tests from CircleCI to GitHub actions" [#677](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/677) ([@yuvipanda](https://github.com/yuvipanda))
- Add the jupyterhub-configurator service [#676](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/676) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Switch integration and upgrade tests from CircleCI to GitHub actions [#673](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/673) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Switch unit tests from CircleCI to GitHub actions [#672](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/672) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Note smallest AWS instance TLJH can run on [#671](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/671) ([@yuvipanda](https://github.com/yuvipanda))
- Pin chardet again and pin it for tests also. [#668](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/668) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Bump traefik-proxy version and remove pin. [#667](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/667) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Added instructions for restarting JupyterHub to docs (re: #455) [#666](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/666) ([@DataCascadia](https://github.com/DataCascadia))
- Add docs to override systemd settings [#663](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/663) ([@jtpio](https://github.com/jtpio))
- Docs: add missing gif for the TLJH is building page [#662](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/662) ([@jtpio](https://github.com/jtpio))
- Upgrade to Jupyterlab 3.0 and Jupyter Resource Usage [#658](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/658) ([@jtpio](https://github.com/jtpio))
- Fix code formatting in the docs [#657](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/657) ([@jtpio](https://github.com/jtpio))
- setup.py: Update repo URL [#656](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/656) ([@jayvdb](https://github.com/jayvdb))
- Own server install sets admin password in step 3 [#652](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/652) ([@leouieda](https://github.com/leouieda))
- Fix link to resource estimation in server requirements docs [#651](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/651) ([@jtpio](https://github.com/jtpio))
- Revert and pin notebook version [#648](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/648) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Upgrade to JupyterLab 3.0 [#647](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/647) ([@yuvipanda](https://github.com/yuvipanda))
- Pin chardet [#643](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/643) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- bump systemdspawner to 0.15 [#639](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/639) ([@minrk](https://github.com/minrk))
- Doc of how users can change password [#637](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/637) ([@mauro3](https://github.com/mauro3))
- Add a necessary step to reset password [#636](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/636) ([@mauro3](https://github.com/mauro3))
- Bump a few of the dependencies [#634](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/634) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- proposed changes for issue #619 [#633](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/633) ([@ewidl](https://github.com/ewidl))
- how to call sudo with changed path [#632](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/632) ([@namin](https://github.com/namin))
- Bump memory again for integration tests [#630](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/630) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Fix html_sidebars [#625](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/625) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Fix doc build [#624](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/624) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Add base_url capability to tljh-config [#623](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/623) ([@jeanmarcalkazzi](https://github.com/jeanmarcalkazzi))
- Fix HTML of bootstrap [#621](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/621) ([@richardbrinkman](https://github.com/richardbrinkman))
- Add link to jupyterhub-idle-culler [#607](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/607) ([@1kastner](https://github.com/1kastner))
- Temporary page while tljh is building [#605](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/605) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Bump systemdspawner [#602](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/602) ([@yuvipanda](https://github.com/yuvipanda))
- Remove CircleCi docs build [#600](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/600) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- ensure_server is now ensure_server_simulate [#599](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/599) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Use http port from config while checking hub [#598](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/598) ([@dongmok](https://github.com/dongmok))
- add -L option to curl to follow redirect [#593](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/593) ([@LTangaF](https://github.com/LTangaF))
- Upgrade JupyterLab version [#591](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/591) ([@yuvipanda](https://github.com/yuvipanda))
- Use tljh.jupyter.org/bootstrap.py to get installer [#590](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/590) ([@yuvipanda](https://github.com/yuvipanda))
- Use /hub/api endpoint to check for hub ready [#587](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/587) ([@jtpio](https://github.com/jtpio))
- Allow extending traefik dynamic config [#586](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/586) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Allow extending traefik config [#582](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/582) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Provide more memory for integration tests [#580](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/580) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Fixed git repo link from markdown to rst [#579](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/579) ([@danlester](https://github.com/danlester))
- Use sha256 sums for verifying miniconda download [#570](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/570) ([@yuvipanda](https://github.com/yuvipanda))
- Add a useful link to the git repo, fix a typo, in docs [#568](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/568) ([@danlester](https://github.com/danlester))
- Add tljh-repo2docker to the list of plugins [#567](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/567) ([@jtpio](https://github.com/jtpio))
- Rename to --bootstrap-pip-spec in the integration tests [#566](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/566) ([@jtpio](https://github.com/jtpio))
- Make bootstrap_pip_spec test argument optional [#563](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/563) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Add documentation to install multiple plugins [#561](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/561) ([@jtpio](https://github.com/jtpio))
- Remove unused plugins argument from run_plugin_actions [#560](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/560) ([@jtpio](https://github.com/jtpio))
- Use idle culler from jupyterhub-idle-culler package [#559](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/559) ([@yuvipanda](https://github.com/yuvipanda))
- Add bootstrap pip spec to the integration test docs [#558](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/558) ([@jtpio](https://github.com/jtpio))
- Fix failing unit test [#553](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/553) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Fixes 'availabe' > 'available' spelling in docs [#552](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/552) ([@sethwoodworth](https://github.com/sethwoodworth))
- Add a section about known TLJH plugins to the documentation [#551](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/551) ([@jtpio](https://github.com/jtpio))
- Provide instructions on how to revert each action of the installer [#545](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/545) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Fix code block formatting in the docs [#541](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/541) ([@jtpio](https://github.com/jtpio))
- Update the docs theme to pydata-sphinx-theme [#538](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/538) ([@jtpio](https://github.com/jtpio))
- Update hub packages to the latest stable versions [#537](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/537) ([@jtpio](https://github.com/jtpio))
- Add a quick note about DNS records [#532](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/532) ([@jtpio](https://github.com/jtpio))
- Use PR username when no CircleCI project [#531](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/531) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Fix typo in --user-requirements-txt-url help [#527](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/527) ([@jtpio](https://github.com/jtpio))
- Fix installer [#519](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/519) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Use the same 1-100 numbers as in the docs and repo description [#516](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/516) ([@jtpio](https://github.com/jtpio))
- Remove configurable-http-proxy references from docs #494 [#514](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/514) ([@shireenrao](https://github.com/shireenrao))
- Update tests [#511](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/511) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Fix missing reference to requirements-base.txt [#504](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/504) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Upgrade jupyterlab to 1.2.6 [#499](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/499) ([@letianw91](https://github.com/letianw91))
- Set tls 1.2 to be the min version [#498](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/498) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Fix integration test for new pip [#491](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/491) ([@betatim](https://github.com/betatim))
- Link contributing guide [#489](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/489) ([@betatim](https://github.com/betatim))
- Fix broken link to resource estimation page [#485](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/485) ([@leouieda](https://github.com/leouieda))
- Fix failing integration tests [#479](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/479) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Upgrade authenticators [#476](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/476) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Added AWS Cognito docs [#472](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/472) ([@budgester](https://github.com/budgester))
- Switch to pandas theme [#468](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/468) ([@yuvipanda](https://github.com/yuvipanda))
- installation failed due to no python3-dev packages [#460](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/460) ([@afonit](https://github.com/afonit))
- Azure docs - add details on the new Azure deploy button [#458](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/458) ([@trallard](https://github.com/trallard))
- switch base environment to requirements file [#457](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/457) ([@minrk](https://github.com/minrk))
- Add hook for new users [#453](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/453) ([@jkfm](https://github.com/jkfm))
- Write out deb line only if it already doesn't exist [#449](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/449) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Update Azure docs [#448](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/448) ([@trallard](https://github.com/trallard))
- Update Amazon AMI selection step [#443](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/443) ([@fomightez](https://github.com/fomightez))
- Upgrade traefik version [#442](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/442) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Disable ProtectHome=tmpfs [#435](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/435) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Make Python3.7 the default [#433](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/433) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Fix failing conda tests [#423](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/423) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- fixed typo in key pair section [#421](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/421) ([@ptcane](https://github.com/ptcane))
- HowTo Google authenticate [#404](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/404) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Docs update: reload proxy after modifying the ports [#403](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/403) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Allow adding multiple admins during install [#399](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/399) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Set admin password during install [#395](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/395) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- fixing typo (remove "can add rules") in amazon.rst [#393](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/393) ([@cornhundred](https://github.com/cornhundred))
- Import containers from collections.abc rather than collections [#392](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/392) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Fix link to the hooks in plugins docs [#390](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/390) ([@jtpio](https://github.com/jtpio))
- Add tljh_post_install hook [#389](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/389) ([@jtpio](https://github.com/jtpio))
- Run idle culler as a python module [#386](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/386) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Replace pre-alpha by beta state in documentation [#385](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/385) ([@lumbric](https://github.com/lumbric))
- Allow adding users to specific groups [#382](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/382) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Tell apt-get to never ask questions [#380](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/380) ([@yuvipanda](https://github.com/yuvipanda))
- Typo fix: `s` -> `is` [#376](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/376) ([@jtpio](https://github.com/jtpio))
- Fix typo: missing "c" for instance [#374](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/374) ([@jtpio](https://github.com/jtpio))
- Minor typo fix: praticular -> particular [#372](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/372) ([@jtpio](https://github.com/jtpio))
- Add Tutorial for OVH [#371](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/371) ([@jtpio](https://github.com/jtpio))
- Clarify the steps to build the docs locally [#370](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/370) ([@jtpio](https://github.com/jtpio))
- Fix typo in README link [#367](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/367) ([@pbugnion](https://github.com/pbugnion))
- Add idle culler [#366](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/366) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Add tmpauthenticator by default to TLJH [#365](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/365) ([@yuvipanda](https://github.com/yuvipanda))
- Docs addition [#364](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/364) ([@kafonek](https://github.com/kafonek))
- Fix typo: cohnfig -> config [#363](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/363) ([@staeiou](https://github.com/staeiou))
- Add port configuration to docs [#362](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/362) ([@staeiou](https://github.com/staeiou))
- Add custom hub package & config hooks [#360](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/360) ([@yuvipanda](https://github.com/yuvipanda))
- Install & use pycurl for requests [#359](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/359) ([@yuvipanda](https://github.com/yuvipanda))
- Minor azure doc cleanup [#358](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/358) ([@yuvipanda](https://github.com/yuvipanda))
- Suppress insecure HTTPS warning when upgrading TLJH [#357](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/357) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Fixed out of date config directory listed in docs for tljh-config [#355](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/355) ([@JuanCab](https://github.com/JuanCab))
- Add "tljh-config unset" option [#352](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/352) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Upgrade while https enabled [#347](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/347) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Remove stray .DS_Store files [#343](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/343) ([@yuvipanda](https://github.com/yuvipanda))
- Add instructions to deploy on Azure [#342](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/342) ([@trallard](https://github.com/trallard))
- Add more validation to bootstrap.py [#340](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/340) ([@yuvipanda](https://github.com/yuvipanda))
- Retry downloading traefik if it fails [#339](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/339) ([@yuvipanda](https://github.com/yuvipanda))
- Provide much better error messages [#337](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/337) ([@yuvipanda](https://github.com/yuvipanda))
- Limit memory available in integration tests [#335](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/335) ([@yuvipanda](https://github.com/yuvipanda))
- Remove stray = in authenticator configuration example [#331](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/331) ([@yuvipanda](https://github.com/yuvipanda))
- Minor cleanup of custom server install documents [#329](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/329) ([@yuvipanda](https://github.com/yuvipanda))
- Cleanup HTTPS documentation [#328](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/328) ([@yuvipanda](https://github.com/yuvipanda))
- Add note about not running on your own laptop or in Docker [#327](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/327) ([@yuvipanda](https://github.com/yuvipanda))
- Use c.Spawner to set mem_limit & cpu_limit [#326](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/326) ([@yuvipanda](https://github.com/yuvipanda))
- Few updates from reading through the docs [#325](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/325) ([@znicholls](https://github.com/znicholls))
- Remove repeated sentence from README.rst [#324](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/324) ([@MayeulC](https://github.com/MayeulC))
- Remove ominous warning with outdated release date [#320](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/320) ([@yuvipanda](https://github.com/yuvipanda))
- Move digital ocean 'resize' docs out of 'install' step [#319](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/319) ([@yuvipanda](https://github.com/yuvipanda))
- Update Readme for the AWS docs link [#317](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/317) ([@shireenrao](https://github.com/shireenrao))
- Upgrade to JupyterHub 1.0 [#313](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/313) ([@minrk](https://github.com/minrk))
- Bump JupyterHub and systemdspawner versions [#311](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/311) ([@yuvipanda](https://github.com/yuvipanda))
- adding sidebar links [#309](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/309) ([@choldgraf](https://github.com/choldgraf))
- Change style to match Jhub main doc [#304](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/304) ([@leportella](https://github.com/leportella))
- Fix the version tag of the notebook package [#303](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/303) ([@betatim](https://github.com/betatim))
- Bump jupyterhub version [#297](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/297) ([@yuvipanda](https://github.com/yuvipanda))
- Update / clarify / shorten docs, add missing image from AWS install [#296](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/296) ([@laxdog](https://github.com/laxdog))
- DOC: moved nativeauthentic config instructions to code block [#294](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/294) ([@story645](https://github.com/story645))
- Pin tornado to <6 [#292](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/292) ([@willirath](https://github.com/willirath))
- typo fix in installer actions [#287](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/287) ([@junctionapps](https://github.com/junctionapps))
- Add NativeAuth as an optional authenticator [#284](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/284) ([@leportella](https://github.com/leportella))
- update dev-setup commands [#276](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/276) ([@minrk](https://github.com/minrk))
- single yaml implementation [#275](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/275) ([@minrk](https://github.com/minrk))
- updating the image size text [#271](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/271) ([@choldgraf](https://github.com/choldgraf))
- Run fix-permissions on each install command [#268](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/268) ([@minrk](https://github.com/minrk))
- Replace chp with traefik-proxy [#266](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/266) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Use --sys-prefix for installing nbextensions [#265](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/265) ([@yuvipanda](https://github.com/yuvipanda))
- Mark flaky test as flaky [#262](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/262) ([@yuvipanda](https://github.com/yuvipanda))
- fix GitHub login config missing callback URL [#261](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/261) ([@huhuhang](https://github.com/huhuhang))
- Use newer firstuseauthenticator [#260](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/260) ([@willirath](https://github.com/willirath))
- Install git explicitly during bootstrap [#254](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/254) ([@yuvipanda](https://github.com/yuvipanda))
- Move custom server troubleshooting code to its own page [#253](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/253) ([@yuvipanda](https://github.com/yuvipanda))
- Add ipywidgets to base installation [#249](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/249) ([@yuvipanda](https://github.com/yuvipanda))
- Use tljh logger in installer [#248](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/248) ([@fm75](https://github.com/fm75))
- Fixing RTD badge [#244](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/244) ([@choldgraf](https://github.com/choldgraf))
- Adds the universe repository to the used sources [#242](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/242) ([@owah](https://github.com/owah))
- Update nodejs to 10.x LTS [#238](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/238) ([@yuvipanda](https://github.com/yuvipanda))
- Exit when tljh-config is called as non-root [#232](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/232) ([@yuvipanda](https://github.com/yuvipanda))
- Documentation behind proxy [#230](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/230) ([@fm75](https://github.com/fm75))
- Removed duplicate 'the' in docs [#227](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/227) ([@altmas5](https://github.com/altmas5))
- consolidate yaml configuration [#224](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/224) ([@minrk](https://github.com/minrk))
- Provide better error message when running on unsupported distro [#221](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/221) ([@yuvipanda](https://github.com/yuvipanda))
- Upgrade package versions [#215](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/215) ([@yuvipanda](https://github.com/yuvipanda))
- Document tljh-config commands by referencing the --help sections [#213](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/213) ([@gillybops](https://github.com/gillybops))
- add warning if tljh-config is called as non-root user [#209](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/209) ([@anyushevai](https://github.com/anyushevai))
- updating theme and storing docs artifacts [#205](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/205) ([@choldgraf](https://github.com/choldgraf))
- No memory limit (continued) [#202](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/202) ([@betatim](https://github.com/betatim))
- enabling jupyter contributed extensions [#201](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/201) ([@wrightaprilm](https://github.com/wrightaprilm))
- Update docs.rst [#196](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/196) ([@jzf2101](https://github.com/jzf2101))
- Fix minor typo: pypy -> pypi [#194](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/194) ([@jtpio](https://github.com/jtpio))
- Issue#182: add amazon installation tutorial [#189](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/189) ([@fomightez](https://github.com/fomightez))
- small typo in docs [#184](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/184) ([@choldgraf](https://github.com/choldgraf))
- adding update on resizing droplet [#181](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/181) ([@wrightaprilm](https://github.com/wrightaprilm))
- Normalize systemuser [#179](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/179) ([@yuvipanda](https://github.com/yuvipanda))
- Remove extra space after opening paren [#178](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/178) ([@yuvipanda](https://github.com/yuvipanda))
- Bump firstuseauthenticator version [#175](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/175) ([@yuvipanda](https://github.com/yuvipanda))
- typo questoins -> questions. [#174](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/174) ([@Carreau](https://github.com/Carreau))
- Remind to use https on custom-servers. [#170](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/170) ([@Carreau](https://github.com/Carreau))
- Don't create home publicly readable [#169](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/169) ([@Carreau](https://github.com/Carreau))
- installer.py: remove unused f"..." [#167](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/167) ([@gyg-github](https://github.com/gyg-github))
- put config in `$tljh/config` directory [#163](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/163) ([@minrk](https://github.com/minrk))
- missing arguments in integration test commands [#162](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/162) ([@minrk](https://github.com/minrk))
- test manual https setup [#161](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/161) ([@minrk](https://github.com/minrk))
- jupyterhub 0.9.2 [#160](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/160) ([@minrk](https://github.com/minrk))
- Fix some typos [#159](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/159) ([@Carreau](https://github.com/Carreau))
- Upgrade to latest version of JupyterLab [#152](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/152) ([@yuvipanda](https://github.com/yuvipanda))
- polish local server install [#151](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/151) ([@Carreau](https://github.com/Carreau))
- Don't capture stderr when calling conda [#149](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/149) ([@yuvipanda](https://github.com/yuvipanda))
- Fix link to custom server install [#143](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/143) ([@jprorama](https://github.com/jprorama))
- Copybutton fix [#140](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/140) ([@choldgraf](https://github.com/choldgraf))
- Install jupyterhub extension for jupyterlab [#139](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/139) ([@yuvipanda](https://github.com/yuvipanda))
- Use node 8, not 10 [#138](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/138) ([@yuvipanda](https://github.com/yuvipanda))
- Added existing property-path for tljh-config set method [#137](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/137) ([@ynnelson](https://github.com/ynnelson))
- Move tljh-config symlink to /usr/bin [#135](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/135) ([@yuvipanda](https://github.com/yuvipanda))
- Remove readthedocs.yml file [#131](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/131) ([@yuvipanda](https://github.com/yuvipanda))
- Switch back to a venv for docs + fix .circle config [#130](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/130) ([@yuvipanda](https://github.com/yuvipanda))
- Make it easier to run multiple independent integration tests [#129](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/129) ([@yuvipanda](https://github.com/yuvipanda))
- Add plugin support to the installer [#127](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/127) ([@yuvipanda](https://github.com/yuvipanda))
- removing extra copybutton files [#126](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/126) ([@choldgraf](https://github.com/choldgraf))
- adding copy button to code blocks and fixing the integration bug [#124](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/124) ([@choldgraf](https://github.com/choldgraf))
- updating content from zexuan's user test [#123](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/123) ([@choldgraf](https://github.com/choldgraf))
- Remove extreneous = [#119](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/119) ([@yuvipanda](https://github.com/yuvipanda))
- adding when to use tljh page [#118](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/118) ([@choldgraf](https://github.com/choldgraf))
- adding documentation for GitHub OAuth [#117](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/117) ([@choldgraf](https://github.com/choldgraf))
- Fix quick links in README [#113](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/113) ([@willirath](https://github.com/willirath))
- Install nbresuse by default [#111](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/111) ([@yuvipanda](https://github.com/yuvipanda))
- Re-organize installation documentation [#110](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/110) ([@yuvipanda](https://github.com/yuvipanda))
- Adding CI for documentation and fixing docs warnings [#107](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/107) ([@betatim](https://github.com/betatim))
- shared data and username emphasis [#103](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/103) ([@choldgraf](https://github.com/choldgraf))
- unittests for traefik [#96](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/96) ([@minrk](https://github.com/minrk))
- fix coverage uploads [#95](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/95) ([@minrk](https://github.com/minrk))
- Symlink tljh-config to /usr/local/bin [#94](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/94) ([@yuvipanda](https://github.com/yuvipanda))
- Document code-review practices [#93](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/93) ([@yuvipanda](https://github.com/yuvipanda))
- small updates to the docs [#91](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/91) ([@choldgraf](https://github.com/choldgraf))
- tests and fixes in tljh-config [#89](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/89) ([@minrk](https://github.com/minrk))
- Fix traefik config reload [#88](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/88) ([@yuvipanda](https://github.com/yuvipanda))
- Load arbitrary .py config files from a conf.d dir [#87](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/87) ([@yuvipanda](https://github.com/yuvipanda))
- Fix notebook user interface switching docs [#86](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/86) ([@yuvipanda](https://github.com/yuvipanda))
- Remove README note about HTTPS not being supported [#85](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/85) ([@yuvipanda](https://github.com/yuvipanda))
- Log bootstrap / installer messages to file as well [#82](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/82) ([@yuvipanda](https://github.com/yuvipanda))
- Add docs on using arbitrary authenticators [#80](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/80) ([@yuvipanda](https://github.com/yuvipanda))
- Customize theme to have better links in sidebar [#79](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/79) ([@yuvipanda](https://github.com/yuvipanda))
- Add tljh-config command [#77](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/77) ([@yuvipanda](https://github.com/yuvipanda))
- Clarify development status warnings [#76](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/76) ([@yuvipanda](https://github.com/yuvipanda))
- Use a venv to run unit tests [#74](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/74) ([@yuvipanda](https://github.com/yuvipanda))
- Add tutorial on how to use nbgitpuller [#73](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/73) ([@yuvipanda](https://github.com/yuvipanda))
- Use a venv to run unit tests [#72](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/72) ([@yuvipanda](https://github.com/yuvipanda))
- Update server requirements documentation [#69](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/69) ([@yuvipanda](https://github.com/yuvipanda))
- Add a how-to guide on selecting VM Memory / CPU / Disk size [#68](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/68) ([@yuvipanda](https://github.com/yuvipanda))
- Add HTTPS support with traefik [#67](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/67) ([@minrk](https://github.com/minrk))
- Replace pointers to yuvipanda/ on github with jupyterhub/ [#66](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/66) ([@yuvipanda](https://github.com/yuvipanda))
- Add doc on customizing installer [#65](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/65) ([@yuvipanda](https://github.com/yuvipanda))
- Use venv for base hub environment [#64](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/64) ([@yuvipanda](https://github.com/yuvipanda))
- fix typo in installer [#63](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/63) ([@gedankenstuecke](https://github.com/gedankenstuecke))
- jupyterhub 0.9.1, notebook 5.6.0 [#60](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/60) ([@minrk](https://github.com/minrk))
- move state outside envs [#59](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/59) ([@minrk](https://github.com/minrk))
- bootstrap: allow conda to be upgraded [#58](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/58) ([@minrk](https://github.com/minrk))
- Install nbgitpuller by default [#55](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/55) ([@yuvipanda](https://github.com/yuvipanda))
- Add option to install requirements.txt file on install [#53](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/53) ([@yuvipanda](https://github.com/yuvipanda))
- Fix link to custom tutorial [#52](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/52) ([@parente](https://github.com/parente))
- run integration tests with pytest [#43](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/43) ([@minrk](https://github.com/minrk))
- Minor typo [#40](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/40) ([@rprimet](https://github.com/rprimet))
- Install all python packages in hub environment with pip [#39](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/39) ([@yuvipanda](https://github.com/yuvipanda))
- Support using arbitrary set of installed authenticators [#37](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/37) ([@yuvipanda](https://github.com/yuvipanda))
- remove —no-cache-dir arg [#34](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/34) ([@minrk](https://github.com/minrk))
- Handle transient errors [#32](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/32) ([@rprimet](https://github.com/rprimet))
- Small text improvements + adding copy buttons to text blocks [#24](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/24) ([@choldgraf](https://github.com/choldgraf))
- update jetstream tutorial with links, minor fixes [#19](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/19) ([@ctb](https://github.com/ctb))
- Pour some tea 🍵 [#7](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/7) ([@rgbkrk](https://github.com/rgbkrk))
- minor fixes to dev-instructions [#6](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/6) ([@gedankenstuecke](https://github.com/gedankenstuecke))
- allow upgrade of miniconda during install [#3](https://github.com/jupyterhub/the-littlest-jupyterhub/pull/3) ([@gedankenstuecke](https://github.com/gedankenstuecke))

## Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterhub/the-littlest-jupyterhub/graphs/contributors?from=2018-06-15&to=2022-11-27&type=c))

[@1kastner](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3A1kastner+updated%3A2018-06-15..2022-11-27&type=Issues) | [@6palace](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3A6palace+updated%3A2018-06-15..2022-11-27&type=Issues) | [@AashitaK](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3AAashitaK+updated%3A2018-06-15..2022-11-27&type=Issues) | [@aboutaaron](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Aaboutaaron+updated%3A2018-06-15..2022-11-27&type=Issues) | [@Adrianhein](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3AAdrianhein+updated%3A2018-06-15..2022-11-27&type=Issues) | [@afonit](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Aafonit+updated%3A2018-06-15..2022-11-27&type=Issues) | [@ajhenley](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Aajhenley+updated%3A2018-06-15..2022-11-27&type=Issues) | [@altmas5](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Aaltmas5+updated%3A2018-06-15..2022-11-27&type=Issues) | [@alvinhuff](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Aalvinhuff+updated%3A2018-06-15..2022-11-27&type=Issues) | [@Amran2k16](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3AAmran2k16+updated%3A2018-06-15..2022-11-27&type=Issues) | [@anyushevai](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Aanyushevai+updated%3A2018-06-15..2022-11-27&type=Issues) | [@aolney](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Aaolney+updated%3A2018-06-15..2022-11-27&type=Issues) | [@astrojuanlu](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Aastrojuanlu+updated%3A2018-06-15..2022-11-27&type=Issues) | [@benbovy](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Abenbovy+updated%3A2018-06-15..2022-11-27&type=Issues) | [@betatim](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Abetatim+updated%3A2018-06-15..2022-11-27&type=Issues) | [@bjornarfjelldal](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Abjornarfjelldal+updated%3A2018-06-15..2022-11-27&type=Issues) | [@budgester](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Abudgester+updated%3A2018-06-15..2022-11-27&type=Issues) | [@CagtayFabry](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3ACagtayFabry+updated%3A2018-06-15..2022-11-27&type=Issues) | [@Carreau](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3ACarreau+updated%3A2018-06-15..2022-11-27&type=Issues) | [@cdibble](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Acdibble+updated%3A2018-06-15..2022-11-27&type=Issues) | [@cgawron](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Acgawron+updated%3A2018-06-15..2022-11-27&type=Issues) | [@cgodkin](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Acgodkin+updated%3A2018-06-15..2022-11-27&type=Issues) | [@choldgraf](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Acholdgraf+updated%3A2018-06-15..2022-11-27&type=Issues) | [@codecov](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Acodecov+updated%3A2018-06-15..2022-11-27&type=Issues) | [@consideRatio](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3AconsideRatio+updated%3A2018-06-15..2023-02-10&type=Issues) | [@cornhundred](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Acornhundred+updated%3A2018-06-15..2022-11-27&type=Issues) | [@ctb](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Actb+updated%3A2018-06-15..2022-11-27&type=Issues) | [@CyborgDroid](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3ACyborgDroid+updated%3A2018-06-15..2022-11-27&type=Issues) | [@danlester](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Adanlester+updated%3A2018-06-15..2022-11-27&type=Issues) | [@DataCascadia](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3ADataCascadia+updated%3A2018-06-15..2022-11-27&type=Issues) | [@davide84](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Adavide84+updated%3A2018-06-15..2022-11-27&type=Issues) | [@davidedelvento](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Adavidedelvento+updated%3A2018-06-15..2022-11-27&type=Issues) | [@deeplook](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Adeeplook+updated%3A2018-06-15..2022-11-27&type=Issues) | [@dependabot](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Adependabot+updated%3A2018-06-15..2022-11-27&type=Issues) | [@dongmok](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Adongmok+updated%3A2018-06-15..2022-11-27&type=Issues) | [@dschofield](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Adschofield+updated%3A2018-06-15..2022-11-27&type=Issues) | [@efedorov-dart](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Aefedorov-dart+updated%3A2018-06-15..2022-11-27&type=Issues) | [@EvilMav](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3AEvilMav+updated%3A2018-06-15..2022-11-27&type=Issues) | [@ewidl](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Aewidl+updated%3A2018-06-15..2022-11-27&type=Issues) | [@fermasia](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Afermasia+updated%3A2018-06-15..2022-11-27&type=Issues) | [@filippo82](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Afilippo82+updated%3A2018-06-15..2022-11-27&type=Issues) | [@fm75](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Afm75+updated%3A2018-06-15..2022-11-27&type=Issues) | [@fomightez](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Afomightez+updated%3A2018-06-15..2022-11-27&type=Issues) | [@fperez](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Afperez+updated%3A2018-06-15..2022-11-27&type=Issues) | [@Fregf](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3AFregf+updated%3A2018-06-15..2022-11-27&type=Issues) | [@frier-sam](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Afrier-sam+updated%3A2018-06-15..2022-11-27&type=Issues) | [@gabefair](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Agabefair+updated%3A2018-06-15..2022-11-27&type=Issues) | [@gantheaume](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Agantheaume+updated%3A2018-06-15..2022-11-27&type=Issues) | [@gedankenstuecke](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Agedankenstuecke+updated%3A2018-06-15..2022-11-27&type=Issues) | [@geoffbacon](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Ageoffbacon+updated%3A2018-06-15..2022-11-27&type=Issues) | [@GeorgianaElena](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3AGeorgianaElena+updated%3A2018-06-15..2022-11-27&type=Issues) | [@gillybops](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Agillybops+updated%3A2018-06-15..2022-11-27&type=Issues) | [@greg-dusek](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Agreg-dusek+updated%3A2018-06-15..2022-11-27&type=Issues) | [@gsemet](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Agsemet+updated%3A2018-06-15..2022-11-27&type=Issues) | [@Guillaume-Garrigos](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3AGuillaume-Garrigos+updated%3A2018-06-15..2022-11-27&type=Issues) | [@gutow](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Agutow+updated%3A2018-06-15..2022-11-27&type=Issues) | [@gvdr](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Agvdr+updated%3A2018-06-15..2022-11-27&type=Issues) | [@gyg-github](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Agyg-github+updated%3A2018-06-15..2022-11-27&type=Issues) | [@Hannnsen](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3AHannnsen+updated%3A2018-06-15..2022-11-27&type=Issues) | [@henfee](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Ahenfee+updated%3A2018-06-15..2022-11-27&type=Issues) | [@hoenie-ams](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Ahoenie-ams+updated%3A2018-06-15..2022-11-27&type=Issues) | [@huhuhang](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Ahuhuhang+updated%3A2018-06-15..2022-11-27&type=Issues) | [@iampatterson](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Aiampatterson+updated%3A2018-06-15..2022-11-27&type=Issues) | [@ian-r-rose](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Aian-r-rose+updated%3A2018-06-15..2022-11-27&type=Issues) | [@ibayer](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Aibayer+updated%3A2018-06-15..2022-11-27&type=Issues) | [@ikhoury](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Aikhoury+updated%3A2018-06-15..2022-11-27&type=Issues) | [@JavierHernandezMontes](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3AJavierHernandezMontes+updated%3A2018-06-15..2022-11-27&type=Issues) | [@jayvdb](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Ajayvdb+updated%3A2018-06-15..2022-11-27&type=Issues) | [@jdelamare](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Ajdelamare+updated%3A2018-06-15..2022-11-27&type=Issues) | [@jdkruzr](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Ajdkruzr+updated%3A2018-06-15..2022-11-27&type=Issues) | [@jeanmarcalkazzi](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Ajeanmarcalkazzi+updated%3A2018-06-15..2022-11-27&type=Issues) | [@jerpson](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Ajerpson+updated%3A2018-06-15..2022-11-27&type=Issues) | [@jhadjar](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Ajhadjar+updated%3A2018-06-15..2022-11-27&type=Issues) | [@jihobak](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Ajihobak+updated%3A2018-06-15..2022-11-27&type=Issues) | [@jkfm](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Ajkfm+updated%3A2018-06-15..2022-11-27&type=Issues) | [@JobinJohan](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3AJobinJohan+updated%3A2018-06-15..2022-11-27&type=Issues) | [@josiahls](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Ajosiahls+updated%3A2018-06-15..2022-11-27&type=Issues) | [@jprorama](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Ajprorama+updated%3A2018-06-15..2022-11-27&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Ajtpio+updated%3A2018-06-15..2022-11-27&type=Issues) | [@JuanCab](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3AJuanCab+updated%3A2018-06-15..2022-11-27&type=Issues) | [@junctionapps](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Ajunctionapps+updated%3A2018-06-15..2022-11-27&type=Issues) | [@jzf2101](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Ajzf2101+updated%3A2018-06-15..2022-11-27&type=Issues) | [@kafonek](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Akafonek+updated%3A2018-06-15..2022-11-27&type=Issues) | [@kannes](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Akannes+updated%3A2018-06-15..2022-11-27&type=Issues) | [@kevmk04](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Akevmk04+updated%3A2018-06-15..2022-11-27&type=Issues) | [@lachlancampbell](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Alachlancampbell+updated%3A2018-06-15..2022-11-27&type=Issues) | [@lambdaTotoro](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3AlambdaTotoro+updated%3A2018-06-15..2022-11-27&type=Issues) | [@laxdog](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Alaxdog+updated%3A2018-06-15..2022-11-27&type=Issues) | [@lee-hodg](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Alee-hodg+updated%3A2018-06-15..2022-11-27&type=Issues) | [@leouieda](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Aleouieda+updated%3A2018-06-15..2022-11-27&type=Issues) | [@leportella](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Aleportella+updated%3A2018-06-15..2022-11-27&type=Issues) | [@letianw91](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Aletianw91+updated%3A2018-06-15..2022-11-27&type=Issues) | [@Louren](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3ALouren+updated%3A2018-06-15..2022-11-27&type=Issues) | [@LTangaF](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3ALTangaF+updated%3A2018-06-15..2022-11-27&type=Issues) | [@lumbric](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Alumbric+updated%3A2018-06-15..2022-11-27&type=Issues) | [@luong-komorebi](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Aluong-komorebi+updated%3A2018-06-15..2022-11-27&type=Issues) | [@mangecoeur](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Amangecoeur+updated%3A2018-06-15..2022-11-27&type=Issues) | [@manics](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Amanics+updated%3A2018-06-15..2022-11-27&type=Issues) | [@MartijnZ](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3AMartijnZ+updated%3A2018-06-15..2022-11-27&type=Issues) | [@mauro3](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Amauro3+updated%3A2018-06-15..2022-11-27&type=Issues) | [@MayeulC](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3AMayeulC+updated%3A2018-06-15..2022-11-27&type=Issues) | [@mbenguig](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Ambenguig+updated%3A2018-06-15..2022-11-27&type=Issues) | [@mdpiper](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Amdpiper+updated%3A2018-06-15..2022-11-27&type=Issues) | [@meeseeksmachine](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Ameeseeksmachine+updated%3A2018-06-15..2022-11-27&type=Issues) | [@mgd722](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Amgd722+updated%3A2018-06-15..2022-11-27&type=Issues) | [@mhwasil](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Amhwasil+updated%3A2018-06-15..2022-11-27&type=Issues) | [@minrk](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Aminrk+updated%3A2018-06-15..2022-11-27&type=Issues) | [@mpkirby](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Ampkirby+updated%3A2018-06-15..2022-11-27&type=Issues) | [@mpound](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Ampound+updated%3A2018-06-15..2022-11-27&type=Issues) | [@MridulS](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3AMridulS+updated%3A2018-06-15..2022-11-27&type=Issues) | [@mskblackbelt](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Amskblackbelt+updated%3A2018-06-15..2022-11-27&type=Issues) | [@mtav](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Amtav+updated%3A2018-06-15..2022-11-27&type=Issues) | [@mukhendra](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Amukhendra+updated%3A2018-06-15..2022-11-27&type=Issues) | [@namin](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Anamin+updated%3A2018-06-15..2022-11-27&type=Issues) | [@nguyenvulong](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Anguyenvulong+updated%3A2018-06-15..2022-11-27&type=Issues) | [@norcalbiostat](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Anorcalbiostat+updated%3A2018-06-15..2022-11-27&type=Issues) | [@oisinBates](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3AoisinBates+updated%3A2018-06-15..2022-11-27&type=Issues) | [@olivierverdier](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Aolivierverdier+updated%3A2018-06-15..2022-11-27&type=Issues) | [@owah](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Aowah+updated%3A2018-06-15..2022-11-27&type=Issues) | [@parente](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Aparente+updated%3A2018-06-15..2022-11-27&type=Issues) | [@parmentelat](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Aparmentelat+updated%3A2018-06-15..2022-11-27&type=Issues) | [@paulnakroshis](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Apaulnakroshis+updated%3A2018-06-15..2022-11-27&type=Issues) | [@pbugnion](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Apbugnion+updated%3A2018-06-15..2022-11-27&type=Issues) | [@pnasrat](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Apbugnion+updated%3A2018-06-15..2023-10-02&type=Issues) | [@psychemedia](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Apsychemedia+updated%3A2018-06-15..2022-11-27&type=Issues) | [@ptcane](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Aptcane+updated%3A2018-06-15..2022-11-27&type=Issues) | [@pulponair](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Apulponair+updated%3A2018-06-15..2022-11-27&type=Issues) | [@raybellwaves](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Araybellwaves+updated%3A2018-06-15..2022-11-27&type=Issues) | [@rdmolony](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Ardmolony+updated%3A2018-06-15..2022-11-27&type=Issues) | [@rgbkrk](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Argbkrk+updated%3A2018-06-15..2022-11-27&type=Issues) | [@richardbrinkman](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Arichardbrinkman+updated%3A2018-06-15..2022-11-27&type=Issues) | [@RobinTTY](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3ARobinTTY+updated%3A2018-06-15..2022-11-27&type=Issues) | [@robnagler](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Arobnagler+updated%3A2018-06-15..2022-11-27&type=Issues) | [@rprimet](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Arprimet+updated%3A2018-06-15..2022-11-27&type=Issues) | [@rraghav13](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Arraghav13+updated%3A2018-06-15..2022-11-27&type=Issues) | [@scottkleinman](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Ascottkleinman+updated%3A2018-06-15..2022-11-27&type=Issues) | [@sethwoodworth](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Asethwoodworth+updated%3A2018-06-15..2022-11-27&type=Issues) | [@shireenrao](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Ashireenrao+updated%3A2018-06-15..2022-11-27&type=Issues) | [@silhouetted](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Asilhouetted+updated%3A2018-06-15..2022-11-27&type=Issues) | [@staeiou](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Astaeiou+updated%3A2018-06-15..2022-11-27&type=Issues) | [@stephen-a2z](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Astephen-a2z+updated%3A2018-06-15..2022-11-27&type=Issues) | [@story645](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Astory645+updated%3A2018-06-15..2022-11-27&type=Issues) | [@subgero](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Asubgero+updated%3A2018-06-15..2022-11-27&type=Issues) | [@sukhjitsehra](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Asukhjitsehra+updated%3A2018-06-15..2022-11-27&type=Issues) | [@support](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Asupport+updated%3A2018-06-15..2022-11-27&type=Issues) | [@t3chbg](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3At3chbg+updated%3A2018-06-15..2022-11-27&type=Issues) | [@tkang007](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Atkang007+updated%3A2018-06-15..2022-11-27&type=Issues) | [@TobiGiese](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3ATobiGiese+updated%3A2018-06-15..2022-11-27&type=Issues) | [@toccalenuvole73](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Atoccalenuvole73+updated%3A2018-06-15..2022-11-27&type=Issues) | [@tomliptrot](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Atomliptrot+updated%3A2018-06-15..2022-11-27&type=Issues) | [@trallard](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Atrallard+updated%3A2018-06-15..2022-11-27&type=Issues) | [@twrobinson](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Atwrobinson+updated%3A2018-06-15..2022-11-27&type=Issues) | [@VincePlantItAi](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3AVincePlantItAi+updated%3A2018-06-15..2022-11-27&type=Issues) | [@vsisl](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Avsisl+updated%3A2018-06-15..2022-11-27&type=Issues) | [@waltermateriais](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Awaltermateriais+updated%3A2018-06-15..2022-11-27&type=Issues) | [@welcome](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Awelcome+updated%3A2018-06-15..2022-11-27&type=Issues) | [@willingc](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Awillingc+updated%3A2018-06-15..2022-11-27&type=Issues) | [@willirath](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Awillirath+updated%3A2018-06-15..2022-11-27&type=Issues) | [@wjcapehart](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Awjcapehart+updated%3A2018-06-15..2022-11-27&type=Issues) | [@wqh17101](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Awqh17101+updated%3A2018-06-15..2022-11-27&type=Issues) | [@wrightaprilm](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Awrightaprilm+updated%3A2018-06-15..2022-11-27&type=Issues) | [@xavierliang](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Axavierliang+updated%3A2018-06-15..2022-11-27&type=Issues) | [@ynnelson](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Aynnelson+updated%3A2018-06-15..2022-11-27&type=Issues) | [@yuvipanda](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Ayuvipanda+updated%3A2018-06-15..2022-11-27&type=Issues) | [@znicholls](https://github.com/search?q=repo%3Ajupyterhub%2Fthe-littlest-jupyterhub+involves%3Aznicholls+updated%3A2018-06-15..2022-11-27&type=Issues)
