"""Extract basepair data from the NDB/NAKB Data Category in mmCif files."""

from pathlib import Path
import pandas as pd
from Bio.PDB.MMCIF2Dict import MMCIF2Dict

# absolute import
from PDBNucleicAcids.utils import get_paired_segments


def basepair_dataframe_from_mmcif(
    mmcif_filepath: str | Path,
) -> pd.DataFrame | None:
    """
    Return dataframe with base pairs data from a mmCif file.

    Note: not all mmCif files contain Data Category "ndb_struct_na_base_pair"

    Parameters
    ----------
    mmcif_filepath : str | Path
        mmCif filepath.

    Returns
    -------
    pandas.DataFrame | None
        Dataframe with base pairs data in the structure.

    """
    mmcif_dict = MMCIF2Dict(str(mmcif_filepath))

    try:
        pair_name = mmcif_dict["_ndb_struct_na_base_pair.pair_name"]
        i_chain_id = mmcif_dict["_ndb_struct_na_base_pair.i_auth_asym_id"]
        i_residue_index = mmcif_dict["_ndb_struct_na_base_pair.i_auth_seq_id"]
        i_residue_name = mmcif_dict["_ndb_struct_na_base_pair.i_label_comp_id"]
        j_chain_id = mmcif_dict["_ndb_struct_na_base_pair.j_auth_asym_id"]
        j_residue_index = mmcif_dict["_ndb_struct_na_base_pair.j_auth_seq_id"]
        j_residue_name = mmcif_dict["_ndb_struct_na_base_pair.j_label_comp_id"]
        base_pairs_df = pd.DataFrame(
            {
                "pair_name": pair_name,
                "i_chain_id": i_chain_id,
                "i_residue_index": list(map(int, i_residue_index)),
                "i_residue_name": i_residue_name,
                "j_chain_id": j_chain_id,
                "j_residue_index": list(map(int, j_residue_index)),
                "j_residue_name": j_residue_name,
            }
        )
    except KeyError as e:
        # in this case at least one of these keys are not present
        # so there is no basepair datastructure
        print(e)
        return None

    polymers_df = polymer_dataframe_from_mmcif(mmcif_filepath)

    # Divide into two dataframes
    # one has the data from the "i" side and the other from the "j" side
    # of the chain
    i_polymers_df = polymers_df.copy()
    j_polymers_df = polymers_df.copy()

    # renaming columns, adding a prefix "i_" and prefix "j_"
    i_polymers_df.columns = map(lambda col: "i_" + col, i_polymers_df.columns)
    j_polymers_df.columns = map(lambda col: "j_" + col, j_polymers_df.columns)

    # dataframe with base pair information AND polymer information
    # by inneri joining the two dataframes, from "i" and "j"
    result_df = pd.merge(base_pairs_df, i_polymers_df, on="i_chain_id")
    result_df = pd.merge(result_df, j_polymers_df, on="j_chain_id")

    # rearranging columns by slicing the dataframe and then concatenating
    i_result_df = result_df[
        [
            "pair_name",
            "i_polymer_type",
            "i_non_standard_linkage",
            "i_non_standard_residue",
            "i_chain_id",
            "i_residue_index",
            "i_residue_name",
        ]
    ]
    j_result_df = result_df[
        [
            "j_residue_name",
            "j_residue_index",
            "j_chain_id",
            "j_non_standard_residue",
            "j_non_standard_linkage",
            "j_polymer_type",
        ]
    ]
    result_df = pd.concat([i_result_df, j_result_df], axis=1)

    # Add a column with an index that indicates a paired segment
    # i.e.
    # A  T  0
    # C  G  0
    # C  G  0
    # T  A  1
    result_df["paired_segment"] = get_paired_segments(result_df)

    return result_df


def polymer_dataframe_from_mmcif(
    mmcif_filepath: str | Path,
) -> pd.DataFrame | None:
    """
    Dataframe with polymer data from a mmCif file.

    Parameters
    ----------
    mmcif_filepath : str | Path
        mmCif filepath.

    Returns
    -------
    pandas.DataFrame | None
        Dataframe with information about each polymer in the structure.

    """
    # TODO test with weird chain ids like multimeric
    # i.e. "A,B,C,D"
    mmcif_dict = MMCIF2Dict(str(mmcif_filepath))

    try:
        polymer_type = mmcif_dict["_entity_poly.type"]
        non_standard_linkage = mmcif_dict["_entity_poly.nstd_linkage"]
        non_standard_residue = mmcif_dict["_entity_poly.nstd_monomer"]
        polymers_df = pd.DataFrame(
            {
                "polymer_type": polymer_type,
                "non_standard_linkage": non_standard_linkage,
                "non_standard_residue": non_standard_residue,
            }
        )
    except KeyError as e:
        print(e)
        return None

    # there are two options for chain IDs:
    # ndb (nucleotide db) and pdbx (protein db X)
    # sometimes it's called chain, sometimes it's called strand
    if "_entity_poly.pdbx_chain_id" in mmcif_dict:
        polymers_df["chain_id"] = mmcif_dict["_entity_poly.pdbx_chain_id"]
    elif "_entity_poly.pdbx_strand_id" in mmcif_dict:
        polymers_df["chain_id"] = mmcif_dict["_entity_poly.pdbx_strand_id"]
    elif "_entity_poly.ndb_chain_id" in mmcif_dict:
        polymers_df["chain_id"] = mmcif_dict["_entity_poly.ndb_chain_id"]
    elif "_entity_poly.ndb_strand_id" in mmcif_dict:
        polymers_df["chain_id"] = mmcif_dict["_entity_poly.ndb_strand_id"]
    else:
        return None

    return polymers_df
