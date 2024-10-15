public class House extends Building {
    private int numBedrooms;
    private boolean hasGarage;

    public House() {
        super();
        this.numBedrooms = 0;
        this.hasGarage = false;
    }

    public House(String address, String owner, int numBedrooms, boolean hasGarage) {
        super(address, owner);
        this.numBedrooms = numBedrooms;
        this.hasGarage = hasGarage;
    }

    public int getNumBedrooms() {
        return this.numBedrooms;
    }

    public void setNumBedrooms(int numBedrooms) {
        this.numBedrooms = numBedrooms;
    }

    public boolean getHasGarage() {
        return this.hasGarage;
    }

    public void setHasGarage(boolean hasGarage) {
        this.hasGarage = hasGarage;
    }

    public String toString() {
        return super.toString() + " and is a house with " +
                this.numBedrooms + " bedrooms.";
    }
}