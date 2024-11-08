public class CardTest {
    public static void main(String[] args) {
        Card card1 = new Card();
        Card card2 = new Card();

        System.out.println("Card 1 is the " + card1);
        System.out.println("Card 2 is the " + card2);

        if (card1.compareTo(card2) > 0) {
            System.out.println("\nCard 1 is bigger.");
        }
        else if (card1.compareTo(card2) < 0) {
            System.out.println("\nCard 2 is bigger.");
        }
        else {
            System.out.println("\nCard 1 and Card 2 are equal.");
        }
    }
}