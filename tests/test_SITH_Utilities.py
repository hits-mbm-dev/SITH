from genericpath import exists
from numpy import extract
import pytest
from SITH_Utilities import *
import pathlib

""" LTMatrix has already been tested by its creator on github,
 but should add in their testing just in case """


def test_atomCreation():
    atom = Atom('C', [2.3, 4.6, 7.8])
    assert atom.element is 'C'

# region Geometry Tests


def test_geometryName():
    geo = Geometry('testName', 3)
    assert geo.name == 'testName'


def test_geometryNAtoms():
    geo = Geometry('testName', 3)
    assert geo.nAtoms == 3


def test_dumbGeoCreationErrors():
    geo = Geometry('blah', 6)
    assert geo.energy == np.inf


def test_getEnergyGood():
    geo = Geometry('blah', 6)
    geo.energy = 42
    assert geo.energy == 42
    assert geo.getEnergy() == 42


def test_getEnergyBad():
    geo = Geometry('blah', 6)
    with pytest.raises(Exception) as e_info:
        blah = geo.getEnergy()


# region Testing Variables
dims = [15, 5, 7, 3]
dimsGoodInput = ["          15           5           7           3"]
dimIndicesGoodInput = ['           1           2           0           0           1           3',
                       '           0           0           1           4           0           0',
                       '           1           5           0           0           5           6',
                       '           0           0           2           1           3           0',
                       '           2           1           4           0           2           1',
                       '           5           0           3           1           4           0',
                       '           3           1           5           0           4           1',
                       '           5           0           1           5           6           0',
                       '           2           1           5           6           3           1',
                       '           5           6           4           1           5           6']
coordLinesGoodInput = ['  2.06335755E+00  2.07679249E+00  2.07679461E+00  2.73743812E+00  1.83354933E+00',
                       '  1.90516186E+00  1.90518195E+00  1.84167462E+00  1.91434964E+00  1.94775283E+00',
                       '  1.94775582E+00  1.96310537E+00 -3.14097002E+00 -1.07379153E+00  1.07501112E+00']
coords = [float(2.06335755E+00), 2.07679249, 2.07679461, 2.73743812, 1.83354933, 1.90516186E+00,
          1.90518195,  1.84167462,  1.91434964,  1.94775283, 1.94775582,  1.96310537, -3.14097002,
          -1.07379153,  1.07501112E+00]
bonds = [float(2.06335755E+00), 2.07679249, 2.07679461, 2.73743812, 1.83354933]
angles = [1.90516186E+00, 1.90518195,  1.84167462,
          1.91434964,  1.94775283, 1.94775582,  1.96310537]
diheds = [-3.14097002, -1.07379153,  1.07501112E+00]

dimIndices = [(1, 2), (1, 3), (1, 4), (1, 5), (5, 6), (2, 1, 3), (2, 1, 4), (2, 1, 5),
              (3, 1, 4), (3, 1, 5), (4, 1, 5), (1, 5, 6), (2, 1, 5, 6), (3, 1, 5, 6), (4, 1, 5, 6)]


# endregion Testing Variables

def test_buildRICGood():
    geo = Geometry('methanol-test', 6)
    geo.buildRIC(dims, dimIndicesGoodInput, coordLinesGoodInput)
    assert geo.dims == dims
    assert geo.dimIndices == dimIndices
    assert geo.rawRIC == coords
    assert geo.lengths == bonds
    assert geo.angles == angles
    assert geo.diheds == diheds


# region bad coordinates

def test_moreCoords():
    coordsMore = coordLinesGoodInput + ['100.78943']
    geo = Geometry('methanol-test', 6)
    with pytest.raises(Exception) as e:
        geo.buildRIC(dims, dimIndicesGoodInput, coordsMore)
    assert str(e.value) == "Mismatch between the number of degrees of freedom expected (" + \
        str(dims[0])+") and number of coordinates given ("+str(dims[0]+1)+")."


def test_lessCoords():
    coordsLess = coordLinesGoodInput[1:]
    geo = Geometry('methanol-test', 6)
    with pytest.raises(Exception) as e:
        geo.buildRIC(dims, dimIndicesGoodInput, coordsLess)
    assert str(e.value) == "Mismatch between the number of degrees of freedom expected (" + \
        str(dims[0])+") and number of coordinates given ("+str(dims[0]-5)+")."


# endregion

# region bad Indices

dimIndices59 = ['           1           2           0           0           1           3',
                '           0           0           1           4           0           0',
                '           1           5           0           0           5           6',
                '           0           0           2           1           3           0',
                '           2           1           4           0           2           1',
                '           5           0           3           1           4           0',
                '           3           1           5           0           4           1',
                '           5           0           1           5           6           0',
                '           2           1           5           6           3           1',
                '           5           6           4           1           5']

dimIndicesLetters = ['           1           2           k           0           1           3',
                     '           0           0           1           4           0           0',
                     '           1           l           0           0           5           6',
                     '           0           0           2           1           3           0',
                     '           2           1           A           0           2           1',
                     '           5           0           t           1           4           0',
                     '           3           1           5           0           4           1',
                     '           5           0           1           5           6           0',
                     '           2           1           5           6           3           1',
                     '           5           6           4           1           5           6']

dimIndicesNumI = ['           1           2           0           0           1           3',
                  '           0           0           1           4           0           0',
                  '           1           5           0           0           5           6',
                  '           0           0           2           1           3           0',
                  '           2           1           4           0           2           1',
                  '           5           0           3           1           4           0',
                  '           3           1           5           0           4           1',
                  '           5           0           1           5           6           0',
                  '           2           1           5           6           3           1',
                  '           5           0           4           1           5           6']


def test_riciBad():
    geo = Geometry('methanol-test', 6)
    with pytest.raises(Exception) as e:
        geo.buildRIC(dims, dimIndices59, coordLinesGoodInput)
    assert str(
        e.value) == "Redundant internal coordinate indices input has invalid dimensions."

#! Modify to have a specific flag for this potentially


def test_riciLetters():
    geo = Geometry('methanol-test', 6)
    with pytest.raises(Exception) as e:
        geo.buildRIC(dims, dimIndicesLetters, coordLinesGoodInput)
    assert str(
        e.value) == "Invalid atom index given as input."


def test_riciNumIndices():
    geo = Geometry('methanol-test', 6)
    with pytest.raises(Exception) as e:
        geo.buildRIC(dims, dimIndicesNumI, coordLinesGoodInput)
    assert str(
        e.value) == "Mismatch between given 'RIC dimensions' and given RIC indices."


def test_riciInvalid():
    dimIndicesInvalid = [
        '           1           7           0           0           1           3']+dimIndicesGoodInput[1:]
    geo = Geometry('methanol-test', 6)
    with pytest.raises(Exception) as e:
        geo.buildRIC(dims, dimIndicesInvalid, coords)
    assert str(e.value) == "Invalid atom index given as input."


def test_buildRICBad():
    geo = Geometry('methanol-test', 6)
    with pytest.raises(Exception) as e:
        geo.buildRIC(dims, dimIndicesGoodInput[2:], coordLinesGoodInput)
    assert str(
        e.value) == "Redundant internal coordinate indices input has invalid dimensions."

# endregion

# region Cartesian


def test_buildCartesian():
    pass


def test_getAtoms():
    pass

# endregion

#region validity as relaxed or deformed (might move to extractor not Geometry? might not even need)

def test_validRelaxed():
    pass
def test_invalidRelaxed():
    pass
def test_validDeformed():
    pass
def test_invalidDeformed():
    pass

# endregion

# region Extractor Tests


testPath = pathlib.Path(
    "/hits/fast/mbm/farrugma/sw/SITH/tests/test-methanol.fchk")

# region Cartesian


def test_writeXYZ():
    pass

# endregion


frankenLines = ["Title Card Required                                                     ",
                "Freq      RBMK                                                        6-31+G              ",
                "Number of atoms                            I                6",
                "Info1-9                                    I   N=           9",
                "          20          20        1002           0           0         100",
                "           6          18        -402",
                "Full Title                                 C   N=           2",
                "Title Card Required     ",
                "Route                                      C   N=           6",
                "#N Geom=AllCheck Guess=TCheck SCRF=Check GenChk RBMK/6-31+G ",
                "Freq        ",
                "Charge                                     I                0",
                "Multiplicity                               I                1",
                "Number of electrons                        I               18",
                "Number of alpha electrons                  I                9",
                "Number of beta electrons                   I                9",
                "Number of basis functions                  I               34",
                "Number of independent functions            I               34",
                "Number of point charges in /Mol/           I                0",
                "Number of translation vectors              I                0",
                "Atomic numbers                             I   N=           6",
                "           6           1           1           1           8           1",
                "Nuclear charges                            R   N=           6",
                "  6.00000000E+00  1.00000000E+00  1.00000000E+00  1.00000000E+00  8.00000000E+00",
                "  1.00000000E+00",
                "Current cartesian coordinates              R   N=          18",
                "  1.29417810E+00 -4.32713119E-02 -5.45952627E-06  2.04157734E+00  1.87996481E+00",
                "  1.24203760E-03  1.96311705E+00 -1.03552819E+00  1.69734955E+00  1.96333305E+00",
                " -1.03345246E+00 -1.69848973E+00 -1.42964555E+00  2.29404703E-01 -6.75348554E-06",
                " -2.29593165E+00 -1.38659392E+00 -1.50733683E-05",
                "Number of symbols in /Mol/                 I                0",
                "Redundant internal dimensions              I   N=           4",
                "          15           5           7           3",
                "Redundant internal coordinate indices      I   N=          60",
                "           1           2           0           0           1           3",
                "           0           0           1           4           0           0",
                "           1           5           0           0           5           6",
                "           0           0           2           1           3           0",
                "           2           1           4           0           2           1",
                "           5           0           3           1           4           0",
                "           3           1           5           0           4           1",
                "           5           0           1           5           6           0",
                "           2           1           5           6           3           1",
                "           5           6           4           1           5           6",
                "Redundant internal coordinates             R   N=          15",
                "  2.06335755E+00  2.07679249E+00  2.07679461E+00  2.73743812E+00  1.83354933E+00",
                "  1.90516186E+00  1.90518195E+00  1.84167462E+00  1.91434964E+00  1.94775283E+00",
                "  1.94775582E+00  1.96310537E+00 -3.14097002E+00 -1.07379153E+00  1.07501112E+00",
                "ZRed-IntVec                                I   N=          15",
                "SCF Energy                                 R     -1.156178353208529E+02",
                "Total Energy                               R     -1.156178353208529E+02",
                "RMS Force                                  R      4.346840957270929E-05",
                "Internal Forces                            R   N=          15",
                " -9.53654507E-07  5.54944244E-05  5.36428926E-05  1.11048939E-04 -1.13114423E-05",
                " -1.04133321E-05 -1.14977466E-05  5.14356085E-05 -2.03746782E-05 -1.12719672E-07",
                " -7.03942022E-06 -2.02593378E-05 -3.55445007E-06  1.47929309E-05 -1.69294398E-05",
                "Internal Force Constants                   R   N=         120",
                "  3.62723627E-01  2.46348927E-03  3.41917429E-01  2.46449426E-03  3.25566476E-03",
                "  3.41950225E-01  7.71914399E-03  1.30144832E-02  1.30190899E-02  3.24845899E-01",
                " -2.18477593E-03  2.12696837E-04  2.11083552E-04 -7.61933194E-03  5.14858537E-01",
                "  7.17776914E-03  9.03061862E-03 -6.02514232E-03 -3.10222678E-02 -5.11022394E-04",
                "  7.55620474E-02  7.17957645E-03 -6.02503247E-03  9.03284208E-03 -3.10249738E-02",
                " -5.12450149E-04  3.50280628E-03  7.55643750E-02  3.51789726E-03 -6.02518942E-03",
                " -6.02417692E-03  3.62331385E-02  6.60675935E-03 -4.07719225E-02 -4.07708165E-02",
                "  1.44603144E-01 -5.07019718E-03  9.17940725E-03  9.18246256E-03 -3.12325787E-02",
                "  1.00393859E-03  4.77039018E-03  4.76856342E-03 -3.31898386E-03  7.63738231E-02",
                " -5.88766275E-03 -3.17944405E-04 -6.26361412E-03  2.83396182E-02 -3.18071640E-03",
                " -3.78565914E-02 -3.40048459E-03 -2.83920351E-02 -4.23288555E-02  1.42663152E-01",
                " -5.88635984E-03 -6.26533369E-03 -3.25987053E-04  2.83457368E-02 -3.17436646E-03",
                " -3.40100972E-03 -3.78585761E-02 -2.83919305E-02 -4.23274108E-02 -3.27461865E-02",
                "  1.42661775E-01  2.12618147E-03 -3.53392980E-04 -3.51024158E-04  5.45172698E-02",
                "  2.37792321E-02 -6.28318797E-03 -6.28838368E-03  2.10278856E-02  5.10326813E-04",
                " -4.30852365E-03 -4.29403633E-03  1.72316804E-01 -2.64064056E-07 -7.19850721E-03",
                "  7.19901756E-03 -2.62564164E-06  1.91208932E-06 -2.23638854E-02  2.23642115E-02",
                " -3.23068814E-06 -2.55120719E-07 -1.87404587E-02  1.87430558E-02 -2.34839767E-06",
                "  2.57500236E-02  7.59781830E-03 -1.57261390E-04 -6.96535945E-03 -4.12347221E-04",
                "  1.67083950E-03  2.36818040E-02  2.73101184E-04  2.29054272E-02 -1.87178773E-02",
                " -5.54264765E-03 -1.97515768E-02  2.80888484E-03 -1.10057269E-02  2.82103520E-02",
                " -7.60122832E-03  6.96755519E-03  1.58797378E-04  4.06144568E-04 -1.66873192E-03",
                " -2.71008719E-04 -2.36830894E-02 -2.29151302E-02  1.87196312E-02  1.97548270E-02",
                "  5.54644198E-03 -2.81529686E-03 -1.10041955E-02 -1.46179929E-02  2.82178084E-02",
                "Mulliken Charges                           R   N=           6"]

energy = -1.156178353208529E+02

hLines = ["  3.62723627E-01  2.46348927E-03  3.41917429E-01  2.46449426E-03  3.25566476E-03",
          "  3.41950225E-01  7.71914399E-03  1.30144832E-02  1.30190899E-02  3.24845899E-01",
          " -2.18477593E-03  2.12696837E-04  2.11083552E-04 -7.61933194E-03  5.14858537E-01",
          "  7.17776914E-03  9.03061862E-03 -6.02514232E-03 -3.10222678E-02 -5.11022394E-04",
          "  7.55620474E-02  7.17957645E-03 -6.02503247E-03  9.03284208E-03 -3.10249738E-02",
          " -5.12450149E-04  3.50280628E-03  7.55643750E-02  3.51789726E-03 -6.02518942E-03",
          " -6.02417692E-03  3.62331385E-02  6.60675935E-03 -4.07719225E-02 -4.07708165E-02",
          "  1.44603144E-01 -5.07019718E-03  9.17940725E-03  9.18246256E-03 -3.12325787E-02",
          "  1.00393859E-03  4.77039018E-03  4.76856342E-03 -3.31898386E-03  7.63738231E-02",
          " -5.88766275E-03 -3.17944405E-04 -6.26361412E-03  2.83396182E-02 -3.18071640E-03",
          " -3.78565914E-02 -3.40048459E-03 -2.83920351E-02 -4.23288555E-02  1.42663152E-01",
          " -5.88635984E-03 -6.26533369E-03 -3.25987053E-04  2.83457368E-02 -3.17436646E-03",
          " -3.40100972E-03 -3.78585761E-02 -2.83919305E-02 -4.23274108E-02 -3.27461865E-02",
          "  1.42661775E-01  2.12618147E-03 -3.53392980E-04 -3.51024158E-04  5.45172698E-02",
          "  2.37792321E-02 -6.28318797E-03 -6.28838368E-03  2.10278856E-02  5.10326813E-04",
          " -4.30852365E-03 -4.29403633E-03  1.72316804E-01 -2.64064056E-07 -7.19850721E-03",
          "  7.19901756E-03 -2.62564164E-06  1.91208932E-06 -2.23638854E-02  2.23642115E-02",
          " -3.23068814E-06 -2.55120719E-07 -1.87404587E-02  1.87430558E-02 -2.34839767E-06",
          "  2.57500236E-02  7.59781830E-03 -1.57261390E-04 -6.96535945E-03 -4.12347221E-04",
          "  1.67083950E-03  2.36818040E-02  2.73101184E-04  2.29054272E-02 -1.87178773E-02",
          " -5.54264765E-03 -1.97515768E-02  2.80888484E-03 -1.10057269E-02  2.82103520E-02",
          " -7.60122832E-03  6.96755519E-03  1.58797378E-04  4.06144568E-04 -1.66873192E-03",
          " -2.71008719E-04 -2.36830894E-02 -2.29151302E-02  1.87196312E-02  1.97548270E-02",
          "  5.54644198E-03 -2.81529686E-03 -1.10041955E-02 -1.46179929E-02  2.82178084E-02"]

ehRaw = [3.62723627E-01,  2.46348927E-03,  3.41917429E-01,  2.46449426E-03,  3.25566476E-03,
         3.41950225E-01,  7.71914399E-03,  1.30144832E-02,  1.30190899E-02,  3.24845899E-01,
         -2.18477593E-03,  2.12696837E-04,  2.11083552E-04, -
         7.61933194E-03,  5.14858537E-01,
         7.17776914E-03,  9.03061862E-03, -6.02514232E-03, -3.10222678E-02, -5.11022394E-04,
         7.55620474E-02,  7.17957645E-03, -6.02503247E-03,  9.03284208E-03, -3.10249738E-02,
         -5.12450149E-04,  3.50280628E-03,  7.55643750E-02,  3.51789726E-03, -6.02518942E-03,
         -6.02417692E-03,  3.62331385E-02,  6.60675935E-03, -
         4.07719225E-02, -4.07708165E-02,
         1.44603144E-01, -5.07019718E-03,  9.17940725E-03,  9.18246256E-03, -3.12325787E-02,
         1.00393859E-03,  4.77039018E-03,  4.76856342E-03, -3.31898386E-03,  7.63738231E-02,
         -5.88766275E-03, -3.17944405E-04, -
         6.26361412E-03,  2.83396182E-02, -3.18071640E-03,
         -3.78565914E-02, -3.40048459E-03, -
         2.83920351E-02, -4.23288555E-02,  1.42663152E-01,
         -5.88635984E-03, -6.26533369E-03, -
         3.25987053E-04,  2.83457368E-02, -3.17436646E-03,
         -3.40100972E-03, -3.78585761E-02, -
         2.83919305E-02, -4.23274108E-02, -3.27461865E-02,
         1.42661775E-01,  2.12618147E-03, -3.53392980E-04, -3.51024158E-04,  5.45172698E-02,
         2.37792321E-02, -6.28318797E-03, -6.28838368E-03,  2.10278856E-02,  5.10326813E-04,
         -4.30852365E-03, -4.29403633E-03,  1.72316804E-01, -
         2.64064056E-07, -7.19850721E-03,
         7.19901756E-03, -2.62564164E-06,  1.91208932E-06, -2.23638854E-02,  2.23642115E-02,
         -3.23068814E-06, -2.55120719E-07, -
         1.87404587E-02,  1.87430558E-02, -2.34839767E-06,
         2.57500236E-02,  7.59781830E-03, -1.57261390E-04, -6.96535945E-03, -4.12347221E-04,
         1.67083950E-03,  2.36818040E-02,  2.73101184E-04,  2.29054272E-02, -1.87178773E-02,
         -5.54264765E-03, -1.97515768E-02,  2.80888484E-03, -
         1.10057269E-02,  2.82103520E-02,
         -7.60122832E-03,  6.96755519E-03,  1.58797378E-04,  4.06144568E-04, -1.66873192E-03,
         -2.71008719E-04, -2.36830894E-02, -
         2.29151302E-02,  1.87196312E-02,  1.97548270E-02,
         5.54644198E-03, -2.81529686E-03, -1.10041955E-02, -1.46179929E-02,  2.82178084E-02]

cartesianLines = ["6",
                  "Title Card Required",
                  "C          0.68485       -0.02290       -0.00000",
                  "H          1.08036        0.99483        0.00066",
                  "H          1.03884       -0.54798        0.89820",
                  "H          1.03895       -0.54688       -0.89880",
                  "O         -0.75654        0.12140       -0.00000",
                  "H         -1.21495       -0.73375       -0.00001"]


def test_creation():
    extractor = Extractor(testPath, frankenLines)
    assert extractor.lines == frankenLines


def test_creationEmptyList():
    extractor = Extractor(testPath, [])
    assert extractor.path == testPath
    assert extractor.name == testPath.stem


def test_extract():
    extractor = Extractor(testPath, frankenLines)
    # Geometry
    extractor.extract()
    assert extractor.hRaw == ehRaw


def test_extractedGeometry():
    extractor = Extractor(testPath, frankenLines)
    # Geometry
    extractor.extract()
    geo = extractor.getGeometry()
    egeo = Geometry(testPath.stem, 6)
    egeo.energy = energy
    egeo.buildRIC(dims, dimIndicesGoodInput, coordLinesGoodInput)
    egeo.buildCartesian(cartesianLines)
    assert geo == egeo


def test_buildHessian():
    extractor = Extractor(testPath, frankenLines)
    # Geometry
    extractor.extract()
    geo = extractor.getGeometry()
    egeo = Geometry(testPath.stem, 6)
    egeo.energy = energy
    egeo.buildRIC(dims, dimIndicesGoodInput, coordLinesGoodInput)
    egeo.buildCartesian(cartesianLines)
    hess = extractor.hessian
    ltMat = LTMatrix(ehRaw)
    ehess = ltMat.fullmat
    assert (ehess == hess).all()



def test_getGeometry():
    pass


def test_getHessian():
    pass


# endregion

# region Unit Converter Tests

# endregion