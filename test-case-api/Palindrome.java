public class Palindrome {

    public void isPalindrome(int[] x) {
        boolean isPal = true;
        for (int i = 0; i <= x.length - 1; i++) {
            if (x[i] != x[x.length - 1 - i]) {
                isPal = false;
            }
        }
        if (isPal) {
            System.out.println("It is a palindrome.");
        } else {
            System.out.println("It is not a palindrome.");
        }
    }
}
//END OF FILE
