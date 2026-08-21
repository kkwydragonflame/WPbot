# List of valid roles for progression
VALID_ROLES = [
    "Åk1", "Åk2", "Åk3", "Alumni"
]

# List of valid progression moves, ie. the allowed transitions between roles such as from Åk1 to Åk2, or from Åk3 to Alumni
VALID_PROGRESSION_MOVES = [
    ("Åk1", "Åk2"),
    ("Åk2", "Åk3"),
    ("Åk3", "Alumni")
]