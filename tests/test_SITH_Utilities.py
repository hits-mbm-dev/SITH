from curses.ascii import SI
from numpy import float32
import pytest
from pytest import approx
from ase import Atom

from src.SITH.Utilities import Extractor, Geometry, UnitConverter, SummaryReader
from src.SITH.SITH import SITH
from tests.test_resources import *
from ase import Atom
from ase import units
from src.SITH.SithWriter import write_summary

""" LTMatrix has already been tested by its creator on github,
 but should add in their testing just in case """


# region Geometry Tests


def test_geometry():
    geo = Geometry('testName', 'blah', 3)
    assert geo.name == 'testName'
    assert geo._path == 'blah'
    assert geo.n_atoms == 3
    assert geo.energy == None


def test_geo_energy():
    geo = Geometry('blah', 'blah', 6)
    geo.energy = 42
    assert geo.name == 'blah'
    assert geo.n_atoms == 6
    assert geo.energy == 42


def test_build_RICGood():
    geo = Geometry('methanol-test', 'blah', 6)
    geo.build_RIC(dims, dim_indicesGoodInput, coordLinesGoodInput)
    assert geo.dims == dims
    assert geo.dim_indices == dim_indices
    assert compare_arrays(geo.ric, coords)


def test_equals():
    geoCopy = deepcopy(refGeo)
    assert geoCopy == refGeo
    assert refGeo != Geometry('test', 'test', 6)
    geo = Geometry('methanol-test', 'blah', 6)
    geo.build_RIC(dims, dim_indicesGoodInput, coordLinesGoodInput)
    assert refGeo != geo
    geoCopy.name = 'blah'
    assert geoCopy != refGeo
    geoCopy.name = refGeo.name
    geoCopy.hessian = geoCopy.hessian[1:]
    assert geoCopy != refGeo
    geoCopy.hessian = refGeo.hessian
    geoCopy.atoms[3].symbol = 'C'
    geoCopy.atoms[3].position = [1., 1., 1.]
    assert geoCopy != refGeo
    geoCopy.atoms = refGeo.atoms
    assert geoCopy == refGeo
    geoCopy.energy = 0
    assert geoCopy != refGeo
    geoCopy.energy = refGeo.energy
    geoCopy.ric[2] = 26
    assert geoCopy != refGeo
    geoCopy.ric = refGeo.ric
    geoCopy.dim_indices[2] = (1, 2)
    assert geoCopy != refGeo


# region bad coordinates


def test_letterCoord():
    letterCoord = coordLinesGoodInput + ['blah']
    geo = Geometry('methanol-test', 'blah', 6)
    with pytest.raises(Exception) as e:
        geo.build_RIC(dims, dim_indicesGoodInput, letterCoord)
    assert str(
        e.value) == "Redundant internal coordinates contains invalid values, such as strings."


def test_moreCoords():
    coordsMore = coordLinesGoodInput + ['100.78943']
    geo = Geometry('methanol-test', 'blah', 6)
    with pytest.raises(Exception) as e:
        geo.build_RIC(dims, dim_indicesGoodInput, coordsMore)
    assert str(e.value) == "Mismatch between the number of degrees of freedom expected (" + \
        str(dims[0])+") and number of coordinates given ("+str(dims[0]+1)+")."


def test_lessCoords():
    coordsLess = coordLinesGoodInput[1:]
    geo = Geometry('methanol-test', 'blah', 6)
    with pytest.raises(Exception) as e:
        geo.build_RIC(dims, dim_indicesGoodInput, coordsLess)
    assert str(e.value) == "Mismatch between the number of degrees of freedom expected (" + \
        str(dims[0])+") and number of coordinates given ("+str(dims[0]-5)+")."


# endregion

# region bad Indices


def test_riciBad():
    geo = Geometry('methanol-test', 'blah', 6)
    with pytest.raises(Exception) as e:
        geo.build_RIC(dims, dim_indices59, coordLinesGoodInput)
    assert str(
        e.value) == "One or more redundant internal coordinate indices are missing or do not have the expected format. Please refer to documentation"
    with pytest.raises(Exception) as e:
        geo.build_RIC(dims, dim_indices59[1:], coordLinesGoodInput)
    assert str(
        e.value) == "One or more redundant internal coordinate indices are missing or do not have the expected format. Please refer to documentation"


def test_riciLetters():
    geo = Geometry('methanol-test', 'blah', 6)
    with pytest.raises(Exception) as e:
        geo.build_RIC(dims, dim_indicesLetters, coordLinesGoodInput)
    assert str(
        e.value) == "Invalid atom index given as input."


def test_riciNumIndices():
    geo = Geometry('methanol-test', 'blah', 6)
    with pytest.raises(Exception) as e:
        geo.build_RIC(dims, dim_indicesNumI, coordLinesGoodInput)
    assert str(
        e.value) == "Mismatch between given 'RIC dimensions' and given RIC indices."


def test_riciInvalid():
    dim_indicesInvalid = [
        '           1           7           0           0           1           3']+dim_indicesGoodInput[1:]
    geo = Geometry('methanol-test', 'blah', 6)
    with pytest.raises(Exception) as e:
        geo.build_RIC(dims, dim_indicesInvalid, coords)
    assert str(e.value) == "Invalid atom index given as input."


def test_build_RICIBad():
    geo = Geometry('methanol-test', 'blah', 6)
    with pytest.raises(Exception) as e:
        geo.build_RIC(dims, dim_indicesGoodInput[2:], coordLinesGoodInput)
    assert str(
        e.value) == "One or more redundant internal coordinate indices are missing or do not have the expected format. Please refer to documentation"

# endregion


def test_build_RIC_badDims():
    geo = Geometry('methanol-test', 'blah', 6)
    with pytest.raises(Exception) as e:
        geo.build_RIC([16, 5, 7, 3], dim_indicesGoodInput, coordLinesGoodInput)
    assert str(
        e.value) == "Invalid quantities of dimension types (bond lengths, angles, dihedrals) given in .fchk."
    with pytest.raises(Exception) as e:
        geo.build_RIC([16, 'h', 7, 3], dim_indicesGoodInput, coordLinesGoodInput)
    assert str(
        e.value) == "Invalid input given for Redundant internal dimensions."

# region Cartesian

def test_build_atoms():
    geo = Geometry('methanol-test', 'blah', 6)
    geo.build_atoms(cartesianCoords, atomicList)
    assert geo.n_atoms == 6 == len(geo.atoms)
    assert all(geo.atoms[i] == refAtoms[i] for i in range(6))


def test_build_atoms_integrated():
    assert refGeo.n_atoms == 6 == len(refGeo.atoms)
    assert all(refGeo.atoms[i] == refAtoms[i] for i in range(6))


# endregion


def test_killDOF():
    sith = SITH(x0string, deformedString)
    sith.extract_data()
    assert compare_arrays(sith.reference.hessian, eHessFull)
    sith._reference._kill_DOFs([0])
    assert all(sith._reference.dim_indices == dim_indices[1:])
    assert sith._reference.dims == array('i', [14, 4, 7, 3])
    assert compare_arrays(sith.reference.hessian, eHessKill0)


def test_kill_DOFs():
    sith = SITH(x0string, deformedString)
    sith.extract_data()
    assert compare_arrays(sith._reference.hessian, eHessFull)
    sith._reference._kill_DOFs([0, 14])
    assert all(sith._reference.dim_indices == dim_indices[1:14])
    assert sith._reference.dims == array('i', [13, 4, 7, 2])
    assert compare_arrays(sith.reference.hessian, eHessKill0_14)

# endregion


# region Extractor Tests


def test_creationEmptyList():
    extractor = Extractor(testPath, [])
    assert extractor._path == testPath
    assert extractor._name == testPath.stem


def test_extract():
    extractor = Extractor(testPath, frankenNoLines)
    extractor._extract()
    assert compare_arrays(np.array(extractor.h_raw), ehRaw)


def test_extractedGeometry():
    extractor = Extractor(Path(
        '/hits/fast/mbm/farrugma/sw/SITH/tests/frankenTest-methanol.fchk'), frankenNoLines)
    extractor._extract()
    geo = extractor.get_geometry()
    egeo = Geometry('frankenTest-methanol', 'blah', 6)
    egeo.energy = energy
    egeo.atoms = geo.atoms
    egeo.build_RIC(dims, dim_indicesGoodInput, coordLinesGoodInput)
    egeo.build_atoms(cartesianCoords, atomicList)
    egeo.hessian = eHessFull
    assert geo == egeo

def test_build_atoms():
    extractor = Extractor(Path(
        '/hits/fast/mbm/farrugma/sw/SITH/tests/frankenTest-methanol.fchk'), frankenNoLines)
    extractor._extract()
    geo = extractor.get_geometry()
    assert geo.atoms.get_chemical_formula() == refAtoms.get_chemical_formula()
    assert geo.atoms.positions.flatten() == approx(refAtoms.positions.flatten(), abs=1E-5)


def test_buildHessian():
    extractor = Extractor(testPath, frankenNoLines)
    extractor._extract()
    hess = extractor.hessian
    assert compare_arrays(eHessFull, hess)


def test_getGeometry():
    extractor = Extractor(testPath, frankenNoLines)
    egeo = Geometry('testName', 'blah', 3)
    with pytest.raises(Exception) as e:
        geo = extractor.get_geometry()
    assert str(e.value) == "There is no geometry."
    extractor.geometry = Geometry('testName', 'blah', 3)
    geo = extractor.get_geometry()
    assert geo == egeo


# endregion

def test_units():
    assert UnitConverter.angstrom_to_bohr(1.3) == approx(2.456644)
    assert UnitConverter.bohr_to_angstrom(1.3) == approx(0.68793035)
    assert UnitConverter.radian_to_degree(1.3) == approx(74.48451)

def test_compares():
    foo = np.full((3,3), 4.678)
    bar = np.full((3,3), 4.67799999)
    assert compare_arrays(foo, bar)
    bar = np.full((3,3), 4.5)
    assert not compare_arrays(foo, bar)


#  Region Summary Reader

def test_summary_reader():
    sith = SITH(x0string, deformedString)
    sith.extract_data()
    sith.analyze()
    write_summary(sith, includeXYZ=True)
    path = sith._referencePath.parent.as_posix()+sith._referencePath.root

    print(path)

    sith_result = SummaryReader(path + 'summary.txt')


    assert sith_result._reference.dim_indices == \
           sith._reference.dim_indices, \
           "Error reading degrees of freedom from summary.txt"
    assert (sith_result._reference.dims == sith._reference.dims).all(), \
           "Error reading dimensions from summary.txt"
    dims = sith_result._reference.dims
    assert sith_result.deltaQ[:dims[1]] == approx(sith.deltaQ[:dims[1]]* units.Bohr)
    assert sith_result.deltaQ[dims[1]:] == approx(sith.deltaQ[dims[1]:]* 180/np.pi)
    e0 = sith._reference.energy
    expected = list()
    for conf in sith._deformed:
        expected.append(conf.energy - e0)
    expected = np.array(expected)

    assert sith_result.accuracy[0] == approx(sith.deformationEnergy[0])
    assert sith_result.accuracy[1] == approx(expected)
    assert sith_result.energies == approx(sith.energies)
    assert sith_result._deformed[0].atoms.positions == \
           approx(sith._deformed[0].atoms.positions)

    # Atoms
    assert sith_result._reference.atoms.positions == approx(sith._reference.atoms.positions)
    assert (sith_result._reference.atoms.get_atomic_numbers() == 
            sith._reference.atoms.get_atomic_numbers()).all()
    for i in range(len(sith_result._deformed)):
        assert sith_result._deformed[i].atoms.positions == approx(sith._deformed[i].atoms.positions)
        assert (sith_result._deformed[i].atoms.get_atomic_numbers() == 
                sith._deformed[i].atoms.get_atomic_numbers()).all()
