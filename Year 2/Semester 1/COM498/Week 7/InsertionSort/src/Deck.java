import java.util.Random;

public class Deck {
   private static final int NUMCARDS = 52;
   private final Card[] CARDS = new Card[52];
   private int cardIndex;

   public Deck() {
      for (int thisCard = 0; thisCard < NUMCARDS; thisCard++) {
         this.CARDS[thisCard] = new Card(thisCard % 13, thisCard / 13);
      }

      this.cardIndex = NUMCARDS - 1;
      this.shuffle();
   }

   private void shuffle() {
      int index;
      Card temp;

      Random random = new Random();

      for (int i = this.CARDS.length - 1; i > 0; i--) {
         index = random.nextInt(i + 1);
         temp = this.CARDS[index];
         this.CARDS[index] = this.CARDS[i];
         this.CARDS[i] = temp;
      }
   }

   public Card deal() {
      return this.CARDS[this.cardIndex--];
   }


//   public static void main(String[] args) {
//
//      Deck deck = new Deck();
//      int count = 0;
//
//      for (int i = 0; i < NUMCARDS; i++) {
//         count++;
//         System.out.println(deck.deal());
//      }
//      System.out.println(count);
//
//   }
}