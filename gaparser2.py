import os
from bibliotheque_create import read_file, generation_code

# -------------------------------------------------------------------
# repertoire / initialisation
directoryExamples = '/examples'
directoryBibliotheque = 'Libraries/'
comserial = "/dev/ttyUSB0"  # le port serie
compilega144 = True  # permet de voir sous forme json le resultat de la compilation
programga144 = False  # programmation du ga144

# -------------------------------------------------------------------

# fichiers code source
#file_ga = "examples/ledpulse.ga"
#file_ga = "examples/fibonacci.ga"
file_ga = "examples/inputwakeup.ga"
file_ga_ = file_ga + '_'

# read code source
code = read_file(file_ga)
print(f"code: \n{code}")


# new code
generation_code(code, directoryBibliotheque, file_ga_)
newcode = read_file(file_ga_)
print(f" nouveau code: \n{newcode}")

# -------------------------------------------------------------------

# compilation / programmation
if compilega144:
    # "python ga.py examples/boutoninput_.ga --json"

    commandecompile = "python ga.py " + file_ga_
    os.system(commandecompile)
if programga144:
    commandprogram = "python ga.py " + file_ga_ + " --port " + comserial
    os.system(commandprogram)
# -------------------------------------------------------------------
