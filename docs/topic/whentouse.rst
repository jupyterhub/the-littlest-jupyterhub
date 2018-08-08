.. _topic/whentouse:

===================================
When to use The Littlest JupyterHub
===================================

The Littlest JupyterHub allows you to deploy a JupyterHub serving user sessions
on a single VM (or your own hardware). The Zero to JupyterHub guide allows you
to deploy JupyterHub on Kubernetes, making it much more scalable.
This page is a brief guide to determining which is best for your use-case.
Many of these ideas were first laid out in a
`blog post announcing TLJH <http://words.yuvi.in/post/the-littlest-jupyterhub/>`_.

The Littlest JupyterHub
-----------------------

The Littlest JupyterHub (TLJH) is an opinionated and pre-configured distribution
to deploy a JupyterHub on a single virtual machine (or your own hardware).
It is designed to be a more lightweight, flexible, and maintainable solution
for use-cases where scalability and cost-savings are not a huge concern.

When to use TLJH
^^^^^^^^^^^^^^^^

* You want to provide easy access to a shared computational resource (CPU, RAM, data, etc)
* You only need to support up to ~100 people
* You aren't concerned about `over-provisioning your cluster <https://community.spiceworks.com/cloud/article/overprovisioning-servers-iaas>`_.
* You don't need production-level security promises for your deployment

TLJH main benefits
^^^^^^^^^^^^^^^^^^

* Simpler to deploy on many kinds of cloud services
* Faster to set up and tear down
* Allows administrators to quickly update user environments
* Is fairly simple in its technical makeup, reducing accidental complexity
* Supports any jupyter-based user workflows

TLJH main drawbacks
^^^^^^^^^^^^^^^^^^^

The Littlest JupyterHub is more lightweight and easy to deploy, which makes it poorly suited for
large userbases or more fine-grained control over the computational resources
your deployment uses. It also doesn't use containers (both a good and a bad thing)
which means it does not support some security and networking features that some
may find useful.


Zero to JupyterHub for Kubernetes
---------------------------------

The other main distribution for deploying JupyterHub is the
`Zero to JupyterHub on Kubernetes <https://z2jh.jupyter.org>`_ guide.
While Kubernetes is fantastic
for managing complex web infrastructure, sometimes it is a more complex
solution than needed. These points should help you decide if this is is the
tool for your use-case.

When to use Z2JH
^^^^^^^^^^^^^^^^

* You may have more than ~100 users at a time
* You do want to avoid over-provisioning your cluster
* You want the security features of containers and Kubernetes
* You want a more "production-ready" JupyterHub deployment

Z2JH main benefits
^^^^^^^^^^^^^^^^^^

* Runs on Kubernetes
* Scalable up to thousands of users
* More cost-effective at this scale (because you can automatically scale up/down the resources used)
* Uses container technology, and all the benefits that come with this
* Supports any user workflow that can run via a browser (Jupyter, RStudio, OpenRefine, etc)

Z2JH main drawbacks
^^^^^^^^^^^^^^^^^^^

JupyterHub on Kubernetes is more complex to deploy because Kubernetes is more
complex. In addition, a more limited number of cloud providers offer
one-click solutions for running Kubernetes. This may provide more technical
overhead than you wish.
