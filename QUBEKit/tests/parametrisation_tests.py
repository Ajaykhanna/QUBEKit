#!/usr/bin/env python3

from QUBEKit.ligand import Ligand
from QUBEKit.parametrisation import AnteChamber, OpenFF

import os
from shutil import copy, rmtree
import unittest


class ParametrisationTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Create temp working directory and copy across test files."""

        cls.files_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files')

        os.mkdir('temp')
        os.chdir('temp')
        copy(os.path.join(cls.files_folder, 'acetone.pdb'), 'acetone.pdb')
        cls.molecule = Ligand('acetone.pdb')
        cls.molecule.testing = True

    def test_antechamber(self):
        """Parametrise with Antechamber and ensure parameters have all been assigned."""

        AnteChamber(self.molecule)

        self.assertEqual(len(self.molecule.HarmonicBondForce), len(list(self.molecule.topology.edges)))

        self.assertEqual(len(self.molecule.HarmonicAngleForce), len(self.molecule.angles))

        self.assertEqual(len(self.molecule.PeriodicTorsionForce),
                         len(self.molecule.dih_phis) + len(self.molecule.improper_torsions))

        self.assertEqual(len(self.molecule.coords['input']), len(self.molecule.NonbondedForce))

    def test_OpenFF(self):
        """Parametrise with OpenFF and ensure parameters have all been assigned."""

        OpenFF(self.molecule)

        self.assertEqual(len(self.molecule.HarmonicBondForce), len(list(self.molecule.topology.edges)))

        self.assertEqual(len(self.molecule.HarmonicAngleForce), len(self.molecule.angles))

        self.assertEqual(len(self.molecule.PeriodicTorsionForce),
                         len(self.molecule.dih_phis) + len(self.molecule.improper_torsions))

        self.assertEqual(len(self.molecule.coords['input']), len(self.molecule.NonbondedForce))

    @classmethod
    def tearDownClass(cls):
        """Remove the working directory and any files produced during testing"""

        os.chdir('../')
        rmtree('temp')


if __name__ == '__main__':

    unittest.main()
