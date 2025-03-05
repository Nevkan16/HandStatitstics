def convert_card_format(card_text):
    RANKS = {"10": "T"}

    try:
        card1, card2 = card_text.split()
        suit1, rank1 = card1[0], RANKS.get(card1[1:], card1[1:])
        suit2, rank2 = card2[0], RANKS.get(card2[1:], card2[1:])

        if get_rank_value(rank2) > get_rank_value(rank1):
            high_rank, low_rank = rank1, rank2
        else:
            high_rank, low_rank = rank2, rank1

        result = high_rank + low_rank

        if rank1 != rank2:
            result += "s" if suit1 == suit2 else "o"

        return result
    except Exception as e:
        print(f"Ошибка при обработке строки '{card_text}': {e}")
        return None

def get_rank_value(rank):
    return "AKQJT98765432".index(rank)