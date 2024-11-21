package schoolProject;

import java.util.Scanner;

public class ikininkatlari {

    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.println("bir sayı giriniz");
        int n = input.nextInt();
        int deger = 2;
        System.out.println(deger);
        while (deger < n) {
            deger = deger * 2;
            if (deger > n) {
                break;
            }

            System.out.println(deger);
        }
    }

}
