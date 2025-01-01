import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

/*
Coursework 2 - Make 15 Game program
By Andrew McCormick (B00988875)
 */


/*
Current issues:

- Minor issues to fix with the game replay feature - functionally seems sound from several tests

 */

public class Make15 {

   // Initialise deck, card hand and score variables, along with an array list for storing high scores and one for storing game logs (i.e., moves, events) for replay function
   private List<Card> playerHand = new ArrayList<>();
   private static List<Score> highScores = new ArrayList<>();
   private Deck deck = new Deck();
   private int score = 0;
   private String playerName;
   private List<String> gameLog;

   Scanner input = new Scanner(System.in); // For receiving input from user

   // Main game class constructor
   private Make15() {
      // Initialise gameLog for replay function later
      gameLog = new ArrayList<>();

      // Deal initial 5 cards to player
      for (int i = 0; i < 5; i++) {
         playerHand.add(deck.dealCard());
      }
   }

   // Method to display the player's hand, the computer's card and the current score for the round
   private static void displayRound(List hand, Card computerCard, int score) {
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
      System.out.println("\n-------\033[1m High Scores \033[0m-------");

      if (highScores.isEmpty()) {
         System.out.println("\nNo high scores available.\n");
      }
      else {
         for (int i = 0; i < highScores.size(); i++) {
            System.out.println((i + 1) + ".  " + highScores.get(i));
         }
      }

      System.out.println("---------------------------");
   }

   // Method to check if a score qualifies for high score table
   private void checkHighScore() {
      String name = null;
      // IF score is greater than 0 (at least 1) AND IF there are less than 5 high scores OR player's score is higher than the lowest score in table
      if (score > 0 && (highScores.size() < 5 || score > highScores.get(highScores.size() - 1).getScore())) {
         System.out.println("\nCongrats! You have made it to the High Scores Table!");

         // WHILE loop to validate name is between 3-15 characters
         while (true) {
            System.out.println("\n==================================");
            System.out.print("Enter your name: ");

            name = input.nextLine().trim();
            if (name.length() >= 3 && name.length() <= 15) {
               break; // Exit loop if name is valid num of chars
            }
            else {
               System.out.println("\nInvalid name. Please enter a name between 3 and 15 characters.");
            }
         }

         // Create new score
         Score newScore = new Score(name, score);
         highScores.add(newScore);
         selectionSort(); // Selection sort to sort high scores in descending order

         // IF the list length is greater than 5, remove the lowest score
         if (highScores.size() > 5) {
            highScores.remove(highScores.size() - 1);
         }

         System.out.println("\n** New High Score for '\033[1m" + name + "\033[0m' added! **"); // Output message for new high scorer
      }
      else {
         System.out.println("\nUnfortunately, you have not qualified for the High Score Table. Better luck next time!"); // NOTE: To qualify, player must achieve at least a score of 1
      }

      playerName = name; // Set global playerName to high score name
   }

   // Method for displaying the game replay after a game completes
   private void displayReplay() {
      // Check if there's a name present (needs high score for this to be true)
      if (playerName == null) {
         System.out.print("\033[1m\u001B[4m\n\n = = = = = = GAME REPLAY = = = = = = \u001B[0m\033[0m");
      }
      else {
         System.out.print("\033[1m\u001B[4m\n\n= = = = GAME REPLAY for " + playerName + " = = = =\u001B[0m\033[0m");
      }

      // FOR each entry in the game log
      for (String entry : gameLog) {
         System.out.println(entry + "\n-------------------------------------------");
      }

      System.out.println();
   }

   // Method for starting a new game
   private void play() {
      // Flag used to determine end of game - necessary as (in certain areas) a break only exits inner loop, and return terminates the whole program
      boolean GAMEOVER = false;
      // Counter for round number
      int round = 1;

      // WHILE NOT GAMEOVER - while the game isn't over
      while (!GAMEOVER) {

         // REPLAY FUNCTION: Round counter
         String roundHeader = String.format("\n\n%-14s%-7s%-12d%-1s", "----", "Round", round++, "----");
         gameLog.add(roundHeader);

         // Checks if the deck or player's hand is empty before continuing
         if (deck.isEmpty()) {
            System.out.println("\nThe deck is empty. GAME OVER!");
            gameLog.add("Deck empty - GAME OVER! Final Score: " + score); // REPLAY FUNCTION: Game Over - Deck empty
            GAMEOVER = true; // End game, exiting the loop
            break;
         }
         if (playerHand.isEmpty()) {
            System.out.println("\nYour hand is empty. GAME OVER!");
            gameLog.add("Hand empty - GAME OVER! Final Score: " + score); // REPLAY FUNCTION: Game Over - Hand empty
            GAMEOVER = true; // End game, exiting the loop
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
               System.out.println("\nInvalid choice: Your input must be between 1-" + playerHand.size() + ".");
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

                  // REPLAY FUNCTION: Made 15
                  gameLog.add("Player's hand:\t\t\t" + playerHand +
                        "\nComputer's card:\t\t" + comCard +
                        "\n\nPlayer played:\t\t\t" + chosenCard +
                        "\n\n_____________________________________" +
                        "\nOutcome:\t\tMade 15! +1 point");

                  // Checking for picture cards in current hand and adding to new list
                  List<Integer> pictureCardPositions = new ArrayList<>();
                  for (int i = 0; i < playerHand.size(); i++) {
                     if (i != choice) {
                        Card card = playerHand.get(i);
                        if (card != null && (card.getRank().equals("Jack") || card.getRank().equals("King") || card.getRank().equals("Queen"))) {
                           pictureCardPositions.add(i);
                        }
                     }
                  }
                  boolean pictureCardsFound = !pictureCardPositions.isEmpty();

                  // Deal new card at choice position AFTER checking the current round's cards
                  if (deck.isEmpty()) {
                     playerHand.set(choice, null);
                  }
                  else {
                     playerHand.set(choice, deck.dealCard());
                  }

                  // IF there are picture cards, prompt player with option to replace one with another from the deck (Level 5)
                  if (pictureCardsFound)
                  {
                     System.out.println("\nYou have the following picture cards in your hand:\n");

                     // FOR each card in the array of picture cards
                     for (int position : pictureCardPositions) {
                        System.out.println((position + 1) + " - " + playerHand.get(position));
                     }

                     // FOR each picture card, ask if player wants to replace card or not
                     for (int position : pictureCardPositions) {
                        boolean validResponse = false;
                        while (!validResponse) {
                           System.out.println("\n==============================================================================================");
                           System.out.print("Would you like to replace the picture card '\033[1m" + playerHand.get(position) + "\033[0m' (yes/no)? ");
                           String responseInput = input.nextLine().toLowerCase();

                           if (responseInput.equals("no") || responseInput.equals("n")) {
                              gameLog.add("\nReplacement card DECLINED: '\033[1m" + playerHand.get(position) + "\033[0m'"); // REPLAY FUNCTION: Replacement Card - Declined

                              validResponse = true;
                           }
                           else if (responseInput.equals("yes") || responseInput.equals("y")) {
                              Card previousCard = playerHand.get(position); // Retrieve card-to-be-replaced before dealing new replacement card in its place - used for output later on

                              // Deal new replacement card at position
                              if (deck.isEmpty()) {
                                 playerHand.set(position, null);
                              }
                              else {
                                 playerHand.set(position, deck.dealCard());
                              }

                              System.out.println("\nThe \033[1m" + previousCard + "\033[0m has been replaced with a new card from the deck.");

                              gameLog.add("\nReplacement card ACCEPTED: '\033[1m" + previousCard + "\033[0m' REPLACED by the '\033[1m" + playerHand.get(position) + "\033[0m'"); // REPLAY FUNCTION: Replacement Card - Accepted

                              validResponse = true;
                           }

                           // IF response is NOT valid
                           if (!validResponse) {
                              System.out.println("\nInvalid choice. Please enter either 'yes/y' or 'no/n'.");
                           }
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

                  // REPLAY FUNCTION: Same Suits
                  gameLog.add("Player's hand:\t\t\t" + playerHand +
                        "\nComputer's card:\t\t" + comCard +
                        "\n\nPlayer played:\t\t\t" + chosenCard +
                        "\n\n_____________________________________" +
                        "\nOutcome:\t\tSame suits. No points");

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

                  // REPLAY FUNCTION: Game Over - No valid moves left
                  gameLog.add("No valid moves left. GAME OVER!");

                  GAMEOVER = true; // Exit outer loop ("while (!GAMEOVER)")
                  break; // Exit inner loop ("while (!validMove)")
               }
               // Move is possible - prompts to try again (NOTE: not entirely sure if this is the intended way it should work at this point in the code - could change this to allow the player to move again)
               else {
                  System.out.println("\nInvalid move. GAME OVER!");

                  // REPLAY FUNCTION: Game Over - Invalid move played
                  gameLog.add("Invalid move. GAME OVER!");

                  GAMEOVER = true; // Exit outer loop ("while (!GAMEOVER)")
                  break; // Exit inner loop ("while (!validMove)")
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
      System.out.printf("%-3s%-25s%-4d|", "|","Final Score:", score);
      System.out.println("\n---------------------------------");

      // IF GAMEOVER = true, check if player made a high score
      if (GAMEOVER) {
         checkHighScore();
         displayHighScores();

         // WHILE loop for validating user answer
         while (true) {
            System.out.println("\n========================================================");
            System.out.print("Would you like to view a replay of the game (yes/no)? ");
            String replayChoice = input.nextLine().trim().toLowerCase();

            // IF answer is yes
            if (replayChoice.equals("yes") || replayChoice.equals("y")) {
               // Call method to show replay for the (now ended game)
               displayReplay();

               System.out.print("\033[1m\u001B[4m = = = = =  END OF REPLAY  = = = = = \u001B[0m\033[0m\n\n");

               break;
            }
            // ELSE IF answer is no
            else if (replayChoice.equals("no") || replayChoice.equals("n")) {
               System.out.println("\nReturning to main menu...\n");

               // Sleep for 0.5 seconds
               try {
                  Thread.sleep(500);
               } catch (InterruptedException e) {
                  e.printStackTrace();
               }

               break;
            }
            // ELSE invalid choice
            else {
               System.out.println("\nInvalid choice. Please enter either 'yes/y' or 'no/n'.");
            }
         }
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
         System.out.println("|  =  =  =  \033[1mWelcome to Make 15!\033[0m  =  =  =  |");
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
               System.out.println();

               break;

            // Option 3 - Rules and Info
            case 3:
               System.out.println("\n-------------------------------------------");
               System.out.println("|          \033[1mRules and Information\033[0m          |");
               System.out.println("-------------------------------------------\n");
               System.out.println("\u001B[1mWhat is Make 15?\u001B[0m\n" +
                                  "- Make 15 is a one-player card game played against the computer.\n" +
                                  "- The game uses a standard shuffled deck of playing cards from which the player is dealt a hand of 5 cards.\n");
               System.out.println("\u001B[1mGeneral Information & How to Play\u001B[0m\n" +
                     "- In this game, the rank value of the picture cards (Jack, Queen, and King) is 11 and the value of the Ace is 12.\n" +
                     "- If the player is successful, a point is scored, and the player’s card is replaced with one dealt from the deck.\n" +
                     "- If a player can Make 15, they can also opt, in the same turn, to play any picture cards in their hand to exchange them for replacement cards dealt from the deck.\n" +
                     "- If the player cannot Make 15, they can play a card of the same suit to allow the game to continue, but no point is scored.\n" +
                     "- The game ends when a player is forced to play a card that does not Make 15 and is not of the same suit or the deck is empty.");
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