
# making/cleaning output directory
rm outputs/*
mkdir outputs

# run the model
python hydrology_and_erosion_model.py

# visualize the maps (output and input)
aguila outputs/*.map inputs/*.map

#~ # visualize the maps (output only)
#~ aguila outputs/*.map

