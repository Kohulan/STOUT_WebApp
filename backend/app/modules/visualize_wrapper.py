from app.modules.rdkit_wrapper import Chem
from app.modules.rdkit_wrapper import get_rdkit_depiction, get_3d_conformers
from jinja2 import Template


def html_embed_molecule(molecule: str) -> str:
    """
    Generates an HTML string that embeds a 3D molecule viewer using the 3Dmol.js library.

    Args:
        molecule (str): A string representation of the molecule in a format recognized by 3Dmol.js.

    Returns:
        str: An HTML string containing the 3D molecule viewer.
    """
    template_str = """
    <html>
    <head>
    <title>3D Molecule Viewer</title>
    <script src="https://code.jquery.com/jquery-3.6.3.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/3Dmol/2.0.1/3Dmol.js"></script>
    <style>
    head, body {
        margin: 0;
        border: 0;
        padding: 0;
        max-height: 100vh
    }
    </style>
    <script>
    $(document).ready(function() {
        var viewer = $3Dmol.createViewer("viewer");
        viewer.setBackgroundColor(0xffffff);
        viewer.addModel(`{{ molecule }}`, "mol");
        viewer.setStyle({stick:{}});
        viewer.zoomTo();
        viewer.render();
    });
    </script>
    </head>
    <body>
        <div id="viewer" style="width: 100%; height: 100vh; margin: 0; padding: 0; border: 0;"></div>
    </body>
    </html>
    """
    template = Template(template_str)
    html_output = template.render(molecule=molecule)

    return html_output


def get_svg_2d(smiles: str) -> str:
    """
    Generates an SVG image representation of a 2D molecular structure from a SMILES string.

    Args:
        smiles (str): A SMILES string representing the molecular structure.

    Returns:
        str: An SVG string representing the 2D molecular structure, or an error message if the SMILES string is invalid.
    """
    smiles = smiles.replace("\\/", "/")
    mol = Chem.MolFromSmiles(smiles)

    image_size = (512, 512)
    if mol:
        svg_2d = get_rdkit_depiction(mol, image_size)

        return svg_2d.replace("\n", "")
    else:
        return "Error reading SMILES string, check again."


def get_html_3d(smiles: str) -> str:
    """
    Generates an HTML string that embeds a 3D molecule viewer for a given SMILES string.

    Args:
        smiles (str): A SMILES string representing the molecular structure.

    Returns:
        str: An HTML string containing the 3D molecule viewer.
    """
    smiles = smiles.replace("\\/", "/")
    mol = Chem.MolFromSmiles(smiles)
    mol_3d = get_3d_conformers(mol)
    html_3d = html_embed_molecule(mol_3d)

    return html_3d
