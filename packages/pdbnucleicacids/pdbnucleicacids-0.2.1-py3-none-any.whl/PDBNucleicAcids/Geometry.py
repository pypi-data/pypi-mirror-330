"""Functions that address atom geometry."""

import numpy as np


def calculate_normal_vector(v1, v2, v3) -> np.float64:
    """Compute normal vector from three 3D points."""
    u1 = v2 - v1
    u2 = v3 - v1

    # Calcolo del vettore normale
    normal = np.cross(u1, u2)

    # Normalizzazione manuale del vettore normale
    norm = np.linalg.norm(normal)
    if norm == 0:
        raise ValueError("Vettore normale nullo")
    normal_normalized = normal / norm

    return normal_normalized


def angle_between_vectors(v1, v2) -> np.float64:
    """Compute angle between two vectors."""
    cos_theta = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

    return np.degrees(np.arccos(np.clip(cos_theta, -1.0, 1.0)))


def angle_between_planes(plane1, plane2) -> np.float64:
    """Compute angle between two planes, composed of three 3D points each."""
    v1, v2, v3 = plane1
    v4, v5, v6 = plane2

    normal1 = calculate_normal_vector(v1, v2, v3)
    normal2 = calculate_normal_vector(v4, v5, v6)

    angle = angle_between_vectors(normal1, normal2)

    return angle


def plane_separation(plane1, plane2) -> np.float64:
    """Calcola la distanza verticale tra due piani."""
    v1, v2, v3 = plane1
    v4, v5, v6 = plane2

    # Ottieni i vettori normali
    normal1 = calculate_normal_vector(v1, v2, v3)
    # normal2 = calculate_normal_vector(v4, v5, v6)

    # Ottieni i centri dei piani
    center1 = np.mean(plane1, axis=0)
    center2 = np.mean(plane2, axis=0)

    # Calcola il vettore tra i centri dei due piani
    center_vector = center2 - center1

    # Proietta il vettore tra i centri lungo la direzione del normale del
    # primo piano
    separation: np.float64 = abs(np.dot(center_vector, normal1))

    return separation
