=====
Usage
=====

To use PDBNucleicAcids in a project:

.. code-block:: python

    import PDBNucleicAcids

You can parse single stranded and double stranded nucleic acids.

.. code-block:: python

    from Bio.PDB.PDBList import PDBList
    from Bio.PDB.MMCIFParser import MMCIFParser
    from PDBNucleicAcids.NucleicAcid import DSNABuilder
    
    # retrive file from PDB using Biopython
    pdbl = PDBList()
    pdbl.retrieve_pdb_file(pdb_code="10MH", pdir=".")
    pdbl.retrieve_assembly_file(pdb_code="10MH", assembly_num=1, pdir=".")
    # ... or else use your own
    
    # parse and build structure with Biopython
    parser = MMCIFParser()
    structure = parser.get_structure(
         structure_id="10MH", filename="10mh-assembly1.cif"
    )
    
    # extract DataFrame with basepairs data
    builder = DSNABuilder()
    dsna_list = builder.build_double_strands(structure)
    
    # take the first double strand nucleic acid as an example
    dsna = dsna_list[0]
    dsna.get_dataframe()

.. code-block:: console

        i_chain_id  i_residue_index i_residue_name j_residue_name  j_residue_index j_chain_id
    0          B              402             DC             DG              433          C
    1          B              403             DC             DG              432          C
    2          B              404             DA             DT              431          C
    3          B              405             DT             DA              430          C
    4          B              406             DG             DC              429          C

In this case we have a gap in the basepairs at ``i_residue_index`` 407 and 408.
This results in two distinct paired segments of dsDNA.

In reality only 408 is a mispair. 407 is a non-standard 5CM-Guanine pair.
It's ignored by PDBNucleicAcids because it currently supports only standard Watson-Crick
basepairs.
