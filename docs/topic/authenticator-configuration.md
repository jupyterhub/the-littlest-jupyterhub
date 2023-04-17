(topic-authenticator-configuration)=

# Configuring JupyterHub authenticators

Any [JupyterHub authenticator](https://github.com/jupyterhub/jupyterhub/wiki/Authenticators)
can be used with TLJH. A number of them ship by default with TLJH:

1. [OAuthenticator](https://github.com/jupyterhub/oauthenticator) - Google, GitHub, CILogon,
   GitLab, Globus, Mediawiki, auth0, generic OpenID connect (for KeyCloak, etc) and other
   OAuth based authentication methods.
2. [LDAPAuthenticator](https://github.com/jupyterhub/ldapauthenticator) - LDAP & Active Directory.
3. [DummyAuthenticator](https://github.com/yuvipanda/jupyterhub-dummy-authenticator) - Any username,
   one shared password. A [how-to guide on using DummyAuthenticator](howto-auth-dummy) is also
   available.
4. [FirstUseAuthenticator](https://github.com/yuvipanda/jupyterhub-firstuseauthenticator) - Users set
   their password when they log in for the first time. Default authenticator used in TLJH.
5. [TmpAuthenticator](https://github.com/jupyterhub/tmpauthenticator) - Opens the JupyterHub to the
   world, makes a new user every time someone logs in.
6. [NativeAuthenticator](https://native-authenticator.readthedocs.io/en/latest/) - Allow users to signup, add password security verification and block users after failed attempts oflogin.

We try to have specific how-to guides & tutorials for common authenticators. Since we can not cover
everything, this guide shows you how to use any authenticator you want with JupyterHub by following
the authenticator's documentation.

## Setting authenticator properties

JupyterHub authenticators are customized by setting _traitlet properties_. In the authenticator's
documentation, you will find these are usually represented as:

```python
c.<AuthenticatorName>.<property-name> = <some-value>
```

You can set these with `tljh-config` with:

```bash
sudo tljh-config set auth.<AuthenticatorName>.<property-name> <some-value>
```

### Example

[LDAPAuthenticator's documentation](https://github.com/jupyterhub/ldapauthenticator#required-configuration)
lists the various configuration options you can set for LDAPAuthenticator.
When the documentation asks you to set `LDAPAuthenticator.server_address`
to some value, you can do that with the following command:

```bash
sudo tljh-config set auth.LDAPAuthenticator.server_address 'my-ldap-server'
```

Most authenticators require you set multiple configuration options before you can
enable them. Read the authenticator's documentation carefully for more information.

## Enabling the authenticator

Once you have configured the authenticator as you want, you should then
enable it. Usually, the documentation for the authenticator would ask you to add
something like the following to your `jupyterhub_config.py` to enable it:

```python
c.JupyterHub.authenticator_class = 'fully-qualified-authenticator-name'
```

You can accomplish the same with `tljh-config`:

```bash
sudo tljh-config set auth.type <fully-qualified-authenticator-name>
```

Once enabled, you need to reload JupyterHub for the config to take effect.

```bash
sudo tljh-config reload
```

Try logging in a separate incognito window to check if your configuration works. This
lets you preserve your terminal in case there were errors. If there are
errors, [](/troubleshooting/logs) should help you debug them.

### Example

From the [documentation](https://github.com/jupyterhub/ldapauthenticator#usage) for
LDAPAuthenticator, we see that the fully qualified name is `ldapauthenticator.LDAPAuthenticator`.
Assuming you have already configured it, the following commands enable LDAPAuthenticator.

```bash
sudo tljh-config set auth.type ldapauthenticator.LDAPAuthenticator
sudo tljh-config reload
```
