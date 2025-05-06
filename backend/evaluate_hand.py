# evaluate_hand.py

def evaluate_hand(hand, board):
    """
    Arvioi käden vahvuuden pre-flop-vaiheessa. 
    Tämä funktio ottaa huomioon parit, korkeat kortit ja mahdolliset suorat ja värit.
    """
    # Poimitaan käden kortit
    card1, card2 = hand[0], hand[1]

    # Arvioi käden vahvuus (alkuperäinen arvo 0-1)
    hand_strength = 0

    # Käden kortit
    rank1, suit1 = card1[0], card1[1]
    rank2, suit2 = card2[0], card2[1]

    # 1. Arvioidaan parit
    if rank1 == rank2:
        if rank1 == 'A':
            hand_strength = 1.0  # AA on vahvin pari
        elif rank1 == 'K':
            hand_strength = 0.95  # KK on toinen vahvin pari
        elif rank1 == 'Q':
            hand_strength = 0.9
        elif rank1 == 'J':
            hand_strength = 0.85
        else:
            hand_strength = 0.75  # Muut parit (10, 9, 8 jne.)

    # 2. Arvioidaan korkeat kortit (AK, AQ, KQ, jne.)
    elif rank1 == 'A' or rank2 == 'A':  # Ässä kädessä on aina erittäin vahva
        if rank1 == 'K' or rank2 == 'K':  # AK on yksi vahvimmista käsistä
            hand_strength = 0.85
        elif rank1 == 'Q' or rank2 == 'Q':  # AQ on myös vahva, mutta heikompi kuin AK
            hand_strength = 0.8
        elif rank1 == 'J' or rank2 == 'J':  # AJ on kohtuullinen
            hand_strength = 0.75
        else:
            hand_strength = 0.7  # Muut korkeammat kädet kuten AT, A9 jne.

    # 3. Muodostuvat suorat ja värit
    # Tarkastetaan, onko kädessä mahdollisuus muodostaa suora tai väri
    elif abs(ord(rank1) - ord(rank2)) == 1:  # Kaksi korttia, jotka voivat muodostaa suoran (esim. 8-9, 5-6)
        hand_strength = 0.6  # Suora ei ole niin vahva pre-flop, mutta parempi kuin heikko käsi

    # 4. Muut käsikombinaatiot
    elif suit1 == suit2:  # Jos kädessä on väri, mutta ei pareja
        hand_strength = 0.65  # Väri on melko vahva pre-flop
    else:
        hand_strength = 0.5  # Heikommat, ei väriä eikä suoraa

    # Jos kädessä on kaksi heikkoa korttia, kuten 7-2, vahvuus on erittäin alhainen
    if hand_strength == 0 and (rank1 in ['2', '3', '4', '5', '6', '7'] and rank2 in ['2', '3', '4', '5', '6', '7']):
        hand_strength = 0.3  # Esimerkiksi 7-2 on hyvin heikko käsi

    return hand_strength
