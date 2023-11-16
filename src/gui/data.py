data_about_body = "Developed by ohyeah2389 at Slip Angle Modding and Development\n\nThe following software, libraries, and assets are used in this program:\n\n" \
                     "Python 3.12: https://www.python.org/\n" \
                     "\tDear PyGui 1.10.1: https://github.com/hoffstadt/DearPyGui\n" \
                     "\twebcolors 1.13: https://github.com/ubernostrum/webcolors\n\n" \
                     "Roboto Mono: https://fonts.google.com/specimen/Roboto+Mono"

data_buildinfo = "Build Info goes here"  # TODO: Put build and/or version info here

data_preprocess_body = None

data_liveprocess_body = None

pagedata = [
    {
        'title': "Pre-Process Audio",
        'header': "Process audio files now for easier use later.",
        'body': data_preprocess_body
    },
    {
        'title': "Live Audio",
        'header': "Process audio live.",
        'body': data_liveprocess_body
    },
    {
        'title': "About",
        'header': "Car Speaker Audio Degrader",
        'body': data_about_body,
        'footer': data_buildinfo
    }
]
