# traefik.toml dynamic config (mostly TLS)
# dynamic config in the static config file will be ignored
{% if https['enabled'] %}
[tls]
  [tls.options.default]
  minVersion = "VersionTLS12"

  {% if https['tls']['cert'] -%}
  [tls.stores.default.defaultCertificate]
    certFile = "{{ https['tls']['cert'] }}"
    keyFile = "{{ https['tls']['key'] }}"
  {%- endif %}

  {% if https['letsencrypt']['email'] and https['letsencrypt']['domains'] -%}
  [tls.stores.default.defaultGeneratedCert]
  resolver = "letsencrypt"
    [tls.stores.default.defaultGeneratedCert.domain]
    main = "{{ https['letsencrypt']['domains'][0] }}"
    sans = [
      {% for domain in https['letsencrypt']['domains'][1:] -%}
      "{{ domain }}",
      {%- endfor %}
    ]
  {%- endif %}
{% endif %}
