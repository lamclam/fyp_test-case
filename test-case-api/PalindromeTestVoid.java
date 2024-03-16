public class PalindromeTestVoid {
    public static void main(String[] args) {
        Palindrome p = new Palindrome();

        int[][] cases = {
            {1, 3, 3, 1}, // Case1
            {1, 2, 3, 2, 1}, // Case2
            {3, 3}, // Case3
            {2}, // Case4
            {1, 1, 3, 3, 1}, // Case5
            {1, 3, 3, 1, 1}, // Case6
            {1, 1, 4, 6, 4, 1}, // Case7
            {1, 4, 6, 4, 1, 1}, // Case8
            {1, 2, 3, 4, 2, 1}, // Case9
            {1, 3, 5, 7, 6, 3, 1}, // Case10
            {1, 3, 4, 4, 3, 2}, // Case11
            {1, 3, 4, 5, 4, 3, 2}, // Case12
            {1, 2, 4, 4, 3, 2}, // Case13
            {2, 1, 3, 4, 1, 1}, // Case14
            {7, 7, 7, 7, 7, 7, 7}, // Case15
            {8, 8, 8, 8, 8, 8} // Case16
        };

        for (int i = 0; i < cases.length; i++) {
            p.isPalindrome(cases[i]);
			// Print a special string after each test case
            System.out.println("***End Of Test Case***");
        }
    }
}
