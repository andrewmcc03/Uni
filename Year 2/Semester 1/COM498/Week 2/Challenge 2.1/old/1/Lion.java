public class Lion extends Animal {
    private String name;
    private int age;
    private boolean ageGiven;
    private String foodType;
    private int lifeExpectancy;
    private static int numOfLions = 0;


    public Lion() {
        super();
        numOfLions++;
    }

    public Lion(String foodType, int lifeExpectancy) {
        this.foodType = foodType;
        this.lifeExpectancy = lifeExpectancy;
        numOfLions++;
    }

    public Lion(String name, String foodType, int lifeExpectancy) {
        super(name);
        this.name = name;
        this.foodType = foodType;
        this.lifeExpectancy = lifeExpectancy;
        numOfLions++;
    }

    public Lion(String name, int age, String foodType, int lifeExpectancy) {
        super(name, age);
        this.name = name;
        this.age = age;
        ageGiven = true;
        this.foodType = foodType;
        this.lifeExpectancy = lifeExpectancy;
        numOfLions++;
    }

    public static String getNumOfLions() {
        return numOfLions + " lions have been created.";
    }

    public void setNumOfLions(int numOfLions) {
        this.numOfLions = numOfLions;
    }

    @Override
    public String toString() {
        String result = "This ";

        // If no name given > set name to unnamed
        if (name == null) name = "un-named lion";

        // If age given > output with age
        if (ageGiven) System.out.print(name + " is " + age + "yrs old. ");
        // Else > output with no age
        else System.out.print(result + name + " is of unknown age. ");

        if (foodType != null) result += foodType + " eater ";

        if (lifeExpectancy == 0)
            result += "lives for an unknown number of years.";
        else result += "typically lives for " + lifeExpectancy + " years.";

        return result;
    }
}