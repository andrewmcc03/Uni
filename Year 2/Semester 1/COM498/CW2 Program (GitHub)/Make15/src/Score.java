public class Score {
   // Variables to store name and score for use in high score methods
   private String name;
   private int score;

   // Constructor for a new high score
   public Score(String name, int score) {
      this.name = name;
      this.score = score;
   }

   // Method to get the name of a player
   public String getName() {
      return name;
   }

   // Method to get the score of a player
   public int getScore() {
      return score;
   }

   // Method to format and return string of name and score of a player
   @Override
   public String toString() {
      return String.format("%-17s: %2d", name, score);
   }
}