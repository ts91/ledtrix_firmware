from itertools import product

# Translates the control designators into actual bit positions in the chain of shift registers
t_ctrl2bit = {
    'L5': 0,
    'L2': 1,
    'L3': 2,
    'L4': 3,
    'L6': 4,
    'L1': 5,
    'L7': 6,
    'L8': 7,
    'H16': 8,
    'H11': 9,
    'H14': 10,
    'H9': 11,
    'H10': 12,
    'H12': 13,
    'H15': 14,
    'H13': 15,
    'L13': 16,
    'L10': 17,
    'L11': 18,
    'L16': 19,
    'L15': 20,
    'L9': 21,
    'L14': 22,
    'L12': 23,
    'H6': 24,
    'H1': 25,
    'H3': 26,
    'H2': 27,
    'H4': 28,
    'H8': 29,
    'H5': 30,
    'H7': 31
}

# A matrix is made out of four 8x8 modules. These maps translate columns and rows into a control designator
map_u203 = {
    'c4' : 'H12', # pin 1
    'c2' : 'H10', # pin 2
    'r2' : 'L2',  # pin 3
    'r3' : 'L3',  # pin 4
    'c1' : 'H9',  # pin 5
    'r5' : 'L5',  # pin 6
    'c3' : 'H11', # pin 7
    'c6' : 'H14', # pin 8
    'c8' : 'H16', # pin 9
    'r4' : 'L4',  # pin 10
    'r6' : 'L6',  # pin 11
    'c5' : 'H13', # pin 12
    'r1' : 'L1',  # pin 13
    'c7' : 'H15', # pin 14
    'r7' : 'L7',  # pin 15
    'r8' : 'L8'   # pin 16
}

map_u201 = {
    'c4' : 'H4', # pin 1
    'c2' : 'H2', # pin 2
    'r2' : 'L3',  # pin 3
    'r3' : 'L2',  # pin 4
    'c1' : 'H1',  # pin 5
    'r5' : 'L5',  # pin 6
    'c3' : 'H3', # pin 7
    'c6' : 'H6', # pin 8
    'c8' : 'H8', # pin 9
    'r4' : 'L8',  # pin 10
    'r6' : 'L7',  # pin 11
    'c5' : 'H5', # pin 12
    'r1' : 'L1',  # pin 13
    'c7' : 'H7', # pin 14
    'r7' : 'L6',  # pin 15
    'r8' : 'L4'   # pin 16
}

map_u202 = {
    'c4' : 'H6', # pin 1
    'c2' : 'H3', # pin 2
    'r2' : 'L10',  # pin 3
    'r3' : 'L11',  # pin 4
    'c1' : 'H1',  # pin 5
    'r5' : 'L13',  # pin 6
    'c3' : 'H2', # pin 7
    'c6' : 'H4', # pin 8
    'c8' : 'H7', # pin 9
    'r4' : 'L12',  # pin 10
    'r6' : 'L14',  # pin 11
    'c5' : 'H5', # pin 12
    'r1' : 'L9',  # pin 13
    'c7' : 'H8', # pin 14
    'r7' : 'L15',  # pin 15
    'r8' : 'L16'   # pin 16
}

map_u204 = {
    'c4' : 'H14', # pin 1
    'c2' : 'H11', # pin 2
    'r2' : 'L13',  # pin 3
    'r3' : 'L11',  # pin 4
    'c1' : 'H9',  # pin 5
    'r5' : 'L10',  # pin 6
    'c3' : 'H10', # pin 7
    'c6' : 'H12', # pin 8
    'c8' : 'H15', # pin 9
    'r4' : 'L16',  # pin 10
    'r6' : 'L15',  # pin 11
    'c5' : 'H13', # pin 12
    'r1' : 'L9',  # pin 13
    'c7' : 'H16', # pin 14
    'r7' : 'L14',  # pin 15
    'r8' : 'L12'   # pin 16
}

# Describes how the matrix is made up of 8x8 modules. There are 4, they are placed in a matrix, and can be rotated
matrix = {
    (1, 1) : {
        'map' : map_u203,
        'rot' : 1
    },
    (1, 2): {
        'map': map_u201,
        'rot': 1
    },
    (2, 1): {
        'map': map_u204,
        'rot': -1
    },
    (2, 2): {
        'map': map_u202,
        'rot': -1
    }
}

def generate_translator(map_ux):
    """
    Makes a translator from rows and columns into the designators. Example:
    (1, 1) -> ("L8", H3")
    :return: translator
    """
    translator = {}
    for x in product(tuple(range(1, 8 + 1)),
                     tuple(range(1, 8 + 1))):
        kstr0 = x[0]
        vstr0 = map_ux['r' + str(x[0])]
        kstr1 = x[1]
        vstr1 = map_ux['c' + str(x[1])]
        translator[(kstr0, kstr1)] = (vstr0, vstr1)
    return translator

def place_module_in_matrix(translator, dir, pos):
    """
    Places module along other modules in the matrix and adjust the translator accordingly
    :param translator: translator for the module
    :param dir: rotation. Can rotate clockwise and ccw
    :param pos: position in matrix
    :return: corrected translator
    """
    ret_rot = {}

    for k,v in translator.items():
        # rotate
        if dir == 1:
            #  90:
            ret_rot[((8 + 1) - k[1], k[0])] = v

        elif dir == -1:
            # -90
            ret_rot[(k[1], (8 + 1) - k[0])] = v

        else: # no rotation
            ret_rot[(k[0], k[1])] = v

    # translate
    ret = {}
    for k,v in ret_rot.items():
        ret[(k[0] + (pos[0] - 1) * 8, k[1] + (pos[1] - 1) * 8)] = v

    return ret

def generate_translator_full():
    """
    Makes the translator for the entire matrix made
    :return: translator from row and columns to designators
    """
    translator = {}
    for k,v in matrix.items():
        for k, v in place_module_in_matrix(generate_translator(v['map']), v['rot'], pos=k).items():
            translator[k] = v

    return {k: (t_ctrl2bit[v[0]], t_ctrl2bit[v[1]]) for k, v in translator.items()}

if __name__=='__main__':
    tt = generate_translator(map_u204)
    print(tt)
    print(place_module_in_matrix(tt, -1, (1,1)))
    print(place_module_in_matrix(tt, -1, (1,1))[(1,1)])
    #translator = generate_translator_full()
    #print(translator)
    #print(format_str_translator(translator))
