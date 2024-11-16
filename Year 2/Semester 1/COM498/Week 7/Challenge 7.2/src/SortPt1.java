import java.util.Arrays;
import java.util.Random;

public class SortPt1 {

   public static int numComparisons = 0, numSwaps = 0, numUpdates = 0;

   public static int[] randomArray(int n) {
      Random rand = new Random();
      int[] arr = new int[n];

      for (int i = 0; i < n; i++) {
         arr[i] = rand.nextInt(100);
      }
      return arr;
   }


   // Challenge 7.2
   private static void shellSort(int[] arr) {
      int temp, index;

      for (int gap = arr.length / 2; gap > 0; gap /= 2) {
         //System.out.println("=========\nGap is " + gap + "\n");
         for (int i = gap; i < arr.length; i++) {
            temp = arr[i];
            numComparisons++;
            for (index = i; index >= gap && arr[index - gap] > temp; index -= gap) {
               arr[index] = arr[index - gap];
               numComparisons++;
               numUpdates++;
            }
            arr[index] = temp;
            numUpdates++;

            //System.out.println("Pass:\t\t" + Arrays.toString(arr));
         }
      }
   }

   public static void main(String[] args) {

      long startTime, endTime;
      int[] arraySizes = {100, 200, 400, 800, 1600, 3200, 6400};

      System.out.println("Array Size\t\t\tSort Time");
      System.out.println("=============================");

      for (int arraySize : arraySizes) {

         // Time calc
         startTime = System.currentTimeMillis();
         for (int i = 0; i < 1000; i++) {
            int[] arr = randomArray(arraySize);
            shellSort(arr);
         }
         endTime = System.currentTimeMillis();

         long totalTime = endTime - startTime;

         System.out.printf("%-20d%-7d%-13s\n", arraySize, totalTime, "ms");
      }
   }
}