"""Core module for extracting Protein-DNA interfaces."""

from Bio.PDB.Polypeptide import PPBuilder
from Bio.PDB.NeighborSearch import NeighborSearch
from Bio.PDB import Atom

# from Bio.PDB import Structure, Model, Chain, Residue
# from Bio.PDB import MMCIFIO

import pandas as pd

from PDBNucleicAcids.NucleicAcid import NABuilder


def build_interfaces(structure, search_radius=5.0) -> list:
    """
    Extract all Protein-DNA interfaces found in a structure.

    Parameters
    ----------
    structure : Bio.PDB.Structure
        Biopython Structure entity.
    search_radius : float | int, optional
        Search radius, measured in Armstrong, within which Protein-DNA
        interactions are found. Default is 5.0

    Returns
    -------
    list
        List of all Protein-DNA interfaces found in a structure.

    """
    # build nucleic acids
    builder = NABuilder()
    na_list = builder.build_nucleic_acids(structure)
    if not na_list:
        return []

    # dna_chain_ids = list({na.get_chain_id() for na in na_list})

    # build peptides
    builder = PPBuilder()
    pp_list = builder.build_peptides(structure)
    if not pp_list:
        return []

    prot_chain_ids = list({pp[0].parent.id for pp in pp_list})

    face_list = []
    for prot_chain_id in prot_chain_ids:
        face = Interface(
            structure=structure,
            protein_chain_id=prot_chain_id,
            search_radius=search_radius,
        )
        face_list.append(face)

    return face_list


class Interface:
    """
    Extract Protein-DNA interface.

    Parameters
    ----------
    structure : Bio.PDB.Structure
        Biopython Structure entity.
    protein_chain_id : str
        Chain id of a protein that may interact with DNA.
    search_radius : float | int, optional
        Search radius, measured in Armstrong, within which Protein-DNA
        interactions are found. Default is 5.0

    """

    def __init__(self, structure, protein_chain_id, search_radius=5.0) -> None:
        self.structure = structure
        self.protein_chain_id = protein_chain_id
        self.search_radius = search_radius

        self.contacts = self._extract_contacts()

        dna_atoms = self.get_dna_atoms()
        self.dna_chain_ids = list(
            {atom.parent.parent.id for atom in dna_atoms}
        )

    def __repr__(self):
        """Return string representation of the nucleic acid."""
        return f"<Interface chains={self.protein_chain_id}:\
{''.join(self.dna_chain_ids)} contacts={len(self.contacts)} search_radius=\
{self.search_radius}>"

    def _extract_contacts(self) -> list[tuple[Atom]]:
        """Extract interface contacts."""
        # get all the atoms from the nucleic acids, in most cases DNA
        na_builder = NABuilder()
        na_list = na_builder.build_nucleic_acids(self.structure)
        na_atoms = []
        for na in na_list:
            na_atoms.extend(na.get_atoms())
        na_atoms = list(set(na_atoms))

        na_chain_ids = [na.get_chain_id() for na in na_list]

        # get all the atoms from the protein chain
        protein_chain = self.structure[0][self.protein_chain_id]
        pp_builder = PPBuilder()
        pp_list = pp_builder.build_peptides(protein_chain)
        pp_atoms = []
        for pp in pp_list:
            for res in pp:
                pp_atoms.extend(res.get_atoms())
        pp_atoms = list(set(pp_atoms))

        # Crea una lista con tutti gli atomi di DNA e proteina
        all_atoms = na_atoms + pp_atoms

        # Filter out hydrogens
        all_atoms = [atom for atom in all_atoms if atom.element != "H"]

        # Usa NeighborSearch per trovare gli atomi vicini entro una certa
        # distanza
        ns = NeighborSearch(all_atoms)

        # Cerca gli atomi vicini entro un raggio di 4 Å tra DNA e proteina
        all_contacts = ns.search_all(self.search_radius)

        # Filtra solo i contatti, ovvero le coppied di atomi,
        # che hanno un atomo di DNA
        temp = [
            (atom1, atom2)
            for atom1, atom2 in all_contacts
            if (
                atom1.parent.parent.id in na_chain_ids
                or atom2.parent.parent.id in na_chain_ids
            )
        ]

        # Filtra solo i contatti tra DNA e proteina
        contacts = [
            (atom1, atom2)
            for atom1, atom2 in temp
            if (
                atom1.parent.parent.id in na_chain_ids
                and atom2.parent.parent.id == self.protein_chain_id
            )
        ] + [
            (atom2, atom1)
            for atom1, atom2 in temp
            if (
                atom1.parent.parent.id == self.protein_chain_id
                and atom2.parent.parent.id in na_chain_ids
            )
        ]
        # temp è utile per greedyness, prima prendi il DNA, che ha meno
        # atomi, escludendo quelli intra-proteina
        # poi escludi anche quelli intra-DNA
        # inoltre ci assicuriamo che la col 0 contenga gli atomi di DNA e
        # che col 1 contenga gli atomi di proteine
        # Ce ne assicuriamo invertendo atom1 e atom2 nella seconda lista

        return contacts

    def get_protein_atoms(self) -> list[Atom]:
        """
        Get only protein atoms in the protein-DNA interface.

        Returns
        -------
        list[Atom]
            List of protein atoms in the interface.

        """
        return list({atom_pair[1] for atom_pair in self.contacts})

    def get_dna_atoms(self) -> list[Atom]:
        """
        Get only DNA atoms in the protein-DNA interface.

        Returns
        -------
        list[Atom]
            List of DNA atoms in the interface.

        """
        return list({atom_pair[0] for atom_pair in self.contacts})

    def get_interface_data(self) -> pd.DataFrame:
        """
        Get all data from the interface, as a dataframe.

        Contains the following data fields:
            Residue hetero field
            Residue number
            Residue insertion code
            Residue name
            Atom name
            Atom alternate location
            Atom element
            Atomic coordinates (x, y, z)
            From both protein and DNA atoms
            Euclidean distance

        Returns
        -------
        df : pd.DataFrame
            All data from the interface.

        """
        data = []

        for na_atom, prot_atom in self.contacts:

            prot_res_hetfield = prot_atom.parent.id[0]
            prot_res_number = prot_atom.parent.id[1]
            prot_res_icode = prot_atom.parent.id[2]
            prot_res_name = prot_atom.parent.resname
            prot_atom_name = prot_atom.name
            prot_atom_altloc = prot_atom.altloc
            prot_atom_element = prot_atom.element
            prot_atom_coord_x = prot_atom.coord[0]
            prot_atom_coord_y = prot_atom.coord[1]
            prot_atom_coord_z = prot_atom.coord[2]

            dna_chain_id = na_atom.parent.parent.id
            dna_res_hetfield = na_atom.parent.id[0]
            dna_res_number = na_atom.parent.id[1]
            dna_res_icode = na_atom.parent.id[2]
            dna_res_name = na_atom.parent.resname
            dna_atom_name = na_atom.name
            dna_atom_altloc = na_atom.altloc
            dna_atom_element = na_atom.element
            dna_atom_coord_x = na_atom.coord[0]
            dna_atom_coord_y = na_atom.coord[1]
            dna_atom_coord_z = na_atom.coord[2]

            euclidian_distance = na_atom - prot_atom

            row = (
                self.protein_chain_id,
                prot_res_hetfield,
                prot_res_number,
                prot_res_icode,
                prot_res_name,
                prot_atom_name,
                prot_atom_altloc,
                prot_atom_element,
                prot_atom_coord_x,
                prot_atom_coord_y,
                prot_atom_coord_z,
                dna_chain_id,
                dna_res_hetfield,
                dna_res_number,
                dna_res_icode,
                dna_res_name,
                dna_atom_name,
                dna_atom_altloc,
                dna_atom_element,
                dna_atom_coord_x,
                dna_atom_coord_y,
                dna_atom_coord_z,
                euclidian_distance,
            )

            data.append(row)

        df = pd.DataFrame(
            data,
            columns=[
                "protein_chain_id",
                "prot_res_hetfield",
                "prot_res_number",
                "prot_res_icode",
                "prot_res_name",
                "prot_atom_name",
                "prot_atom_altloc",
                "prot_atom_element",
                "prot_atom_coord_x",
                "prot_atom_coord_y",
                "prot_atom_coord_z",
                "dna_chain_id",
                "dna_res_hetfield",
                "dna_res_number",
                "dna_res_icode",
                "dna_res_name",
                "dna_atom_name",
                "dna_atom_altloc",
                "dna_atom_element",
                "dna_atom_coord_x",
                "dna_atom_coord_y",
                "dna_atom_coord_z",
                "euclidian_distance",
            ],
        )

        return df


# def export_atom_list(structure_id, atom_list, out_filepath):
#     """Export atom list."""
#     # not in Path but in string
#     out_filepath = str(out_filepath)

#     new_structure = Structure.Structure(structure_id)
#     for atom in atom_list:
#         _add_atom_to_new_structure(atom, new_structure)

#     # Prepare IO object
#     io = MMCIFIO()
#     io.set_structure(new_structure)

#     # Esporta la nuova struttura in un file PDB
#     # necessita di string type filepath
#     io.save(out_filepath)


# def _add_atom_to_new_structure(atom, new_structure):
#     model_id = (
#         atom.get_parent().get_parent().get_parent().id
#     )  # Ottieni l'ID del modello
#     chain_id = atom.get_parent().get_parent().id  # Ottieni l'ID della catena
#     residue_id = atom.get_parent().id  # Ottieni l'ID del residuo
#     resname = atom.get_parent().resname  # Nome del residuo

#     # Controlla se il modello esiste già nel nuovo modello
#     if model_id in [model.id for model in new_structure]:
#         new_model = new_structure[model_id]
#     else:
#         new_model = Model.Model(model_id)
#         new_structure.add(new_model)

#     # Controlla se la catena esiste già nel nuovo modello
#     if chain_id in [chain.id for chain in new_model]:
#         new_chain = new_model[chain_id]
#     else:
#         new_chain = Chain.Chain(chain_id)
#         new_model.add(new_chain)

#     # Controlla se il residuo esiste già nella nuova catena
#     if residue_id in [res.id for res in new_chain]:
#         new_residue = new_chain[residue_id]
#     else:
#         new_residue = Residue.Residue(
#             residue_id, resname, atom.get_parent().segid
#         )
#         new_chain.add(new_residue)

#     # Copia l'atomo e aggiungilo al residuo
#     new_atom = atom.copy()
#     new_residue.add(new_atom)
