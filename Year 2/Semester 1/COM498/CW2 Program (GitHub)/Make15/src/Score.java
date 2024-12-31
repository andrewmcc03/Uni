public class Score implements Comparable<Score> {

   private String name;
   private int score;

   public Score(String name, int score) {
      this.name = name;
      this.score = score;
   }

   public String getName() {
      return name;
   }

   public int getScore() {
      return score;
   }

   @Override
   public String toString() {
      return String.format("%-17s: %2d", name, score);
   }

   @Override
   public int compareTo(Score other) {
      return Integer.compare(this.score, other.score);
   }
}