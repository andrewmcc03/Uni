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


   // Challenge 8.1

   // Insertion Sort
   public static void insertionSort(int[] arr) {
      int nextToInsert, index;

      for (int i = 1; i < arr.length; i++) {
         nextToInsert = arr[i];

         index = i - 1;
         numComparisons++;
         while (index >= 0 && arr[index] > nextToInsert) {
            arr[index + 1] = arr[index];
            numUpdates++;
            index--;
            numComparisons++;
         }

         arr[index + 1] = nextToInsert;
         numUpdates++;
      }
   }

   // Recursive version of above method ^^
   public static void insertionSort_r(int[] arr, int firstPos, int lastPos) {
      int nextToInsert, index;

      numComparisons++;
      if (firstPos < lastPos) {
         insertionSort_r(arr, firstPos, lastPos - 1);
         nextToInsert = arr[lastPos];

         index = lastPos - 1;
         numComparisons++;
         while (index >= 0 && arr[index] > nextToInsert) {
            arr[index + 1] = arr[index];
            numUpdates++;
            index--;
            numComparisons++;
         }

         arr[index + 1] = nextToInsert;
         numUpdates++;
      }
   }

   // Quick Sort
   private static void swap(int[] arr, int first, int second) {
      int temp = arr[first];
      arr[first] = arr[second];
      arr[second] = temp;
      numUpdates += 2;
   }

   private static void orderThree(int[] arr, int first, int second, int third) {
      if (arr[first] > arr[second]) {
         swap(arr, first, second);
      }
      if (arr[first] > arr[third]) {
         swap(arr, first, third);
      }
      if (arr[second] > arr[third]) {
         swap(arr, second, third);
      }
      numComparisons += 3;
   }
   public static void quickSort(int[] arr) {
      quickSort_r(arr, 0, arr.length - 1);
   }

   public static void quickSort_r(int[] arr, int first, int last) {
      // Check sub-array <= 100 - insertion sort if true
      if (last - first + 1 <= 100) {
         insertionSort_r(arr, first, last);
         return;
      }

      int middle = (first + last) / 2;
      orderThree(arr, first, middle, last);
      swap(arr, middle, last);

      int pivot = arr[last];
      int indexFromLeft = first, indexFromRight = last;

      while (indexFromLeft <= indexFromRight) {
         numComparisons++;
         while (arr[indexFromLeft] < pivot) {
            indexFromLeft++;
            numComparisons++;
         }
         numComparisons++;
         while (arr[indexFromRight] > pivot) {
            indexFromRight--;
            numComparisons++;
         }

         if (indexFromLeft <= indexFromRight) {
            swap(arr, indexFromLeft++, indexFromRight--);
         }
      }

      if (first < indexFromRight) {
         quickSort_r(arr, first, indexFromRight);
      }
      if (indexFromLeft < last) {
         quickSort_r(arr, indexFromLeft, last);
      }
   }


   public static void main(String[] args) {

      long startTime, endTime, quickSortTime, recQuickSortTime;
      //int[] arraySizes = {100, 200, 400, 800, 1600, 3200, 6400};
      int[] arraySizes = {10000, 50000, 100000};

      for (int arraySize : arraySizes) {

         // Time calc for quick sort
         startTime = System.currentTimeMillis();
         for (int i = 0; i < 1000; i++) {
            int[] arr = randomArray(arraySize);
            quickSort(arr);
         }
         endTime = System.currentTimeMillis();

         quickSortTime = endTime - startTime;

         // Time calc for recursive quick sort
         startTime = System.currentTimeMillis();
         for (int i = 0; i < 1000; i++) {
            int[] arr = randomArray(arraySize);
            quickSort_r(arr, 0, arr.length - 1);
         }
         endTime = System.currentTimeMillis();

         recQuickSortTime = endTime - startTime;

         System.out.println("\nArray size: " + arraySize);
         System.out.println("Pure Quick Sort: " + quickSortTime + "ms");
         System.out.println("Using Insertion Sort for sub-arrays <= 100: " + recQuickSortTime + "ms");

         // NOTE: Unsure why the times aren't vastly different as shown in example
         //       The code seems correct, but I can't seem to figure out which part is causing this
      }
   }
}