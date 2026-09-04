# List of valid roles for progression
VALID_ROLES = {
    "Åk1", "Åk2", "Åk3", "Alumni"
}

# List of valid progression moves, ie. the allowed transitions between roles such as from Åk1 to Åk2, or from Åk3 to Alumni
VALID_PROGRESSION_MOVES = {
    "Åk1": "Åk2",
    "Åk2": "Åk3",
    "Åk3": "Alumni"
}

def get_next_role(current_role):
    """
    Given a current role, return the next role in the progression.
    """
    return VALID_PROGRESSION_MOVES.get(current_role)


def can_progress(current_role, target_role):
    """
    Check if a user can progress from the current role to the target role.
    Returns True if the progression is valid, False otherwise.
    """
    return VALID_PROGRESSION_MOVES.get(current_role) == target_role