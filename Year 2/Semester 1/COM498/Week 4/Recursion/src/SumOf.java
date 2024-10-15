public class SumOf {
    public static int sumOf(int n) {
        if (n == 1) return 1;   // BASE CASE
        else return n + sumOf(n - 1);
    }

    public static void main(String[] args) {
        System.out.println("Sum of integers up to 3 is " + sumOf(3));
        System.out.println("Sum of integers up to 5 is " + sumOf(5));
        System.out.println("Sum of integers up to 10 is " + sumOf(10));
    }
}