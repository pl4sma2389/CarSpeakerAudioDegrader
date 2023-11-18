from gui.core import run_gui
from cfg.core import load_config

'''print("Inputs:", AudioStream.input_device_names, "\nOutputs:", AudioStream.output_device_names)

with AudioStream(
    input_device_name="CABLE Output (VB-Audio Virtual",
    output_device_name="Primary Sound Driver"
) as stream:
    filters = Pedalboard([LowpassFilter(cutoff_frequency_hz=50), Gain(gain_db=5)])
    stream.plugins.append(filters)
    input("Press enter to stop streaming...")'''

run_gui(config=load_config())
