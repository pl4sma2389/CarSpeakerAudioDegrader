import dearpygui.dearpygui as dpg
import tkinter.filedialog
from src.audio_pre.core import assemble_pb, preprocess_audio
from src.audio_pre.data import effect_library, effect_chain

data_about_body = "Developed by ohyeah2389 at Slip Angle Modding and Development\n\nThe following software, libraries, and assets are used in this program:\n\n" \
                     "Python 3.12: https://www.python.org/\n" \
                     "\tDear PyGui 1.10.1: https://github.com/hoffstadt/DearPyGui\n" \
                     "\twebcolors 1.13: https://github.com/ubernostrum/webcolors\n\n" \
                     "Roboto Mono: https://fonts.google.com/specimen/Roboto+Mono"

data_buildinfo = "Build Info goes here"  # TODO: Put build and/or version info here


def data_preprocess_body():
    dpg.add_file_dialog(show=False, tag="preprocess_file_picker", width=700, height=400)
    dpg.add_button(label="Test Button", callback=lambda: preprocess_audio(
        pedalboard_to_use=assemble_pb(library=effect_library, chain=effect_chain), # TODO: Add ability to load arbitrary effect libraries and effect chains from files
        audio_file_path=tkinter.filedialog.askopenfilename()
    ))


data_liveprocess_body = None

pagedata = [
    {
        'title': "Pre-Process Audio",
        'header': "Process audio files now for easier use later.",
        'body': data_preprocess_body,
    },
    {
        'title': "Live Audio",
        'header': "Process audio live.",
        'body': data_liveprocess_body,
    },
    {
        'title': "About",
        'header': "Car Speaker Audio Degrader",
        'body': data_about_body,
        'footer': data_buildinfo,
    }
]
