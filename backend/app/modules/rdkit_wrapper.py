from __future__ import annotations
from typing import Tuple
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdDepictor
from rdkit.Chem.Draw import rdMolDraw2D


def get_3d_conformers(molecule: any, depict=True) -> Chem.Mol:
    """Convert a SMILES string to an RDKit Mol object with 3D coordinates.

    Args:
        molecule (Chem.Mol): RDKit molecule object.
        depict (bool, optional): If True, returns the molecule's 3D structure in MolBlock format. If False, returns the 3D molecule without hydrogen atoms.

    Returns:
        str or rdkit.Chem.rdchem.Mol: If `depict` is True, returns the 3D structure in MolBlock format. Otherwise, returns an RDKit Mol object.
    """
    if molecule:
        molecule = Chem.AddHs(molecule)
        AllChem.EmbedMolecule(molecule, maxAttempts=5000, useRandomCoords=True)
        print(molecule)
        try:
            AllChem.MMFFOptimizeMolecule(molecule)
        except Exception:
            AllChem.EmbedMolecule(
                molecule,
                maxAttempts=5000,
                useRandomCoords=True,
            )
            print(molecule)
        if depict:
            return Chem.MolToMolBlock(molecule)
        else:
            molecule = Chem.RemoveHs(molecule)
            return Chem.MolToMolBlock(molecule)


def get_rdkit_depiction(
    molecule: any,
    molSize: Tuple[int, int] = (512, 512),
    rotate: int = 0,
    kekulize: bool = True,
) -> str:
    """This function takes the user input SMILES and Canonicalize it using the.

    RDKit.

    Args:
        molecule (Chem.Mol): RDKit molecule object.

    Returns:
        image (SVG): RDKit Structure Depiction as an SVG image.
    """
    if molecule:
        mc = Chem.Mol(molecule.ToBinary())
        if kekulize:
            try:
                Chem.Kekulize(mc)
            except Exception as e:
                print(e, flush=True)
                mc = Chem.Mol(molecule.ToBinary())
        if not mc.GetNumConformers():
            rdDepictor.Compute2DCoords(mc)
        drawer = rdMolDraw2D.MolDraw2DSVG(molSize[0], molSize[1])
        drawer.drawOptions().rotate = rotate
        drawer.DrawMolecule(mc)
        drawer.FinishDrawing()
        svg = drawer.GetDrawingText()
        return svg.replace("svg:", "")
    else:
        return "Error reading SMILES string, check again."
