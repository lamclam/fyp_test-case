import java.util.Scanner;

public class PrimeNumber {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Enter a number n: ");
        int n = scanner.nextInt();
        scanner.close();

        boolean isPrime = true;
        if (n <= 1) {
            isPrime = false;
        } else {
            int x = (int) Math.sqrt(n);
            for (int i = 2; i <= x; i++) {
                if (n % i == 0) {
                    isPrime = false;
                    break;
                }
            }
        }

        if (isPrime) {
            System.out.println(n + " is a prime number.");
        } else {
            System.out.println(n + " is not a prime number.");
        }
    }
}
