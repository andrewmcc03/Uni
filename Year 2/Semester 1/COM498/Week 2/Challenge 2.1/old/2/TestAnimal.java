public class TestAnimal {
    public static void main(String[] args) {
        // Create two Lion objects
        Lion myLion1 = new Lion("meat", 15, 2, "Simba");
        Lion myLion2 = new Lion("meat", 12, 5, "Mufasa");

        // Set age of myLion1 to 3
        myLion1.setAge(3);

        // Print out details of myLion1 and the number of Lions created
        System.out.println(myLion1);
        System.out.println(Lion.numberOfLions() + " lions have been created.");
    }
}