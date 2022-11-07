package projects;

import java.util.Scanner;
import java.util.Random;

public class numberguesser {

    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        Random pcsayi = new Random();
        System.out.println("sayıyı bulmak için 3 hakkınız var\n"+"bir sayı giriniz");
        int rand = pcsayi.nextInt(10);
        int hak = 0;
        while (true) {
            if (hak == 3) {
                System.out.println("Hakkınız bitti.");
                break;
            } else {
                int sayi = input.nextInt();
                if (sayi == rand) {
                    System.out.println("sayıyı doğru bildiniz");
                    break;
                } else {
                    System.out.println("tekrar deneyiniz");
                    hak++;
                }
            }

        }
    }
}
