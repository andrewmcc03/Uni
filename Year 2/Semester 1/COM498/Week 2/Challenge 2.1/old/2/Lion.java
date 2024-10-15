public class Lion extends Animal {
    // Class variable to count the number of Lion objects
    private static int numOfLions = 0;

    // Instance variables
    private int age;
    private String name;

    // Default constructor
    public Lion() {
        super();
        this.age = 0;
        this.name = "Unnamed Lion";
        numOfLions++;
    }

    // Constructor with parameters for food, lifeExpectancy, age, and name
    public Lion(String food, int lifeExpectancy, int age, String name) {
        super(food, lifeExpectancy);
        this.age = age;
        this.name = name;
        numOfLions++;
    }

    // Method to set age
    public void setAge(int age) {
        this.age = age;
    }

    // Method to return a string representation of Lion
    @Override
    public String toString() {
        String mane = (age >= 3) ? " has a mane." : " doesn't have a mane.";
        return "Lion " + name + " is " + age + " years old and " + super.toString() + mane;
    }

    // Method to return the number of Lion objects created
    public static int numberOfLions() {
        return numOfLions;
    }
}