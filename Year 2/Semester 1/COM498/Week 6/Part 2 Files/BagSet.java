public class BagSet<T> {

    // TO DO
    // Modify the class definition so that BagSet is a SUBCLASS of class Bag



    // TO DO
    // add a new method addNewEntry() to over-ride the inherited behaviour
    // and make sure that any value is added at most once to a BagSet
    // HINT - use the superclass method addNewEntry() in your solution



    /*
     * Method to return the union of a BagSet with another BagSet 
     * passed as a parameter.  The result BagSet should contain all
     * items that appear in EITHER BagSet
     *
     * @param (BagSet) - a second Bagset to be merged
     * @return (BagSet) - the union of the BagSets
     *
     * THIS METHOD IS PROVIDED AS AN EXAMPLE OF SOME OF THE TECHNIQUES
     * THAT WILL BE USEFUL IN PROVIDING THE OTHER METHODS
     */
    public BagSet<T> union(BagSet<T> anotherBagSet) {
        BagSet<T> resultSet = new BagSet<T>(); // declare a Bagset to return as the result
        T[] thisSet = this.toArray(); // convert the object BagSet to an array for easy manipulation
        T[] otherSet = anotherBagSet.toArray(); // convert the parameter BagSet to an array 
        for (T element : thisSet) resultSet.addNewEntry(element); // Add all elements to result BagSet
        for (T element : otherSet) resultSet.addNewEntry(element); // Add all elements to result BagsSet
                                                                   // - any duplicates will be rejected by the new
                                                                   // addNewEntry() method.
        return resultSet; // return the result
    }
    


    /*
     * Method to return the intersection of a BagSet with another BagSet 
     * passed as a parameter.  The result BagSet should contain only the
     * items that appear in BOTH BagSets
     *
     * @param (BagSet) - a second Bagset to be merged
     * @return (BagSet) - the intersection of the BagSets
     */
    public BagSet<T> intersection(BagSet<T> anotherSet) {

        // TO DO
        // Provide the body for this method

        return null; // Change this line as required
    }




    /*
     * Method to return the difference between a BagSet and another BagSet 
     * passed as a parameter.  The result BagSet should contain all
     * items that appear in the object BagSet but NOT in the parameter BagSet
     *
     * @param (BagSet) - a second Bagset to be merged
     * @return (BagSet) - the difference between the BagSets
     */
    public BagSet<T> difference(BagSet<T> anotherSet) {

        // TO DO
        // Provide the body for this method

        return null; // Change this line as required
    }




    /*
     * Method to return true if the set of elements contained in a BagSet
     * is the same as those in another BagSet passed as a parameter.
     * The order of elements is insignificant, so Bag [A, B, C] equals Bag [C, B, A]
     *
     * @param (BagSet) - a second Bagset to be merged
     * @return (boolean) - true if the collections are the same, false otherwise
     */
    public boolean equals(BagSet<T> anotherSet) {

        // TO DO
        // Provide the body for this method

        return true; // Change this line as required
    }
}