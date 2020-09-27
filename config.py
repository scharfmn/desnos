from functools import partial


TEXTBOX_KEY = partial("box_{0}".format)
TEXTBOXES = "textboxes"
LABELS = "labels"
EVENT_TITLE_TEXT = "event_text"

EVENTS = {
    "qa": {
        TEXTBOXES: {TEXTBOX_KEY("a"): "question", TEXTBOX_KEY("b"): "answer", },
        EVENT_TITLE_TEXT: ["language event", "question · answer"],
    },
    "if-then": {
        TEXTBOXES: {TEXTBOX_KEY("a"): "if (or when)", TEXTBOX_KEY("b"): "then", },
        EVENT_TITLE_TEXT: ["language event", "if · then"],
    },
    "after": {
        TEXTBOXES: {TEXTBOX_KEY("a"): "after", TEXTBOX_KEY("b"): "(...)"},
        EVENT_TITLE_TEXT: ["language event", "Nihaal Prasad’s “After”"],
    },
}

TEST_DATA = {
    "box_a": [
        "When foxes return from eating at the abandoned marketplace",
        "When the curtain of darkness falls in the valley past the viaduct",
        "When figures appear to disavow the things we had thought unchanging and material",
        "When the so-called simple things begin to be incredibly difficult",
        "When the condensers of the stolen milk cool the air",
        "When every teaching suddenly fades",
        "When the fourth thing that comes to mind in rhyme stops",
        "When we decide to go by twos and threes",
        "When the apple really does not fall far from the tree",
        "When it does not seem like any have had sufficient to suffice",
    ],
    "box_b": [
        "then the horizon will actually change",
        "then the cake will actually blossom",
        "then the fan will actually whirr and chirr with non-plastic efficiency",
        "then there will be little teethmarks everywhere",
        "then we will go tootling through the trellis of the bird wires",
        "then we will see it behind the zinc counter of the lac banc",
        "then the previous plectrum will fly toward other instruments",
        "then long exposures will be a thing of the past",
    ],
}
