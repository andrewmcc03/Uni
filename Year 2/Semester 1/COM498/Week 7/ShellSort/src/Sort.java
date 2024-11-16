import java.util.Arrays;
import java.util.Random;

public class Sort {

    public static int numComparisons = 0, numSwaps = 0, numUpdates = 0;

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
            // 7.1 pt2 System.out.println("Pass " + (i + 1) + ":\t\t" + Arrays.toString(arr));
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

            // 7.1 pt1 System.out.println("Pass " + i + ": \t" + Arrays.toString(arr));
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

            // 7.1 pt1 System.out.println("Pass " + lastPos + ": \t" + Arrays.toString(arr));
        }
    }

    private static void shellSort(int[] arr) {
        int temp, index;

        for (int gap = arr.length / 2; gap > 0; gap /= 2) {
            System.out.println("=========\nGap is " + gap + "\n");
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

                System.out.println("Pass:\t\t" + Arrays.toString(arr));
            }
        }
    }

    public static void main(String[] args) {

        // 7.2
        //int[] arr = {9, 2, 7, 1, 10, 3, 6, 4, 5, 8};
        //int[] arr = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        int[] arr = {10, 9, 8, 7, 6, 5, 4, 3, 2, 1};
        //int[] arr = {5, 9, 1, 10, 3, 8, 2, 4, 7, 6};

        System.out.println("\nBefore:\t\t" + Arrays.toString(arr) + "\n");
        shellSort(arr);
        System.out.println("\n=========\nAfter:\t\t" + Arrays.toString(arr));

        System.out.println("\n\nTotal Comparisons:\t" + numComparisons);
        System.out.println("Total Updates:\t\t" + numUpdates);
    }
}