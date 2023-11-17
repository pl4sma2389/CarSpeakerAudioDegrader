from pedalboard import Pedalboard, load_plugin, Mix, Gain, Reverb, HighpassFilter, MP3Compressor, LowpassFilter
import pedalboard as pb
from pedalboard.io import AudioStream


def init_pb_old():
    print("Loading VSTs...")  # Load required VSTs
    plg_binaural_bass = load_plugin("./VST3s/Sennheiser AMBEO Orbit.vst3")
    plg_binaural_nonbass = load_plugin("./VST3s/Sennheiser AMBEO Orbit.vst3")
    plg_haas = load_plugin("./VST3s/kHs Haas.vst3")
    plg_filter_bass = load_plugin("./VST3s/kHs Filter.vst3")
    plg_filter_nonbass = load_plugin("./VST3s/kHs Filter.vst3")
    plg_supermassive = load_plugin("./VST3s/ValhallaSupermassive.vst3")
    print("Finished loading VSTs.")

    print("Setting parameters...")  # Set plugin parameters
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
    print("Finished setting parameters.")

    print("Returning master Pedalboard...")
    return Pedalboard([
        Mix([
            Pedalboard([Gain(gain_db=-8), plg_binaural_nonbass, plg_filter_nonbass]),
            Pedalboard([Gain(gain_db=-8), plg_binaural_bass, plg_filter_bass])
        ]),
        plg_haas,
        plg_supermassive
    ])


def assemble_pb(library=None, chain=None):
    assembled_pedalboard = []
    if library and chain:
        for effect_name in chain:
            if type(effect_name) is str:
                for effect_slot in library:
                    if effect_slot["ident"] == effect_name:
                        print("Assembling plugin", effect_slot["location"])
                        if type(effect_slot["location"]) is str:
                            plugin = pb.load_plugin(effect_slot["location"])
                            for setting in effect_slot["params"].items():
                                print("Setting", setting, "on plugin", plugin)
                                setattr(plugin, setting[0], setting[1])
                            assembled_pedalboard.append(plugin)
                            print("Assembled plugin", effect_slot["location"])
                        else:
                            builtin_key, builtin_value = None, None
                            for key, value in effect_slot["params"].items():
                                builtin_key, builtin_value = key, value
                            exec(f"assembled_pedalboard.append(effect_slot['location']({builtin_key}={builtin_value}))")
                            print("Assembled plugin", effect_slot["location"], "with built-in key", builtin_key, "and value", builtin_value)

    elif chain:
        print("Effect library is empty!")
    elif library:
        print("Effect chain is empty!")
    else:
        print("Effect library and chain are empty!")

    print(assembled_pedalboard)

    return Pedalboard(assembled_pedalboard)
