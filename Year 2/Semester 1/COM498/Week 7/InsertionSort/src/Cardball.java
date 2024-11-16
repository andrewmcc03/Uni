public class Cardball {
   private static final int NUMCARDS = 5;
   private Card[] player1 = new Card[NUMCARDS];
   private Card[] player2 = new Card[NUMCARDS];
   private int score_p1 = 0, score_p2 = 0;

   public Cardball() {
      Deck deck = new Deck();

      for (int i = 0; i < NUMCARDS; i++) {
         this.player1[i] = deck.deal();
         this.player2[i] = deck.deal();
      }

      sort(player1);
      sort(player2);
   }

   private static <T extends Comparable <T>> void sort(T[] arr) {
      T nextToInsert;
      int index;

      for (int i = 1; i < arr.length; i++) {
         nextToInsert = arr[i];

         index = i - 1;
         while (index >= 0 && arr[index].compareTo(nextToInsert) > 0) {
            arr[index + 1] = arr[index];
            index--;
         }

         arr[index + 1] = nextToInsert;
      }
   }

   public static void main(String[] args) {
      Cardball game = new Cardball();
      int ns = 0;

      for (int i = NUMCARDS - 1; i >= 0; i--) {
         System.out.println("Player 1: " + game.player1[i]);
         System.out.println("Player 2: " + game.player2[i]);

         if (game.player1[i].compareTo(game.player2[i]) > 0) {
            System.out.println("GOALASO to Player 1!\n");
            game.score_p1++;
         } else if (game.player1[i].compareTo(game.player2[i]) < 0) {
               System.out.println("GOALASO to Player 2!\n");
               game.score_p2++;
         }
         else {
            System.out.println("No score.\n");
            ns++;
         }
      }

      System.out.println("\nFINAL SCORE:");
      System.out.println("=============");
      System.out.println("Player 1:\t" + game.score_p1);
      System.out.println("Player 2:\t" + game.score_p2);
      System.out.println("\nNo score:\t" + ns);
   }
}