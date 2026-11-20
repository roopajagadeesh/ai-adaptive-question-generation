def get_next_difficulty(score_percentage):

    if score_percentage >= 80:
        return "Hard"

    elif score_percentage >= 50:
        return "Medium"

    else:
        return "Easy"