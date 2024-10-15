// PROGRAM BY ANDREW MCCORMICK
// Student ID: B00988875

public class TestAnimal {
    public static void main(String[] args) {
        // Create two Lion objects
        Lion myLion1 = new Lion("vegetation", 10, 4, "Leo");    // Normal parameters
        Lion myLion2 = new Lion(null, 0, 0, null);              // Empty parameters

        // Set age of myLion1 to 3 (declared as 4 during object creation above)
        myLion1.setAge(3);

        // Print details of myLion1
        System.out.println(myLion1);

        // Print details of myLion2
        System.out.println(myLion2);

        // Print the number of Lion objects created
        System.out.println(Lion.numberOfLions() + " lions have been created.");
    }
}