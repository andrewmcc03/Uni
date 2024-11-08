//public class Snap {
//   public static void main(String[] args) {
//      // Creates 100 new cards
//      Card snapCards[] = new Card[100];
//      int numSnaps = 0;
//
//      System.out.println("SNAP CARD GAME!");
//      System.out.println("---------------\n");
//
//      for (int i = 0; i < 100; i++) {
//
//         snapCards[i] = new Card(); // Generate new cards (up to 100)
//
//         System.out.println(snapCards[i]);   // Output each card
//
//         // IF a card is the same as the following card, output SNAP and add 1 to total snaps
//         if (i > 0 && snapCards[i].getRankValue() == snapCards[i - 1].getRankValue()) {
//            System.out.println("SNAP!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
//            numSnaps++;
//         }
//      }
//
//      System.out.println("\n==========================");
//      System.out.println("Total Number of Snaps:\t" + numSnaps);
//   }
//}