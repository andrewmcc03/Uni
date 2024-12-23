import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.Scanner;

public class Make15 {

   // Initialise deck, card hand and score variables
   private List<Card> playerHand = new ArrayList<>();
   private Deck deck = new Deck();
   private int score = 0;

   Random random = new Random(); // For random number/value generation
   Scanner input = new Scanner(System.in); // For receiving input from user

   // Main game class constructor
   public Make15() {

      // Deal initial 5 cards to player
      for (int i = 0; i < 5; i++) {
         playerHand.add(deck.dealCard());
      }
   }

   // Method to display the player's hand, the computer's card and the current score for the round
   public static void displayRound(List hand, Card computerCard, int score) {
      // TEMP FOR TESTING
      //System.out.println("\n**Display Type: " + type);

      // Output current player score
      System.out.println("\n\n[  Current score:  " + score + "  ]\n");

      // Output current (randomised) player hand
      System.out.println("\nYour Hand:\t\t\t\t" + hand);

      // Output current (randomised) computer/opponent card
      System.out.println("\nComputer's card:\t\t" + computerCard);
   }

   public void play() {

      // Flag used to determine end of game - necessary as (in certain areas) a break only exits inner loop, and return terminates the whole program
      boolean GAMEOVER = false;

      // WHILE NOT GAMEOVER - while the game isn't over
      while (!GAMEOVER) {
         // Checks if the deck or player's hand is empty before continuing
         if (deck.isEmpty()) {
            System.out.println("\nThe deck is empty. GAME OVER!");
            break;
         }
         if (playerHand.isEmpty()) {
            System.out.println("\nYour hand is empty. GAME OVER!");
            break;
         }

         Card comCard = deck.dealCard(); // Creating computer's (opponent's) card
         displayRound(playerHand, comCard, score);
         //displayRound(playerHand, comCard, "1 - WHILE !GAMEOVER loop");

         boolean validMove = false;
         while (!validMove) {
            System.out.println("\n==================================");
            System.out.print("Choose a card to play (1 to " + playerHand.size() + "): ");
            int choice = input.nextInt() - 1;

            // Check IF choice is between 1-5
            if (choice >= 0 && choice < playerHand.size()) {
               // Get card at choice position
               Card chosenCard = playerHand.get(choice);

               // Check IF chosen card value and computer's card value equal 15
               if (chosenCard.getRankValue() + comCard.getRankValue() == 15) {
                  System.out.println("\nYOU MADE 15! +1 POINT scored.");
                  score++;

                  if (deck.isEmpty()) {
                     playerHand.set(choice, null);
                  }
                  else {
                     playerHand.set(choice, deck.dealCard());
                  }

                  validMove = true;
               }
               else if (chosenCard.getSuit().equals((comCard.getSuit()))) {
                  System.out.println("\nSame suits have been played by both players. NO POINTS scored.");

                  if (deck.isEmpty()) {
                     playerHand.set(choice, null);
                  }
                  else {
                     playerHand.set(choice, deck.dealCard());
                  }

                  validMove = true;
               }
               // Invalid move
               else if (!validMovesLeft(comCard)) { // Checks IF another move is possible
                  System.out.println("\nInvalid move. No valid moves left. GAME OVER!");
                  GAMEOVER = true; // Exit outer loop ("while (!GAMEOVER)")
                  break; // Exit inner loop ("while (!validMove)")
               }
               // Move is possible - prompts to try again
               else {
                  System.out.println("\nInvalid move. Try again.");

                  displayRound(playerHand, comCard, score);
                  //displayRound(playerHand, comCard, "2 - Invalid move");
               }
            }
            // Invalid choice
            else {
               System.out.println("\nInvalid choice: Your input must be between 1-" + playerHand.size() + ".");

               displayRound(playerHand, comCard, score);
               //displayRound(playerHand, comCard, "3 - Invalid choice");
            }
         }
      }

      // Output the final score once no moves are available to the player
      System.out.println("\n---------------------------");
      System.out.println("Final score:\t\t\t" + score);
      System.out.println("---------------------------");

      input.close(); // End scanner input
   }

   // Method for checking if there are any valid moves left
   private boolean validMovesLeft(Card computerCard) {
      for (Card card : playerHand) {
         if (card != null && makes15(card, computerCard)) {
            return true;
         }
      }
      return false;
   }

   private boolean makes15(Card playerCard, Card computerCard) {
      // Return TRUE IF the rank value of both player and computer cards add up to 15 OR IF the player card suit is equal to the computer's card suit
      return playerCard.getRankValue() + computerCard.getRankValue() == 15 || playerCard.getSuit().equals(computerCard.getSuit());
   }


   public static void main(String[] args) {

      System.out.println("\n-------------------------------------------");
      System.out.println("|  =  =  =  Welcome to Make 15!  =  =  =  |");
      System.out.println("-------------------------------------------");
//      System.out.println("|                  RULES                   ");
//      System.out.println("-------------------------------------------");
//      System.out.println("");

      // Create new game
      Make15 game = new Make15();

      // Call method to play game
      game.play();
   }
}