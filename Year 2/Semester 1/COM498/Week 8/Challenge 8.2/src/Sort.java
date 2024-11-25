import java.util.Random;
import java.util.Scanner;

public class Sort {

   public static int[] randomArray(int n) {
      Random rand = new Random();
      int[] arr = new int[n];

      for (int i = 0; i < n; i++) {
         arr[i] = rand.nextInt(100);
      }
      return arr;
   }

   // Case 1 method: Bubble Sort
   public static void bubbleSort(int arr[]) {

      int firstPos = 0, lastPos = arr.length - 1;
      int temp, lastSwapPos;

      while (firstPos < lastPos) {
         lastSwapPos = firstPos;
         for (int j = firstPos; j < lastPos; j++) {
            if (arr[j] > arr[j + 1]) {
               temp = arr[j];
               arr[j] = arr[j + 1];
               arr[j + 1] = temp;
               lastSwapPos = j;
            }
         }
         lastPos = lastSwapPos;
      }
   }

   // Case 2 method: Selection Sort
   public static void selectionSort(int[] arr) {
      int firstPos = 0, lastPos = arr.length - 1;
      int temp, smallestPos;

      for (int i = firstPos; i < lastPos; i++) {
         smallestPos = i;
         for (int j = i + 1; j <= lastPos; j++) {
            if (arr[j] < arr[smallestPos]) {
               smallestPos = j;
            }
         }
         temp = arr[smallestPos];
         arr[smallestPos] = arr[i];
         arr[i] = temp;
      }
   }

   // Case 3 method: Insertion Sort
   public static void insertionSort(int[] arr) {
      int nextToInsert, index;

      for (int i = 1; i < arr.length; i++) {
         nextToInsert = arr[i];

         index = i - 1;
         while (index >= 0 && arr[index] > nextToInsert) {
            arr[index + 1] = arr[index];
            index--;
         }

         arr[index + 1] = nextToInsert;
      }
   }

   // Case 4 method: Shell Sort
   private static void shellSort(int[] arr) {
      int temp, index;

      for (int gap = arr.length / 2; gap > 0; gap /= 2) {
         for (int i = gap; i < arr.length; i++) {
            temp = arr[i];
            for (index = i; index >= gap && arr[index - gap] > temp; index -= gap) {
               arr[index] = arr[index - gap];
            }
            arr[index] = temp;
         }
      }
   }

   // Case 5 method: Merge Sort
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

   // Case 6 method: Quick Sort
   private static void swap(int[] arr, int first, int second) {
      int temp = arr[first];
      arr[first] = arr[second];
      arr[second] = temp;
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
   }

   public static void quickSort(int[] arr) {
      quickSort_r(arr, 0, arr.length - 1);
   }

   public static void quickSort_r(int[] arr, int first, int last) {
      int middle = (first + last) / 2;
      orderThree(arr, first, middle, last);
      swap(arr, middle, last);

      int pivot = arr[last];
      int indexFromLeft = first, indexFromRight = last;

      while (indexFromLeft <= indexFromRight) {
         while (arr[indexFromLeft] < pivot) {
            indexFromLeft++;
         }
         while (arr[indexFromRight] > pivot) {
            indexFromRight--;
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


   // Main
   public static void main(String[] args) {
      Scanner input = new Scanner(System.in);
      int choice = -1;

      System.out.println("\n===============================================");
      System.out.println("===        Sort Performance Analyser        ===");
      System.out.println("===============================================");
      System.out.println("Measures execution time when sorting arrays of" +
                       "\n10, 100, 1k, 10k, 100k and 1 million elements");
      System.out.println("-----------------------------------------------");

      while (choice != 0) {
         System.out.println("\nChoose a sort algorithm");
         System.out.println("-----------------------");
         System.out.println("1 - Bubble Sort");
         System.out.println("2 - Selection Sort");
         System.out.println("3 - Insertion Sort");
         System.out.println("4 - Shell Sort");
         System.out.println("5 - Merge Sort");
         System.out.println("6 - Quick Sort");
         System.out.println("0 - Exit\n");

         System.out.print("Enter your choice: ");
         String choiceInput = input.nextLine();

         System.out.println();

         // Input validation
         try
         {
            choice = Integer.parseInt(choiceInput);
         }
         catch (NumberFormatException e) {
            System.out.println("Invalid choice.");
            continue;
         }

         if (choice < 0 || choice > 6) {
            System.out.println("Invalid choice.");
            continue;
         }

         long startTime, endTime;
         int[] arraySizes = {10, 100, 1000, 10000, 100000, 1000000};

         long lastSortTime = 0;

         // Switch block
         switch (choice) {
            // 1 - Bubble Sort
            case 1:
               System.out.println("\n-------------------");
               System.out.println("Bubble Sort results");
               System.out.println("-------------------\n");
               System.out.println("Array Size\t\t\tSort Time (ns)\t\t\tRate of Increase");
               System.out.println("------------------------------------------------------------");

               lastSortTime = 0;

               for (int arraySize : arraySizes)
               {
                  // Time calc
                  startTime = System.nanoTime();
                  for (int i = 0; i < 1000; i++)
                  {
                     int[] arr = randomArray(arraySize);
                     bubbleSort(arr);
                  }
                  endTime = System.nanoTime();

                  long sortTime = endTime - startTime;

                  double rateOfIncrease;

                  if (lastSortTime != 0) {
                     rateOfIncrease = (double) sortTime / lastSortTime;
                     System.out.printf("%-20d%-24d%-1.2f%-1s\n", arraySize, sortTime, rateOfIncrease, "x");
                  }
                  else {
                     System.out.printf("%-20d%-24d%-1s\n", arraySize, sortTime, "N/A");
                  }

                  lastSortTime = sortTime;
               }
               System.out.println();
               break;

            // 2 - Selection Sort
            case 2:
               System.out.println("\n----------------------");
               System.out.println("Selection Sort results");
               System.out.println("----------------------\n");
               System.out.println("Array Size\t\t\tSort Time (ns)\t\t\tRate of Increase");
               System.out.println("------------------------------------------------------------");

               lastSortTime = 0;

               for (int arraySize : arraySizes)
               {
                  // Time calc
                  startTime = System.nanoTime();
                  for (int i = 0; i < 1000; i++)
                  {
                     int[] arr = randomArray(arraySize);
                     selectionSort(arr);
                  }
                  endTime = System.nanoTime();

                  long sortTime = endTime - startTime;

                  double rateOfIncrease;

                  if (lastSortTime != 0) {
                     rateOfIncrease = (double) sortTime / lastSortTime;
                     System.out.printf("%-20d%-24d%-1.2f%-1s\n", arraySize, sortTime, rateOfIncrease, "x");
                  }
                  else {
                     System.out.printf("%-20d%-24d%-1s\n", arraySize, sortTime, "N/A");
                  }

                  lastSortTime = sortTime;
               }
               System.out.println();
               break;

            // 3 - Insertion Sort
            case 3:
               System.out.println("\n----------------------");
               System.out.println("Insertion Sort results");
               System.out.println("----------------------\n");
               System.out.println("Array Size\t\t\tSort Time (ns)\t\t\tRate of Increase");
               System.out.println("------------------------------------------------------------");

               lastSortTime = 0;

               for (int arraySize : arraySizes)
               {
                  // Time calc
                  startTime = System.nanoTime();
                  for (int i = 0; i < 1000; i++)
                  {
                     int[] arr = randomArray(arraySize);
                     insertionSort(arr);
                  }
                  endTime = System.nanoTime();

                  long sortTime = endTime - startTime;

                  double rateOfIncrease;

                  if (lastSortTime != 0) {
                     rateOfIncrease = (double) sortTime / lastSortTime;
                     System.out.printf("%-20d%-24d%-1.2f%-1s\n", arraySize, sortTime, rateOfIncrease, "x");
                  }
                  else {
                     System.out.printf("%-20d%-24d%-1s\n", arraySize, sortTime, "N/A");
                  }

                  lastSortTime = sortTime;
               }
               System.out.println();
               break;

            // 4 - Shell Sort
            case 4:
               System.out.println("\n------------------");
               System.out.println("Shell Sort results");
               System.out.println("------------------\n");
               System.out.println("Array Size\t\t\tSort Time (ns)\t\t\tRate of Increase");
               System.out.println("------------------------------------------------------------");

               lastSortTime = 0;

               for (int arraySize : arraySizes)
               {
                  // Time calc
                  startTime = System.nanoTime();
                  for (int i = 0; i < 1000; i++)
                  {
                     int[] arr = randomArray(arraySize);
                     shellSort(arr);
                  }
                  endTime = System.nanoTime();

                  long sortTime = endTime - startTime;

                  double rateOfIncrease;

                  if (lastSortTime != 0) {
                     rateOfIncrease = (double) sortTime / lastSortTime;
                     System.out.printf("%-20d%-24d%-1.2f%-1s\n", arraySize, sortTime, rateOfIncrease, "x");
                  }
                  else {
                     System.out.printf("%-20d%-24d%-1s\n", arraySize, sortTime, "N/A");
                  }

                  lastSortTime = sortTime;
               }
               System.out.println();
               break;

            // 5 - Merge Sort
            case 5:
               System.out.println("\n------------------");
               System.out.println("Merge Sort results");
               System.out.println("------------------\n");
               System.out.println("Array Size\t\t\tSort Time (ns)\t\t\tRate of Increase");
               System.out.println("------------------------------------------------------------");

               lastSortTime = 0;

               for (int arraySize : arraySizes)
               {
                  // Time calc
                  startTime = System.nanoTime();
                  for (int i = 0; i < 1000; i++)
                  {
                     int[] arr = randomArray(arraySize);
                     mergeSort(arr);
                  }
                  endTime = System.nanoTime();

                  long sortTime = endTime - startTime;

                  double rateOfIncrease;

                  if (lastSortTime != 0) {
                     rateOfIncrease = (double) sortTime / lastSortTime;
                     System.out.printf("%-20d%-24d%-1.2f%-1s\n", arraySize, sortTime, rateOfIncrease, "x");
                  }
                  else {
                     System.out.printf("%-20d%-24d%-1s\n", arraySize, sortTime, "N/A");
                  }

                  lastSortTime = sortTime;
               }
               System.out.println();
               break;

            // 6 - Quick Sort
            case 6:
               System.out.println("\n------------------");
               System.out.println("Quick Sort results");
               System.out.println("------------------\n");
               System.out.println("Array Size\t\t\tSort Time (ns)\t\t\tRate of Increase");
               System.out.println("------------------------------------------------------------");

               lastSortTime = 0;

               for (int arraySize : arraySizes)
               {
                  // Time calc
                  startTime = System.nanoTime();
                  for (int i = 0; i < 1000; i++)
                  {
                     int[] arr = randomArray(arraySize);
                     quickSort(arr);
                  }
                  endTime = System.nanoTime();

                  long sortTime = endTime - startTime;

                  double rateOfIncrease;

                  if (lastSortTime != 0) {
                     rateOfIncrease = (double) sortTime / lastSortTime;
                     System.out.printf("%-20d%-24d%-1.2f%-1s\n", arraySize, sortTime, rateOfIncrease, "x");
                  }
                  else {
                     System.out.printf("%-20d%-24d%-1s\n", arraySize, sortTime, "N/A");
                  }

                  lastSortTime = sortTime;
               }
               System.out.println();
               break;

            // 0 - Exit
            case 0:
               System.out.println("Exiting...");
               System.exit(0);
               break;

            // Default case to return to menu
            default:
               System.out.println("Error - Returning to main menu...");
               break;
         }
      }
   }
}