import numpy as np
from scipy.io.wavfile import write

samplerate = 44100 #Frequecy in Hz

# Creds to https://towardsdatascience.com/mathematics-of-music-in-python-b7d838c84f72 
# for how to create sound from numpy arrays, maths and music theory!
def get_wave(freq, duration=0.5, amp=1):
    '''
    Function takes the "frequecy" and "time_duration" for a wave 
    as the input and returns a "numpy array" of values at all points 
    in time
    '''
    
    amplitude = 4096 * amp
    t = np.linspace(0, duration, int(samplerate * duration))
    wave = amplitude * np.sin(2 * np.pi * freq * t)
    
    return wave

# To get a 1 second long wave of frequency 440Hz
# a_wave = get_wave(440, 1)

#wave features
# print(len(a_wave)) # 44100
# print(np.max(a_wave)) # 4096
# print(np.min(a_wave)) # -4096

def get_piano_notes():
    '''
    Returns a dict object for all the piano 
    note's frequencies
    '''
    # White keys are in Uppercase and black keys (sharps) are in lowercase
    octave = ['C', 'c', 'D', 'd', 'E', 'F', 'f', 'G', 'g', 'A', 'a', 'B'] 
    base_freq = 261.63 #Frequency of Note C4
    
    note_freqs = {octave[i]: base_freq * pow(2,(i/12)) for i in range(len(octave))}        
    note_freqs[''] = 0.0 # silent note
    
    return note_freqs
  
def play_note(note, duration, amp):
    '''
    Returns an array representing the note played for the specified duration.
    `Note` is given as a letter e.g. 'C'.
    '''
    # To get the piano note's frequencies
    note_freqs = get_piano_notes()
    frequency = note_freqs[note]
    return get_wave(frequency, duration, amp)
    
def play_melody(melody, duration, amp):
    '''
    Returns an array representing the concatenation of all notes, each played for the specified duration.
    `Melody` is given as a string. "-" represents a pause.
    '''
    result = None
    for note in melody:
        wave = np.zeros(samplerate)

        if note.isalpha():
            wave = play_note(note, duration, amp)

        if result is None:
            result = wave
        else:
            result = np.append(result, wave)
    # print(len(result) / samplerate)
    return result

def get_triad_chord(tonic):
    mappings = {
        "C": ["C", "E", "G"],
        "D": ["D", "F", "A"],
        "E": ["E", "G", "B"],
        "F": ["F", "A", "C"],
        "G": ["G", "B", "D"],
        "A": ["A", "C", "E"],
        "B": ["B", "D", "F"],
    }
    return mappings[tonic]

def convert_melody_to_chord_progressions(melody, chord_pattern):
    result = ""
    for note in melody:
        triad = get_triad_chord(note)
        for number in chord_pattern:
            result += triad[number]

    return result
        
def convert_numbers_to_melody(numbers):
    result = ""
    mappings = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    for number in numbers:
        result += mappings[(number - 1) % 7]
    return result        

# music_notes_twinkle_star = 'CCGGAAG-FFEEDDC-GGFFEED-GGFFEED-CCGGAAG-FFEEDDC-'

numbers_one = [3,1,4,1,5,9,2,6,5,3,5,8,9,7,9,3,2,1]
pattern_one = [0,2,1,2]
melody_one = convert_numbers_to_melody(numbers_one)
music_notes_one = convert_melody_to_chord_progressions(melody_one, pattern_one)

numbers_two = [3,1,4,1,5,9,2,6,5,3,5,8,9,7,9,3,2,1]
pattern_two = [0]
melody_two = convert_numbers_to_melody(numbers_one)
music_notes_two = convert_melody_to_chord_progressions(melody_two, pattern_two)

data = play_melody(music_notes_one, 0.25, 1)
data_two = play_melody(music_notes_two, 1, 2)

data = data * 0.5 + data_two * 0.5

write('my-music.wav', samplerate, data.astype(np.int16))