# AerE 461/462 Fuselage Optimization
# 12/05/2023
# Chris Psenica

# =============================================================================
# Imports
# =============================================================================
import os
import argparse
import numpy as np
from mpi4py import MPI
import openmdao.api as om
from mphys.multipoint import Multipoint
from dafoam.mphys import DAFoamBuilder, OptFuncs
from mphys.scenario_aerodynamic import ScenarioAerodynamic
from pygeo.mphys import OM_DVGEOCOMP
from pygeo import geo_utils

# =============================================================================
# Opt Settings
# =============================================================================
parser = argparse.ArgumentParser()
parser.add_argument("-optimizer", help="optimizer to use", type=str, default="SNOPT")   # which optimizer to use. Options are: IPOPT (default), SLSQP, and SNOPT
parser.add_argument("-task", help="type of run to do", type=str, default="opt")         # which task to run. Options are: opt (default), runPrimal, runAdjoint, checkTotals
args = parser.parse_args()

# =============================================================================
# Opt Parameters
# =============================================================================
U0 = 15.433
p0 = 101325.0
T0 = 300.0
rho0 = p0 / T0 / 287.0
nuTilda0 = 4.5e-5
k0 = 0.375
epsilon0 = 168.75
omega0 = 5000.0
CL_baseline = -0.001775
aoa0 = 5.0
A0 = 0.1

# =============================================================================
# DaOptions Setup
# =============================================================================
daOptions = {
    "designSurfaces": ["body"],
    "solverName": "DARhoSimpleFoam",
    "primalMinResTol": 1.0e-8,
    "primalBC": {
        "U0": {"variable": "U", "patches": ["inout"], "value": [0.0, 1.3450745778246085, -15.374272775649908]},
        "p0": {"variable": "p", "patches": ["inout"], "value": [p0]},
        "T0": {"variable": "T", "patches": ["inout"], "value": [T0]},
        "nuTilda0": {"variable": "nuTilda", "patches": ["inout"], "value": [nuTilda0]},
        "k0": {"variable": "k", "patches": ["inout"], "value": [k0]},
        "epsilon0": {"variable": "epsilon", "patches": ["inout"], "value": [epsilon0]},
        "omega0": {"variable": "omega", "patches": ["inout"], "value": [omega0]},
        "useWallFunction": True,
    },
    "objFunc": {
        "CD": {
            "part1": {
                "type": "force",
                "source": "patchToFace",
                "patches": ["body"],
                "directionMode": "fixedDirection",
                "direction": [0.0, 0.08715574274765817, -0.9961946980917455],
                "scale": 1.0 / (0.5 * U0 * U0 * A0 * rho0),
                "addToAdjoint": True,
            }
        },
        "CL": {
            "part1": {
                "type": "force",
                "source": "patchToFace",
                "patches": ["body"],
                "directionMode": "fixedDirection",
                "direction": [0.0, 0.9961946980917455, 0.08715574274765817],
                "scale": 1.0 / (0.5 * U0 * U0 * A0 * rho0),
                "addToAdjoint": True,
            }
        },
    },
    "adjEqnOption": {
        "gmresRelTol": 1.0e-6,
        "pcFillLevel": 1,
        "jacMatReOrdering": "rcm",
        "gmresMaxIters": 1000,
        "gmresRestart": 1000,
    },
    "normalizeStates": {
        "U": U0,
        "p": p0,
        "T": T0,
        "nuTilda": 1e-3,
        "k": 1.0,
        "omega": 100.0,
        "epsilon": 10.0,
        "phi": 1.0,
    },
    "designVar": {
        "ULS": {"designVarType": "FFD"},
        "ULE": {"designVarType": "FFD"},

        "BLS": {"designVarType": "FFD"},
        "BLE": {"designVarType": "FFD"},
    },
}

# =============================================================================
# Mesh Setup
# ============================================================================= 
meshOptions = {
    "gridFile": os.getcwd(),
    "fileType": "OpenFOAM",
    "symmetryPlanes": [[[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]],   # point and normal for the symmetry plane
}

# =============================================================================
# Top class to setup the optimization problem
# =============================================================================
class Top(Multipoint):
    def setup(self):

        # create the builder to initialize the DASolvers
        dafoam_builder = DAFoamBuilder(daOptions, meshOptions, scenario="aerodynamic")
        dafoam_builder.initialize(self.comm)

        # add the design variable component to keep the top level design variables
        self.add_subsystem("dvs", om.IndepVarComp(), promotes=["*"])

        # add the mesh component
        self.add_subsystem("mesh", dafoam_builder.get_mesh_coordinate_subsystem())

        # add the geometry component (FFD)
        self.add_subsystem("geometry", OM_DVGEOCOMP(file="FFD/BodyFFD.xyz", type="ffd"))

        # add a scenario (flow condition) for optimization, we pass the builder to the scenario to actually run the flow and adjoint
        self.mphys_add_scenario("cruise", ScenarioAerodynamic(aero_builder=dafoam_builder))

        # need to manually connect the x_aero0 between the mesh and geometry components here x_aero0 means the surface coordinates of structurally undeformed mesh
        self.connect("mesh.x_aero0", "geometry.x_aero_in")

        # need to manually connect the x_aero0 between the geometry component and the cruise scenario group
        self.connect("geometry.x_aero0", "cruise.x_aero")

    def configure(self):

        # add the objective function to the cruise scenario
        self.cruise.aero_post.mphys_add_funcs()

        # get the surface coordinates from the mesh component
        points = self.mesh.mphys_get_surface_mesh()

        # add pointset to the geometry component
        self.geometry.nom_add_discipline_coords("aero", points)

        # get index of points
        pts = self.geometry.DVGeo.getLocalIndex(0)
   
        # define design variables and assign them FFD points
        # ULS
        indexList = []
        indexList = pts[2 : 6 , 0 , 0].flatten()
        PS = geo_utils.PointSelect("list", indexList)
        ULSVAL = self.geometry.nom_addLocalDV(dvName="ULS", axis = "y" , pointSelect=PS)

        # ULE
        indexList = []
        indexList = pts[2 : 6 , 1 , 0].flatten()
        PS = geo_utils.PointSelect("list", indexList)
        ULEVAL = self.geometry.nom_addLocalDV(dvName="ULE", axis = "y" , pointSelect=PS)
     
        # BLS
        indexList = []
        indexList = pts[2 : 6 , 0 , 1].flatten()
        PS = geo_utils.PointSelect("list", indexList)
        BLSVAL = self.geometry.nom_addLocalDV(dvName="BLS", axis = "y" , pointSelect=PS)

        # BLE
        indexList = []
        indexList = pts[2 : 6 , 1 , 1].flatten()
        PS = geo_utils.PointSelect("list", indexList)
        BLEVAL = self.geometry.nom_addLocalDV(dvName="BLE", axis = "y" , pointSelect=PS)

        if args.task == "opt":
            # add the design variables to the dvs component's output
            self.dvs.add_output("ULS", val=np.array([0] * ULSVAL))
            self.dvs.add_output("ULE", val=np.array([0] * ULEVAL))

            self.dvs.add_output("BLS", val=np.array([0] * BLSVAL))
            self.dvs.add_output("BLE", val=np.array([0] * BLEVAL))

        elif args.task == "checkTotals":
            # add the design variables to the dvs component's output
            self.dvs.add_output("ULS", val=np.array([0]))
            self.dvs.add_output("ULE", val=np.array([0]))

            self.dvs.add_output("BLS", val=np.array([0]))
            self.dvs.add_output("BLE", val=np.array([0])) 

        # manually connect the dvs output to the geometry and cruise
        self.connect("ULS", "geometry.ULS")
        self.connect("ULE", "geometry.ULE")

        self.connect("BLS", "geometry.BLS")
        self.connect("BLE", "geometry.BLE")

        # define the design variables
        self.add_design_var("ULS", lower = -0.01 , upper = 0.01 , scaler = 100.0)
        self.add_design_var("ULE", lower = -0.001 , upper = 0.001 , scaler = 1000.0)

        self.add_design_var("BLS", lower = -0.01 , upper = 0.01 , scaler = 100.0)
        self.add_design_var("BLE", lower = -0.001 , upper = 0.001 , scaler = 1000.0)

        # add objective and constraints to the top level
        self.add_objective("cruise.aero_post.CD", scaler = 1.0)
        self.add_constraint("cruise.aero_post.CL", lower = CL_baseline , scaler = 1.0)

# =============================================================================
# OpenMDAO setup
# =============================================================================
prob = om.Problem()
prob.model = Top()
prob.setup(mode="rev")
om.n2(prob, show_browser=False, outfile="mphys.html")

# initialize the optimization function
optFuncs = OptFuncs(daOptions, prob)

# use pyoptsparse to setup optimization
prob.driver = om.pyOptSparseDriver()
prob.driver.options["optimizer"] = args.optimizer
# options for optimizers
if args.optimizer == "SNOPT":

    prob.driver.opt_settings = {
        "Major feasibility tolerance": 1.0e-5,
        "Major optimality tolerance": 1.0e-7,
        "Minor feasibility tolerance": 1.0e-5,
        "Verify level": -1,
        "Function precision": 1.0e-5,
        "Major iterations limit": 1000,
        "Nonderivative linesearch": None,
        "Print file": "opt_SNOPT_print.txt",
        "Summary file": "opt_SNOPT_summary.txt",
    }

elif args.optimizer == "IPOPT":

    prob.driver.opt_settings = {
        "tol": 1.0e-5,
        "constr_viol_tol": 1.0e-5,
        "max_iter": 100,
        "print_level": 5,
        "output_file": "opt_IPOPT.txt",
        "mu_strategy": "adaptive",
        "limited_memory_max_history": 10,
        "nlp_scaling_method": "none",
        "alpha_for_y": "full",
        "recalc_y": "yes",
    }

elif args.optimizer == "SLSQP":

    prob.driver.opt_settings = {
        "ACC": 1.0e-5,
        "MAXIT": 100,
        "IFILE": "opt_SLSQP.txt",
    }

else:

    print("optimizer arg not valid!")
    exit(1)

prob.driver.options["debug_print"] = ["nl_cons", "objs", "desvars"]
prob.driver.options["print_opt_prob"] = True
prob.driver.hist_file = "OptView.hst"


if args.task == "opt":

    # run the optimization
    prob.run_driver()

elif args.task == "runPrimal":

    # just run the primal once
    prob.run_model()

elif args.task == "runAdjoint":

    # just run the primal and adjoint once
    prob.run_model()
    totals = prob.compute_totals()

    if MPI.COMM_WORLD.rank == 0:

        print(totals)

elif args.task == "checkTotals":

    # verify the total derivatives against the finite-difference
    prob.run_model()
    prob.check_totals(
        of = ["cruise.aero_post.CD" , "cruise.aero_post.CL"], wrt = ["ULS" , "ULE" , "BLS" , "BLE"], compact_print = False , step = 1e-6 , form="central" , step_calc = "abs"
    )

else:

    print("task arg not found!")
    exit(1)