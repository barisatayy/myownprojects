package schoolProject;

import java.util.Scanner;

public class basamakOgrenme {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.println("pay giriniz");
        int pay = input.nextInt();
        System.out.println("payda giriniz");
        int payda = input.nextInt();
        int k = pay / payda;
        int r = 0;
        System.out.println(k);
        System.out.println("kaçıncı basamağı öğrenmek istediğinizi seçin");
        int n = input.nextInt();
        for (int i = 1; i <= n; i++) {
            r = k % 10;
            k = k / 10;
        }
        System.out.println(r);
    }
}
