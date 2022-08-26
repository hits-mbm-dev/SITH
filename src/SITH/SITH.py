"""SITH class: calculates & houses SITH analysis data."""
import sys
from typing import Tuple
import pathlib
from pathlib import Path
import numpy as np
from SITH.Utilities import Extractor


class SITH:
    """A class to calculate & house SITH analysis data. Publicly accessable variables & methods:

    ...

    Attributes
    ----------
    q0 : numpy.ndarray
        RIC values of reference geometry [DOF index, deformation index]
    qF : numpy.ndarray
        RIC value matrix  of deformed geometries [DOF index, deformation index]
    deltaQ : numpy.ndarray
        RIC value matrix  of deformed - reference [DOF index, deformation index]
    hessian : numpy.ndarray
        Hessian matrix of reference geometry
    energies : numpy.ndarray
        stress energy per DOF per deformation [DOF index, deformation index]
    pEnergies : numpy.ndarray
        Proportion of total stress energy [DOF index, deformation index]
    deformationEnergy : numpy.ndarray
        Total stress energy per deformation [deformation index]

    Methods
    -------
    reference():
        Returns the reference geometry.
    deformed():
        Returns the list of deformed geometries.
    setKillAtoms(atoms: list[int]):
        Marks atoms to be ignored and removed from the reference geometry upon extraction.
    setKillDOFs(dofs: list[Tuple]):
        Marks DOFs to be ignored and removed from the reference geometry upon extraction.
    removeMismatchedDOFs():
        Removes DOFs from the deformed geometry which do not appear in the reference geometry upon extraction.
    extractData():
        Indicates that any killing of atoms and DOFs is finished, begins extraction and organization of data from input .fchk files.
    energyAnalysis():
        Conducts the SITH energy analysis.
    """

    def __init__(self, rePath='', dePath=''):
        """Takes in the reference geometry .fchk file path and the deformed geometry .fchk file path or path to directory of deformed geometries .fchk files.

        Notes
        -----
        """
        self._workingPath = Path.cwd()

        self._referencePath = None
        """Path to reference geometry, specified on SITH construction"""

        self._deformedPath = None
        """Path to deformed geometry or directory of deformed geometries, specified on SITH construction"""

        if(rePath == ''):
            #self._referencePath = Path('/hits/fast/mbm/farrugma/sw/SITH/tests/x0.fchk')
            self._referencePath = self._workingPath / 'x0.fchk'
        else:
            self._referencePath = self._workingPath / rePath

        if(dePath == ''):
            #self._deformedPath = Path('/hits/fast/mbm/farrugma/sw/SITH/tests/xF.fchk')
            self._deformedPath = self._workingPath / 'xF.fchk'
        else:
            self._deformedPath = self._workingPath / dePath

        # region variable documentation

        self.energies = None
        """Stress energy associated with a DOF for each deformation organized in the form of [DOF index, deformation index]
        
        Notes
        -----
        While this may be publicly accessed, please refrain from manually setting this value as it is an analysis result."""
        self.deformationEnergy = None
        """Total stress energy associated with going from the reference structure to the ith deformed structure.
        
        Notes
        -----
        While this may be publicly accessed, please refrain from manually setting this value as it is an analysis result."""
        self.pEnergies = None
        """Proportion of stress energy in each degree of freedom to the each structure's total stress energy 
        in the form [DOF index, deformation index]
        
        Notes
        -----
        While this may be publicly accessed, please refrain from manually setting this value as it is an analysis result."""

        self._reference = None
        """Reference Geometry object
        
        Notes
        -----
        Please refrain from manually setting this value as other analysis variables depend upon it.
        
        If you would like to manually change this value for a SITH object, instead implement the method setReference() and the associated refactoring recommended in its documentation."""

        self._deformed = None
        """List of deformed Geometry objects

        Notes
        -----
        While this may be publicly accessed, please refrain from manually setting this value as other analysis variables depend upon it."""

        # qF columns correspond to each deformed geometry, the rows correspond to the degrees of freedom
        # qF[d.o.f. index, row or deformed geometry index] -> value of d.o.f. for deformed geometry at index of self.deformed
        self.q0 = None
        """Vector of RIC values of reference geometry
        
        q[d.o.f. index, 0] -> value of d.o.f. for reference geometry

        Notes
        -----
        Publicly accessable for retrieval and reference, please refrain from manually setting this value as other analysis variables depend upon it."""

        self.qF = None
        """Matrix of RIC values of deformed geometries
        
        qF[d.o.f. index, row or deformed geometry index] -> value of d.o.f. for deformed geometry at index of self.deformed

        Notes
        -----
        Publicly accessable for retrieval and reference, please refrain from manually setting this value as other analysis variables depend upon it."""

        self.deltaQ = None
        """Matrix of changes in RIC values from reference geometry to each deformed geometry.
        
        deltaQ[d.o.f. index, row or deformed geometry index] -> value of d.o.f. for deformed geometry at index of self.deformed

        Notes
        -----
        Publicly accessable for retrieval and reference, please refrain from manually setting this value as other analysis variables depend upon it
        and it is a result of calculations in _populateQ()."""

        self._kill = False
        """Sentinel value indicating if any atoms of DOFs present in the input files should be removed from geometries, hessian, and analysis."""
        self._killAtoms = list()
        """List of atoms to be removed from geometries, hessian, and analysis"""
        self._killDOFs = list()
        """List of DOFs to be removed from geometries, hessian, and analysis"""

        # endregion

        self._validateFiles()
        print("Successfully initialized SITH object with given input files...")

# region Atomic Homicide

    def __kill(self):
        """Executes the removal of degrees of freedom (DOFs) specified and any associated with specified atoms."""
        print("Killing atoms and degrees of freedom...")
        self.__killDOFs(self._killDOFs)
        dimsToKill = list()
        for atom in self._killAtoms:
            dimsToKill.extend(
                [dim for dim in self._reference.dimIndices if atom in dim])
        self.__killDOFs(dimsToKill)
        print("Atoms and DOFs killed...")

        """Use Case Note:
        This is a private method to limit user error. Specification of these DOFs is made by the user programmatically with the public functions SetKillAtoms(atoms: list)
        and SetKillDOFs(dofs: list) prior to data extraction by calling SITH.extractData(). If no mismatch between
        number of DOFs in each geometry's coordinates and Hessian, this can be manually called after extractData()
        as well but is not recommended."""

    def __killDOFs(self, dofs: list[Tuple]):
        """
        Removes the indicated degrees of freedom from the JEDI analysis, as such it removes them from the geometries' RICs
        as well as from the Hessian matrix.
        """
        rIndices = list()
        for dof in dofs:
            rIndices.extend([i for i in range(self._reference.dims[0])
                            if self._reference.dimIndices[i] == dof])
        self._reference._killDOFs(rIndices)

# endregion

# region Public Functions meant to be used by novice-intermediate user

    @property
    def reference(self):
        """
        Return the reference geometry (SITH_Utilities.Geometry)
        """
        return getattr(self, '_reference')

    @property
    def deformed(self):
        """
        Return the list of deformed geometries (list<SITH_Utilities.Geometry>)
        """
        return getattr(self, '_deformed')

    @property
    def hessian(self):
        """Returns Hessian matrix used to calculate the stress energy analysis, default value is that of the reference Geometry's Hessian.

        Notes
        -----
        Hessian matrix is the analytical gradient of the harmonic potential energy surface at a reference geometry as calculated
        by a frequency analysis at the level of DFT or higher.

        While this value is accessable through the reference Geometry for retrieval purposes, please refrain from manually setting it.
        If you would like to manually change this value for a SITH object, instead implement the method setReference() and the associated refactoring recommended in its documentation."""
        return self.reference.hessian

    def setKillAtoms(self, atoms: list):
        """
        Takes in the atoms which should be removed from the reference geometry, must be used prior to calling SITH.extractData(), which also
        runs removeMismatchedDOFs.
        """
        self._killAtoms = atoms
        self._kill = True
        print("Atoms to be killed are set...")

    def setKillDOFs(self, dofs: list):
        """
        Takes in the DOFs (degrees of freedom) which should be removed from the reference geometry, must be used prior to calling SITH.extractData(),
        which also runs removeMismatchedDOFs.
        """
        self._killDOFs = dofs
        self._kill = True
        print("DOFs to be killed are set...")

    def removeMismatchedDOFs(self):
        """
        Removes any DOFs which are not in the reference geometry to ensure that all geometries have the correct DOFs.

        -----
        NOTE: If there are DOFs in the reference geometry that do not exist in the deformed geometry, it will mess up this method
        and indicates an issue with the calculation which must be fixed in the generation of input. Solution: https://gaussian.com/gic/ specify Active GIC in deformed opt
        """
        print("Removing DOFs in the deformed geometries which are not present in the reference geometry...")
        for deformation in self._deformed:
            dofsToRemove = list()
            for j in range(max(deformation.dims[0], self._reference.dims[0])):
                if j < deformation.dims[0]:
                    # deformed not in reference
                    if deformation.dimIndices[j] not in list(self._reference.dimIndices):
                        dofsToRemove.append(j)
                if j < self._reference.dims[0]:  # reference not in deformed
                    assert self._reference.dimIndices[j] in deformation.dimIndices, "Deformed geometry ("+deformation.name+") is missing reference DOF "+str(
                        self._reference.dimIndices[j])+"."

            deformation._killDOFs(dofsToRemove)

    def extractData(self):
        """
        Extracts, validates, curates data from input files, removes any specified atoms and DOFs .  

        -----
        Input files specified in SITH constructor, atoms and DOFs to remove previously specified by the user with
        SetKillAtoms or SetKillDOFs This method must always be called prior to energyAnalysis to extract and set up
        the relevant data."""
        print("Beginning data extraction...")
        self._getContents()

        rExtractor = Extractor(self._referencePath, self._rData)
        rExtractor._extract()
        # Create Geometry objects from reference and deformed data
        self._reference = rExtractor.getGeometry()
        self._deformed = list()
        for dd in self._dData:
            dExtractor = Extractor(dd[0], dd[1])
            dExtractor._extract()
            self._deformed.append(dExtractor.getGeometry())

        print("Finished data extraction...")

        # Defaults to the reference geometry Hessian, it is recommended to make new SITH objects for each new analysis for the
        # sake of clearer output files but implementation of SITH.SetReference() as a public function would enable the user to
        # manually swap the reference geometry with that of another geometry in the deformd list and then re-run analysis.

        # Killing of atoms should occur here prior to validation for the sake of DOF # atoms consistency, as well as before
        # populating the q vectors to ensure that no data which should be ignored leaks into the analysis
        if self._kill:
            self.__kill()

        self.removeMismatchedDOFs()

        self._validateGeometries()

        self._populateQ()
        print("Finished setting up for energy analysis...")

    def energyAnalysis(self):
        """
        Performs the SITH energy analysis, populates energies, deformationEnergy, and pEnergies.

        Notes
        -----
        Consists of the dot multiplication of the deformation vectors and the Hessian matrix 
        (analytical gradient of the harmonic potential energy surface) to produce both the total calculated change in energy
        between the reference structure and each deformed structure (SITH.deformationEnergy) as well as the subdivision of that energy into
        each DOF (SITH.energies)."""
        print("Performing energy analysis...")
        if self.deltaQ is None or self.q0 is None or self.qF is None:
            raise Exception(
                "Populate Q has not been executed so necessary data for analysis is lacking. This is likely due to not calling extractData().")
        self.energies = np.zeros(
            (self.reference.dims[0], len(self._deformed)))
        self.deformationEnergy = np.zeros((1, len(self._deformed)))
        self.pEnergies = np.zeros(
            (self._reference.dims[0], len(self._deformed)))

        for i in range(len(self._deformed)):
            self.deformationEnergy[0, i] = 0.5 * np.transpose(self.deltaQ[:, i]).dot(
                self._reference.hessian).dot(self.deltaQ[:, i])  # scalar 1x1 total Energy
            for j in range(self._reference.dims[0]):
                isolatedDOF = np.hstack((np.zeros(j), self.deltaQ[j, i], np.zeros(
                    self._reference.dims[0]-j-1)))
                self.energies[j, i] = 0.5 * \
                    (isolatedDOF).dot(self._reference.hessian).dot(
                        self.deltaQ[:, i])
            self.pEnergies[:, i] = float(
                100) * self.energies[:, i] / self.deformationEnergy[0, i]

        print("Execute Order 67. Successful energy analysis completed.")

    def setReference(self, geometryName: str):
        """
        Replaces the current reference geometry used for calculation of stress energy with the specified geometry, pushing the current
        reference geometry to the deforation list.
        If the specified geometry does not exist or has no Hessian, the reference geometry will simply not be changed. Deformation
        energy is still calculated for all geometries aside from the new reference geometry.
        """

        """Implementation Instructions:
        To implement this without re-extracting the data (which is basically the current workflow of creating a new SITH instead),
        you must set the SITH._reference geometry to that with the new geometryName, move the old reference geometry into the list of
        deformed geometries, and then _validateGeometries() _populateQ(). This seems unnecessary as the cost which it saves is minimal."""
        raise NotImplementedError(
            "Unimplemented due to current lack of necessity, contact @mmfarrugia on github for more info.")
        """Use Case Note:
        This can be useful for cases where the error increases unacceptably and multiple reference points along a 
        deformation are needed in order to have a more accurate energy calculation as the stretching coordinate progresses."""

# endregion

# region Validation

    def _validateFiles(self):
        """
        Check that all files exist and whether the deformed path is a directory
        """
        print("Validating input files...")
        assert self._referencePath.exists(), "Path to reference geometry data does not exist."
        assert self._deformedPath.exists(), "Path to deformed geometry data does not exist."

        self.__deformedIsDirectory = self._deformedPath.is_dir()

    def _validateGeometries(self):
        """
        Ensure that the reference and deformed geometries are compatible(# atoms, # dofs, etc.)
        """
        print("Validating geometries...")
        assert all([deformn.nAtoms == self._reference.nAtoms and np.array_equal(deformn.dims, self._reference.dims) and np.array_equal(
            deformn.dimIndices, self._reference.dimIndices) for deformn in self._deformed]), "Incompatible number of atoms or dimensions amongst input files."

# endregion

    def _getContents(self):
        """
        Gets the contents of the input files, including those in a deformed directory and verifies they are not empty.
        """
        print("Retrieving file contents...")
        try:
            with self._referencePath.open() as rFile:
                self._rData = rFile.readlines()
                assert len(self._rData) > 0, "Reference data file is empty."

            self._dData = list()
            if self.__deformedIsDirectory:
                dPaths = list(sorted(self._deformedPath.glob('*.fchk')))
                dPaths = [pathlib.Path(dp) for dp in dPaths]
            else:
                dPaths = [self._deformedPath]

            assert len(dPaths) > 0, "Deformed directory is empty."
            for dp in dPaths:
                with dp.open() as dFile:
                    dLines = dFile.readlines()
                    assert len(
                        dLines) > 0, "One or more deformed files are empty."
                    self._dData.append((dp, dLines))

        except AssertionError:
            # This exception catch is specific so that the AssertionErrors are not caught and only "raise" is called so as to maintain the original
            # stack trace
            raise
        except:
            print(
                "An exception occurred during the extraction of the input files' contents.")
            sys.exit(sys.exc_info()[0])

    def _populateQ(self):
        """Populates the reference RIC vector q0, deformed RIC matrix qF, and a matrix deltaQ containing the changes in RICs."""
        print("Populating RIC vectors and calculating \u0394q...")
        self.q0 = np.zeros((self._reference.dims[0], 1))
        self.qF = np.zeros((self._reference.dims[0], 1))
        self.q0[:, 0] = np.transpose(np.asarray(self._reference.ric))
        # qF columns correspond to each deformed geometry, the rows correspond to the degrees of freedom
        # qF[d.o.f. index, row or deformed geometry index] -> value of d.o.f. for deformed geometry at index of self.deformed
        self.qF[:, 0] = np.transpose(np.asarray(self._deformed[0].ric))
        if len(self._deformed) > 1:
            for i in range(1, len(self._deformed)):
                deformation = self._deformed[i]
                temp = np.transpose(np.asarray(deformation.ric))
                self.qF = np.column_stack((self.qF, temp))
            # delta_q is organized in the same shape as qF
        self.deltaQ = np.subtract(self.qF, self.q0)

        """This adjustment is to account for cases where dihedral angles oscillate about 180 degrees or pi and, since the 
        coordinate system in Gaussian for example is from pi to -pi, where k and l are small, it shows up as 
        -   -(pi-k) - (pi - l) = -2pi + (k+l) should be: -(k + l) 
                --> -(result + 2pi)
        +   (pi - k) - -(pi - l) = 2pi - (k+l) should be (k+l)
                --> -(result - 2pi) = 2pi - result
        """
        with np.nditer(self.deltaQ, op_flags=['readwrite']) as dqit:
            for dq in dqit:
                #         dq[...] = np.abs(dq - 2*np.pi) if dq > (2*np.pi -
                #                                                 0.005) else (dq + 2*np.pi if dq < -(2*np.pi - 0.005) else dq)
                if dq > np.pi:
                    blah = 3
                dq[...] = 2*np.pi - dq if dq > np.pi else (-(dq + 2*np.pi) if dq < -np.pi else dq)
