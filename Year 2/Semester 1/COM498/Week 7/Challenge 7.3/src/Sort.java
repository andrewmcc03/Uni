import java.util.Arrays;
import java.util.Random;

public class Sort {

   public static int numComparisons = 0, numSwaps = 0, numUpdates = 0;

   public static int[] randomArray(int n) {
      Random rand = new Random();
      int[] arr = new int[n];

      for (int i = 0; i < n; i++) {
         arr[i] = rand.nextInt(100);
      }
      return arr;
   }

   // Normal merge methods - passing as parameter
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
         if (arr[pos1] <= arr[pos2]) {
            temp[index++] = arr[pos1++];
         }
         else {
            temp[index++] = arr[pos2++];
         }
      }

      while (pos1 <= mid) {
         temp[index++] = arr[pos1++];
      }
      while (pos2 <= last) {
         temp[index++] = arr[pos2++];
      }

      for (int i = first; i <= last; i++) {
         arr[i] = temp[i];
      }
   }


   // Temp merge methods
   public static void mergeSortTemp(int[] arr) {

      int[] temp = new int[arr.length];
      mergeSort_rTemp(arr, 0, arr.length - 1);
   }

   private static void mergeSort_rTemp(int[] arr, int first, int last) {
      if (first < last) {
         int mid = (first + last) / 2;
         mergeSort_rTemp(arr, first, mid);
         mergeSort_rTemp(arr, mid + 1, last);
         mergeTemp(arr, first, mid, last); // This method now creates new temp array
      }
   }

   private static void mergeTemp(int[] arr, int first, int mid, int last) { // Removed temp array parameter
      int pos1 = first, pos2 = mid + 1, index = first;

      int[] temp = new int[arr.length];   // Creating new temp array each call

      while (pos1 <= mid && pos2 <= last) {
         if (arr[pos1] <= arr[pos2]) {
            temp[index++] = arr[pos1++];
         }
         else {
            temp[index++] = arr[pos2++];
         }
      }

      while (pos1 <= mid) {
         temp[index++] = arr[pos1++];
      }
      while (pos2 <= last) {
         temp[index++] = arr[pos2++];
      }

      for (int i = first; i <= last; i++) {
         arr[i] = temp[i];
      }
   }


   public static void main(String[] args) {

      long startTime, endTime, totalTime;
      int[] arraySizes = {5000, 10000};

      for (int arraySize : arraySizes) {
         System.out.println("\nArray size: " + arraySize);

         // i) With the temp array passed as a parameter (as in our implementation)
         startTime = System.currentTimeMillis();
         for (int i = 0; i < 1000; i++) {
            int[] arr = randomArray(arraySize);
            mergeSort(arr); // Using original mergeSort method - passing temp array as parameter
         }
         endTime = System.currentTimeMillis();
         totalTime = endTime - startTime;
         System.out.println("Temporary array passed as a parameter:\t\t" + totalTime + "ms");


         // ii) With the temp array generated anew each time the merge() method is
         //     called. Remember to remove temp from all parameter lists for this test.
         startTime = System.currentTimeMillis();
         for (int i = 0; i < 1000; i++) {
            int[] arr = randomArray(arraySize);
            mergeSortTemp(arr); // Using mergeSort method without temp array parameter
         }
         endTime = System.currentTimeMillis();
         totalTime = endTime - startTime;
         System.out.println("Temporary array generated in merge method:\t" + totalTime + "ms");
      }
   }
}