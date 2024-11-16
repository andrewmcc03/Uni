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

    // Method for gap sequence A: n/2, n/4, n/8, …, 1 (as in our algorithm)
    public static int[] gapSequenceA(int length) {
        int maxGaps = 0;

        for (int gap = length / 2; gap > 0; gap = gap / 2) {
            maxGaps++;
        }

        int[] gaps = new int[maxGaps];
        for (int i = 0, gap = length / 2; gap > 0; i++, gap = gap / 2) {
            gaps[i] = gap;
        }

        return gaps;
    }

    // Method for gap sequence B: n/3, n/6, n/9, … 1 (divide by 3 rather than by 2 at each stage)
    public static int[] gapSequenceB(int length) {
        int maxGaps = 0;

        for (int gap = length / 3; gap > 0; gap = gap / 3) {
            maxGaps++;
        }

        int[] gaps = new int[maxGaps];
        for (int i = 0, gap = length / 3; gap > 0; i++, gap = gap / 3) {
            gaps[i] = gap;
        }

        return gaps;
    }

    // Method for gap sequence C: n/4, n/16, n/64, … 1 (divide by 4 at each stage)
    public static int[] gapSequenceC(int length) {
        int maxGaps = 0;

        // Same as before but div by 4 this time
        for (int gap = length / 4; gap > 0; gap = gap / 4) {
            maxGaps++;
        }

        int[] gaps = new int[maxGaps];
        for (int i = 0, gap = length / 4; gap > 0; i++, gap = gap / 4) {
            gaps[i] = gap;
        }

        return gaps;
    }

    // Method for mean of primes sequence: 3785, 1695, 749, 326, 138, 57, 23, 9, 4, 1 (mean of prime numbers sequence)
    public static int[] gapSequenceMeanPrime() {
        return new int[] {3785, 1695, 749, 326, 138, 57, 23, 9, 4, 1};
    }


    public static void main(String[] args) {

        long startTime, endTime;

        int[][] gapSequences = {gapSequenceA(10000), gapSequenceB(10000), gapSequenceC(10000), gapSequenceMeanPrime()};

        for (int[] gapSequence : gapSequences) {
            System.out.println("\nGap list:\t\t\t" + Arrays.toString(gapSequence));

            // Time calc
            startTime = System.currentTimeMillis();
            for (int i = 0; i < 1000; i++) {
                int[] arr = randomArray(10000); // 10000 elements from arrays
                shellSort(arr);
            }
            endTime = System.currentTimeMillis();

            long totalTime = endTime - startTime;

            System.out.println("Execution time:\t\t" + totalTime + "ms");
        }

        // NOTE: Couldn't get 3rd sequence's gap array to show the last int (1) at the end
    }
}