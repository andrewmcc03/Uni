public class Card {

    private final String suit;
    private final String rank;
    private final int rankValue;

    public Card(String suit, String rank, int rankValue) {
        this.suit = suit;
        this.rank = rank;
        this.rankValue = rankValue;
    }

    public String getSuit() {
        return suit;
    }

    public String getRank() {
        return rank;
    }

    public int getRankValue() {
        return rankValue;
    }

    @Override
    public String toString() {
        return getRank() + " of " + getSuit();
    }
}