import java.util.Scanner;

public class TowersOfHanoi {
    private static final String SOURCE = "Source";
    private static final String SPARE = "Spare ";
    private static final String TARGET = "Target";

    public static void solveTowers(int numberOfDiscs, String source, String spare, String target) {
        if (numberOfDiscs == 1) {
            System.out.println(source + " => " + target);
        }
        else {
            solveTowers(numberOfDiscs - 1, source, target, spare);
            System.out.println(source + " => " + target);
            solveTowers(numberOfDiscs - 1, spare, source, target);
        }
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter the number of discs: ");
        int numberOfDiscs = scanner.nextInt();
        System.out.println();
        solveTowers(numberOfDiscs, SOURCE, SPARE, TARGET);
    }
}