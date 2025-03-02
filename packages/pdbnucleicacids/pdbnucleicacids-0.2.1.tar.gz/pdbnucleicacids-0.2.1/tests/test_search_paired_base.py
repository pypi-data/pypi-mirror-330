"""Testing the Pairing module from PDBNucleicAcids."""

# import pytest
from Bio.PDB.MMCIFParser import MMCIFParser

# to be tested
from PDBNucleicAcids.NucleicAcid import search_paired_base


def get_test_structure():
    filepath = "tests/data/gattaca.cif"
    parser = MMCIFParser(QUIET=True)
    structure = parser.get_structure("gattaca", filepath)

    # reset hetero-atom flag
    # for residue in structure.get_residues():
    #     residue_id = list(residue.id)
    #     residue_id[0] = " "
    #     residue.id = tuple(residue_id)

    return structure


def test_invalid_residue():
    """Test per verificare il comportamento con residuo non nucleico."""
    structure = get_test_structure()

    # Rinomina un residuo nucleico (es: guanina)
    # in un residuo non nucleico (es: istidina)
    invalid_residue = structure[0]["A"][1]
    invalid_residue.resname = "HIS"

    assert search_paired_base(invalid_residue) is None


def test_no_paired_base_found():
    """Test per verificare quando non viene trovata una base complementare."""
    structure = get_test_structure()

    # Prendiamo solo la prima guanina
    guanine = structure[0]["A"][1]

    # Rimuoviamo la citosina appaiata con la guanina
    structure[0]["B"].detach_child((" ", -1, " "))

    assert search_paired_base(guanine) is None


def test_paired_base_found():
    """Test per verificare quando viene trovata una base complementare."""
    structure = get_test_structure()

    # Prendiamo la prima guanina e la prima citosina
    guanine = structure[0]["A"][1]
    cytosine = structure[0]["B"][-1]

    assert search_paired_base(guanine) is cytosine


def test_invalid_geometry():
    """Test per verificare quando la geometria del legame è invalida."""
    structure = get_test_structure()

    # Prendiamo la prima guanina e la prima citosina
    guanine = structure[0]["A"][1]
    cytosine = structure[0]["B"][-1]

    # Modifichiamo la posizione dell'atomo per rendere la geometria invalida
    # (distanza troppo grande)
    cytosine["N3"].set_coord([10, 0, 0])

    assert search_paired_base(guanine) is None


# def test_multiple_paired_bases():
#     """Test per verificare la gestione di più basi complementari."""
#     structure = setup_mock_structure()

#     # Prendiamo l'adenina e la timina corretta
#     chain = structure[0]["A"]
#     adenine = chain[1]

#     result = search_paired_base(
#         adenine,
#         nucleic_chain_ids=["A"],
#         pairing_rules=mock_WatsonCrickBasePairsRules,
#     )

#     # Assumi che la funzione prenda la prima base valida
#     assert result is None
