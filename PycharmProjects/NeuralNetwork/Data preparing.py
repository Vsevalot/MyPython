channels=['IED_AF3','IED_F7','IED_F3','IED_FC5','IED_T7','IED_P7','IED_O1','IED_O2','IED_P8','IED_T8','IED_FC6','IED_F4','IED_F8','IED_AF4']
for element in range(len(channels)):
    channels[element]=channels[element][4:]
print(channels)