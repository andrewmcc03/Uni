import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

/*
Coursework 2 - Make 15 Game program
By Andrew McCormick (B00988875)
 */


/*
Current issues:

- No issues ATM - need to start implementing replay function

 */

public class Make15 {

   // Initialise deck, card hand and score variables, along with an array list for storing high scores
   private List<Card> playerHand = new ArrayList<>();
   private static List<Score> highScores = new ArrayList<>();
   private Deck deck = new Deck();
   private int score = 0;

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
      // Output current player score
      System.out.println("\n\n[  Current score:  " + score + "  ]\n");

      // Output current (randomised) player hand
      System.out.println("\nYour Hand:\t\t\t\t" + hand);

      // Output current (randomised) computer/opponent card
      System.out.println("\nComputer's card:\t\t" + computerCard);
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

   // Method to check if choice makes 15
   private boolean makes15(Card playerCard, Card computerCard) {
      // Return TRUE IF the rank value of both player and computer cards add up to 15
      return playerCard.getRankValue() + computerCard.getRankValue() == 15;
   }

   // Selection sort method to sort high scores in descending order
   private void selectionSort() {
      for (int i = 0; i < highScores.size() - 1; i++) {
         int maxIndex = i;
         for (int j = i + 1; j < highScores.size(); j++) {
            if (highScores.get(j).getScore() > highScores.get(maxIndex).getScore()) {
               maxIndex = j;
            }
         }

         // Swap max score found with the first unsorted position
         Score temp = highScores.get(maxIndex);
         highScores.set(maxIndex, highScores.get(i));
         highScores.set(i, temp);
      }
   }

   // Method for displaying ordered high score table
   private static void displayHighScores() {
      System.out.println("\n------ High Scores ------");

      if (highScores.isEmpty()) {
         System.out.println("\nNo high scores available.\n");
      }
      else {
         for (int i = 0; i < highScores.size(); i++) {
            System.out.println((i + 1) + ". " + highScores.get(i));
         }
      }

      System.out.println("-------------------------");
   }

   // Method to check if a score qualifies for high score table
   private void checkHighScore() {
      // IF there's less than 5 high scores OR player's score is higher than the lowest score in table
      if (score > 0 && (highScores.size() < 5 || score > highScores.get(highScores.size() - 1).getScore())) {
         System.out.println("\nCongrats! You have made it to the High Scores Table!");

         String playerName;
         while (true) {
            System.out.println("\n===================");
            System.out.print("Enter your name: ");

            playerName = input.nextLine().trim();
            if (playerName.length() >= 3 && playerName.length() <= 15) {
               break; // Exit loop if name is valid num of chars
            }
            else {
               System.out.println("\nInvalid name. Please enter a name between 3 and 15 characters.");
            }
         }

         // Create new score
         Score newScore = new Score(playerName, score);
         highScores.add(newScore);
         selectionSort(); // Selection sort to sort high scores in descending order

         // IF the list length is greater than 5, remove the lowest score
         if (highScores.size() > 5) {
            highScores.remove(highScores.size() - 1);
         }

         System.out.println("\n** New High Score for '" + playerName + "' added! **"); // Output message for new high scorer
      }
      else {
         System.out.println("\nUnfortunately, you have not qualified for the High Score Table. Better luck next time!");
      }
   }


   // Method for starting a new game
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

         int choice; // Choice variable - defined outside loop to allow access

         boolean validMove = false;
         // WHILE NOT a valid move, keep looping
         while (!validMove) {
            System.out.println("\n==================================");
            System.out.print("Choose a card to play (1 to " + playerHand.size() + "): ");
            String choiceInput = input.nextLine();

            // Try/Catch to ensure correct format is entered (i.e., no letters, special characters etc.)
            try {
               choice = Integer.parseInt(choiceInput) - 1; // NOTE: -1 here is better for using the choice for getting index position later on - this is not a mistake for this instance
            }
            catch (NumberFormatException e) {
               System.out.println("\nInvalid choice. Try again.");
               displayRound(playerHand, comCard, score);

               continue; // Allows program to continue after error handling
            }

            // Check IF choice is between 1-5
            if (choice >= 0 && choice < playerHand.size()) {

               Card chosenCard = playerHand.get(choice); // Get card at choice position

               // Check IF chosen card value and computer's card value equal 15
               if (makes15(chosenCard, comCard)) {
                  System.out.println("\nYOU MADE 15! +1 POINT scored.");
                  score++;

                  // Checking for picture cards and adding to new list
                  boolean pictureCardsFound = false;
                  List<Integer> pictureCardPositions = new ArrayList<>();
                  for (int i = 0; i < playerHand.size(); i++) {
                     Card card = playerHand.get(i);
                     if (card != null && (card.getRank().equals("Jack") || card.getRank().equals("King") || card.getRank().equals("Queen"))) {
                        pictureCardPositions.add(i);
                        pictureCardsFound = true;
                     }
                  }

                  // Deal new card at choice position AFTER checking the current round's cards
                  if (deck.isEmpty()) {
                     playerHand.set(choice, null);
                  }
                  else {
                     playerHand.set(choice, deck.dealCard());
                  }

                  // IF there are picture cards, prompt player with option to replace one with another from the deck (Level 5)
                  if (pictureCardsFound && !(chosenCard.getRank().equals("Jack") || chosenCard.getRank().equals("King") || chosenCard.getRank().equals("Queen"))) {
                     boolean validResponse = false;
                     while (!validResponse) {
                        System.out.println("\nYou have the following picture cards in your hand:\n");

                        for (int position : pictureCardPositions) {
                           System.out.println((position + 1) + " - " + playerHand.get(position));
                        }

                        System.out.println("\nType 'no' or 'n' to decline a replacement card and continue as normal.");

                        int[] availablePositionsArr = new int[pictureCardPositions.size()];
                        String availablePositions = "";
                        for (int i = 0; i < pictureCardPositions.size(); i++) {
                           if (i > 0) {
                              availablePositions += ", ";
                           }
                           availablePositions += (pictureCardPositions.get(i) + 1);
                           availablePositionsArr[i] = (pictureCardPositions.get(i) + 1);
                        }

                        System.out.println("\n==============================================================================================");
                        System.out.print("Would you like to replace one of the current picture cards in your hand? If so, which card? ");
                        String responseInput = input.nextLine();
                        int response = -1;

                        if (responseInput.equals("no") || responseInput.equals("n")) {
                           validResponse = true;
                        }
                        else {
                           try {
                              response = Integer.parseInt(responseInput); // Tries to parse String input to int
                           }
                           catch (NumberFormatException e) { // Catches any attempt to convert a String with an incorrect format to an integer or a double
                              System.out.println("\nInvalid choice."); // Outputs 'Invalid choice' message
                              continue;
                           }
                        }

                        // Search for position in the array
                        for (int position : availablePositionsArr) {
                           if (position == response) {
                              response -= 1; // Move response value back 1 to align with correct index position in array
                              Card previousCard = playerHand.get(response); // Retrieves card at response position (for output shown further below)

                              // Deal new replacement card at position
                              if (deck.isEmpty()) {
                                 playerHand.set(response, null);
                              }
                              else {
                                 playerHand.set(response, deck.dealCard());
                              }

                              System.out.println("\nThe card '" + previousCard + "' has been replaced with a new card from the deck.");

                              validResponse = true;
                              break;
                           }
                        }

                        // IF response is NOT valid
                        if (!validResponse) {
                           System.out.println("\nInvalid choice. Please see the list below and choose from the following positions: " + availablePositions);
                        }
                     }
                  }
                  // IF there aren't any picture cards...
                  else {
                     // Deals new card for choice position
                     if (deck.isEmpty()) {
                        playerHand.set(choice, null);
                     }
                     else {
                        playerHand.set(choice, deck.dealCard());
                     }
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
               // Move is possible - prompts to try again (NOTE: not entirely sure if this is the intended way it should work at this point in the code)
               else {
                  System.out.println("\nInvalid move. Try again.");

                  displayRound(playerHand, comCard, score);
               }
            }
            // Invalid choice
            else {
               System.out.println("\nInvalid choice: Your input must be between 1-" + playerHand.size() + ".");

               displayRound(playerHand, comCard, score);
            }
         } // while (!validMove)
      } // while (!GAMEOVER)

      // Output the final score once no moves are available to the player
      System.out.println("\n---------------------------------");
      System.out.println("|  Final score:\t\t\t" + score + "\t\t|");
      System.out.println("---------------------------------");

      // IF GAMEOVER = true, check if player made a high score
      if (GAMEOVER) {
         checkHighScore();
         displayHighScores();
      }
   }

   ///

   public static void main(String[] args) {

      Scanner input = new Scanner(System.in); // Scanner for keyboard input

      ///

      int mainMenuChoice = -1;

      while (mainMenuChoice != 0)
      {
         System.out.println("\n-------------------------------------------");
         System.out.println("|  =  =  =  Welcome to Make 15!  =  =  =  |");
         System.out.println("-------------------------------------------");
         System.out.println("1 - Start a New Game");
         System.out.println("2 - High Score Table");
         System.out.println("3 - Rules and Information");
         System.out.println("0 - Exit\n");

         System.out.print("Enter your choice: "); // Prompts user for choice
         String mainMenuChoiceInput = input.nextLine(); // Takes in input as String and gives it a separate variable

         System.out.println();

         try {
            mainMenuChoice = Integer.parseInt(mainMenuChoiceInput); // Tries to parse String input to int
         }
         catch (NumberFormatException e) { // Catches any attempt to convert a String with an incorrect format to an integer or a double
            System.out.println("Invalid choice."); // Outputs 'Invalid choice' message (catch, main menu)
            continue;
         }

         if (mainMenuChoice < 0 || mainMenuChoice > 3) { // If choice is less than 0 or greater than 3 ...
            System.out.println("Invalid choice."); // Outputs 'Invalid choice' message (if, main menu)
            continue;
         }

         // Start of Main Menu switch block
         switch (mainMenuChoice) {
            // Option 1 - Start Game
            case 1:
               System.out.println("\n-------------------------------------------");
               System.out.println("|  =  =  =  Welcome to Make 15!  =  =  =  |");
               System.out.println("-------------------------------------------");

               // Create new game
               Make15 game = new Make15();

               // Display high scores before new game starts
               displayHighScores();

               // Call method to play game
               game.play();

               break;

            // Option 2 - High Score Table
            case 2:
               displayHighScores();

               break;

            // Option 3 - Rules and Info
            case 3:
               System.out.println("\n-------------------------------------------");
               System.out.println("|          Rules and Information          |");
               System.out.println("-------------------------------------------\n");
               System.out.println("Make 15 is a one-player card game played against the computer.\n" +
                                  "The game uses a standard shuffled deck of playing cards from which the player is dealt a hand of 5 cards.\n" +
                                  "In each round of the game, the computer deals a card face-up from the deck and the player attempts to add a card from his hand such that the total rank score of the two cards is 15.\n" +
                                  "In this game, the rank value of the picture cards (Jack, Queen, and King) is 11 and the value of the Ace is 12.\n" +
                                  "If the player is successful, a point is scored, and the player’s card is replaced with one dealt from the deck.\n" +
                                  "If a player can Make 15, they can also opt, in the same turn, to play any picture cards in their hand to exchange them for replacement cards dealt from the deck.\n" +
                                  "If the player cannot Make 15, they can play a card of the same suit to allow the game to continue, but no point is scored.\n" +
                                  "The game ends when a player is forced to play a card that does not Make 15 and is not of the same suit or the deck is empty.");
               System.out.println("\n-------------------------------------------\n");

               break;

            // Option 0 - Exit program
            case 0:
               System.out.println("Exiting...");
               System.exit(0); // Uses code 0 to indicate a normal program termination

               break; // Breaks out of program (System.exit should terminate the program before it reaches this point anyway)
         } // Main Menu switch

      } // while

   } // main

} // class