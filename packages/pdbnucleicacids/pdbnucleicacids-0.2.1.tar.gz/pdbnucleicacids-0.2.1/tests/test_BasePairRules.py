"""Tests for the BasePairRules module from PDBNucleicAcids."""

import pytest
import numpy as np
from unittest.mock import MagicMock
from Bio.PDB.Residue import Residue
from Bio.PDB.Atom import Atom

# to be tested
from PDBNucleicAcids.BasePairRules import dsDNAWatsonCrickBasePairRules


@pytest.fixture
def mock_residue():
    """Fixture for creating a mock residue with specific atoms."""
    residue = MagicMock(spec=Residue)
    residue.get_resname.return_value = "DA"
    residue.atoms = {
        "N1": Atom("N1", np.array([0.0, 0.0, 0.0]), 1.0, 1.0, " ", "N1", 1),
        "C2": Atom("C2", np.array([1.0, 0.0, 0.0]), 1.0, 1.0, " ", "C2", 2),
        "C6": Atom("C6", np.array([0.0, 1.0, 0.0]), 1.0, 1.0, " ", "C6", 3),
    }
    residue.__getitem__.side_effect = residue.atoms.__getitem__

    # Aggiunta del parent come catena mock
    chain = MagicMock()
    chain.id = "A"  # Identificatore della catena
    residue.parent = chain

    return residue


@pytest.fixture
def complementary_residue():
    """Fixture for creating a complementary mock residue."""
    residue = MagicMock(spec=Residue)
    residue.get_resname.return_value = "DT"
    residue.atoms = {
        "N3": Atom("N3", np.array([0.0, 0.0, 2.5]), 1.0, 1.0, " ", "N3", 4),
        "C2": Atom("C2", np.array([1.0, 0.0, 2.5]), 1.0, 1.0, " ", "C2", 5),
        "C4": Atom("C4", np.array([0.0, 1.0, 2.5]), 1.0, 1.0, " ", "C4", 6),
    }
    residue.__getitem__.side_effect = residue.atoms.__getitem__

    # Aggiunta del parent come un'altra catena mock
    chain = MagicMock()
    chain.id = "B"  # Identificatore della catena, diverso da mock_residue
    residue.parent = chain

    return residue


@pytest.fixture
def base_pair_rules():
    """Fixture for the dsDNAWatsonCrickBasePairRules instance."""
    return dsDNAWatsonCrickBasePairRules()


def test_initialization(base_pair_rules):
    """Test to verify base parameters initialization."""
    assert base_pair_rules.max_distance == 4
    assert base_pair_rules.max_angle == 65
    assert base_pair_rules.max_stagger == 2.5
    assert ("DA", "DT") in base_pair_rules.complementary_pairs


def test_is_different_residue(
    base_pair_rules, mock_residue, complementary_residue
):
    """Test to verify same/different bases."""
    # Positive test, two different complementary base
    assert base_pair_rules.is_different_residue(
        mock_residue, complementary_residue
    )

    # same base
    assert not base_pair_rules.is_different_residue(mock_residue, mock_residue)
    assert not base_pair_rules.is_candidate(mock_residue, mock_residue)


def test_is_complementary(
    base_pair_rules, mock_residue, complementary_residue
):
    """Test to verify base complementarity."""
    # Positive test, complementary base
    assert base_pair_rules.is_complementary(
        mock_residue, complementary_residue
    )

    # not complementary base
    complementary_residue.get_resname.return_value = "DG"
    assert not base_pair_rules.is_complementary(
        mock_residue, complementary_residue
    )
    assert not base_pair_rules.is_candidate(
        mock_residue, complementary_residue
    )


def test_is_from_different_chain(
    base_pair_rules, mock_residue, complementary_residue
):
    """Test to verify base complementarity."""
    # Positive test, different chains
    assert base_pair_rules.is_from_different_chain(
        mock_residue, complementary_residue
    )

    # same chain
    complementary_residue.parent = mock_residue.parent

    assert not base_pair_rules.is_from_different_chain(
        mock_residue, complementary_residue
    )
    assert not base_pair_rules.is_candidate(
        mock_residue, complementary_residue
    )


def test_is_valid_distance(
    base_pair_rules, mock_residue, complementary_residue
):
    """Test to verify valid distance between bases."""
    # Positive test
    assert base_pair_rules.is_valid_distance(
        mock_residue, complementary_residue
    )

    # Test with larger distance
    complementary_residue["N3"].coord = np.array([0.0, 0.0, 8.0])

    assert not base_pair_rules.is_valid_distance(
        mock_residue, complementary_residue
    )
    assert not base_pair_rules.is_candidate(
        mock_residue, complementary_residue
    )

    # internal methods return None
    mock_residue.get_resname.return_value = "HOH"
    assert not base_pair_rules.is_valid_distance(
        mock_residue, complementary_residue
    )


def test_is_valid_angle(base_pair_rules, mock_residue, complementary_residue):
    """Test to verify valid angle between bases."""
    # Positive test
    assert base_pair_rules.is_valid_angle(mock_residue, complementary_residue)

    # Out-of-limit angle
    complementary_residue["N3"].coord = np.array([0.0, 0.0, 8.0])

    assert not base_pair_rules.is_valid_angle(
        mock_residue, complementary_residue
    )
    assert not base_pair_rules.is_candidate(
        mock_residue, complementary_residue
    )

    # internal methods return None
    mock_residue.get_resname.return_value = "HOH"
    assert not base_pair_rules.is_valid_angle(
        mock_residue, complementary_residue
    )


def test_is_valid_stagger(
    base_pair_rules, mock_residue, complementary_residue
):
    """Test to verify valid angle between bases."""
    # Positive test
    assert base_pair_rules.is_valid_stagger(
        mock_residue, complementary_residue
    )

    # Out-of-limit angle
    complementary_residue["N3"].coord[2] = 3
    complementary_residue["C2"].coord[2] = 3
    complementary_residue["C4"].coord[2] = 3

    assert not base_pair_rules.is_valid_stagger(
        mock_residue, complementary_residue
    )
    assert not base_pair_rules.is_candidate(
        mock_residue, complementary_residue
    )

    # internal methods return None
    mock_residue.get_resname.return_value = "HOH"
    assert not base_pair_rules.is_valid_stagger(
        mock_residue, complementary_residue
    )


def test_is_candidate(base_pair_rules, mock_residue, complementary_residue):
    """Test to verify if a pair of bases meets candidate criteria."""
    # Positive test
    assert base_pair_rules.is_candidate(mock_residue, complementary_residue)

    # non-nucleic residue test
    mock_residue.get_resname.return_value = "LYS"
    assert not base_pair_rules.is_candidate(
        mock_residue, complementary_residue
    )

    # non-nucleic residue test
    mock_residue.get_resname.return_value = "DA"
    complementary_residue.get_resname.return_value = "LYS"
    assert not base_pair_rules.is_candidate(
        mock_residue, complementary_residue
    )

    # non-standard nucleic base test
    mock_residue.get_resname.return_value = "A2L"
    complementary_residue.get_resname.return_value = "DA"
    assert not base_pair_rules.is_candidate(
        mock_residue, complementary_residue
    )

    # non-standard nucleic base test
    mock_residue.get_resname.return_value = "DA"
    complementary_residue.get_resname.return_value = "A2L"
    assert not base_pair_rules.is_candidate(
        mock_residue, complementary_residue
    )
