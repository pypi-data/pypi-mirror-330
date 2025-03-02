'''
Date: 2025-02-20 22:02:45
LastEditors: BHM-Bob 2262029386@qq.com
LastEditTime: 2025-02-21 19:39:33
Description: 
'''
import numpy as np
from mbapy_lite.base import put_err
from MDAnalysis.core.groups import AtomGroup
from MDAnalysis.analysis.gnm import order_list, closeContactGNMAnalysis


def generate_ordered_pairs(positions, cutoff):
    """
    Generate all ordered pairs of atoms within a cutoff distance using NumPy operations.

    Parameters
    ----------
    positions : ndarray
        Atom coordinates as an array of shape (n_atoms, 3)
    cutoff : float
        Distance threshold

    Returns
    -------
    list of tuples
        Pairs of atom indices (i, j) where distance is less than cutoff
    """
    positions = np.asarray(positions)
    n_atoms = positions.shape[0]
    
    # Compute pairwise squared distances using broadcasting
    coords = positions
    diff = coords[:, np.newaxis, :] - coords[np.newaxis, :, :]
    distance_sq = np.sum(diff ** 2, axis=-1)
    
    # Create a mask for distances below cutoff squared, excluding self-pairs
    mask = distance_sq < cutoff ** 2
    np.fill_diagonal(mask, False)
    
    # Extract the indices where the mask is True
    i, j = np.where(mask)
    
    return list(zip(i, j))

def generate_matrix(positions, cutoff):
    positions = np.asarray(positions)
    natoms = positions.shape[0]
    cutoff_sq = cutoff ** 2

    # Generate all pairs from neighbour_generator
    all_pairs = generate_ordered_pairs(positions, cutoff)
    
    if not all_pairs:
        return np.zeros((natoms, natoms), dtype=np.float64)
    
    pairs = np.array(all_pairs)
    i = pairs[:, 0]
    j = pairs[:, 1]

    # Filter pairs where i < j to avoid duplicates
    mask = j > i
    i_filtered = i[mask]
    j_filtered = j[mask]

    # Calculate squared distances using NumPy's vectorized operations
    a = positions[i_filtered]
    b = positions[j_filtered]
    distance_squared = np.sum((a - b) ** 2, axis=1)

    # Apply cutoff and get valid indices
    valid = distance_squared < cutoff_sq

    # Create matrix and set symmetric entries
    matrix = np.zeros((natoms, natoms), dtype=np.float64)
    matrix[i_filtered[valid], j_filtered[valid]] = -1.0
    matrix[j_filtered[valid], i_filtered[valid]] = -1.0

    # Calculate diagonal entries as the count of neighbors
    row_counts = np.sum(matrix < 0, axis=1)
    np.fill_diagonal(matrix, row_counts)

    return matrix

        
def calcu_GNMAnalysis(positions: np.ndarray, cutoff: float = 7,
                      gen_matrix_fn = None, **kwargs):
    """Generate the Kirchhoff matrix of contacts.

    This generates the neighbour matrix by generating a grid of
    near-neighbours and then calculating which are are within
    the cutoff.

    Returns
    -------
        eigenvectors
        eigenvalues
    """
    gen_matrix_fn = gen_matrix_fn or generate_matrix
    matrix = gen_matrix_fn(positions, cutoff, **kwargs)
    try:
        _, w, v = np.linalg.svd(matrix)
    except np.linalg.LinAlgError:
        return put_err(f"SVD with cutoff {cutoff} failed to converge, return None")
    list_map = np.argsort(w)
    return w[list_map[1]], v[list_map[1]]


def generate_close_matrix(positions: np.ndarray, cutoff,
                          atom2residue: np.ndarray, residue_size: np.ndarray,
                          n_residue: int, weights="size"):
    """Generate the Kirchhoff matrix of closeContactGNMAnalysis contacts.

    This generates the neighbour matrix by generating a grid of
    near-neighbours and then calculating which are are within
    the cutoff.

    Returns
    -------
    array
            the resulting Kirchhoff matrix
    """
    cutoff_sq = cutoff ** 2

    # Compute residue sizes
    if weights == 'size':
        inv_sqrt_res_sizes = 1.0 / np.sqrt(residue_size)
    else:
        inv_sqrt_res_sizes = np.ones(n_residue, dtype=np.float64)

    # Generate all atom pairs within cutoff
    # Note: Using previous generate_ordered_pairs function (adjusted for pairs)
    all_pairs = generate_ordered_pairs(positions, cutoff)

    if not all_pairs:
        return np.zeros((n_residue, n_residue), dtype=np.float64)

    pairs = np.array(all_pairs)
    i_atom = pairs[:, 0]
    j_atom = pairs[:, 1]

    # Mask for i < j to avoid duplicate pairs
    mask = j_atom > i_atom
    i_filtered = i_atom[mask]
    j_filtered = j_atom[mask]

    # Compute squared distances and apply cutoff
    diff = positions[i_filtered] - positions[j_filtered]
    distance_sq = np.sum(diff ** 2, axis=1)
    valid = distance_sq < cutoff_sq

    # Get valid residue indices
    iresidues = atom2residue[i_filtered[valid]]
    jresidues = atom2residue[j_filtered[valid]]

    # Compute contact values
    contact = inv_sqrt_res_sizes[iresidues] * inv_sqrt_res_sizes[jresidues]

    # Initialize Kirkhoff matrix
    matrix = np.zeros((n_residue, n_residue), dtype=np.float64)

    # Update symmetric pairs
    matrix[iresidues, jresidues] -= contact
    matrix[jresidues, iresidues] -= contact
    matrix[iresidues, iresidues] += contact
    matrix[jresidues, jresidues] += contact

    # # Update diagonal elements
    # for res in range(n_residue):
    #     diagonal_contacts = contact[(iresidues == res) | (jresidues == res)]
    #     matrix[res, res] += np.sum(diagonal_contacts)
    
    # # Update diagonal elements using bincount
    # # Combine iresidues and jresidues and concatenate the contact twice
    # ire_jre_concat = np.concatenate((iresidues, jresidues))
    # contact_concat = np.concatenate((contact, contact))

    # # Compute the bincount for the combined residues
    # bincounts = np.bincount(ire_jre_concat, weights=contact_concat, minlength=n_residue)

    # # Add the bincounts to the diagonal of the matrix
    # np.fill_diagonal(matrix, bincounts)

    return matrix


def genarate_atom2residue(atoms: AtomGroup):
    """
    return
        - a 1d array where each element is the residue index of the atom
        - a 1d array where each element is the number of atoms in the residue
    """
    return atoms.resindices.copy(), np.array([r.atoms.n_atoms for r in atoms.residues])


def calcu_closeContactGNMAnalysis(positions: np.ndarray, cutoff: float, atom2residue: np.ndarray,
                                  residue_size: np.ndarray, n_residue: int, weights="size"):
    """Generate the Kirchhoff matrix of contacts.

    This generates the neighbour matrix by generating a grid of
    near-neighbours and then calculating which are are within
    the cutoff.

    Returns
    -------
        eigenvectors
        eigenvalues
    """
    return calcu_GNMAnalysis(positions, cutoff, gen_matrix_fn=generate_close_matrix,
                             atom2residue=atom2residue, residue_size=residue_size,
                             n_residue=n_residue, weights=weights)
