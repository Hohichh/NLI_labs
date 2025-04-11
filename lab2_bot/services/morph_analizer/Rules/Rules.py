noun_rules = {
    "singular" : {
        "non-posessive" : "{BASE}",
        "posessive" : "{SPOS}"
    },
    "plural" : {
        "non-posessive" : "{PLUR}",
        "posessive" : "{PPOS}"
    }
}

verb_rules = {
    "present": {
        "simple": {
            "singular": {
                "first": {"active": "{BASE}", "passive": "am {PART}"},
                "second": {"active": "{BASE}", "passive": "are {PART}"},
                "third": {"active": "{_3S}", "passive": "is {PART}"}
            },
            "plural": {
                "first": {"active": "{BASE}", "passive": "are {PART}"},
                "second": {"active": "{BASE}", "passive": "are {PART}"},
                "third": {"active": "{BASE}", "passive": "are {PART}"}
            }
        },
        "continuous": {
            "singular": {
                "first": {"active": "am {GER}", "passive": "am being {PART}"},
                "second": {"active": "are {GER}", "passive": "are being {PART}"},
                "third": {"active": "is {GER}", "passive": "is being {PART}"}
            },
            "plural": {
                "first": {"active": "are {GER}", "passive": "are being {PART}"},
                "second": {"active": "are {GER}", "passive": "are being {PART}"},
                "third": {"active": "are {GER}", "passive": "are being {PART}"}
            }
        },
        "perfect": {
            "singular": {
                "first": {"active": "have {PART}", "passive": "have been {PART}"},
                "second": {"active": "have {PART}", "passive": "have been {PART}"},
                "third": {"active": "has {PART}", "passive": "has been {PART}"}
            },
            "plural": {
                "first": {"active": "have {PART}", "passive": "have been {PART}"},
                "second": {"active": "have {PART}", "passive": "have been {PART}"},
                "third": {"active": "have {PART}", "passive": "have been {PART}"}
            }
        },
        "perfect-continuous": {
            "singular": {
                "first": {"active": "have been {GER}", "passive": "have been being {PART}"},
                "second": {"active": "have been {GER}", "passive": "have been being {PART}"},
                "third": {"active": "has been {GER}", "passive": "has been being {PART}"}
            },
            "plural": {
                "first": {"active": "have been {GER}", "passive": "have been being {PART}"},
                "second": {"active": "have been {GER}", "passive": "have been being {PART}"},
                "third": {"active": "have been {GER}", "passive": "have been being {PART}"}
            }
        }
    },
    "past": {
        "simple": {
            "singular": {
                "first": {"active": "{PAST}", "passive": "was {PART}"},
                "second": {"active": "{PAST}", "passive": "were {PART}"},
                "third": {"active": "{PAST}", "passive": "was {PART}"}
            },
            "plural": {
                "first": {"active": "{PAST}", "passive": "were {PART}"},
                "second": {"active": "{PAST}", "passive": "were {PART}"},
                "third": {"active": "{PAST}", "passive": "were {PART}"}
            }
        },
        "continuous": {
            "singular": {
                "first": {"active": "was {GER}", "passive": "was being {PART}"},
                "second": {"active": "were {GER}", "passive": "were being {PART}"},
                "third": {"active": "was {GER}", "passive": "was being {PART}"}
            },
            "plural": {
                "first": {"active": "were {GER}", "passive": "were being {PART}"},
                "second": {"active": "were {GER}", "passive": "were being {PART}"},
                "third": {"active": "were {GER}", "passive": "were being {PART}"}
            }
        },
        "perfect": {
            "singular": {
                "first": {"active": "had {PART}", "passive": "had been {PART}"},
                "second": {"active": "had {PART}", "passive": "had been {PART}"},
                "third": {"active": "had {PART}", "passive": "had been {PART}"}
            },
            "plural": {
                "first": {"active": "had {PART}", "passive": "had been {PART}"},
                "second": {"active": "had {PART}", "passive": "had been {PART}"},
                "third": {"active": "had {PART}", "passive": "had been {PART}"}
            }
        },
        "perfect-continuous": {
            "singular": {
                "first": {"active": "had been {GER}", "passive": "had been being {PART}"},
                "second": {"active": "had been {GER}", "passive": "had been being {PART}"},
                "third": {"active": "had been {GER}", "passive": "had been being {PART}"}
            },
            "plural": {
                "first": {"active": "had been {GER}", "passive": "had been being {PART}"},
                "second": {"active": "had been {GER}", "passive": "had been being {PART}"},
                "third": {"active": "had been {GER}", "passive": "had been being {PART}"}
            }
        }
    },
    "future": {
        "simple": {
            "singular": {
                "first": {"active": "will {BASE}", "passive": "will be {PART}"},
                "second": {"active": "will {BASE}", "passive": "will be {PART}"},
                "third": {"active": "will {BASE}", "passive": "will be {PART}"}
            },
            "plural": {
                "first": {"active": "will {BASE}", "passive": "will be {PART}"},
                "second": {"active": "will {BASE}", "passive": "will be {PART}"},
                "third": {"active": "will {BASE}", "passive": "will be {PART}"}
            }
        },
        "continuous": {
            "singular": {
                "first": {"active": "will be {GER}", "passive": "will be being {PART}"},
                "second": {"active": "will be {GER}", "passive": "will be being {PART}"},
                "third": {"active": "will be {GER}", "passive": "will be being {PART}"}
            },
            "plural": {
                "first": {"active": "will be {GER}", "passive": "will be being {PART}"},
                "second": {"active": "will be {GER}", "passive": "will be being {PART}"},
                "third": {"active": "will be {GER}", "passive": "will be being {PART}"}
            }
        },
        "perfect": {
            "singular": {
                "first": {"active": "will have {PART}", "passive": "will have been {PART}"},
                "second": {"active": "will have {PART}", "passive": "will have been {PART}"},
                "third": {"active": "will have {PART}", "passive": "will have been {PART}"}
            },
            "plural": {
                "first": {"active": "will have {PART}", "passive": "will have been {PART}"},
                "second": {"active": "will have {PART}", "passive": "will have been {PART}"},
                "third": {"active": "will have {PART}", "passive": "will have been {PART}"}
            }
        },
        "perfect-continuous": {
            "singular": {
                "first": {"active": "will have been {GER}", "passive": "will have been being {PART}"},
                "second": {"active": "will have been {GER}", "passive": "will have been being {PART}"},
                "third": {"active": "will have been {GER}", "passive": "will have been being {PART}"}
            },
            "plural": {
                "first": {"active": "will have been {GER}", "passive": "will have been being {PART}"},
                "second": {"active": "will have been {GER}", "passive": "will have been being {PART}"},
                "third": {"active": "will have been {GER}", "passive": "will have been being {PART}"}
            }
        }
    }
}

