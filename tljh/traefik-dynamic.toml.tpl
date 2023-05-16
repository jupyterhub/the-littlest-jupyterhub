# traefik.toml dynamic config (mostly TLS)
# dynamic config in the static config file will be ignored
{% if https['enabled'] %}
[tls]
  [tls.options.default]
  minVersion = "VersionTLS12"
  cipherSuites = [
    "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
    "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
    "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
    "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
    "TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305",
    "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305",
  ]
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
