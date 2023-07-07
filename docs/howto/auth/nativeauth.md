(howto-auth-nativeauth)=

# Let users sign up with a username and password

```{warning}
This documentation is not being updated regularly and may be out of date. Due to
that, please only use this _as a complement_ to the official
[NativeAuthenticator documentation].

[NativeAuthenticator documentation]: https://native-authenticator.readthedocs.io/en/latest/

Going onwards, the goal is to ensure we have good documentation in the
NativeAuthenticator project and reference that instead of maintaining similar
documentation in this project also.
```

The **Native Authenticator** lets users signup for creating a new username
and password.
When they signup, they won't be able to login until they are authorized by an
admin. Users that are characterized as admin have to signup as well, but they
will be authorized automatically.

## Enabling the authenticator

Enable the authenticator and reload config to apply the configuration:

```bash
sudo tljh-config set auth.type nativeauthenticator.NativeAuthenticator
sudo tljh-config reload
```

## Allowing all users to be authorized after signup

By default, all users created on signup don't have authorization to login.
If you wish to allow **any** user to access
the JupyterHub just after the signup, run the following command:

```bash
tljh-config set auth.NativeAuthenticator.open_signup true
tljh-config reload
```

## Optional features

More optional features are available on the `authenticator documentation <https://native-authenticator.readthedocs.io/en/latest/>`
