"""Testing the NucleicAcid module from PDBNucleicAcids."""

# import pytest
from Bio.PDB.MMCIFParser import MMCIFParser

# to be tested
from PDBNucleicAcids.NucleicAcid import NABuilder
from PDBNucleicAcids.NucleicAcid import DSNABuilder


def get_test_structure():
    filepath = "tests/data/gattaca.cif"
    parser = MMCIFParser(QUIET=True)
    structure = parser.get_structure("gattaca", filepath)

    return structure


def test_NABuilder():
    """Test per verificare il comportamento con residuo non nucleico."""
    structure = get_test_structure()

    builder = NABuilder()
    na_list = builder.build_nucleic_acids(structure)
    print(na_list)

    na = na_list[0]
    print(na.get_sequence())
    print(na.get_atoms())
    print(na.get_nucleic_acid_type())

    assert True


def test_DSNABuilder():
    """Test per verificare il comportamento con residuo non nucleico."""
    structure = get_test_structure()

    builder = DSNABuilder()
    dsna_list = builder.build_double_strands(structure)
    print(dsna_list)

    dsna = dsna_list[0]
    print(dsna.get_atoms())
    print(dsna.get_i_strand())
    print(dsna.get_j_strand())
    print(dsna.get_nucleic_acid_complex_type())
    print(dsna.get_stagger_values())
    print(dsna.get_dataframe())

    assert True
