public class Snap extends CardTest {
   public static void main(String[] args) {
      // Creates 100 new cards
      Card snapCards[] = new Card[100];
      int numSnaps = 0, numSupersnaps = 0;

      System.out.println("SNAP CARD GAME!");
      System.out.println("---------------\n");

      for (int i = 0; i < 100; i++) {

         snapCards[i] = new Card(); // Generate new cards (up to 100)

         System.out.println(snapCards[i]);   // Output each card

         // IF a card is the same colour AND the same rank as the previous card, output SUPERSNAP and add 1 to total supersnaps
         if (i > 0 && snapCards[i].getColour() == snapCards[i - 1].getColour() && snapCards[i].getRankValue() == snapCards[i - 1].getRankValue()) {
            System.out.println("!!!!! SUPERSNAP !!!!!");
            numSupersnaps++;
         }
         // IF a card is the same as the previous card, output SNAP and add 1 to total snaps
         else if (i > 0 && snapCards[i].getRankValue() == snapCards[i - 1].getRankValue()) {
            System.out.println("!!!!! SNAP !!!!!");
            numSnaps++;
         }
      }

      numSupersnaps = numSupersnaps + numSnaps; // Supersnaps total include Snaps total

      System.out.println("\n==================================");
      System.out.println("Total Number of SNAPS:\t\t\t" + numSnaps);
      System.out.println("Total Number of SUPERSNAPS:\t\t" + numSupersnaps);
   }
}