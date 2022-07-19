from re import L
from typing import Tuple
from SITH import SITH
from SITH_Utilities import UnitConverter
import numpy as np


class SithResults:

    def writeFiles(self, sith: SITH) -> bool:
        pass

    def writeSummary(self, sith:SITH):
        totE = self.buildTotEnergiesString(sith)
        dq = self.buildDeltaQString(sith)
        ric = self.buildInternalCoordsString(sith)
        energies = self.buildEnergyMatrix(sith)

        with open(sith.rPath.parent.as_posix()+'summary.txt', "w") as s:
            s.write("Summary of SITH analysis\n")
            s.write("Redundant Internal Coordinate Definitions\n**Defined by indices of involved atoms**\n")
            s.writelines('\n'.join(ric))
            s.write("Changes in internal coordinates (Delta q)\n**Distances given in Angstroms, angles given in degrees**\n")
            s.writelines('\n'.join(dq))


    def buildTotEnergiesString(self, sith: SITH) -> list:
        pass

    def buildDeltaQString(self, sith: SITH) -> list:
        """
        Returns a list of strings containing the change in internal coordinates in each degree of freedom 
        per deformed geometry. Data is in Angstroms and degrees of the format:
        DOF Index       Deformation 1       Deformation 2       ...
        1               change              change              ...
        2               change              change              ...
        ...
        """
        uc = UnitConverter()
        dqAngstroms = list()
        header = "DOF \t"
        for deformation in sith.deformed:
            header += str(deformation.name)+"\t"
        dqAngstroms.append(header)
        dqAng = [uc.bohrToAngstrom(dq)
                 for dq in sith.delta_q[0:sith.relaxed.dims[1], :]]
        dqAng = np.asarray(dqAng)
        dqAng = dqAng.astype(str)
        for dof in range(sith.relaxed.dims[1]):
            if len(sith.deformed) > 1:
                line = str(dof+1) + "\t" + '\t'.join(dqAng[dof, :])
                dqAngstroms.append(line)
            else:
                line = str(dof+1) + "\t" + dqAng[dof][1:-2]
                dqAngstroms.append(line)
        dqDeg = np.degrees(sith.delta_q[sith.relaxed.dims[1]:, :])
        dqDeg = np.asarray(dqDeg)
        dqDeg = dqDeg.astype(str)
        for dof in range(sith.relaxed.dims[2]+sith.relaxed.dims[3]):
            if len(sith.deformed) > 1:
                line = str(
                    dof+1+sith.relaxed.dims[1]) + "\t" + '\t'.join(dqDeg[dof, :])
                dqAngstroms.append(line)
            else:
                line = str(
                    dof+1+sith.relaxed.dims[1]) + "\t" + str(dqDeg[dof][0])
                dqAngstroms.append(line)

        return dqAngstroms

    def writeDeltaQ(self, sith: SITH) -> bool:
        dqPrint = self.buildDeltaQString(sith)
        with open('delta_q.txt', "w") as dq:
            dq.writelines('\n'.join(dqPrint))

    def buildInternalCoordsString(self, sith: SITH) -> list:
        """
        Returns a list of strings containing the atom indices involved in each degree of freedom.
        """
        return [str(dof+1) + '\t' + str(sith.relaxed.dimIndices[dof]) for dof in range(sith.relaxed.dims[0])]

    def buildEnergyMatrix(self, sith: SITH) -> list:
        """
        Returns a list of strings containing the energy in each degree of freedom per deformed geometry.
        Data is in Hartrees and of the format:
        DOF Index       Deformation 1       Deformation 2       ...
        1               stress E            stress E            ...
        2               stress E            stress E            ...
        ...             ...                 ...                 ...
        """
        uc = UnitConverter()
        eMat = list()
        header = "DOF \t"
        for deformation in sith.deformed:
            header += str(deformation.name)+"\t"
        eMat.append(header)
        eStrings = sith.energies.astype(str)
        for dof in range(sith.relaxed.dims[0]):
            line = str(dof+1) + "\t" + '\t'.join(eStrings[dof, :])
            eMat.append(line)
        return eMat

    def writeEnergyMatrix(self, sith: SITH) -> bool:
        ePrint = self.buildEnergyMatrix(sith)
        with open('E_RICS.txt', "w") as dq:
            dq.writelines('\n'.join(ePrint))

    def compareEnergies(self, sith: SITH) -> Tuple:
        expectedDE = np.zeros((1, len(sith.deformed)))
        for i in range(len(sith.deformed)):
            expectedDE[0, i] = sith.deformed[i].energy - sith.relaxed.energy
        errorDE = sith.deformationEnergy - expectedDE
        pErrorDE = 100 * errorDE / expectedDE
        return (expectedDE, errorDE, pErrorDE)

    def writeComparison(self, sith: SITH):
        expectedDE, errorDE, pErrorDE = self.compareEnergies(sith)
        with open('pError.txt', "w") as dq:
            dq.writelines('\n'.join(pErrorDE.astype(str)))
