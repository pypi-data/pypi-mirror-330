import numpy as np
from qupled.classic import Stls
from qupled.util import Hdf

# Define the object used to solve the scheme
stls = Stls()

# Define the input parameters
inputs = Stls.Input(10.0, 1.0)
inputs.mixing = 0.5

# Solve scheme
stls.compute(inputs)

# Plot some results
stls.plot(["ssf", "slfc", "rdf"])

# Plot the ideal density response for a few matsubara frequencies
stls.plot(["idr"], matsubara=np.arange(1, 10, 2))

# Access the static structure factor from the output file
ssf = Hdf().read(stls.hdfFileName, ["ssf"])["ssf"]
print("Static structure factor from the output file: ")
print(ssf)

# Compute the internal energy
print("Internal energy: ")
print(stls.computeInternalEnergy())
