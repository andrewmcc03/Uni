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
            //System.out.println("Pass " + (i + 1) + ":  " + Arrays.toString(arr));
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
            System.out.println("Pass:    " + Arrays.toString(arr));
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
            //System.out.println("Pass " + (i + 1) + ":\t\t" + Arrays.toString(arr));
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
            //System.out.println("Pass:\t\t" + Arrays.toString(arr));

            // Recursive call, adding 2 to existing first position
            selectionSort_r(arr, firstPos + 1, lastPos);
        }
    }

    public static void main(String[] args) {

        long startTimeI, endTimeI, startTimeR, endTimeR;
        int[] arraySizes = {100, 200, 400, 800, 1600, 3200, 6400};

        System.out.println("Array Size\t\t\tIterative\t\t\tRecursive");
        System.out.println("=================================================");

        for (int arraySize : arraySizes) {

            // Iterative time calc
            startTimeI = System.currentTimeMillis();
            for (int i = 0; i < 1000; i++) {
                int[] arr = randomArray(arraySize);
                selectionSort(arr);
            }
            endTimeI = System.currentTimeMillis();

            // Recursive time calc
            startTimeR = System.currentTimeMillis();
            for (int i = 0; i < 1000; i++) {
                int[] arr = randomArray(arraySize);
                selectionSort_r(arr, 0, arr.length - 1);
            }
            endTimeR = System.currentTimeMillis();

            long iterativeTime = endTimeI - startTimeI;
            long recursiveTime = endTimeR - startTimeR;

            System.out.printf("%-20d%-7d%-13s%-7d%-6s\n", arraySize, iterativeTime, "ms", recursiveTime, "ms");
        }
    }
}