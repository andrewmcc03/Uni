public class Printer {
    public static void main(String[] args) {
        Integer[] intArray = {1, 2, 3};
        String[] stringArray = {"One", "Two", "Three"};

        printArray(intArray);
        printArray(stringArray);
    }

    public static <T> void printArray(T[] arr) {
        for (T element : arr) System.out.println(element);
    }
}