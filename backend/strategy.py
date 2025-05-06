import random

# Arvioi käden vahvuus (yksinkertaistettu)
def evaluate_hand(hand, board):
    """
    Tämä on yksinkertainen arviointifunktio, joka analysoi käden ja pöydän.
    """
    hand_strength = random.uniform(0, 1)  # Arvioi käden voimakkuus 0-1 välillä
    return hand_strength

# Pelistrategian suositukset
def make_move(hand, board, pot_size, player_chips, game_stage):
    """
    Tämä funktio antaa suosituksia siitä, mitä pelaajan pitäisi tehdä.
    """
    hand_strength = evaluate_hand(hand, board)
    
    if game_stage == "pre-flop":
        if hand_strength > 0.8:  # Hyvä käsi (esim. AA, KK)
            return "raise", pot_size * 2  # Suuri korotus
        elif hand_strength > 0.5:  # Keskivahva käsi (esim. KQ, AJ)
            return "call", pot_size * 0.5  # Maksaa (call)
        else:
            return "check", 0  # Heikko käsi, tarkista
    elif game_stage == "flop":
        if hand_strength > 0.8:  # Hyvä osuma flopista (esim. väri tai suora)
            return "raise", pot_size * 3  # Suuri korotus
        elif hand_strength > 0.3:  # Keskivahva osuma
            return "call", pot_size * 0.5  # Maksaa
        else:
            return "check", 0  # Heikko käsi, tarkista
    elif game_stage == "turn" or game_stage == "river":
        if hand_strength > 0.9:
            return "raise", pot_size * 3  # Suuri korotus, jos todella vahva käsi
        elif hand_strength > 0.5:
            return "call", pot_size * 0.5  # Maksaa, jos käsi on kohtuullinen
        else:
            return "fold", 0  # Heikko käsi, heitä pois
