.. This README is meant for consumption by humans and PyPI. PyPI can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on PyPI or github. It is a comment.

.. image:: https://github.com/imio/imio.fpaudit/actions/workflows/plone-package.yml/badge.svg
    :target: https://github.com/imio/imio.fpaudit/actions/workflows/plone-package.yml

.. image:: https://coveralls.io/repos/github/imio/imio.fpaudit/badge.svg?branch=main
    :target: https://coveralls.io/github/imio/imio.fpaudit?branch=main
    :alt: Coveralls

.. image:: https://codecov.io/gh/imio/imio.fpaudit/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/imio/imio.fpaudit

.. image:: https://img.shields.io/pypi/v/imio.fpaudit.svg
    :target: https://pypi.python.org/pypi/imio.fpaudit/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/imio.fpaudit.svg
    :target: https://pypi.python.org/pypi/imio.fpaudit
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/imio.fpaudit.svg?style=plastic   :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/imio.fpaudit.svg
    :target: https://pypi.python.org/pypi/imio.fpaudit/
    :alt: License

=============
imio.fpaudit
=============

Fingerpointing log audit helper

Features
========

- logs can be defined in a plone configlet
- an helper method `utils.fplog` can be used to write to a defined log file
- a template (collective.documentgenerator) can be used to generate an ods or xls file from the logs.
  The template object must define the following context vars:

    * log_id: the id of the log to use
    * actions: a list of actions to filter on (ex: AUDIT,ERROR)
    * extras: a list of extra fields to use in the template (ex: col_a,col_b)

Translations
============

This product has been translated into

- Klingon (thanks, K'Plai)

Installation
============

Install imio.fpaudit by adding it to your buildout::

    [buildout]

    ...

    eggs =
        imio.fpaudit

It is also necessary to include some config lines in instance zope.conf or in buildout config,
where xxx is the path to the plone site::

    [instance]
    zope-conf-additional +=
       <product-config imio.fpaudit>
         plone-path xxx
       </product-config>

and then running ``bin/buildout``

Contribute
==========

- Issue Tracker: https://github.com/imio/imio.fpaudit/issues
- Source Code: https://github.com/imio/imio.fpaudit

License
=======

The project is licensed under the GPLv2.
