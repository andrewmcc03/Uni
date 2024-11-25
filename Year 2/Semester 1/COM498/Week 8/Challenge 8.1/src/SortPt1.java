//import java.util.Arrays;
//import java.util.Random;
//
//public class Sort {
//
//   public static int numComparisons = 0, numSwaps = 0, numUpdates = 0;
//
//   public static int[] randomArray(int n) {
//      Random rand = new Random();
//      int[] arr = new int[n];
//
//      for (int i = 0; i < n; i++) {
//         arr[i] = rand.nextInt(100);
//      }
//      return arr;
//   }
//
//
//   // Challenge 8.1
//
//   // Quick Sort
//   private static void swap(int[] arr, int first, int second) {
//      int temp = arr[first];
//      arr[first] = arr[second];
//      arr[second] = temp;
//      numUpdates += 2;
//   }
//
//   private static void orderThree(int[] arr, int first, int second, int third) {
//      if (arr[first] > arr[second]) {
//         swap(arr, first, second);
//      }
//      if (arr[first] > arr[third]) {
//         swap(arr, first, third);
//      }
//      if (arr[second] > arr[third]) {
//         swap(arr, second, third);
//      }
//      numComparisons += 3;
//   }
//   public static void quickSort(int[] arr) {
//      quickSort_r(arr, 0, arr.length - 1);
//   }
//
//   public static void quickSort_r(int[] arr, int first, int last) {
//      int middle = (first + last) / 2;
//      orderThree(arr, first, middle, last);
//      swap(arr, middle, last);
//
//      int pivot = arr[last];
//      int indexFromLeft = first, indexFromRight = last;
//
//      while (indexFromLeft <= indexFromRight) {
//         numComparisons++;
//         while (arr[indexFromLeft] < pivot) {
//            indexFromLeft++;
//            numComparisons++;
//         }
//         numComparisons++;
//         while (arr[indexFromRight] > pivot) {
//            indexFromRight--;
//            numComparisons++;
//         }
//
//         if (indexFromLeft <= indexFromRight) {
//            swap(arr, indexFromLeft++, indexFromRight--);
//         }
//      }
//
//      if (first < indexFromRight) {
//         quickSort_r(arr, first, indexFromRight);
//      }
//      if (indexFromLeft < last) {
//         quickSort_r(arr, indexFromLeft, last);
//      }
//   }
//
//
//   public static void main(String[] args) {
//
//      long startTime, endTime;
//      int[] arraySizes = {100, 200, 400, 800, 1600, 3200, 6400};
//
//      System.out.println("Array Size\t\t\tSort Time");
//      System.out.println("=============================");
//
//      for (int arraySize : arraySizes) {
//
//         // Time calc
//         startTime = System.currentTimeMillis();
//         for (int i = 0; i < 1000; i++) {
//            int[] arr = randomArray(arraySize);
//            quickSort_r(arr, 0, arr.length - 1);
//         }
//         endTime = System.currentTimeMillis();
//
//         long totalTime = endTime - startTime;
//
//         System.out.printf("%-20d%-7d%-13s\n", arraySize, totalTime, "ms");
//      }
//   }
//}