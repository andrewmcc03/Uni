public class SumAnalysis {
    public static long sum_A(int n) {
        long sum = 0;

        for (int i = 1; i <= n; i++) {
            sum = sum + i;
        }
        return sum;
    }

    public static long sum_B(int n) {
        long sum = 0;

        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= i; j++) {
                sum = sum + 1;
            }
        }
        return sum;
    }

    public static long sum_C(int n) {
        long sum = 0;
        sum = n * (n + 1) / 2;
        return sum;
    }

    public static void main(String[] args) {
//        long startTime, endTime;
//
//        startTime = System.nanoTime();
//        System.out.println(sum_A(10000));
//        endTime = System.nanoTime();
//        System.out.println("Algorithm A: " + (endTime - startTime) + "ns\n");
//
//        startTime = System.nanoTime();
//        System.out.println(sum_B(10000));
//        endTime = System.nanoTime();
//        System.out.println("Algorithm B: " + (endTime - startTime) + "ns\n");
//
//        startTime = System.nanoTime();
//        System.out.println(sum_C(10000));
//        endTime = System.nanoTime();
//        System.out.println("Algorithm C: " + (endTime - startTime) + "ns\n");
//
//        System.out.println("========================");

        int[] testValues = {1, 10, 100, 1000, 10000, 100000, 1000000};

        // Table header
        System.out.printf("\n%-15s%-20s%-20s%-20s\n\n", "No. Elements", "Algorithm A", "Algorithm B", "Algorithm C");

        // Measure and show program execution times
        for (int n : testValues) {
            // Sum A time calculation
            long startTime = System.nanoTime();
            sum_A(n);
            long endTime = System.nanoTime();
            long timeA = endTime - startTime;

            // Sum B time calculation
            startTime = System.nanoTime();
            sum_B(n);
            endTime = System.nanoTime();
            long timeB = endTime - startTime;

            // Sum C time calculation
            startTime = System.nanoTime();
            sum_C(n);
            endTime = System.nanoTime();
            long timeC = endTime - startTime;

            // Output results of calculations
            System.out.printf("%-15d%-20d%-20d%-20d\n", n, timeA, timeB, timeC);
        }
    }
}