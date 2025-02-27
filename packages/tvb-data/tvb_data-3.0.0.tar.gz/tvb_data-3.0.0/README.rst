TVB Data
========

Various demonstration datasets for use with The Virtual Brain are provided here.

Here you will find:

* compatible file/folder structures that can be uploaded thorugh the web interface of TVB
* the default datasets used when working in ``console`` or `library` mode.

Integration of tvb-data with Datalad
------------------------------------
This package makes use of the `Datalad <https://www.datalad.org/>`_ management system, making *tvb-data* a Datalad `dataset`.

Datalad allows large repositories to store their entire file structure (i.e. organisation into files and folders) on
a repository hosting service (e.g. GitHub, GitLab, Bitbucket, etc.), while the actual `content` of large files is stored
on a separate external storage.

This makes it possible for this repository to store its regular-sized data here, on GitLab, and larger files on external resources.
For this reason, when cloning this repository, the contents of some large files (e.g. ``tvb_data/Default_Project.zip``)
will not be available and you will have to retrieve it from the file storage.

The following section is a walkthrough on how to install all the necessary tools, clone this repository and download
the content of large files, in order to be able to use this package.

How to install tvb-data from GitLab
===================================


Pre-requisites
--------------

Before installing Datalad, you should make sure you have the following tools installed:

* Git: https://git-scm.com/downloads
* Git-annex (for storing/retrieving large files): https://git-annex.branchable.com/install

Installing Datalad
------------------
The installation process for Datalad, depending on your OS, is thoroughly explained here:
https://handbook.datalad.org/en/latest/intro/installation.html. Moreover, the following command is OS-agnostic and
installs datalad on any system::

    pip install datalad

Installing tvb-data
-------------------
You should clone this repository, either with HTTPS or SSH. After that::

    cd tvb-datalad
    # download the content of all large files (approx. 176 MB) stored externally
    datalad get .

*You can learn more about this mechanism here:* https://handbook.datalad.org/en/latest/basics/101-105-install.html#keep-whatever-you-like

Now that you have all the contents of this repository on your local machine, you can go ahead and treat it like any other python module,
installing it using::

    pip install -e .

Installing tvb-data from PyPi
=============================

`tvb-data` also is shared on Pypi, but it has fewer files, due to size restrictions there.
To work with this package from pypi, run::

    pip install tvb-data

Further Resources
=================

- For issue tracking we are using Jira: https://tvb-projects.atlassian.net/jira
- For API documentation and live demos, have a look here: http://docs.thevirtualbrain.org
- A public mailing list for users of The Virtual Brain can be joined and followed using: tvb-users@googlegroups.com
- Raw demo IPython Notebooks can be found under: https://github.com/the-virtual-brain/tvb-documentation/tree/master/demos
- Data from here will be used by `tvb-library` and `tvb-framework` packages on Pypi
- For more information on Datalad and tutorials, their official Handbook is a great resource: https://handbook.datalad.org/en/latest
