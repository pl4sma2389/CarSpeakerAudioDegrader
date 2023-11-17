effect_library = [
    {
        "ident": "gain_reduce",
        "builtin": True,
        "location": "Gain",
        "params": {
            "gain_db": -8
        }
    },
    {
        "ident": "binaural_nonbass",
        "builtin": False,
        "location": "./VST3s/Sennheiser AMBEO Orbit.vst3",
        "params": {
            "azimuth": 10,
            "elevation": -15,
            "reflection_enable": False,
            "clarity": 75,
            "width": 100
        }
    },
    {
        "ident": "binaural_bass",
        "builtin": False,
        "location": "./VST3s/Sennheiser AMBEO Orbit.vst3",
        "params": {
            "azimuth": 180,
            "elevation": -30,
            "reflection_enable": False,
            "clarity": 75,
            "width": 30
        }
    },
    {
        "ident": "filter_nonbass",
        "builtin": False,
        "location": "./VST3s/kHs Filter.vst3",
        "params": {
            "type": "High pass",
            "cutoff": 32.2,
            "Q": 0.275,
        }
    },
    {
        "ident": "filter_bass",
        "builtin": False,
        "location": "./VST3s/kHs Filter.vst3",
        "params": {
            "type": "Low pass",
            "cutoff": 267,
            "Q": 0.1,
        }
    },
    {
        "ident": "haas",
        "builtin": False,
        "location": "./VST3s/kHs Haas.vst3",
        "params": {
            "delay": '0.20\u202fms',
        }
    },
    {
        "ident": "supermassive",
        "builtin": False,
        "location": "./VST3s/ValhallaSupermassive.vst3",
        "params": {
            "width": 100,
            "lowcut": 10,
            "mode": "Gemini",
        }
    },
]

effect_chain_complex = [
    [
        ["gain_reduce", "binaural_nonbass", "filter_nonbass"],
        ["gain_reduce", "binaural_bass", "filter_bass"]
    ],
    "haas",
    "supermassive"
]

effect_chain = [
    "gain_reduce",
    "haas",
    "supermassive"
]