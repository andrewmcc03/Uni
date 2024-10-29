public class BagSetTest {

    public static void main(String[] args) {
        BagSet mySet1 = new BagSet();
        mySet1.addNewEntry("A");
        mySet1.addNewEntry("B");
        mySet1.addNewEntry("C");
        System.out.println("A = " + mySet1);

        BagSet mySet2 = new BagSet();
        mySet2.addNewEntry("C");
        mySet2.addNewEntry("D");
        System.out.println("B = " + mySet2);

        System.out.println();

        BagSet unionResult = new BagSet();
        unionResult.addNewEntry("A");
        unionResult.addNewEntry("B");
        unionResult.addNewEntry("C");
        unionResult.addNewEntry("D");

        BagSet intersectionResult = new BagSet();
        intersectionResult.addNewEntry("C");

        BagSet differenceResult = new BagSet();
        differenceResult.addNewEntry("A");
        differenceResult.addNewEntry("B");

        System.out.println("A union B = " + mySet1.union(mySet2));
        System.out.println("Union test - " + unionResult.equals(mySet1.union(mySet2)) + "\n");

        System.out.println("A intersection B = " + mySet1.intersection(mySet2));
        System.out.println("Intersection test - " + intersectionResult.equals(mySet1.intersection(mySet2)) + "\n");

        System.out.println("A difference B = " + mySet1.difference(mySet2));
        System.out.println("Difference test - " + differenceResult.equals(mySet1.difference(mySet2)) + "\n");

        System.out.println("A == B is " + mySet1.equals(mySet2));
        mySet2.remove("D");
        mySet2.addNewEntry("B");
        mySet2.addNewEntry("A");
        System.out.println("B = " + mySet2);
        System.out.println("A == B is " + mySet1.equals(mySet2));
    }
}