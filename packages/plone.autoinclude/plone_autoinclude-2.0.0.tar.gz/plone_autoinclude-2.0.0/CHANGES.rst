Changelog
=========


.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start

2.0.0 (2025-02-27)
------------------

Breaking changes:


- Support Plone 6.0, 6.1, 6.2, Python 3.9-3.13, and Buildout 4.
  Drop support for older Plone, Python and Buildout versions.
  Drop support for PyPy.  Technically it may still work, but we no longer test it.  It is irrelevant for Plone.
  [maurits] (#24)


Bug fixes:


- Fix importing module when the module name differs from the project name.
  This can easily happen with ``setuptools`` 75.8.1, though maybe 75.8.2 fixes it in some cases.
  [maurits] (#25)


1.0.1 (2022-12-10)
------------------

Bug fixes:


- Revert "Use setuptools/pkg_resources regex to compute safe name for a project" to fix an error importing packages with dashes. [davisagli] (#22)


1.0.0 (2022-12-01)
------------------

Bug fixes:


- Use setuptools/pkg_resources regex to compute safe name for a project.
  [gforcada] (#17)


1.0.0a5 (2022-05-24)
--------------------

New features:


- Raise an exception when a module is not found.
  When environment variable ``AUTOINCLUDE_ALLOW_MODULE_NOT_FOUND_ERROR=1`` is set, we log an error and continue.
  To accept ``ModuleNotFoundError`` only in specific packages, use a comma-separated list of project names, with or without spaces.
  See `issue 19 <https://github.com/plone/plone.autoinclude/issues/19>`_.
  [maurits] (#19)


1.0.0a4 (2022-02-23)
--------------------

Bug fixes:


- Replace dash with lowdash in project_name, as Python Project are normally divided by dash and modul name uses lowdash [MrTango] (#16)


1.0.0a3 (2021-12-03)
--------------------

Bug fixes:


- Decrease verbosity when loading packages (#11)


1.0.0a2 (2021-10-20)
--------------------

Bug fixes:


- Improved documentation, especially on how to include this.
  Added zcml in a ploneinclude directory to make this easier for now.
  [maurits] (#1)


1.0.0a1 (2021-10-15)
--------------------

New features:

- Initial release.
  [maurits, tschorr]
