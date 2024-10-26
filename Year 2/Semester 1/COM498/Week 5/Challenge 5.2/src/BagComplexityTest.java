import java.util.Random;

public class BagComplexityTest {
    public static void main(String[] args) {
        // New LinkedBag object
        LinkedBag<Integer> newBag = new LinkedBag<Integer>();
        // Random values
        Random rdm = new Random();

        int[] testValues = {10, 100, 1000, 10000, 100000};

        // Output perf analysis
        System.out.println("\nLinkedBag Performance Analysis (time in ns)");
        System.out.println("===========================================");

        // Table header
        System.out.printf("\n%-25s%-30s%-30s%-30s%-30s\n\n", "LinkedBag Size", "Total Time to Add", "Avg. Time to Add", "Total Time to Remove", "Avg. Time to Remove");

        for (int n : testValues) {
            // "Adding to bag" times
            long addingStartTime = System.nanoTime();
            for (int i = 0; i < n; i++) {
                int rdmInt = rdm.nextInt(n * 10);
                newBag.addNewEntry(rdmInt);
            }

            long addingEndTime = System.nanoTime();
            long totalAddTime = addingEndTime - addingStartTime;
            long avgAddTime = totalAddTime / n;

            // "Removing from bag" times
            long removingStartTime = System.nanoTime();
            for (int i = 0; i < n; i++) {
                int rdmInt = rdm.nextInt(n * 10);
                newBag.addNewEntry(rdmInt);
            }

            long removingEndTime = System.nanoTime();
            long totalRemoveTime = removingEndTime - removingStartTime;
            long avgRemoveTime = totalRemoveTime / n;

            // Output results of calculations
            System.out.printf("%-25d%-30d%-30d%-30d%-30d\n", n, totalAddTime, avgAddTime, totalRemoveTime, avgRemoveTime);
        }
    }
}