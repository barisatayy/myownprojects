package schoolProject;
import java.util.Scanner;
public class us {
     

    
    public static void main(String[] args) {
     Scanner input = new Scanner(System.in);
     
     System.out.println("Üs almak istediğiniz sayıyı giriniz");
     int taban= input.nextInt();
     
     System.out.println("Üssü giriniz");
     int us=input.nextInt();
     
     int sonuc=1;
     for(int i=1; i<=us; i++)
     {
        sonuc=sonuc*taban;
     }

     System.out.println(sonuc);
    }
    }

