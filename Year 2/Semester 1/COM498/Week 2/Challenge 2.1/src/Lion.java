public class Lion extends Animal {
    // Class variable to count the number of Lion objects created
    private static int numOfLions = 0;

    // Instance variables for each Lion object
    private int age;
    private String name;

    // Default constructor
    public Lion() {
        super();  // Calls the default constructor of the Animal class
        this.age = 0;  // Default age
        this.name = "un-named";  // Default name
        numOfLions++;
    }

    // Constructor with parameters
    public Lion(String food, int lifeExpectancy, int age, String name) {
        super(food, lifeExpectancy);  // Calls the constructor of the Animal class
        this.age = age;
        this.name = name;
        numOfLions++;
    }

    // Method to set the age of the lion
    public void setAge(int age) {
        this.age = age;
    }

    // Method to return a string of the Lion object
    @Override
    public String toString() {
        String maneStatus = (this.name != null && !this.name.equals("un-named")) ? this.name : "This un-named lion";
        String result = maneStatus + " is " + (this.age > 0 ? this.age + "yrs old" : "of unknown age") + ". ";
        result += super.toString();
        return result;
    }

    // Method to return the number of Lion objects created
    public static int numberOfLions() {
        return numOfLions;
    }
}