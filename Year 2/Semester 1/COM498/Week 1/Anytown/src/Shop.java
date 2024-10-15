public class Shop extends Building {
    private int numEmployees;
    private int averageTurnover;

    public Shop() {
        super();
        this.numEmployees = 0;
        this.averageTurnover = 0;
    }

    public Shop(String address, String owner, int numEmployees, int averageTurnover) {
        super(address, owner);
        this.numEmployees = numEmployees;
        this.averageTurnover = averageTurnover;
    }

    public int getNumEmployees() {
        return this.numEmployees;
    }

    public void setNumEmployees(int numEmployees) {
        this.numEmployees = numEmployees;
    }

    public int getAverageTurnover() {
        return this.averageTurnover;
    }

    public void setAverageTurnover(int averageTurnover) {
        this.averageTurnover = averageTurnover;
    }

    public String toString() {
        return super.toString() + " and is a shop with " +
                this.numEmployees + " employees.";
    }
}