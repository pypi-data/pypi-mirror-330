============
imagemounter
============

imagemounter is a command-line utility and Python package to ease the mounting and unmounting of EnCase, Affuse, vmdk
and dd disk images (and other formats supported by supported tools). It supports mounting disk images using xmount (with
optional RW cache), affuse, ewfmount and vmware-mount; detecting DOS, BSD, Sun, Mac and GPT volume systems; mounting
FAT, Ext, XFS UFS, HFS+, LUKS and NTFS volumes, in addition to some less known filesystems; detecting (nested) LVM
volume systems and mounting its subvolumes; and reconstructing Linux Software RAID arrays.

In its default mode, imagemounter will try to start mounting the base image on a temporary mount point,
detect the volume system and then mount each volume seperately. If it fails finding a volume system,
it will try to mount the entire image as a whole if it succeeds in detecting what it actually is.

This package supports Python 3.6+.

Example
=======
A very basic example of a valid mount is as follows. The command-line utility has much more features, but results vary
wildly depending on the exact type of disk you are trying to mount::

    # imount lvm_containing_dos_volumesystem_containing_ext4
    [+] Mounting image lvm_containing_dos_volumesystem_containing_ext4 using auto...
    [+] Mounted raw image [1/1]
    [+] Mounted volume 2.0 GiB 4.0.2:Ext4 / [Linux] on /tmp/im_4.0.2_8l86mZ.
    >>> Press [enter] to unmount the volume, or ^C to keep mounted...
    [+] Parsed all volumes!
    [+] Analysis complete, unmounting...
    [+] All cleaned up

If you want to see for yourself, you could try executing ``imount /dev/sda`` first.

Documentation
=============
Full documentation of this project is available from http://imagemounter.readthedocs.org/ or in the ``docs/`` directory.

Installation
============
This package does not require other packages, though ``termcolor`` is recommended and ``pytsk3`` is needed if you wish to
use this package for volume detection.

Just perform the following commands for a basic installation::

    apt-get install xmount ewf-tools afflib-tools sleuthkit
    pip3 install imagemounter-mitre
    imount --check

Use ``imount --check`` to verify which packages are (not) installed. Install additional packages as needed.

Contributing
============
Since imagemounter is an open source project, contributions of many forms are welcomed. Examples of possible
contributions include:

* Bug patches
* New features
* Documentation improvements
* Bug reports and reviews of pull requests


RELEASE STATEMENT
-----------------
Approved for Public Release; Distribution Unlimited. Public Release Case Number 22-3208.
