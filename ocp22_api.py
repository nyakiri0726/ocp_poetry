# Standard Library
import json

# Third Party Library
import numpy as np
from ase import Atoms
from fastapi import FastAPI
from ocpmodels.common.relaxation.ase_utils import OCPCalculator
from pydantic import BaseModel


class Mol(BaseModel):
    atoms: list
    xyz: list
    
app = FastAPI() 

path_config="/workspaces/ocp22/ocp/configs/oc22/s2ef/gemnet-oc/gemnet_oc_finetune.yml"
path_chpt="/workspaces/ocp22/gnoc_finetune_all_s2ef.pt"


# Define the calculator
calc = OCPCalculator(config_yml=None, checkpoint=path_chpt)

def set_mol(atoms: list, xyz: list) -> Atoms:
    mol=Atoms(symbols=atoms,positions=xyz)
    mol.set_tags(2)
    
    return mol

@app.post("/ocp22/")
async def ocp_calc(input: Mol):
    mol=set_mol(input.atoms,input.xyz)
    mol.calc=calc
    energy=mol.get_potential_energy()
    force=mol.get_forces()
    resp = {"energy": energy, "force": json.dumps(force.tolist())}
    return resp

@app.get("/")
async def hello_world():

    return {"message": "Hello World"}