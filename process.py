import numpy as np
import pandas as pd
import re

def etl(chords): #Convert string to array
    chords_arr = []
    for i in range(len(chords)):# Remove numbers 
        x = re.sub(r'[0-9]+', '', chords[i])
        x = x[1:].replace(';.','')
        chords_arr.append(x)
    to_remove = [s for s in chords_arr if s.startswith('N')]
    for i in to_remove: # Remove 'N' beats
        chords_arr.remove(i)
    return chords_arr

def chord_array(ch_arr,grados,acordes):
    norm = []
    for i in ch_arr:
        acorde = i.split(':')[0]
        x = i.replace(acorde, grados[acordes.index(acorde)])
        norm.append(x)

    norm = np.array(norm)
    return norm

def data(norm):
    new_list = [[i, v] for i, v in enumerate(norm)]
    dicto2 = {'beat':[],'chord':[]}
    for i in new_list:
        dicto2['beat'].append(i[0])
        dicto2['chord'].append(i[1])
    data = pd.DataFrame(dicto2) 
    return data
