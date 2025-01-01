public class Card {
    // Variables to store values for suit, rank and rank values for use in arrays later
    private final String suit;
    private final String rank;
    private final int rankValue;

    // Card constructor
    public Card(String suit, String rank, int rankValue) {
        this.suit = suit;
        this.rank = rank;
        this.rankValue = rankValue;
    }

    // Method to get suit of a card
    public String getSuit() {
        return suit;
    }

    // Method to get rank of a card
    public String getRank() {
        return rank;
    }

    // Method to get rank value of a card
    public int getRankValue() {
        return rankValue;
    }

    // Method to output full card
    @Override
    public String toString() {
        return getRank() + " of " + getSuit();
    }
}