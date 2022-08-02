from numpy import float32
import pytest
from src.SITH.Utilities import *
from src.SITH.SITH import SITH
import pathlib

""" LTMatrix has already been tested by its creator on github,
 but should add in their testing just in case """

# region Expected Variables

dims = array('i', [15, 5, 7, 3])
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
coords = np.array([float(2.06335755E+00), 2.07679249, 2.07679461, 2.73743812, 1.83354933, 1.90516186E+00+np.pi,
                   1.90518195+np.pi,  1.84167462+np.pi,  1.91434964+np.pi,  1.94775283 +
                   np.pi, 1.94775582+np.pi,  1.96310537+np.pi, -3.14097002+np.pi,
                   -1.07379153+np.pi,  1.07501112E+00+np.pi], dtype=float32)
bonds = [float(2.06335755E+00), 2.07679249, 2.07679461, 2.73743812, 1.83354933]
angles = [1.90516186E+00+np.pi, 1.90518195+np.pi,  1.84167462+np.pi,
          1.91434964+np.pi,  1.94775283+np.pi, 1.94775582+np.pi,  1.96310537+np.pi]
diheds = [-3.14097002+np.pi, -1.07379153+np.pi,  1.07501112E+00+np.pi]

dimIndices = [(1, 2), (1, 3), (1, 4), (1, 5), (5, 6), (2, 1, 3), (2, 1, 4), (2, 1, 5),
              (3, 1, 4), (3, 1, 5), (4, 1, 5), (1, 5, 6), (2, 1, 5, 6), (3, 1, 5, 6), (4, 1, 5, 6)]

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

testPath = pathlib.Path(
    "/hits/fast/mbm/farrugma/sw/SITH/tests/test-methanol.fchk")

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

eHessFull = [[3.62723627e-01,  2.46348927e-03,  2.46449426e-03,  7.71914399e-03,
              -2.18477593e-03,  7.17776914e-03,  7.17957645e-03,  3.51789726e-03,
              -5.07019718e-03, -5.88766275e-03, -5.88635984e-03,  2.12618147e-03,
              -2.64064056e-07,  7.59781830e-03, -7.60122832e-03],
             [2.46348927e-03,  3.41917429e-01,  3.25566476e-03,  1.30144832e-02,
              2.12696837e-04,  9.03061862e-03, -6.02503247e-03, -6.02518942e-03,
              9.17940725e-03, -3.17944405e-04, -6.26533369e-03, -3.53392980e-04,
              -7.19850721e-03, -1.57261390e-04,  6.96755519e-03],
             [2.46449426e-03,  3.25566476e-03,  3.41950225e-01,  1.30190899e-02,
              2.11083552e-04, -6.02514232e-03,  9.03284208e-03, -6.02417692e-03,
              9.18246256e-03, -6.26361412e-03, -3.25987053e-04, -3.51024158e-04,
              7.19901756e-03, -6.96535945e-03,  1.58797378e-04],
             [7.71914399e-03,  1.30144832e-02,  1.30190899e-02,  3.24845899e-01,
              -7.61933194e-03, -3.10222678e-02, -3.10249738e-02,  3.62331385e-02,
              -3.12325787e-02,  2.83396182e-02,  2.83457368e-02,  5.45172698e-02,
              -2.62564164e-06, -4.12347221e-04,  4.06144568e-04],
             [-2.18477593e-03,  2.12696837e-04,  2.11083552e-04, -7.61933194e-03,
              5.14858537e-01, -5.11022394e-04, -5.12450149e-04,  6.60675935e-03,
              1.00393859e-03, -3.18071640e-03, -3.17436646e-03,  2.37792321e-02,
              1.91208932e-06,  1.67083950e-03, -1.66873192e-03],
             [7.17776914e-03,  9.03061862e-03, -6.02514232e-03, -3.10222678e-02,
              -5.11022394e-04,  7.55620474e-02,  3.50280628e-03, -4.07719225e-02,
              4.77039018e-03, -3.78565914e-02, -3.40100972e-03, -6.28318797e-03,
              -2.23638854e-02,  2.36818040e-02, -2.71008719e-04],
             [7.17957645e-03, -6.02503247e-03,  9.03284208e-03, -3.10249738e-02,
              -5.12450149e-04,  3.50280628e-03,  7.55643750e-02, -4.07708165e-02,
              4.76856342e-03, -3.40048459e-03, -3.78585761e-02, -6.28838368e-03,
              2.23642115e-02,  2.73101184e-04, -2.36830894e-02],
             [3.51789726e-03, -6.02518942e-03, -6.02417692e-03,  3.62331385e-02,
              6.60675935e-03, -4.07719225e-02, -4.07708165e-02,  1.44603144e-01,
              -3.31898386e-03, -2.83920351e-02, -2.83919305e-02,  2.10278856e-02,
              -3.23068814e-06,  2.29054272e-02, -2.29151302e-02],
             [-5.07019718e-03,  9.17940725e-03,  9.18246256e-03, -3.12325787e-02,
              1.00393859e-03,  4.77039018e-03,  4.76856342e-03, -3.31898386e-03,
              7.63738231e-02, -4.23288555e-02, -4.23274108e-02,  5.10326813e-04,
              -2.55120719e-07, -1.87178773e-02,  1.87196312e-02],
             [-5.88766275e-03, -3.17944405e-04, -6.26361412e-03,  2.83396182e-02,
              -3.18071640e-03, -3.78565914e-02, -3.40048459e-03, -2.83920351e-02,
              -4.23288555e-02,  1.42663152e-01, -3.27461865e-02, -4.30852365e-03,
              -1.87404587e-02, -5.54264765e-03,  1.97548270e-02],
             [-5.88635984e-03, -6.26533369e-03, -3.25987053e-04,  2.83457368e-02,
              -3.17436646e-03, -3.40100972e-03, -3.78585761e-02, -2.83919305e-02,
              -4.23274108e-02, -3.27461865e-02,  1.42661775e-01, -4.29403633e-03,
              1.87430558e-02, -1.97515768e-02,  5.54644198e-03],
             [2.12618147e-03, -3.53392980e-04, -3.51024158e-04,  5.45172698e-02,
              2.37792321e-02, -6.28318797e-03, -6.28838368e-03,  2.10278856e-02,
              5.10326813e-04, -4.30852365e-03, -4.29403633e-03,  1.72316804e-01,
              -2.34839767e-06,  2.80888484e-03, -2.81529686e-03],
             [-2.64064056e-07, -7.19850721e-03,  7.19901756e-03, -2.62564164e-06,
              1.91208932e-06, -2.23638854e-02,  2.23642115e-02, -3.23068814e-06,
              -2.55120719e-07, -1.87404587e-02,  1.87430558e-02, -2.34839767e-06,
              2.57500236e-02, -1.10057269e-02, -1.10041955e-02],
             [7.59781830e-03, -1.57261390e-04, -6.96535945e-03, -4.12347221e-04,
              1.67083950e-03,  2.36818040e-02,  2.73101184e-04,  2.29054272e-02,
              -1.87178773e-02, -5.54264765e-03, -1.97515768e-02,  2.80888484e-03,
              -1.10057269e-02,  2.82103520e-02, -1.46179929e-02],
             [-7.60122832e-03,  6.96755519e-03,  1.58797378e-04,  4.06144568e-04,
              -1.66873192e-03, -2.71008719e-04, -2.36830894e-02, -2.29151302e-02,
              1.87196312e-02,  1.97548270e-02,  5.54644198e-03, -2.81529686e-03,
              -1.10041955e-02, -1.46179929e-02,  2.82178084e-02]]

eHessKill0 = [[3.41917429e-01,  3.25566476e-03,  1.30144832e-02,
               2.12696837e-04,  9.03061862e-03, -6.02503247e-03, -6.02518942e-03,
               9.17940725e-03, -3.17944405e-04, -6.26533369e-03, -3.53392980e-04,
               -7.19850721e-03, -1.57261390e-04,  6.96755519e-03],
              [3.25566476e-03,  3.41950225e-01,  1.30190899e-02,
               2.11083552e-04, -6.02514232e-03,  9.03284208e-03, -6.02417692e-03,
               9.18246256e-03, -6.26361412e-03, -3.25987053e-04, -3.51024158e-04,
               7.19901756e-03, -6.96535945e-03,  1.58797378e-04],
              [1.30144832e-02,  1.30190899e-02,  3.24845899e-01,
               -7.61933194e-03, -3.10222678e-02, -3.10249738e-02,  3.62331385e-02,
               -3.12325787e-02,  2.83396182e-02,  2.83457368e-02,  5.45172698e-02,
               -2.62564164e-06, -4.12347221e-04,  4.06144568e-04],
              [2.12696837e-04,  2.11083552e-04, -7.61933194e-03,
               5.14858537e-01, -5.11022394e-04, -5.12450149e-04,  6.60675935e-03,
               1.00393859e-03, -3.18071640e-03, -3.17436646e-03,  2.37792321e-02,
               1.91208932e-06,  1.67083950e-03, -1.66873192e-03],
              [9.03061862e-03, -6.02514232e-03, -3.10222678e-02,
               -5.11022394e-04,  7.55620474e-02,  3.50280628e-03, -4.07719225e-02,
               4.77039018e-03, -3.78565914e-02, -3.40100972e-03, -6.28318797e-03,
               -2.23638854e-02,  2.36818040e-02, -2.71008719e-04],
              [-6.02503247e-03,  9.03284208e-03, -3.10249738e-02,
               -5.12450149e-04,  3.50280628e-03,  7.55643750e-02, -4.07708165e-02,
               4.76856342e-03, -3.40048459e-03, -3.78585761e-02, -6.28838368e-03,
               2.23642115e-02,  2.73101184e-04, -2.36830894e-02],
              [-6.02518942e-03, -6.02417692e-03,  3.62331385e-02,
               6.60675935e-03, -4.07719225e-02, -4.07708165e-02,  1.44603144e-01,
               -3.31898386e-03, -2.83920351e-02, -2.83919305e-02,  2.10278856e-02,
               -3.23068814e-06,  2.29054272e-02, -2.29151302e-02],
              [9.17940725e-03,  9.18246256e-03, -3.12325787e-02,
               1.00393859e-03,  4.77039018e-03,  4.76856342e-03, -3.31898386e-03,
               7.63738231e-02, -4.23288555e-02, -4.23274108e-02,  5.10326813e-04,
               -2.55120719e-07, -1.87178773e-02,  1.87196312e-02],
              [-3.17944405e-04, -6.26361412e-03,  2.83396182e-02,
               -3.18071640e-03, -3.78565914e-02, -3.40048459e-03, -2.83920351e-02,
               -4.23288555e-02,  1.42663152e-01, -3.27461865e-02, -4.30852365e-03,
               -1.87404587e-02, -5.54264765e-03,  1.97548270e-02],
              [-6.26533369e-03, -3.25987053e-04,  2.83457368e-02,
               -3.17436646e-03, -3.40100972e-03, -3.78585761e-02, -2.83919305e-02,
               -4.23274108e-02, -3.27461865e-02,  1.42661775e-01, -4.29403633e-03,
               1.87430558e-02, -1.97515768e-02,  5.54644198e-03],
              [-3.53392980e-04, -3.51024158e-04,  5.45172698e-02,
               2.37792321e-02, -6.28318797e-03, -6.28838368e-03,  2.10278856e-02,
               5.10326813e-04, -4.30852365e-03, -4.29403633e-03,  1.72316804e-01,
               -2.34839767e-06,  2.80888484e-03, -2.81529686e-03],
              [-7.19850721e-03,  7.19901756e-03, -2.62564164e-06,
               1.91208932e-06, -2.23638854e-02,  2.23642115e-02, -3.23068814e-06,
               -2.55120719e-07, -1.87404587e-02,  1.87430558e-02, -2.34839767e-06,
               2.57500236e-02, -1.10057269e-02, -1.10041955e-02],
              [-1.57261390e-04, -6.96535945e-03, -4.12347221e-04,
               1.67083950e-03,  2.36818040e-02,  2.73101184e-04,  2.29054272e-02,
               -1.87178773e-02, -5.54264765e-03, -1.97515768e-02,  2.80888484e-03,
               -1.10057269e-02,  2.82103520e-02, -1.46179929e-02],
              [6.96755519e-03,  1.58797378e-04,  4.06144568e-04,
               -1.66873192e-03, -2.71008719e-04, -2.36830894e-02, -2.29151302e-02,
               1.87196312e-02,  1.97548270e-02,  5.54644198e-03, -2.81529686e-03,
               -1.10041955e-02, -1.46179929e-02,  2.82178084e-02]]


fullHessianMOH = [[3.60723640e-01, -1.02888793e-03, -1.02902258e-03,  4.74000287e-03,
                   4.07054526e-03,  1.45350294e-03,  1.45408162e-03,  7.57041583e-03,
                   1.49136899e-03, -8.17155032e-03, -8.17476603e-03,  4.09136324e-03,
                   -1.23676179e-06,  6.59554712e-03, -6.59403624e-03],
                  [-1.02888793e-03,  3.52895715e-01, -2.78829205e-04,  2.91357100e-03,
                   -1.32912524e-04,  3.14419986e-03,  3.14379478e-03, -5.77527106e-03,
                   -2.07497635e-03, -4.25087022e-03, -4.24866991e-03, -8.08115781e-03,
                   -8.64421305e-08, -6.03586708e-03,  6.03508597e-03],
                  [-1.02902258e-03, -2.78829205e-04,  3.52895046e-01,  2.91213499e-03,
                   -1.33245720e-04,  3.14424748e-03,  3.14384237e-03, -5.77634582e-03,
                   -2.07490266e-03, -4.25094875e-03, -4.24874804e-03, -8.08204252e-03,
                   -8.64539715e-08, -6.03621487e-03,  6.03543366e-03],
                  [4.74000287e-03,  2.91357100e-03,  2.91213499e-03,  3.76838853e-01,
                   -7.07512816e-03, -2.93744769e-02, -2.93740926e-02,  4.50061464e-02,
                   -2.07566738e-02,  3.32373123e-02,  3.32354313e-02,  6.09388500e-02,
                   -6.05946051e-07, -1.91285355e-03,  1.91237509e-03],
                  [4.07054526e-03, -1.32912524e-04, -1.33245720e-04, -7.07512816e-03,
                   4.99846479e-01, -1.00219502e-02, -1.00207327e-02,  1.16308677e-02,
                   1.03250437e-02,  8.64729051e-03,  8.64545089e-03,  1.74597184e-02,
                   -1.11719327e-06,  1.86141281e-02, -1.86123829e-02],
                  [1.45350294e-03,  3.14419986e-03,  3.14424748e-03, -2.93744769e-02,
                   -1.00219502e-02,  1.51413467e-01, -8.58643141e-03, -2.17187634e-02,
                   1.19659396e-02,  5.30978585e-03,  5.32252338e-03, -1.00017758e-02,
                   -2.11438487e-06,  6.01226002e-03, -6.01374076e-03],
                  [1.45408162e-03,  3.14379478e-03,  3.14384237e-03, -2.93740926e-02,
                   -1.00207327e-02, -8.58643141e-03,  1.51413670e-01, -2.17170259e-02,
                   1.19666161e-02,  5.30871804e-03,  5.32145485e-03, -1.00008349e-02,
                   -2.11455538e-06,  6.01381337e-03, -6.01529385e-03],
                  [7.57041583e-03, -5.77527106e-03, -5.77634582e-03,  4.50061464e-02,
                   1.16308677e-02, -2.17187634e-02, -2.17170259e-02,  1.79424160e-01,
                   2.43654270e-02,  1.11564358e-02,  1.11657844e-02,  2.21879501e-02,
                   -5.17211890e-06,  2.76243227e-02, -2.76233711e-02],
                  [1.49136899e-03, -2.07497635e-03, -2.07490266e-03, -2.07566738e-02,
                   1.03250437e-02,  1.19659396e-02,  1.19666161e-02,  2.43654270e-02,
                   1.46337842e-01, -1.42346694e-02, -1.42552584e-02,  1.23896296e-02,
                   2.24394960e-06,  1.28347418e-03, -1.28050888e-03],
                  [-8.17155032e-03, -4.25087022e-03, -4.25094875e-03,  3.32373123e-02,
                   8.64729051e-03,  5.30978585e-03,  5.30871804e-03,  1.11564358e-02,
                   -1.42346694e-02,  1.62650532e-01,  2.64640060e-03,  3.96829059e-04,
                   2.66715035e-06, -1.92045473e-02,  1.92026795e-02],
                  [-8.17476603e-03, -4.24866991e-03, -4.24874804e-03,  3.32354313e-02,
                   8.64545089e-03,  5.32252338e-03,  5.32145485e-03,  1.11657844e-02,
                   -1.42552584e-02,  2.64640060e-03,  1.62642255e-01,  4.01072347e-04,
                   2.67112611e-06, -1.92189218e-02,  1.92170551e-02],
                  [4.09136324e-03, -8.08115781e-03, -8.08204252e-03,  6.09388500e-02,
                   1.74597184e-02, -1.00017758e-02, -1.00008349e-02,  2.21879501e-02,
                   1.23896296e-02,  3.96829059e-04,  4.01072347e-04,  1.73552374e-01,
                   -3.59322887e-06,  1.26332094e-02, -1.26327620e-02],
                  [-1.23676179e-06, -8.64421305e-08, -8.64539715e-08, -6.05946051e-07,
                   -1.11719327e-06, -2.11438487e-06, -2.11455538e-06, -5.17211890e-06,
                   2.24394960e-06,  2.66715035e-06,  2.67112611e-06, -3.59322887e-06,
                   3.68971879e-03, -1.33071253e-06,  1.32981275e-06],
                  [6.59554712e-03, -6.03586708e-03, -6.03621487e-03, -1.91285355e-03,
                   1.86141281e-02,  6.01226002e-03,  6.01381337e-03,  2.76243227e-02,
                   1.28347418e-03, -1.92045473e-02, -1.92189218e-02,  1.26332094e-02,
                   -1.33071253e-06,  1.87769810e-02, -1.50837670e-02],
                  [-6.59403624e-03,  6.03508597e-03,  6.03543366e-03,  1.91237509e-03,
                   -1.86123829e-02, -6.01374076e-03, -6.01529385e-03, -2.76233711e-02,
                   -1.28050888e-03,  1.92026795e-02,  1.92170551e-02, -1.26327620e-02,
                   1.32981275e-06, -1.50837670e-02,  1.87699912e-02]]

# endregion


def test_atomCreation():
    atom = Atom('C', [2.3, 4.6, 7.8])
    assert atom.element is 'C'

# region Geometry Tests


def test_geometryName():
    geo = Geometry('testName', 'blah', 3)
    assert geo.name == 'testName'


def test_geometryNAtoms():
    geo = Geometry('testName', 'blah', 3)
    assert geo.nAtoms == 3


def test_dumbGeoCreationErrors():
    geo = Geometry('blah', 'blah', 6)
    assert geo.energy == None


def test_getEnergyGood():
    geo = Geometry('blah', 'blah', 6)
    geo.energy = 42
    assert geo.energy == 42


def test_buildRICGood():
    geo = Geometry('methanol-test', 'blah', 6)
    geo.buildRIC(dims, dimIndicesGoodInput, coordLinesGoodInput)
    assert geo.dims == dims
    assert geo.dimIndices == dimIndices
    assert [geo.ric[i] == coords[i] for i in range(len(coords))]

# TODO


def test_killDOFs():
    sith = SITH('/hits/fast/mbm/farrugma/sw/SITH/tests/x0.fchk',
                '/hits/fast/mbm/farrugma/sw/SITH/tests/deformed')
    sith.extractData()
    assert (sith._reference.hessian == eHessFull).all()
    sith._reference._killDOFs([0])
    assert all(sith._reference.dimIndices == dimIndices[1:])
    assert sith._reference.dims == array('i', [14, 4, 7, 3])
    assert (sith._reference.hessian == eHessKill0).all()


# region bad coordinates

def test_moreCoords():
    coordsMore = coordLinesGoodInput + ['100.78943']
    geo = Geometry('methanol-test', 'blah', 6)
    with pytest.raises(Exception) as e:
        geo.buildRIC(dims, dimIndicesGoodInput, coordsMore)
    assert str(e.value) == "Mismatch between the number of degrees of freedom expected (" + \
        str(dims[0])+") and number of coordinates given ("+str(dims[0]+1)+")."


def test_lessCoords():
    coordsLess = coordLinesGoodInput[1:]
    geo = Geometry('methanol-test', 'blah', 6)
    with pytest.raises(Exception) as e:
        geo.buildRIC(dims, dimIndicesGoodInput, coordsLess)
    assert str(e.value) == "Mismatch between the number of degrees of freedom expected (" + \
        str(dims[0])+") and number of coordinates given ("+str(dims[0]-5)+")."


# endregion

# region bad Indices


def test_riciBad():
    geo = Geometry('methanol-test', 'blah', 6)
    with pytest.raises(Exception) as e:
        geo.buildRIC(dims, dimIndices59, coordLinesGoodInput)
    assert str(
        e.value) == "One or more redundant internal coordinate indices are missing or do not have the expected format. Please refer to documentation"


def test_riciLetters():
    geo = Geometry('methanol-test', 'blah', 6)
    with pytest.raises(Exception) as e:
        geo.buildRIC(dims, dimIndicesLetters, coordLinesGoodInput)
    assert str(
        e.value) == "Invalid atom index given as input."


def test_riciNumIndices():
    geo = Geometry('methanol-test', 'blah', 6)
    with pytest.raises(Exception) as e:
        geo.buildRIC(dims, dimIndicesNumI, coordLinesGoodInput)
    assert str(
        e.value) == "Mismatch between given 'RIC dimensions' and given RIC indices."


def test_riciInvalid():
    dimIndicesInvalid = [
        '           1           7           0           0           1           3']+dimIndicesGoodInput[1:]
    geo = Geometry('methanol-test', 'blah', 6)
    with pytest.raises(Exception) as e:
        geo.buildRIC(dims, dimIndicesInvalid, coords)
    assert str(e.value) == "Invalid atom index given as input."


def test_buildRICBad():
    geo = Geometry('methanol-test', 'blah', 6)
    with pytest.raises(Exception) as e:
        geo.buildRIC(dims, dimIndicesGoodInput[2:], coordLinesGoodInput)
    assert str(
        e.value) == "One or more redundant internal coordinate indices are missing or do not have the expected format. Please refer to documentation"

# endregion

# region Cartesian

def test_buildCartesian():
    pass


def test_getAtoms():
    pass

# endregion

# region validity as reference or deformed (might move to extractor not Geometry? might not even need)


def test_validReference():
    pass


def test_invalidReference():
    pass


def test_validDeformed():
    pass


def test_invalidDeformed():
    pass

# endregion

# region Extractor Tests


# region Cartesian

#TODO also put in test_SithWriter
def test_writeXYZ():
    pass

# endregion


def test_creationEmptyList():
    extractor = Extractor(testPath, [])
    assert extractor._path == testPath
    assert extractor._name == testPath.stem


def test_extract():
    extractor = Extractor(testPath, frankenLines)
    # Geometry
    extractor._extract()
    assert extractor.hRaw == ehRaw


def test_extractedGeometry():
    extractor = Extractor(testPath, frankenLines)
    # Geometry
    extractor._extract()
    geo = extractor.getGeometry()
    egeo = Geometry(testPath.stem, 'blah', 6)
    egeo.energy = energy
    egeo.buildRIC(dims, dimIndicesGoodInput, coordLinesGoodInput)
    egeo.buildCartesian(cartesianLines)
    assert geo == egeo


def test_buildHessian():
    extractor = Extractor(testPath, frankenLines)
    # Geometry
    extractor._extract()
    geo = extractor.getGeometry()
    egeo = Geometry(testPath.stem, 'blah', 6)
    egeo.energy = energy
    egeo.buildRIC(dims, dimIndicesGoodInput, coordLinesGoodInput)
    egeo.buildCartesian(cartesianLines)
    hess = extractor.hessian

    assert (eHessFull == hess).all()


def test_getGeometry():
    pass


def test_getHessian():
    pass


# endregion

# region Unit Converter Tests

# endregion
