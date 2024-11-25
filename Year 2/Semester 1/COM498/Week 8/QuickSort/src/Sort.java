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

                // 7.2 pt? System.out.println("Pass:\t\t" + Arrays.toString(arr));
            }
        }
    }


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

        // 7.3
        int[] arr = {9, 2, 7, 1, 10, 3, 6, 4, 5, 8};
        //int[] arr = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        //int[] arr = {10, 9, 8, 7, 6, 5, 4, 3, 2, 1};
        //int[] arr = {5, 9, 1, 10, 3, 8, 2, 4, 7, 6};

        System.out.println("\nBefore:\t\t" + Arrays.toString(arr));
        quickSort(arr);
        System.out.println("\nAfter:\t\t" + Arrays.toString(arr));

        System.out.println("\n\nTotal Comparisons:\t" + numComparisons);
        System.out.println("Total Updates:\t\t" + numUpdates);
    }
}
