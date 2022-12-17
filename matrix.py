""" Makes a

Each shift-register is represented by 8 bits and each led instruction is represented by a tuple of two values (row, col)

"""
# h
#
# row is a low-side shift register value and col a high-side
# generate a frame in the ordinary way
# compliment the high side bytes
# slice it into 4

from translator import generate_translator_full

class Sreg():
    """
    This holds a state for a single shiftregister. Bits a shifted in such that MSB is QA and the LSB is QH.
    """
    def __init__(self, bits = 0b00000000, hl = 0b00000000):
        self.bits = bits
        self.hl = hl # initially assumes that all are low-side controllers

    def set_bit_hl(self, position, state=1):
        if state == 1:
            self.hl |= 1 << position
            return
        if state == 0:
            self.h1 &= ~(1 << position)
        raise ValueError('Unknown high/low state {state}')

    def set_bit_hl_all_high(self):
        for i in range(8):
            self.set_bit_hl(i, 1)

    def set_bit_hl_all_low(self):
        for i in range(8):
            self.set_hl(i, 0)

    def set_bit(self, position):
        self.bits |= 1 << position

    def __repr__(self):
        bstr = list(bin(self.bits ^ self.hl))[2:]

        bstr_proto = list('0b' + '0' * 8)[2:]  # dont want the '0b' part
        bstr_proto = list(reversed(bstr_proto))

        for i, c in enumerate(reversed(bstr)):
            bstr_proto[len(bstr_proto) - 1 - i] = c

        return ('0b' + ''.join(list(bstr_proto)))

class Frame():
    """
    A frame is shift register states. The states in the arrya belongs to [U205, U206, U207, U208]
    """
    def __init__(self, translator, sregs):
        self.translator = translator
        self.sregs = sregs

    def add_led(self, led): # led, a two element tuple
        i, j = self.translator[led]
        self.sregs[i // 8].set_bit((i % 8))
        self.sregs[j // 8].set_bit((j % 8))

    def __repr__(self):
        return(str(self.sregs))

    def get_sregs(self):
        return [str(s) for s in self.sregs]

class Movie():
    """
    16 frames to amovie. This cuts the number of frames down to the minimum needed to produce the movie by cycling
    through the states. To get a uniform brightness between frames it is required to add filler frames. This can be
    done in firmware.
    """
    def __init__(self, translator, identifier):
        self.frames = {
        }
        self.translator = translator
        self.identifier = identifier

    def get_frame_number(self, led):
        i, j = self.translator[led]

        if i // 8 in (0, 2):
            return i -  i // (2 * 8)

        if j // 8 in (0, 2):
            return j - j // (2 * 8)

    def add(self, movie):
        leds = sorted(movie)
        for led in leds:
            fn = self.get_frame_number(led)
            #print(f'Added led {led} to frame number : {fn}')
            if not fn in self.frames:
                new_frame = Frame(self.translator, sregs=[Sreg(), Sreg(hl=0b11111111), Sreg(), Sreg(hl=0b11111111)])
                self.frames[fn] = new_frame

            self.frames[fn].add_led(led)

    def __repr__(self):
        return(str(self.frames))

    def format_ccode(self, ftype = 'uint8_t'):
        """
        Output a C-formatted string that can be copied into firmware.
        :param ftype:
        :return:
        """
        retstr = ftype + ' ' + self.identifier + '[' + str(len(self.frames) * 4) + ']' + ' = { '
        for k, v in self.frames.items():
            retstr += ', '.join(v.get_sregs()) + ', '# + '\n'
        retstr = retstr[:-2]
        retstr  += ' };\n'
        return(retstr)

if __name__=='__main__':
    from patterns import characters

    my_translator = generate_translator_full()

    with open('./firmware/patterns.c', 'w') as fh:
        fh.write('//typedef unsigned char uint8_t;\n\n')
        for k,v in characters.items():
            print(f'Making C-code for the character \'{k}\'...')
            m = Movie(my_translator, 'char_' + k)
            m.add(v)
            fh.write(m.format_ccode())
        print(f'Done!')
