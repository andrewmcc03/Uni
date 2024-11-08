import java.util.Random;

public class Card implements Comparable<Card>{
    private final int RANK, SUIT;
    private static final Random GENERATOR = new Random();

    private static final String[] RANKS = {"2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"};
    private static final String[] SUITS = {"Clubs", "Diamonds", "Hearts", "Spades"};

    public Card() {
        RANK = GENERATOR.nextInt(RANKS.length);
        SUIT = GENERATOR.nextInt(SUITS.length);;
    }

    public String getRank() {
        return RANKS[RANK];
    }

    public String getSuit() {
        return SUITS[SUIT];
    }

    public int getRankValue() {
        return RANK;
    }

    // Challenge 6.1
    public String getColour() {
        if (SUITS[SUIT].equals("Diamonds") || SUITS[SUIT].equals("Hearts")) {
            return "Red";
        }
        else {
            return "Black";
        }
    }

    @Override
    public String toString() {
        return getRank() + " of " + getSuit();
    }

    @Override
    public int compareTo(Card otherCard) {
        if (this.getRankValue() > otherCard.getRankValue()) {
            return 1;
        }
        else if (this.getRankValue() < otherCard.getRankValue()) {
            return -1;
        }
        else {
            return 0;
        }
    }
}