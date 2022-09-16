import numpy as np
import pandas as pd


def get_key(tonalidad, modo='jonico'):
    #grados  = ['Ib','I','I#','IIb','II','II#','IIIb','III','III#','IVb','IV','IV#','Vb','V','V#','VIb','VI','VI#','VIIb','VII','VII#']
    grados  = ['Ib','I','I','IIb','II','II#','IIIb','III','III','IVb','IV','IV#','Vb','V','V#','VIb','VI','VI','VIIb','VIIb','VII']
    acordes = ['Cb','C','C#','Db' ,'D' ,'D#' ,'Eb'  ,'E'  ,'E#'  ,'Fb' ,'F' ,'F#' ,'Gb','G','G#','Ab' ,'A' ,'A#' ,'Bb'  ,'B'  ,'B#']
    trans = acordes.index(tonalidad)
    if modo == 'jonico':
        transportado = list(np.roll(acordes,-trans))
        grados = list(np.roll(grados,-1))
    elif modo =='eolico':
        transportado = list(np.roll(acordes,-trans-5))
        grados = list(np.roll(grados,-1))

    return [transportado, grados]
    #return [transportado, grados]

def detect_tone(df):

    major = df[(df['chord'] == 'I:maj')].count()['chord']
    minor = df[(df['chord'] == 'I:min')].count()['chord']

    if major > minor:
        return "mayor"
    else:
        return "minor"

def get_linked(arr):
    enlaces = []
    c = 0
    while c < len(arr)-1:
        if arr[c] != arr[c+1]:
            enlaces.append(arr[c] +'/'+ arr[c+1])
            c += 1
        else:
            c += 1

    enlaces_num = [[i, v] for i, v in enumerate(enlaces)]
    enlaces_dict = {'beat':[],'chord':[]}
    for i in enlaces_num:
        print(i)
        enlaces_dict['beat'].append(i[0])
        enlaces_dict['chord'].append(i[1])

    enlaces_df = pd.DataFrame(enlaces_dict);
    
    return enlaces_df

def get_modals(enlaces_df,mode):
    sus = ['II:sus', 'V:sus', 'VIIb:sus']
    if mode == 'mayor':
        mode = ['I:maj','II:min','III:min','IV:maj','V:maj','VI:min','VII:min']
    elif mode == 'minor':
        mode = ['I:min','II:min','IIIb:maj','IV:min','V:min','VIb:maj','VIIb:maj']
    
    modals = []
    modes = []
    for enlace in enlaces_df['chord']:
        for acorde in enlace.split('/'):
            if acorde not in mode and acorde not in sus:
                modals.append(enlace)
                modes.append(acorde)
            else:
                pass

    return [set(modals), set(modes)]


def modal_exchange(modes):

    modes_list = {
            'jonic'      : ['I:maj','II:min' ,'III:min' ,'IV:maj' ,'V:maj' ,'VI:min' ,'VII:min' ],
            'doric'      : ['I:min','II:min' ,'IIIb:maj','IV:maj' ,'V:min' ,'VIb:maj','VIIb:maj'],
            'frigian'    : ['I:min','IIb:maj','IIIb:maj','IV:min' ,'V:min' ,'VIb:min','VIIb:min'],
            'lidian'     : ['I:maj','II:maj' ,'III:min' ,'IV#:min','V:maj' ,'VI:min' ,'VII:min' ],
            'mixolidian' : ['I:maj','II:min' ,'III:min' ,'IV:maj' ,'V:min' ,'VI:min' ,'VIIb:maj'],
            'eolic'      : ['I:min','II:min' ,'IIIb:maj','IV:min' ,'V:min' ,'VIb:maj','VIIb:maj'],
            'locrian'    : ['I:min','IIb:maj','IIIb:min','IV:min' ,'Vb:maj','VIb:maj','VIIb:min']
        }

    dominants = {'III:maj': 'V7/VI'}

    resources = {'mode': []}

    c = 0
    for mode in modes:
        resources['mode'].append({mode:[]})
        for mode_ in modes_list:
            if mode in modes_list[mode_]:
                resources['mode'][c][mode].append(mode_)
   
        for mode_ in dominants:
            if mode in dominants:
                resources['mode'][c][mode].append(dominants[mode])

        c += 1

    return resources

