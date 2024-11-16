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


   // Challenge 7.3
   public static void mergeSort(int[] arr) {

      int[] temp = new int[arr.length];
      mergeSort_r(arr, temp, 0, arr.length - 1);
   }

   private static void mergeSort_r(int[] arr, int[] temp, int first, int last) {
      if (first < last) {
         int mid = (first + last) / 2;
         mergeSort_r(arr, temp, first, mid);
         mergeSort_r(arr, temp, mid + 1, last);
         merge(arr, temp, first, mid, last);
      }
   }

   private static void merge(int[] arr, int[] temp, int first, int mid, int last) {
      int pos1 = first, pos2 = mid + 1, index = first;

      // NO LONGER NEEDED AS WE NOW USE mergeSort FOR THIS
      //int[] temp = new int[arr.length];

      while (pos1 <= mid && pos2 <= last) {
         numComparisons++;
         if (arr[pos1] <= arr[pos2]) {
            temp[index++] = arr[pos1++];
         }
         else {
            temp[index++] = arr[pos2++];
         }
         numUpdates++;
      }

      numUpdates += mid - pos1 + 1;
      while (pos1 <= mid) {
         temp[index++] = arr[pos1++];
      }
      numUpdates += last - pos2 + 1;
      while (pos2 <= last) {
         temp[index++] = arr[pos2++];
      }

      for (int i = first; i <= last; i++) {
         arr[i] = temp[i];
      }
      numUpdates += last - first + 1;
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
            mergeSort(arr);
         }
         endTime = System.currentTimeMillis();

         long totalTime = endTime - startTime;

         System.out.printf("%-20d%-7d%-13s\n", arraySize, totalTime, "ms");
      }
   }
}