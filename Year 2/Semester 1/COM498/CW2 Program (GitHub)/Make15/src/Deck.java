import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class Deck {
   // List for storing deck of cards
   private List<Card> cards;

   // Deck constructor
   public Deck() {
      cards = new ArrayList<>();

      // Rank Values:    2    3    4    5    6    7    8    9    10    11      11       11      12
      String[] ranks = {"2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"};
      String[] suits = {"Clubs", "Diamonds", "Hearts", "Spades"};
      int[] rankValues = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 11, 11, 12};
      // NOTE: These rank values align with the standard that, beyond normal cards 2-10, Jacks, Kings and Queens are worth 11 points, and Aces are worth 12

      // For each suit in suits array
      for (String suit : suits) {
         for (int i = 0; i < ranks.length; i++) {
            cards.add(new Card(suit, ranks[i], rankValues[i]));
         }
      }

      // Shuffle created deck before dealing
      shuffle();
   }

   // Method to deal a new card for both player's hand and computer's card
   public Card dealCard() {
      if (!cards.isEmpty()) {
         return cards.remove(cards.size() - 1);
      }
      return null;
   }

   // Method to shuffle the deck in a randomised order
   public void shuffle() {
      Random random = new Random(); // For random number/value generation

      for (int i = cards.size() - 1; i > 0; i--) {
         int j = random.nextInt(i + 1);
         Card temp = cards.get(i);
         cards.set(i, cards.get(j));
         cards.set(j, temp);
      }
   }

   // Method to check if arrays/lists are or aren't empty
   public boolean isEmpty() {
      return cards.isEmpty();
   }
}