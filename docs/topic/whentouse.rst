.. _topic/whentouse:

===================================
When to use The Littlest JupyterHub
===================================

This page is a brief guide to determining whether to use The Littlest JupyterHub
(TLJH) or `Zero to JupyterHub for Kubernetes <https://zero-to-jupyterhub.readthedocs.io/en/latest/>`_ (Z2JH).
Many of these ideas were first laid out in a
`blog post announcing TLJH <http://words.yuvi.in/post/the-littlest-jupyterhub/>`_.

`**The Littlest JupyterHub (TLJH)** <https://the-littlest-jupyterhub.readthedocs.io/en/latest/>`_ is an opinionated and pre-configured distribution
to deploy a JupyterHub on a **single machine** (in the cloud or on your own hardware).
It is designed to be a more lightweight and maintainable solution
for use-cases where size, scalability, and cost-savings are not a huge concern.

`**Zero to JupyterHub on Kubernetes** <https://zero-to-jupyterhub.readthedocs.io/en/latest/>`_ allows you
to deploy JupyterHub on **Kubernetes**. This allows JupyterHub to scale to many thousands
of users, to flexibly grow/shrink the size of resources it needs, and to use
container technology in administering user sessions.

When to use TLJH vs. Z2JH
=========================

The choice between TLJH and Z2JH ultimately comes down to only a few questions:

1. Do you want your hub and all users to live on a **single, larger machine** vs. spreading users on a **cluster of smaller machines** that are scaled up or down?

   * If you can use a single machine, we recommend **The Littlest JupyterHub**.
   * If you wish to use multiple machines, we recommend **Zero to JupyterHub for Kubernetes**.
2. Do you **need to use container technology**?

   * If no, we recommend **The Littlest JupyterHub**.
   * If yes, we recommend **Zero to JupyterHub for Kubernetes**.
