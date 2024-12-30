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
      return name + ":\t\t" + score;
   }

   @Override
   public int compareTo(Score other) {
      return Integer.compare(this.score, other.score);
   }
}