from array import array
from multiprocessing.sharedctypes import Value
from importlib.resources import path
from pathlib import Path
from typing import Tuple
from ase.units import Bohr

import numpy as np
from openbabel import openbabel as ob


class LTMatrix(list):
    """LTMatrix class and code comes from https://github.com/ruixingw/rxcclib/blob/dev/utils/my/LTMatrix.py"""
    def __init__(self, L):
        """
        Accept a list of elements in a lower triangular matrix.
        """
        list.__init__(self, L)
        self.list = L
        i, j = LTMatrix.getRowColumn(len(L) - 1)
        assert i == j, "Not a LTMatrix"
        self.dimension = i + 1

    def __getitem__(self, key):
        """
        Accept one or two integers.
        ONE: get item at the given position (count from zero)
        TWO: get item at the given (row, column) (both counted from zero)
        """
        if type(key) is tuple:
            return self.list[LTMatrix.getPosition(*key)]
        else:
            return self.list[key]

    @staticmethod
    def getRowColumn(N):
        """
        Return the row and column number of the Nth entry  of a lower triangular matrix.
        N, ROW, COLUMN are counted from ZERO!
        Example:
           C0 C1 C2 C3 C4 C5
        R0 0
        R1 1  2
        R2 3  4  5
        R3 6  7  8  9
        R4 10 11 12 13 14
        R5 15 16 17 18 19 20
        >>> LTMatrix.getRowColumn(18)
        (5, 3)
        18th element is at row 5 and column 3. (count from zero)
        """
        N += 1
        y = int((np.sqrt(1 + 8 * N) - 1) / 2)
        b = int(N - (y**2 + y) / 2)
        if b == 0:
            return (y - 1, y - 1)
        else:
            return (y, b - 1)

    @staticmethod
    def getPosition(i, j):
        """
        Return the number of entry in the i-th row and j-th column of a symmetric matrix.
        All numbers are counted from ZERO.
        >>> LTMatrix.getPosition(3, 4)
        13
        """
        i += 1
        j += 1
        if i < j:
            i, j = j, i
        num = (i * (i - 1) / 2) + j
        num = int(num)
        return num - 1

    def buildFullMat(self):
        """
        build full matrix (np.ndarray).
        """
        L = []
        for i in range(self.dimension):
            L.append([])
            for j in range(self.dimension):
                L[-1].append(self[i, j])
        self._fullmat = np.array(L)
        return self._fullmat

    @property
    def fullmat(self):
        """
        Return the full matrix (np.ndarray)
        """
        return getattr(self, '_fullmat', self.buildFullMat())

    def inverse(self):
        return np.linalg.inv(self.fullmat)

    def uppermat(self):
        up = []
        for i, row in enumerate(self.fullmat):
            up.extend(row[i:])
        return up

    @staticmethod
    def newFromUpperMat(uppermat):
        """
        Example:
           C0 C1 C2 C3 C4 C5
        R0  0  1  2  3  4  5
        R1     6  7  8  9 10
        R2       11 12 13 14
        R3          15 16 17
        R4             18 19
        R5                20
        """
        dimension = LTMatrix.getRowColumn(len(uppermat)-1)[0] + 1

        def getUpperPosition(i, j, dimension):
            firstnum = dimension
            if i == 0:
                return j
            lastnum = firstnum - i + 1
            countnum = i
            abovenums = (firstnum + lastnum)*countnum / 2
            position = abovenums + j - i
            return int(position)
        L = []
        for i in range(dimension):
            for j in range(i+1):
                L.append(uppermat[getUpperPosition(j, i, dimension)])
        return LTMatrix(L)

# TODO: sandbox all variables meant to be publicly accessible as properties


class Geometry:
    """Houses data associated with a molecular structure, all public variables are intended for access not modification."""

    def __init__(self, name: str, nAtoms: int) -> None:
        self.name = name
        """Name of geometry, based off of stem of .fchk file path unless otherwise modified."""
        self.ric = array('f')
        """Redundant Internal Coordinates of geometry in atomic units (Bohr radius)"""
        self.energy = None
        """Energy associated with geometry based on the DFT or higher level calculations used to generate the .fchk file input"""
        self.atoms = list()
        """List of <SITH_Utilities.Atom> objects associated with geometry."""
        self.nAtoms = nAtoms
        """Number of atoms"""
        self.dims = array('i')
        """Array of number of dimensions of DOF type
        [0]: total dimensions/DOFs
        [1]: bond lengths
        [2]: bond angles
        [3]: dihedral angles
        """
        self.dimIndices = list()
        """List of Tuples referring to the indices of the atoms involved in each dimension/DOF in order of DOF index in ric"""

    #TODO: Need to adapt to new format, make sure to specify and/or convert units
    def buildCartesian(self, lines: list):
        first = lines[0]
        if len(first.split()) == 1:
            nAtoms = int(first)
            if nAtoms != self.nAtoms:
                raise Exception("Mismatch in number of atoms.")
        for line in lines:
            sLine = line.split()
            if len(sLine) > 1 and len(sLine) < 5:
                a = Atom(sLine[0], sLine[1:4])
                self.atoms.append(a)
            elif len(sLine) >= 5:
                pass

    def buildRIC(self, dims: list, dimILines: list, coordLines: list):
        self.dims = array('i', [int(d) for d in dims])

        # region Indices
        # Parses through the 'dimILines' input which indicates which atoms (by index)
        # are involved in each RIC degree of freedom

        rawIndices = list()
        for iLine in dimILines:
            iSplit = iLine.split()
            try:
                rawIndices.extend([int(i) for i in iSplit])
            except ValueError as ve:
                print(ve)
                raise Exception("Invalid atom index given as input.")

        # Check that # indices is divisible by 4
        assert len(rawIndices) % 4 == 0 and len(
            rawIndices) == self.dims[0] * 4, "Redundant internal coordinate indices input has invalid dimensions."

        # Parse into sets of 4, then into tuples of the relevant number of values
        for i in range(0, len(rawIndices), 4):
            a1 = rawIndices[i]
            a2 = rawIndices[i+1]
            a3 = rawIndices[i+2]
            a4 = rawIndices[i+3]
            # Check that the number of values in each tuple matches the dimension type (length, angle, dihedral) for that dim index
            # These should line up with self.dims correctly
            assert a1 <= self.nAtoms and a2 <= self.nAtoms and a3 <= self.nAtoms and a4 <= self.nAtoms, "Invalid atom index given as input."
            assert a1 != 0 and a2 != 0, "Mismatch between given 'RIC dimensions' and given RIC indices."
            # bond lengths check
            if i < self.dims[1]*4:
                assert a3 == 0 and a4 == 0, "Mismatch between given 'RIC dimensions' and given RIC indices."
                self.dimIndices.append((a1, a2))
            # bond angles check
            elif i < (self.dims[1] + self.dims[2])*4:
                assert a3 != 0 and a4 == 0, "Mismatch between given 'RIC dimensions' and given RIC indices."
                self.dimIndices.append((a1, a2, a3))
            # dihedral angles check
            elif i < (self.dims[1] + self.dims[2] + self.dims[3])*4:
                assert a3 != 0 and a4 != 0, "Mismatch between given 'RIC dimensions' and given RIC indices."
                self.dimIndices.append((a1, a2, a3, a4))

        # endregion

        for line in coordLines:
            self.ric.extend([float(ric) for ric in line.split()])
        self.ric = np.asarray(self.ric)
        assert len(self.ric) == self.dims[0], "Mismatch between the number of degrees of freedom expected ("+str(
            dims[0])+") and number of coordinates given ("+str(len(self.ric))+")."

    def killDOFs(self, dofis: list[int]):
        self.ric = np.delete(self.ric, dofis)
        self.dimIndices = np.delete(self.dimIndices, dofis)
        lengthsDeleted = sum(x < self.dims[1] and x >= 0 for x in dofis)
        anglesDeleted = sum(
            x < self.dims[2] + self.dims[1] and x >= self.dims[1] for x in dofis)
        dihedralsDeleted = sum(
            x < self.dims[0] and x >= self.dims[2] for x in dofis)
        self.dims[0] -= len(dofis)
        self.dims[1] -= lengthsDeleted
        self.dims[2] -= anglesDeleted
        self.dims[3] -= dihedralsDeleted

    def __eq__(self, __o: object) -> bool:
        b = True
        b = b and self.name == __o.name
        b = b and all(self.ric == __o.ric)
        b = b and self.energy == __o.energy
        b = b and self.atoms == __o.atoms
        b = b and self.nAtoms == __o.nAtoms
        b = b and self.dims == __o.dims
        b = b and self.dimIndices == __o.dimIndices
        return b


class Atom:
    def __init__(self, element: str, coords: list) -> None:
        self.element = element
        self.coords = coords

    def __eq__(self, __o: object) -> bool:
        return self.element == __o.element and self.coords == __o.coords


class UnitConverter:
    """
    Class to convert units utilizing Atomic Simulation Environment (ase) constants
    xyz standard input is in Angstrom
    RIC are in atomic units
    internal Hessian is in atomic units of length: Ha/Bohr^2 angle: Hartree/radian^2
    Note: values in all Gaussian version 3 formatted checkpoint files are in atomic units
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def angstromToBohr(a: float) -> float:
        return a * Bohr

    @staticmethod
    def bohrToAngstrom(b: float) -> float:
        return b / Bohr

    @staticmethod
    def radianToDegree(r: float) -> float:
        return


class Extractor:

    def __init__(self, path: Path, linesList: list) -> None:
        self.eHeader = "Total Energy"
        self.hessHeader = "Internal Force Constants"
        self.hEnder = "Mulliken Charges"
        self.xcHeader = "Current cartesian coordinates"
        self.xcEnder = "Force Field"
        self.ricHeader = "Redundant internal coordinates"
        self.xrEnder = "ZRed-IntVec"
        self.dimHeader = "Redundant internal dimensions"
        self.dimIndicesHeader = "Redundant internal coordinate indices"
        self.nHeader = "Number of atoms"
        self.aHeader = "Atomic numbers"

        self.path = path
        self.name = path.stem

        self.lines = linesList

    def writeXYZ(self):
        obConversion = ob.OBConversion()
        obConversion.SetInAndOutFormats("fchk", "xyz")

        mol = ob.OBMol()
        assert self.path.exists(), "Path to fchk file does not exist"
        assert obConversion.ReadFile(mol, self.path.as_posix(
        )), "Reading fchk file with openbabel failed."
        assert obConversion.WriteFile(mol, str(
            self.path.parent.as_posix()+self.path.root+self.path.stem+".xyz")), "Could not write XYZ file."

    def extract(self):
        self.writeXYZ()

        #! Change to a while < len loop?
        # TODO: make end based on number of values to expect (N = ) not the next header
        i = 0
        while i < len(self.lines):
            line = self.lines[i]

            # This all must be in order
            #! Sandbox this ASAP you dummy
            if self.nHeader in line:
                splitLine = line.split()
                numAtoms = int(splitLine[len(splitLine)-1])
                self.geometry = Geometry(self.name, numAtoms)

            elif self.aHeader in line:
                i = i+1
                lin = self.lines[i]
                atomicNums = lin.split()

            elif self.eHeader in line:
                splitLine = line.split()
                self.geometry.energy = float(splitLine[len(splitLine)-1])

            elif self.dimHeader in line:
                i = i+1
                lin = self.lines[i]
                rDims = lin.split()

            elif self.dimIndicesHeader in line:
                rdiStart = i+1
                while self.ricHeader not in self.lines[i+1]:
                    i = i+1
                xrDims = self.lines[rdiStart:i+1]
                #! assert validation of number of degrees of freedom?
                assert len(
                    xrDims) > 0, "Missing 'Redundant internal coordinate indices'."

            if self.ricHeader in line:
                i = i+1
                xrStart = i
                while self.xrEnder not in self.lines[i]:
                    i = i+1
                xrRaw = self.lines[xrStart:i]
                self.geometry.buildRIC(rDims, xrDims, xrRaw)
                # TODO: build in validation for RICs in ^ if not already there

            elif self.hessHeader in line:
                hFirst = line.split()
                i = i+1
                self.hRaw = list()
                while self.hEnder not in self.lines[i]:
                    row = self.lines[i]
                    rowsplit = row.split()
                    self.hRaw.extend([float(i) for i in rowsplit])
                    i = i+1

            i = i + 1
        with open(self.path.parent.as_posix()+self.path.root + self.path.stem + ".xyz", "r") as xyz:
            xyzLines = xyz.readlines()
            self.geometry.buildCartesian(xyzLines)
        self.buildHessian()

    def buildHessian(self):
        ltMat = LTMatrix(self.hRaw)
        self.hessian = ltMat.fullmat
        self.geometry.hessian = self.hessian

    def getGeometry(self) -> Geometry:
        if self.geometry:
            return self.geometry
        else:
            raise Exception("There is no geometry.")
