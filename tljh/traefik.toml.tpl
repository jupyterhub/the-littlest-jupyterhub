# traefik.toml static config file template
# dynamic config (e.g. TLS) goes in traefik-dynamic.toml.tpl

# enable API
[api]

[log]
level = "INFO"

# log errors, which could be proxy errors
[accessLog]
format = "json"

[accessLog.filters]
statusCodes = ["500-999"]

[accessLog.fields.headers.names]
Authorization = "redact"
Cookie = "redact"
Set-Cookie = "redact"
X-Xsrftoken = "redact"

[entryPoints]
  [entryPoints.http]
  address = ":{{ http['port'] }}"
  [entryPoints.http.transport.respondingTimeouts]
  idleTimeout = "10m"

  {% if https['enabled'] %}
  [entryPoints.http.http.redirections.entryPoint]
  to = "https"
  scheme = "https"

  [entryPoints.https]
  address = ":{{ https['port'] }}"
  [entryPoints.https.http.tls]
  options = "default"

  [entryPoints.https.transport.respondingTimeouts]
  idleTimeout = "10m"
  {% endif %}

  [entryPoints.auth_api]
  address = "localhost:{{ traefik_api['port'] }}"

{% if https['enabled'] and https['letsencrypt']['email'] and https['letsencrypt']['domains'] %}
[certificatesResolvers.letsencrypt.acme]
email = "{{ https['letsencrypt']['email'] }}"
storage = "acme.json"
{% if https['letsencrypt']['staging'] -%}
caServer = "https://acme-staging-v02.api.letsencrypt.org/directory"
{%- endif %}
[certificatesResolvers.letsencrypt.acme.tlsChallenge]
{% endif %}

[providers]
providersThrottleDuration = "0s"

[providers.file]
directory = "{{ traefik_dynamic_config_dir }}"
watch = true
