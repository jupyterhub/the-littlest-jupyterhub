(howto-providers-google)=

# Perform common Google Cloud configuration tasks

This page lists various common tasks you can perform on your
Google Cloud virtual machine.

(howto-providers-google-resize-disk)=

## Increasing your boot disk size
Google Cloud Compute Engine supports *increasing* (but not *decreasing*) the size of existing disks.
If you selected a boot disk with a supported version of **Ubuntu** or **Debian** as the operating 
system, then your boot disk can be resized easily from the console with these steps.

:::{note}
Google Cloud resizes the root partition and file system for *boot* disks with *public* images
(such as the TLJH supported **Ubuntu** and **Debian** images) automatically after your increase 
the size of your disk. If you have any other *non-boot* disks attached to your instance, you 
will need to perform extra steps yourself after resizing your disk. For more information on 
this and other aspects of resizing persistent disks, see 
[Google's documentation](https://cloud.google.com/compute/docs/disks/resize-persistent-disk). 
:::


1. Go to [Google Cloud Console -> Compute Engine -> VM instances](https://console.cloud.google.com/compute/instances) and select your TLJH instance.


1. Scroll down until you find your boot disk and select it.
   ```{image} ../../images/providers/google/boot-disk-resize.png
   :alt: Boot disk with Ubuntu jammy image
   ```


1. Select **Edit** in the top menu. This may require selecting the kebab menu (the 3 vertical dots).
   ```{image} ../../images/providers/google/boot-disk-edit-button.png
   :alt: Disk edit button
   ```


1. Update the **Size** property and save the changes at the bottom of the page.
   ```{image} ../../images/providers/google/boot-disk-resize-properties.png
   :alt: Boot disk size property
   ```


1. Reboot the VM instance by logging into your TLJH, opening the terminal, and running `sudo reboot`.
   You will lose your connection to the instance while it restarts. Once it comes back up, your disk
   will reflect your changes. You can verify that the automatic resize of your root partition and 
   file system took place by running `df -h` in the terminal, which will show the size of the disk 
   mounted on `/`:
   ```bash
   $ df -h
   Filesystem      Size  Used Avail Use% Mounted on
   /dev/root        25G  6.9G   18G  28% /
   tmpfs           2.0G     0  2.0G   0% /dev/shm
   tmpfs           785M  956K  784M   1% /run
   tmpfs           5.0M     0  5.0M   0% /run/lock
   /dev/sda15      105M  6.1M   99M   6% /boot/efi
   ```
