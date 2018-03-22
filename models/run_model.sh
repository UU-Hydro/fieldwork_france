
# making/cleaning output directory
rm output/*
mkdir output

# run the model
python hydrology_and_erosion_model.py

# visualize the maps (output and input)
aguila output/*.map input_maps/*.map
