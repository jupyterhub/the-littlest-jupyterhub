.. _howto/admin/resource-estimation:

===================================
Estimate Memory / CPU / Disk needed
===================================

This page helps you estimate how much Memory / CPU / Disk the server you install
The Littlest JupyterHub on should have. These are just guidelines to help
with estimation - your actual needs will vary.

Memory
======

Memory is usually the biggest determinant of server size in most JupyterHub
installations. At minimum, your server must have at least **1GB** of RAM
for TLJH to install.

.. math::

    Recommended\, Memory =
    (Max\, concurrent\, users \times Max\, mem\, per\, user) + 128MB


The ``128MB`` is overhead for TLJH and related services. **Server Memory Recommended**
is the amount of Memory (RAM) the server you acquire should have - we recommend
erring on the side of 'more Memory'. The other terms are explained below.

Maximum concurrent users
------------------------

Even if your class has 100 students, most of them will not be using the JupyterHub
actively at a single given moment. At 2am on a normal night, maybe you'll have 10 students
using it. At 2am before a final, maybe you'll have 60 students using it. Maybe
you'll have a lab session with all 100 of your students using it at the same time.

The *maximum* number of users actively using the JupyterHub at any given time determines
how much memory your server will need. You'll get better at estimating this number
over time. We generally recommend between 40-60% of your total class size to start with.

Maximum memory allowed per user
-------------------------------

Depending on what kind of work your users are doing, they will use different amounts
of memory. The easiest way to determine this is to run through a typical user
workflow yourself, and measure how much memory is used. You can use :ref:`howto/admin/nbresuse`
to determine how much memory your user is using.

A good rule of thumb is to take the maximum amount of memory you used during
your session, and add 20-40% headroom for users to 'play around'. This is the
maximum amount of memory that should be given to each user.

If users use *more* than this alloted amount of memory, their notebook kernel will *restart*.

CPU
===

CPU estimation is more forgiving than Memory estimation. If there isn't
enough CPU for your users, their computation becomes very slow - but does not
stop, unlike with RAM.

.. math::

    Recommended\, CPU = (Max\, concurrent\, users \times Max\, CPU\, usage\, per\, user) + 20\%

The ``20%`` is overhead for TLJH and related services. This is around 20% of a
single modern CPU. This, of course, is just an estimate. We recommend using
the same process used to estimate Memory required for estimating CPU required.
You cannot use jupyter-resource-usage for this, but you should carry out normal workflow and
investigate the CPU usage on the machine.

Disk space
==========

Unlike Memory & CPU, disk space is predicated on **total** number of users,
rather than **maximum concurrent** users.

.. math::

    Recommended\, Disk\, Size = (Total\, users \times Max\, disk\, usage\, per\, user) + 2GB

Resizing your server
====================

Lots of cloud providers let your dynamically resize your server if you need it
to be larger or smaller. Usually this requires a restart of the whole server -
active users will be logged out, but otherwise usually nothing bad happens.
