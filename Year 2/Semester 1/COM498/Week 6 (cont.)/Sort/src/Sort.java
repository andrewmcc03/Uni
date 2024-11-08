import java.util.Arrays;
import java.util.Random;

public class Sort {

    public static int numComparisons = 0, numSwaps = 0;

    public static void bubbleSort_slow(int arr[]) {

        int lastPos = arr.length - 1;
        int innerLastPos = lastPos;
        int temp;

        for (int i = 0; i < lastPos; i++) {
            for (int j = 0; j < innerLastPos; j++) {
                numComparisons++;
                if (arr[j] > arr[j + 1]) {
                    temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                    numSwaps++;
                }
            }
            innerLastPos--;
            System.out.println("Pass " + (i + 1) + ":  " + Arrays.toString(arr));
        }
    }

    public static void bubbleSort(int arr[]) {

        int firstPos = 0, lastPos = arr.length - 1;
        int temp, lastSwapPos;

        while (firstPos < lastPos) {
            lastSwapPos = firstPos;
            for (int j = firstPos; j < lastPos; j++) {
                numComparisons++;
                if (arr[j] > arr[j + 1]) {
                    temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                    numSwaps++;
                    lastSwapPos = j;
                }
            }
            lastPos = lastSwapPos;
            //System.out.println("Pass:    " + Arrays.toString(arr));
        }
    }

    public static int[] randomArray(int n) {
        Random rand = new Random();
        int[] arr = new int[n];

        for (int i = 0; i < n; i++) {
            arr[i] = rand.nextInt(100);
        }
        return arr;
    }

    public static void selectionSort(int[] arr) {
        int firstPos = 0, lastPos = arr.length - 1;
        int temp, smallestPos;

        for (int i = firstPos; i < lastPos; i++) {
            smallestPos = i;
            for (int j = i + 1; j <= lastPos; j++) {
                numComparisons++;
                if (arr[j] < arr[smallestPos]) {
                    smallestPos = j;
                }
            }
            temp = arr[smallestPos];
            arr[smallestPos] = arr[i];
            arr[i] = temp;

            numSwaps++;
            System.out.println("Pass " + (i + 1) + ":\t\t" + Arrays.toString(arr));
        }
    }

    // Recursive version of above method ^^
    public static void selectionSort_r(int[] arr, int firstPos, int lastPos) {
        int temp, smallestPos;

        numComparisons++;   // Because we've added a new comparison at the very top of the method, add 1 to numComparisons here

        if (firstPos < lastPos) {
            smallestPos = firstPos;
            for (int j = firstPos + 1; j <= lastPos; j++) {
                numComparisons++;
                if (arr[j] < arr[smallestPos]) {
                    smallestPos = j;
                }
            }
            temp = arr[smallestPos];
            arr[smallestPos] = arr[firstPos];
            arr[firstPos] = temp;

            numSwaps++;
            System.out.println("Pass:\t\t" + Arrays.toString(arr));

            // Recursive call, adding 2 to existing first position
            selectionSort_r(arr, firstPos + 1, lastPos);
        }
    }

    public static void main(String[] args) {

        // (bubbleSort_slow) Each of these do the same number of comparisons (45 comparisons), however swaps differ ...
        //int[] arr = {9, 2, 7, 1, 10, 3, 6, 4, 5, 8};  // (bubbleSort_slow) Totals 21 swaps
        //int[] arr = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};  // (bubbleSort_slow) Totals 0 swaps
        //int[] arr = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};    // (bubbleSort_slow) Totals all 45 swaps

//        // 6.2
//        long startTime, endTime;
//        int[] arraySizes = {100, 200, 400, 800, 1600, 3200, 6400};
//
//        for (int arraySize : arraySizes) {
//            startTime = System.currentTimeMillis();
//            for (int i = 0; i < 1000; i++) {
//                int[] arr = randomArray(arraySize);
//                bubbleSort(arr);
//            }
//            endTime = System.currentTimeMillis();
//
//            System.out.println(arraySize + ":\t" + (endTime - startTime) + "ms");
//
//            // As 'n' doubles, the execution time grows by 'n' squared
//        }

        // 6.3
        int[] arr = {5, 9, 1, 10, 3, 8, 2, 4, 7, 6};

        System.out.println("\nBefore:\t\t" + Arrays.toString(arr) + "\n");
//        selectionSort(arr);
        selectionSort_r(arr, 0, arr.length - 1);
        System.out.println("\nAfter:\t\t" + Arrays.toString(arr));

        System.out.println("\n\nTotal Comparisons:\t" + numComparisons);
        System.out.println("Total Swaps:\t\t" + numSwaps);
    }
}
