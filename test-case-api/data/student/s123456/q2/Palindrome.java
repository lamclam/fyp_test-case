
import java.util.Scanner;

public class PrimeNumber {

    public static void main(String[] args) {

        Scanner input = new Scanner(System.in);
        
        boolean prime = true;
        
            System.out.println("Enter a number: ");
            int num = input.nextInt();
            int n = (int) Math.sqrt(num);
            
            for (int i = 2; i <= n; i++) {
                if (num%i == 0) {
                    prime = false;
                    break;
                }
            }       
            if(!prime){
            System.out.println(num + " is a not a prime number");
            }
            else{
            System.out.println(num + " is  a prime number");    
            }
        }
        
    
}
