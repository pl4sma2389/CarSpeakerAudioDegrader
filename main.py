from pedalboard import Pedalboard, load_plugin, Mix, Gain
from pedalboard.io import AudioFile
import os

print("Loading VSTs...")
# Load required VSTs
plg_binaural_bass = load_plugin("./VST3s/Sennheiser AMBEO Orbit.vst3")
plg_binaural_nonbass = load_plugin("./VST3s/Sennheiser AMBEO Orbit.vst3")
plg_haas = load_plugin("./VST3s/kHs Haas.vst3")
plg_filter_bass = load_plugin("./VST3s/kHs Filter.vst3")
plg_filter_nonbass = load_plugin("./VST3s/kHs Filter.vst3")
plg_supermassive = load_plugin("./VST3s/ValhallaSupermassive.vst3")

print("Finished loading VSTs.\nSetting parameters...")

# Set plugin parameters
setattr(plg_binaural_bass, "azimuth", 180)
setattr(plg_binaural_bass, "elevation", -30)
setattr(plg_binaural_bass, "reflection_enable", False)
setattr(plg_binaural_bass, "clarity", 75)
setattr(plg_binaural_bass, "width", 30)

setattr(plg_binaural_nonbass, "azimuth", 10)
setattr(plg_binaural_nonbass, "elevation", -15)
setattr(plg_binaural_nonbass, "reflection_enable", False)
setattr(plg_binaural_nonbass, "clarity", 75)
setattr(plg_binaural_nonbass, "width", 100)

setattr(plg_filter_bass, "type", "Low pass")
setattr(plg_filter_bass, "cutoff", 267)
setattr(plg_filter_bass, "Q", 0.1)

setattr(plg_filter_nonbass, "type", "High pass")
setattr(plg_filter_nonbass, "cutoff", 32.2)
setattr(plg_filter_nonbass, "Q", 0.275)

setattr(plg_haas, "delay", '0.20\u202fms')

# setattr(plg_supermassive, "mix", 60)
# setattr(plg_supermassive, "delay_ms", '20\u202fms')
# setattr(plg_supermassive, "delaywarp", 50)
# setattr(plg_supermassive, "feedback", 30)
# setattr(plg_supermassive, "density", 100)
setattr(plg_supermassive, "width", 100)
setattr(plg_supermassive, "lowcut", 10)
# setattr(plg_supermassive, "highcut", 6500)
# setattr(plg_supermassive, "modrate", 0.01)
# setattr(plg_supermassive, "moddepth", 0)
setattr(plg_supermassive, "mode", "Gemini")

print("Finished setting parameters.\nStarting processing...")

'''# Read in a whole audio file:
with AudioFile('or2ed5.mp3', 'r') as f:
    audio = f.read(f.frames)
    samplerate = f.samplerate'''


'''print("Binaural:", plg_binaural_bass.parameters.keys(),
      "\nHaas:", plg_haas.parameters.keys(),
      "\nFilter:", plg_filter_bass.parameters.keys())'''


# Make a Pedalboard object, containing multiple plugins:
bass = Pedalboard([Gain(gain_db=-8), plg_binaural_bass, plg_filter_bass])
nonbass = Pedalboard([Gain(gain_db=-8), plg_binaural_nonbass, plg_filter_nonbass])

rejoin = Pedalboard([Mix([nonbass, bass])])
finalboard = Pedalboard([rejoin, plg_haas, plg_supermassive])

'''# Run the audio through this pedalboard!
effected = finalboard(audio, samplerate)

# Write the audio back as a wav file:
with AudioFile('processed-output.wav', 'w', samplerate, effected.shape[0]) as f:
    f.write(effected)'''

for file in os.listdir("./ToProcess"):
    if file.endswith(".txt"):
        continue
    print("Now processing:", file)
    with AudioFile('./ToProcess/'+file, 'r') as f:
        audio = f.read(f.frames)
        samplerate = f.samplerate

    effected = finalboard(audio, samplerate)
    print("Now writing:", file)
    with AudioFile('./Processed/'+file, 'w', samplerate, effected.shape[0]) as f:
        f.write(effected)
print("Finished processing. Enjoy your crappy car audio!")
os.system("pause")
