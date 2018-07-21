# traefik.toml file template
{% if https['enabled'] %}
defaultEntryPoints = ["http", "https"]
{% else %}
defaultEntryPoints = ["http"]
{% endif %}

logLevel = "INFO"
# log errors, which could be proxy errors
[accessLog]
format = "json"
[accessLog.filters]
status = ["500-999"]

[respondingTimeouts]
idleTimeout = "10m0s"

[entryPoints]
  [entryPoints.http]
  address = ":{{http['port']}}"
  {% if https['enabled'] %}
    [entryPoints.http.redirect]
    entryPoint = "https"
  {% endif %}

  {% if https['enabled'] %}
  [entryPoints.https]
  address = ":{{https['port']}}"
  backend = "jupyterhub"
  [entryPoints.https.tls]
  {% if https['tls']['cert'] %}
    [[entryPoints.https.tls.certificates]]
      certFile = "{{https['tls']['cert']}}"
      keyFile = "{{https['tls']['key']}}"
  {% endif %}
  {% endif %}

{% if https['enabled'] and https['letsencrypt']['email'] %}
[acme]
email = "{{https['letsencrypt']['email']}}"
storage = "acme.json"
entryPoint = "https"
  [acme.httpChallenge]
  entryPoint = "http"

{% for domain in https['letsencrypt']['domains'] %}
[[acme.domains]]
  main = "{{domain}}"
{% endfor %}
{% endif %}

[file]

[frontends]
  [frontends.jupyterhub]
  backend = "jupyterhub"
  passHostHeader = true
[backends]
  [backends.jupyterhub]
    [backends.jupyterhub.servers.chp]
    url = "http://127.0.0.1:15003"

