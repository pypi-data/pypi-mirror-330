============
BioInterface
============


.. image:: https://img.shields.io/pypi/v/biointerface.svg
        :target: https://pypi.python.org/pypi/biointerface

.. image:: https://readthedocs.org/projects/biointerface/badge/?version=latest
        :target: https://biointerface.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/MorfeoRenai/biointerface/shield.svg
     :target: https://pyup.io/repos/github/MorfeoRenai/biointerface/
     :alt: Updates


BioInterface is a `Biopython <https://biopython.org/>`_ based package that extracts Protein-DNA
interfaces in a PDB structures.

* Free software: MIT license
* Documentation: https://biointerface.readthedocs.io.


Get Started
-----------

This is a little tutorial on how to use the BioInterface package.

The official release is found in the Python Package Index (PyPI)

.. code-block:: console

    $ pip install biointerface

You can extract a single Protein-DNA interface from a single protein chain.

.. code-block:: python

    from Bio.PDB.MMCIFParser import MMCIFParser
    from biointerface import Interface, build_interfaces
    
    # parse and build structure with Biopython
    parser = MMCIFParser()
    structure = parser.get_structure(
        structure_id="1A02", filename="1a02-assembly1.cif"
    )
    
    # extract interface from a specific protein chain
    face = Interface(
        structure=structure,
        protein_chain_id="A",
        search_radius=5.0
    )
    face

.. code-block:: console

    <Interface chains=F:BA contacts=258 search_radius=5.0>

Check the official documentation for more information.


TODO
--------

* Proper tests (WIP)


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
