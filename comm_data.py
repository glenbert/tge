import pandas as pd
import numpy as np

u1 = {
    "Plant":["Sibulan A","Sibulan A","Sibulan A","Sibulan A","Sibulan A","Sibulan B","Sibulan B","Sibulan B","Sibulan B","Sibulan B"],
    "Unit Flow":[0.54, 1.04, 1.49, 2.01, 2.56, 0.95, 1.83, 2.7, 3.57, 4.48],
    "Net Head":[381.11, 380.36, 379.72, 379.33, 378.15, 343.21, 342.09, 338.8, 340.31, 339.6],
    "Turbine Guaranted Eff.":[0.872, 0.900, 0.902, 0.905, 0.902, 0.86, 0.896, 0.899, 0.901, 0.901],
    "Generator Guaranted Eff.":[0.930, 0.957, 0.97, 0.975, 0.975, 0.934, 0.958, 0.972, 0.9760, 0.978],
    "Overall Eff.":[0.811, 0.8613, 0.8749, 0.8824, 0.8795, 0.8032, 0.8584, 0.8738, 0.8794, 0.8812],
    "Power Output":[1720.0, 3440.0, 5160.0, 6880.0, 8540.0, 2650.0, 5300.0, 7950.0, 10600.0, 13300.0]
    }

u2 = {
    "Plant":["Sibulan A","Sibulan A","Sibulan A","Sibulan A","Sibulan A","Sibulan B","Sibulan B","Sibulan B","Sibulan B","Sibulan B"],
    "Unit Flow":[0.54, 1.03, 1.76, 2.01, 2.58, 0.95, 1.81, 2.65, 3.56, 4.51],
    "Net Head":[383.15, 382.40, 381.05, 380.36, 380.23, 341.07, 341.88, 341.63, 338.98, 338.61],
    "Turbine Guaranted Eff.":[0.872, 0.900, 0.902, 0.905, 0.902, 0.86, 0.896, 0.896, 0.901, 0.901],
    "Generator Guaranted Eff.":[0.930, 0.957, 0.973, 0.975, 0.975, 0.934, 0.958, 0.972, 0.976, 0.978],
    "Overall Eff.":[0.811, 0.8613, 0.8806, 0.8824, 0.8795, 0.8032, 0.8584, 0.8709, 0.8794, 0.8812],
    "Power Output":[1720.0, 3440.0, 6020.0, 6880.0, 8550.0, 2650.0, 5300.0, 7950.0, 10600.0, 13300.0]
    }


df_comm_unit_1 = pd.DataFrame(u1)
df_comm_unit_2 = pd.DataFrame(u2)