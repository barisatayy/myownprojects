package projects;

import java.util.Scanner;

public class ikininkatlarifor {

    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.println("bir sayı giriniz");
        int k = input.nextInt();
        int deger = 2;
        for (int i = deger; deger < k; i++) {
            deger = deger * 2;
            System.out.println(deger);
            if (i >= k) {
                break;
            }
        }
    }
}
