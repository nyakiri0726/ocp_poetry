# Standard Library
import os
import time

# Third Party Library
import ase.io
import numpy as np
import yaml
from ase.build import add_adsorbate, fcc100, molecule
from ase.constraints import FixAtoms
from ase.optimize import BFGS
from ocpmodels.common.relaxation.ase_utils import OCPCalculator

path_config="/workspaces/ocp22/ocp/configs/oc22/s2ef/gemnet-oc/gemnet_oc_finetune.yml"
path_chpt="/workspaces/ocp22/gnoc_finetune_all_s2ef.pt"

with open(path_config, 'r') as yml:
    config = yaml.safe_load(yml)
# print("---------config---------")
# print(config)
# print("---------config[model]---------")
# print(config["model"])
# print("---------config[optim][lr_ini]---------")
# print(config["optim"]["lr_initial"])

# Define the calculator
calc = OCPCalculator(config_yml=None, checkpoint=path_chpt)

# Construct a sample structure
adslab = fcc100("Cu", size=(3, 3, 3))
adsorbate = molecule("CH2OCH2")
add_adsorbate(adslab, adsorbate, 3, offset=(1, 1))
tags = np.zeros(len(adslab))
tags[18:27] = 1
tags[27:] = 2
adslab.set_tags(tags)
cons= FixAtoms(indices=[atom.index for atom in adslab if (atom.tag == 0)])
adslab.set_constraint(cons)
adslab.center(vacuum=13.0, axis=2)
adslab.set_pbc(True)
print(adslab.get_positions())
print(adslab.get_atomic_numbers())


# # Set up the calculator
adslab.calc = calc

# os.makedirs("data/sample_ml_relax", exist_ok=True)
# opt = BFGS(adslab, trajectory="data/sample_ml_relax/toy_c3h8_relax.traj")

# test=opt.run(fmax=0.05, steps=100)
# print(test)
# Standard Library
# import pdb

# pdb.set_trace()
# adslab.calc.get_forces()
# adslab.calc.get_potential_energy()

# Third Party Library
from ase import Atoms
from ase.io import read, write

# read from file
amino=read("test.xyz")
print(amino)
print(type(amino))
pos=amino.get_positions()
amino.calc = calc
print(amino.get_atomic_numbers())
print(type(pos))
print(pos.shape)
xyz=np.random.rand(18,3)

print(xyz)
tags = np.zeros(len(amino))
tags[:] = 2
amino.set_tags(tags)
# cons= FixAtoms(indices=[atom.index for atom in amino if (atom.tag == 0)])
# amino.set_constraint(cons)
# tags[27:] = 2
# na2_atoms.calc=calc
energy=amino.get_forces()
os.makedirs("data/sample_ml_relax", exist_ok=True)
# opt = BFGS(amino, trajectory="data/sample_ml_relax/toy_c3h8_relax.traj")

# opt.run(fmax=0.05, steps=100)
for _ in range(3):
    # pos=amino.get_positions()
    # amino.calc
    energy=amino.get_potential_energy()
    # print(force)
    print(energy)
    xyz=np.random.rand(18,3)
    # print(pos+xyz)
    amino.set_positions(pos+xyz)
    # amino.calc = calc
    # print(amino.get_positions())
    # print(amino)
# Third Party Library
from ase.visualize import view

view(amino)
