public class Searching {

    public static <T> boolean inArray(T[] arr, T entry) {
        boolean found = false;
        int index = 0;

        while (!found && index < arr.length) {
            if (arr[index++].equals(entry)) {
                found = true;
            }
        }
        return found;
    }

    public static <T> boolean inArray_r(T[] arr, int first, int last, T entry) {
        if (first > last) {
            return false;
        }
        else if (arr[first].equals(entry)) {
            return true;
        }
        else {
            return inArray_r(arr, first + 1, last, entry);
        }
    }




    public static void  main(String[] args) {
        Integer[] integers = {1, 3, 5, 7, 9};
        String[] strings = {"one", "three", "five", "seven", "nine"};
        //
        AListChain myListInteger = new AListChain();
        AListChain myListString = new AListChain();

        System.out.println("5 in integer array: " + inArray(integers, 5));
        System.out.println("6 in integer array: " + inArray(integers, 6));
        System.out.println("9 in integer array: " + inArray(integers, 9));

        System.out.println("\nFive in string array: " + inArray(strings, "five"));
        System.out.println("Six in string array: " + inArray(strings, "six"));
        System.out.println("Nine in string array: " + inArray(strings, "nine"));

        // Recursive
        System.out.println("\n\n5 in (recursive) integer array: " + inArray_r(integers, 0, integers.length - 1, 5));
        System.out.println("6 in (recursive) integer array: " + inArray_r(integers, 0, integers.length - 1, 6));
        System.out.println("9 in (recursive) integer array: " + inArray_r(integers, 0, integers.length - 1, 9));

        System.out.println("\nFive in (recursive) string array: " + inArray_r(strings, 0, integers.length - 1, "five"));
        System.out.println("Six in (recursive) string array: " + inArray_r(strings, 0, integers.length - 1, "six"));
        System.out.println("Nine in (recursive) string array: " + inArray_r(strings, 0, integers.length - 1, "nine"));

        //
        myListInteger.add(1);
        myListInteger.add(3);
        myListInteger.add(5);
        myListInteger.add(7);
        myListInteger.add(9);

        System.out.println("\n\n5 in myListInteger: " + myListInteger.contains_r(5));
        System.out.println("6 in myListInteger: " + myListInteger.contains_r(6));
        System.out.println("9 in myListInteger: " + myListInteger.contains_r(9));

        myListString.add("one");
        myListString.add("three");
        myListString.add("five");
        myListString.add("seven");
        myListString.add("nine");

        System.out.println("\nFive in myListString: " + myListString.contains_r("five"));
        System.out.println("Six in myListString: " + myListString.contains_r("six"));
        System.out.println("Nine in myListString: " + myListString.contains_r("nine"));
    }
}