"""Testing the Geometry module from PDBNucleicAcids."""

import pytest
import numpy as np

# to be tested
from PDBNucleicAcids.Geometry import calculate_normal_vector
from PDBNucleicAcids.Geometry import angle_between_vectors
from PDBNucleicAcids.Geometry import angle_between_planes
from PDBNucleicAcids.Geometry import plane_separation


def test_calculate_normal_vector():
    # Definisce tre punti che giacciono su un piano
    v1 = np.array([1, 0, 0])
    v2 = np.array([0, 1, 0])
    v3 = np.array([0, 0, 1])
    # Calcola il vettore normale atteso per questi punti
    expected_normal = np.array([1, 1, 1]) / np.sqrt(3)
    # Testa che il risultato sia come atteso
    result = calculate_normal_vector(v1, v2, v3)
    assert np.allclose(
        result, expected_normal
    ), f"Expected {expected_normal}, got {result}"

    # Testa il caso limite in cui i punti sono collineari
    v1, v2, v3 = np.array([0, 0, 0]), np.array([1, 1, 1]), np.array([2, 2, 2])
    with pytest.raises(ValueError, match="Vettore normale nullo"):
        calculate_normal_vector(v1, v2, v3)


def test_angle_between_vectors():
    # Definisce due vettori perpendicolari
    v1 = np.array([1, 0, 0])
    v2 = np.array([0, 1, 0])
    # L'angolo atteso tra di essi è di 90 gradi
    assert angle_between_vectors(v1, v2) == pytest.approx(90.0, rel=1e-6)

    # Testa due vettori paralleli
    v1 = np.array([1, 1, 0])
    v2 = np.array([2, 2, 0])
    # L'angolo atteso è 0 gradi
    assert angle_between_vectors(v1, v2) == pytest.approx(0.0, abs=1e-5)

    # Testa due vettori opposti
    v1 = np.array([1, 0, 0])
    v2 = np.array([-1, 0, 0])
    # L'angolo atteso è 180 gradi
    assert angle_between_vectors(v1, v2) == pytest.approx(180.0, rel=1e-6)


def test_angle_between_planes():
    # Definisce due piani ortogonali
    plane1 = [np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([0, 0, 0])]
    plane2 = [np.array([0, 0, 0]), np.array([0, 1, 0]), np.array([0, 0, 1])]
    # L'angolo atteso è di 90 gradi
    assert angle_between_planes(plane1, plane2) == pytest.approx(
        90.0, rel=1e-6
    )

    # Testa due piani paralleli
    plane1 = [np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([0, 1, 0])]
    plane2 = [np.array([0, 0, 1]), np.array([1, 0, 1]), np.array([0, 1, 1])]
    # L'angolo atteso è di 0 gradi
    assert angle_between_planes(plane1, plane2) == pytest.approx(0.0, rel=1e-6)


def test_plane_separation():
    # Due piani paralleli separati da una distanza di 1 lungo l'asse Z
    plane1 = [np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([0, 1, 0])]
    plane2 = [np.array([0, 0, 1]), np.array([1, 0, 1]), np.array([0, 1, 1])]
    # La separazione verticale attesa è 1
    assert plane_separation(plane1, plane2) == pytest.approx(1.0, rel=1e-6)

    # Testa due piani coincidenti
    plane1 = [np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([0, 1, 0])]
    plane2 = [np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([0, 1, 0])]
    # La separazione attesa è 0
    assert plane_separation(plane1, plane2) == pytest.approx(0.0, rel=1e-6)
