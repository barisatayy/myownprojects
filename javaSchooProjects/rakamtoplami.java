package schoolProject;
import java.util.Scanner;

public class rakamtoplami {

    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.println("bir sayı giriniz");
        int n = input.nextInt();
        int l = 0;
        while (n > 0) {
            int k = n % 10;
            n = n / 10;
            l = l + k * k * k;
        }
        if (l == n) {
            System.out.println("sayınızın basamaklarının küplerinin toplamı sayıya eşittir");
        } else {
            System.out.println("değildir");
        }
        System.out.println("basamaklarının küplerinin toplamı= " + l);
    }

}
