from pedalboard import Pedalboard
import pedalboard as pb
import numpy as np


def init_pb_old():
    print("Loading VSTs...")  # Load required VSTs
    plg_binaural_bass = pb.load_plugin("./VST3s/Sennheiser AMBEO Orbit.vst3")
    plg_binaural_nonbass = pb.load_plugin("./VST3s/Sennheiser AMBEO Orbit.vst3")
    plg_haas = pb.load_plugin("./VST3s/kHs Haas.vst3")
    plg_filter_bass = pb.load_plugin("./VST3s/kHs Filter.vst3")
    plg_filter_nonbass = pb.load_plugin("./VST3s/kHs Filter.vst3")
    plg_supermassive = pb.load_plugin("./VST3s/ValhallaSupermassive.vst3")
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
        pb.Mix([
            Pedalboard([pb.Gain(gain_db=-8), plg_binaural_nonbass, plg_filter_nonbass]),
            Pedalboard([pb.Gain(gain_db=-8), plg_binaural_bass, plg_filter_bass])
        ]),
        plg_haas,
        plg_supermassive
    ])


def effect_handler(slot=None, library=None):
    print("Handler handling plugin", slot)
    if slot == 'mix':
        return slot
    else:
        for effect in library:
            if effect["ident"] == slot:
                print("Handler Assembling plugin", effect["location"])
                if type(effect["location"]) is str:  # This must be an external plugin
                    # print("This plugin is external")
                    plugin = pb.load_plugin(effect["location"])
                    for setting in effect["params"].items():
                        # print("Setting", setting, "on plugin", plugin)
                        setattr(plugin, setting[0], setting[1])
                    print("Handler Returning ext", plugin)
                    return plugin
                else:  # This must be an internal plugin
                    # print("This plugin is", type(effect["location"]))
                    builtin_key, builtin_value = None, None
                    for key, value in effect["params"].items():
                        builtin_key, builtin_value = key, value
                    plugin = f"effect['location']({builtin_key}={builtin_value})"
                    # print("Assembled plugin", effect["location"], "with built-in key", builtin_key, "and value", builtin_value)
                    print("Handler Returning int", eval(plugin))
                    return eval(plugin)


def raw_pb_component(library=None, chain=None):  # Loads and configures plugins from the "library" according to their order in the "chain"
    for index, item in enumerate(chain):
        if isinstance(item, str):
            chain[index] = effect_handler(slot=item, library=library)
        else:
            raw_pb_component(library=library, chain=item)

    return chain


def bake_pb_component(chain=None):
    if isinstance(chain, list):
        for index, item in enumerate(chain):
            if isinstance(item, list):
                if item[index] == 'mix':
                    bake_pb_component(chain=item)
                else:
                    print('Making chain:', pb.Chain(item))
                    chain[index] = pb.Chain(item)
            else:
                bake_pb_component(chain=item)

    return chain


def ice_pb_component(chain=None):
    if isinstance(chain, list):
        for index, item in enumerate(chain):
            if isinstance(item, list):
                if item[index] == 'mix':
                    item.pop(0)
                    print('Making mix:', item)
                    chain[index] = pb.Mix(item)
                else:
                    pass
            else:
                pass

    return chain


def assemble_pb(library=None, chain=None):
    assembled_pedalboard = []
    library_buffer = library.copy()
    chain_buffer = chain.copy()
    if library and chain:
        to_append = ice_pb_component(chain=bake_pb_component(chain=raw_pb_component(library=library_buffer, chain=chain_buffer)))
        assembled_pedalboard.append(to_append)
        print('Appended', to_append)
    elif chain:
        print("Effect library is empty!")
    elif library:
        print("Effect chain is empty!")
    else:
        print("Effect library and chain are empty!")

    print("Assembled Pedalboard:", assembled_pedalboard)

    return Pedalboard(assembled_pedalboard[0])


def preprocess_audio(pedalboard_to_use=None, audio_file_path=None):
    if not pedalboard_to_use:
        print("No Pedalboard specified to process the audio through. Aborting audio processing.")
        return None

    if not audio_file_path:
        print("No audio file specified. Aborting audio processing.")
        return None

    with pb.io.AudioFile(audio_file_path) as f:
        with pb.io.AudioFile('output.wav', 'w', f.samplerate, f.num_channels) as o:
            while f.tell() < f.frames:
                chunk = f.read(int(f.samplerate / 8))
                effected = pedalboard_to_use(chunk, f.samplerate, reset=False)
                o.write(effected)
