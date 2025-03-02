=====
Usage
=====

To use BioInterface in a Python project:

.. code-block:: python

    import biointerface

You can extract a single Protein-DNA interface from a single protein chain.

.. code-block:: python

    from Bio.PDB.PDBList import PDBList
    from Bio.PDB.MMCIFParser import MMCIFParser
    from biointerface import Interface, build_interfaces

    # retrive file from PDB using Biopython
    pdbl = PDBList()
    pdbl.retrieve_pdb_file(pdb_code="1A02", pdir=".")
    pdbl.retrieve_assembly_file(pdb_code="1A02", assembly_num=1, pdir=".")
    # ... or else use your own
    
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

You can also extract all Protein-DNA interface from an entire structure.

.. code-block:: python

    face_list = build_interfaces(structure=structure, search_radius=5.0)
    face_list

.. code-block:: console

    [<Interface chains=J:BA contacts=189 search_radius=5.0>,
     <Interface chains=F:BA contacts=258 search_radius=5.0>,
     <Interface chains=N:BA contacts=529 search_radius=5.0>]