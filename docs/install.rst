Installation
============

Install ``Sphinx-Test-Report`` via ``pip install sphinx-test-reports``.

After that the extension must to be added to the ``conf.py`` file::

   extensions = ['sphinxcontrib.needs',
                 'sphinxcontrib.test_reports',
                 'sphinxcontrib.plantuml']

Please note, ``Sphinx-Test-Report`` is based on the
`Sphinx-needs extension <https://sphinxcontrib-needs.readthedocs.io/en/latest/>`_.
Therefore it must also be added to the ``extensions`` list!

And same for `PlantUML <http://plantuml.com>`_, which is important to render flowcharts for filtered
test-cases.

More details can be find in the
`installation-guide <https://sphinxcontrib-needs.readthedocs.io/en/latest/installation.html>`_
of ``Sphinx-Needs``.

