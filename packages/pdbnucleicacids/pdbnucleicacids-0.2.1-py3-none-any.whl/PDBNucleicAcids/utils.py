"""Utils."""

import pandas as pd


def get_paired_segments(df: pd.DataFrame) -> list[int]:
    """
    Get paired segments indexes.

    A - T      0
    T - A      0
    A - T      0
    C   C  ->       ->  [0, 0, 0, 1, 1, 1]
    T   A
    C - G      1
    G - C      1
    T - A      1

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with basepairs data.

    Returns
    -------
    list[int]
        An array of integers of the same length of the input dataframe.
        Integers identify the uninterrupted segments of basepairs.

    """
    # trivially true
    # if there is only one pair base that there is only one paired segment
    if len(df) == 1:
        return [0]

    paired_segment_ids: list[int] = []

    # initialized data from previous bp and current bp as None
    previous_i_chain_id: str | None = None
    previous_i_residue_index: int | None = None
    previous_j_chain_id: str | None = None
    previous_j_residue_index: int | None = None

    current_paired_segment = 0  # the first paired segment is index 0

    current_i_chain_id: str | None = None
    current_i_residue_index: int | None = None
    current_j_chain_id: str | None = None
    current_j_residue_index: int | None = None

    for i, row in df.iterrows():
        # update data for the current base pair (row : base pair)
        current_i_chain_id: str = row["i_chain_id"]
        current_i_residue_index: int = row["i_residue_index"]
        current_j_chain_id: str = row["j_chain_id"]
        current_j_residue_index: int = row["j_residue_index"]

        if previous_i_chain_id is None:
            # starting case, the very first base pair encountered
            paired_segment_ids.append(current_paired_segment)

        elif (
            previous_i_chain_id == current_i_chain_id
            and previous_j_chain_id == current_j_chain_id
            and previous_i_residue_index + 1 == current_i_residue_index
            and previous_j_residue_index - 1 == current_j_residue_index
        ):
            # step case, all the other base pairs encountered
            # continuity case
            paired_segment_ids.append(current_paired_segment)
        else:
            # step case, all the other base pairs encountered
            # discontinuity case
            current_paired_segment += 1
            paired_segment_ids.append(current_paired_segment)

        # update data for the previous base pair (row : base pair)
        previous_i_chain_id = current_i_chain_id
        previous_i_residue_index = current_i_residue_index
        previous_j_chain_id = current_j_chain_id
        previous_j_residue_index = current_j_residue_index

    # an array of segment indexes
    return paired_segment_ids
