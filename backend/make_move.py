# make_move.py
from evaluate_hand import evaluate_hand

def make_move(hand, board, pot_size, player_chips, game_stage):
    """
    Tämä funktio antaa suosituksia siitä, mitä pelaajan pitäisi tehdä.
    Pelin eri vaiheessa (pre-flop, flop, turn, river) arvioidaan käden vahvuus 
    ja pelistrategia päätetään tämän perusteella.
    """
    
    # Arvioi käden vahvuus
    hand_strength = evaluate_hand(hand, board)

    # Pre-flop-vaihe
    if game_stage == "pre-flop":
        if hand_strength > 0.9:  # Hyvä käsi (esim. AA, KK, AK)
            return "raise", pot_size * 2  # Suuri korotus
        elif hand_strength > 0.7:  # Keskivahva käsi (esim. KQ, AJ, TT)
            return "call", pot_size * 0.5  # Maksaa
        elif hand_strength > 0.5:  # Hyvin kohtuullinen käsi (esim. AQ, KJ, 99)
            return "call", pot_size * 0.3  # Maksaa pienempi panos
        else:
            return "fold", 0  # Heikko käsi, foldataan

    # Flop-vaihe
    elif game_stage == "flop":
        if hand_strength > 0.85:  # Hyvä osuma flopista (esim. väri tai suora)
            return "raise", pot_size * 3  # Suuri korotus
        elif hand_strength > 0.6:  # Keskivahva osuma
            if any(card in board for card in ['A', 'K', 'Q', 'J', 'T']):  # Korkeat kortit pöydässä
                return "call", pot_size * 0.5  # Maksaa
            else:
                return "check", 0  # Ei vielä vahva, tarkistetaan
        elif hand_strength > 0.3:  # Heikko osuma
            if any(card in board for card in ['A', 'K', 'Q']):  # Hyvin korkeat kortit pöydässä
                return "check", 0  # Heikko käsi, tarkista
            else:
                return "fold", 0  # Heikko käsi ja ei hyviä mahdollisuuksia, foldataan
        else:
            return "fold", 0  # Todella heikko käsi, foldataan

    # Turn-vaihe
    elif game_stage == "turn":
        if hand_strength > 0.9:  # Hyvä käsi, esim. väri tai suora muodostettu
            return "raise", pot_size * 3  # Suuri korotus
        elif hand_strength > 0.6:  # Keskivahva käsi, mutta ei vielä suoraa tai väriä
            return "call", pot_size * 0.5  # Maksaa, jos hyvä osuma
        elif hand_strength > 0.4:  # Käsissä ei vielä suoraa eikä väriä
            return "check", 0  # Tarkistetaan, jos ei ole hyvä osuma
        else:
            return "fold", 0  # Heikko käsi, foldataan

    # River-vaihe
    elif game_stage == "river":
        if hand_strength > 0.95:  # Hyvin vahva käsi (esim. suora, väri tai täyskäsi)
            return "raise", pot_size * 4  # Suuri korotus, käytetään kaikki hyvä mahdollisuus
        elif hand_strength > 0.75:  # Keskivahva käsi, mutta ei tarpeeksi vahva
            return "call", pot_size * 0.6  # Maksaa kohtuullinen panos
        elif hand_strength > 0.5:  # Oletetaan kohtuullinen tilanne
            return "call", pot_size * 0.3  # Maksaa pienempi panos
        else:
            return "fold", 0  # Heikko käsi, foldataan

    # Jos peli ei ole pre-flop, flop, turn tai river, ei tehdä liikettä
    return "check", 0
