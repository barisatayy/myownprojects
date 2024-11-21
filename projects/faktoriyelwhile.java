/*
adım1: başla
adım2: a değeri al
adım3: fakt=1, s=1
adım4: s<=a ise fakt=fakt*s s=s+1
adım5: faktöriyeli yazdır
adım6: bitir
 */
package schoolProject;

import java.util.Scanner;

public class faktoriyelwhile {

    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.println("bir sayı giriniz");
        int a = input.nextInt();
        int fakt = 1;
        int s = 1;
        while (s <= a) {
            fakt = fakt * s;
            s = s + 1;
        }
        System.out.println(a + " sayısının faktöriyeli= " + fakt);
    }

}
