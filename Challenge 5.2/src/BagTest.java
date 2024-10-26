public class BagTest {
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {

        // Create an object of ArrayBag<String>
        LinkedBag<String> testArrayBag = new LinkedBag<>();
        System.out.println("------------------------------------------------------");
        System.out.println("BAG TEST:");
        System.out.println("Initial state of Bag:");

        // Output the current status of the bag:
        bagStatusReport(testArrayBag);
        System.out.println("\n");

        System.out.println("Adding 8 strings to the bag: A, A, B, B, C, C, D, D");

        // (Done) TODO: Add the following strings to the bag: "A", "A", "B", "B". "C", "C", "D", "D":
        testArrayBag.addNewEntry("A");
        testArrayBag.addNewEntry("A");
        testArrayBag.addNewEntry("B");
        testArrayBag.addNewEntry("B");
        testArrayBag.addNewEntry("C");
        testArrayBag.addNewEntry("C");
        testArrayBag.addNewEntry("D");
        testArrayBag.addNewEntry("D");

        // Output the current status of the bag:
        bagStatusReport(testArrayBag);
        System.out.println("\n");

        System.out.println("---------------------");
        System.out.println("Remove C from the bag");

        // (Done) TODO: Remove C from the bag:
        testArrayBag.remove("C");

        // Output the current status of the bag:
        bagStatusReport(testArrayBag);
        System.out.println("\n");

        System.out.println("---------------------------");
        System.out.println("Remove A and B from the bag");

        // (Done) TODO: Remove A and B from the bag:
        testArrayBag.remove("A");
        testArrayBag.remove("B");


        /// Output the current status of the bag:
        bagStatusReport(testArrayBag);
        System.out.println("\n");

        System.out.println("----------------------------------------");
        System.out.println("Remove an unspecified entry from the bag");

        // (Done) TODO: Remove an unspecified entry from the bag:
        testArrayBag.remove();


        // Output the current status of the bag:
        bagStatusReport(testArrayBag);
        System.out.println("\n");

        System.out.println("---------------------------------------------");
        System.out.println("Remove another unspecified entry from the bag");

        // (Done) TODO: Remove another unspecified entry from the bag:
        testArrayBag.remove();

        // Output the current status of the bag:
        bagStatusReport(testArrayBag);
        System.out.println("\n");

        System.out.println("Bag test completed");
        System.out.println("-----------------------------------------------");
    }


    /**
     * Method to output a report on the current contents and status of the bag.
     * @param myBag The bag being reported upon.
     */
    public static void bagStatusReport(LinkedBag<String> myBag) {
        System.out.println("Bag contents: " + myBag);
        System.out.println("Size: " + myBag.getCurrentSize());
        System.out.println("Is empty: " + myBag.isEmpty());
        System.out.println("Frequency of A: " + myBag.getFrequencyOf("A"));
        System.out.println("Frequency of B: " + myBag.getFrequencyOf("B"));
        System.out.println("Frequency of C: " + myBag.getFrequencyOf("C"));
        System.out.println("Frequency of D: " + myBag.getFrequencyOf("D"));
        System.out.println("Bag contains A: " + myBag.contains("A"));
        System.out.println("Bag contains B: " + myBag.contains("B"));
        System.out.println("Bag contains C: " + myBag.contains("C"));
        System.out.println("Bag contains D: " + myBag.contains("D"));
    }
}
