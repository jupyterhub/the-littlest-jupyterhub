.. _howto/resource-estimation:

===================================
Estimate Memory / CPU / Disk needed
===================================

This page helps you estimate how much Memory / CPU / Disk the server you install
The Littlest JupyterHub on should have. These are just guidelines to help
with estimation - your actual needs will vary.

Memory
======

Memory is usually the biggest determinant of server size in most JupyterHub
installations.

.. math::

    Server Memory Recommended = (Maximum concurrent users \times Maximum memory allowed per user) + 128MB


The ``128MB`` is overhead for TLJH and related services. **Server Memory Recommended**
is the amount of Memory (RAM) the server you aquire should have - we recommend
erring on the side of 'more Memory'. The other terms are explained below.

Maximum concurrent users
------------------------

Even if your class has 100 students, most of them will not be using the JupyterHub
actively at an given moment. At 2am on a normal night, maybe you'll have 10 students
using it. At 2am before a final, maybe you'll have 60 students using it. Maybe
you'll have a lab session with all 100 of your students using it at the same time.

The *maximum* number of users actively using the JupyterHub at any given time determines
how much memory your server will need. You'll get better at estimating this number
over time. We generally recommend between 40-60% of your total class size to start with.

Maximum memory allowed per user
-------------------------------

Depending on what kinda work your users are doing, they will use different amounts
of memory. The easiest way to determine this is to run through a typical user
workflow yourself, and measure how much memory is used. You can use :ref:`howto/nbresuse`
to determine how much memory your user is using.

A good rule of thumb is to take the maximum amount of memory you used during
your session, and add 20-40% headroom for users to 'play around'. This is the
maximum amount of memory that should be given to each user.

If users use *more* than this alloted amount of memory, their notebook kernel will restart.

CPU
===

CPU estimation is more forgiving than Memory estimation. If there isn't
enough CPU for your users, their computation becomes very slow - but does not
stop, unlike with RAM.

.. math::

    Server CPU Recommended = (Maximum concurrent users \times Maximum CPU usage per user) + 0.2

The ``0.2`` is overhead for TLJH and related services. **Server CPU Recommended**
is the amount of CPU the server you acquire should have. We recommend using
the same process used to estimate Memory required for estimating CPU required.

Disk space
==========

Unlike Memory & CPU, disk space is predicated on **total** number of users,
rather than **maximum concurrent** users.

.. math::

    Server Disk Size Recommended = (Total \times Maximum disk usage per user) + 2GB

Resizing your server
====================

Lots of cloud providers let your dynamically resize your server if you need it
to be larger or smaller. Usually this requires a restart of the whole server -
active users will be logged out, but otherwise usually nothing bad happens.
