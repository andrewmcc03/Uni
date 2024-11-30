public class MyNode2<T> {

   private T data;
   private MyNode2<T> next;
   private MyNode2<T> previous;

   public MyNode2(T dataValue) {
      data = dataValue;
      next = null;
      previous = null;
   }

   public MyNode2<T> getNextNode() {
      return next;
   }

   public MyNode2<T> getPreviousNode() {
      return previous;
   }

   public T getData() {
      return data;
   }

   public void setData(T dataValue) {
      data = dataValue;
   }

   public void setNextNode(MyNode2<T> nextNode) {
      next = nextNode;
   }

   public void setPreviousNode(MyNode2<T> previousNode) {
      previous = previousNode;
   }
}