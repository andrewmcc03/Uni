public interface BagInterface<T> {
    public int getCurrentSize();
    /* Number of elements currently contained in the bag

    @return - (int) number of elements
    */

    public boolean isEmpty();
    /* Test for an empty bag

    @return - (boolean) true if the number of element is 0, otherwise false
    */

    public boolean addNewEntry(T newEntry);
    /* Test for space capacity in the bag and if it exists, add the new element and increment the number of elements in the bag

    @param (T) newEntry = the item to be added to the bag

    @return - (boolean) true if the item is added, otherwise false
    */

    public T remove();
    /* Remove any element from the bag if one is available, and decrement the number of elements. Return the remove element or null if none is available

    @return - (T) the element removed from the bag, or null
     */

    public boolean remove (T anEntry);
    /* Remove the specified element from the bag if it is present, and decrement the number of elements

    @return - (boolean) true if the element is available, otherwise false
    */

    public void clear();
    /* Empty/clear the bag - set number of elements to 0 */

    public int getFrequencyOf(T anEntry);
    /* Count how many times a given element appears in the bag

    @param (T) anEntry - the element to look for in the bag

    @return - (int) the number of times that the given element appears
    */

    public boolean contains(T anEntry);
    /* Check for the presence of a specified element in the bag

    @param (T) anEntry - the item to look for in the bag

    @return - (boolean) true if the bag contains the element, otherwise false
    */

    public T[] toArray();
    /* Find all elements in the bag

    @return - (T[]) an array of the size number of elements, containing all contents of the bag
    */
}