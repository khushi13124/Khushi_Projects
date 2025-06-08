import java.util.Scanner;
import java.io.*;

// X in the program is the choice variable
public class admin
{   
    String[] product_name = new String[20];
    int[] product_price = new int[20];
    int[] stock_product_qty = new int[20];
    int i=0, update_price, update_qty; //used in update_stock
    int j=0; //choice variable for add stock 
    void add_stock()
    {
        String x="y";
        Scanner sc = new Scanner(System.in);
        System.out.println("---Stock Product Details--- ");
        while(x.equalsIgnoreCase("y"))
        {
            if(j>=20)
            {
                System.out.println("Cannot Add more than 20 items!!");
                break;
            }
            System.out.print("Enter Product Name: ");
            product_name[j] = sc.nextLine();

            System.out.print("Enter Product Price: ");
            product_price[j] = sc.nextInt();

            System.out.print("Enter Product Quantity: ");
            stock_product_qty[j] = sc.nextInt();
            System.out.println();
            System.out.print("Do you want to add another product? Y(yes): ");
            x = sc.next();
            sc.nextLine();
            j++;
        }

    }
    void display_stock()
    {
        System.out.println("------------------------------------------------------------------------------------");
        System.out.printf("%-20s %-20s %-20s %-20s %n","Product Number","Product Name","Product Price","Quantity Available");
        System.out.println("------------------------------------------------------------------------------------");
        for(i=0; i<20; i++)
        {
            if(product_name[i] != null)
            {
                System.out.printf("%-20s %-20s %-20s %-20s %n",i+1,product_name[i],product_price[i],stock_product_qty[i]);
            }
        }

    }
    void update_stock()
    {
        int u=0,x;// u- update product number, x- choice var for price and quantity
        String x1="y";
        Scanner sc = new Scanner(System.in);
        display_stock();
        while(x1.equalsIgnoreCase("y"))
        {
            System.out.println("TO UPDATE");
            System.out.print("Enter the product Number: ");
            u = sc.nextInt();
            if(u>=20 || product_name[u-1] == null )
            {
                System.out.println("Invalid Product Number!\nTry Again\n");
                continue;
            }
            System.out.println("What do you want to update?");
            System.out.println("------------------------------------------------------------------------------------");
            System.out.printf("%-20s %-20s %-20s %-20s %n","Product Number","Product Name","Product Price","Quantity Available");
            System.out.println("------------------------------------------------------------------------------------");
            System.out.printf("%-20s %-20s %-20s %-20s %n",u,product_name[u-1],product_price[u-1],stock_product_qty[u-1]);
            System.out.println();
            System.out.print("1.Price\n2.Quantity\n3.Both(Price & Quantity)\nEnter number: ");
            x= sc.nextInt();
            if(x==1)
            {
                System.out.print("Enter new Price: ");
                update_price = sc.nextInt(); 
                product_price[u-1]=update_price;
            }
            else if(x==2)
            {
                System.out.print("Enter Quantity to add: ");
                update_qty = sc.nextInt();
                stock_product_qty[u-1]+=update_qty;   
            }
            else if(x==3)
            {
                System.out.print("Enter Quantity to add: ");
                update_qty = sc.nextInt();
                stock_product_qty[u-1]+=update_qty;
                System.out.print("Enter new Price: ");
                update_price = sc.nextInt(); 
                product_price[u-1]=update_price;
            }
            else
            {
                System.out.println("Invalid Input!!\nTry Again\n"); //K- want to jump line 67
                continue;
            }
            sc.nextLine();
            System.out.println("After Updation");
            System.out.println("------------------------------------------------------------------------------------");
            System.out.printf("%-20s %-20s %-20s %-20s %n","Product Number","Product Name","Product Price","Quantity Available");
            System.out.println("------------------------------------------------------------------------------------");
            System.out.printf("%-20s %-20s %-20s %-20s %n",u,product_name[u-1],product_price[u-1],stock_product_qty[u-1]);
            System.out.println();
            System.out.print("Do you want to update for another product? Y(yes): ");
            x1 = sc.nextLine();       

        }
    }
    void delete_stock()
    {
        //takes invalid value only thrice
        String x3 = "y";
        int count=0;
        int d;
        Scanner sc = new Scanner(System.in);
        while(x3.equalsIgnoreCase("y"))
        {
            System.out.println("To Delete");
            System.out.print("Enter the product Number: ");
            d = sc.nextInt();
            sc.nextLine();
            if(d>20 || product_name[d-1] == null)
            {
                count++;
                System.out.println("Invalid Product Number!!");
                if(count == 3)
                { 
                    count = 0;
                    break; 
                }
                continue;
            }
            else
            {
                for(i=0; i<20; i++)
                {
                    if(product_name[i] != null && (i>=(d-1)))
                    {
                        product_name[d-1]=product_name[i+1];
                        product_price[d-1]=product_price[i+1];
                        stock_product_qty[d-1]= stock_product_qty[i+1];
                        d+=1;
                    }
                }
                System.out.println("Product deleted Successfully!!");
            }
            System.out.print("Do you want to Delete Another Product? y(yes): ");
            x3= sc.nextLine();
        }
        
    }
    void search_stock()
    {
        //2 invalid cases
        String s,x4="y";
        int invalid_count=0;
        int temp;
        int count = 0;
        Scanner sc = new Scanner(System.in);
        while(x4.equalsIgnoreCase("y") && invalid_count <=3)
        {
            System.out.println("To Search");
            System.out.print("Enter the Product Number or Product Name: ");
            s = sc.nextLine();
            if(s.length()==2 && (Character.isDigit(s.charAt(1))) && (Character.isDigit(s.charAt(0))))
            {
                count=0;
                temp = Integer.parseInt(s);
                temp= temp-1;
                for(i=0; i<20; i++)
                {
                    if((i == temp) && ((product_name[i])!= null))
                    {
                        count =1;
                        System.out.println("------------------------------------------------------------------------------------");
                        System.out.printf("%-20s %-20s %-20s %-20s %n","Product Number","Product Name","Product Price","Quantity Available");
                        System.out.println("------------------------------------------------------------------------------------");
                        System.out.printf("%-20s %-20s %-20s %-20s %n",i+1,product_name[i],product_price[i],stock_product_qty[i]);
                        break;
                    }
                }
                if(count == 0)
                {
                    invalid_count++;
                    System.out.println("Product not Found!!");
                    continue;
                }
                if(s.length()>2)
                {
                    invalid_count++;
                    System.out.println("Product not Found!!");
                }
            }
            else if(s.length()==1 && (Character.isDigit(s.charAt(0))))
            {
                count=0;
                temp = Integer.parseInt(s);
                temp= temp-1;
                for(i=0; i<20; i++)
                {
                    if((i == temp) && ((product_name[i])!= null))
                    {
                        count =1;
                        System.out.println("------------------------------------------------------------------------------------");
                        System.out.printf("%-20s %-20s %-20s %-20s %n","Product Number","Product Name","Product Price","Quantity Available");
                        System.out.println("------------------------------------------------------------------------------------");
                        System.out.printf("%-20s %-20s %-20s %-20s %n",i+1,product_name[i],product_price[i],stock_product_qty[i]);
                        break;
                    }
                }
                if(count == 0)
                {
                    invalid_count++;
                    System.out.println("Product not Found!!");
                    continue;
                }
                if(s.length()>2)
                {
                    invalid_count++;
                    System.out.println("Product not Found!!");
                }
            }
            else if(s.equals(null))
            {
                invalid_count++;
                System.out.println("Invalid String!");
                break;
            }
            else 
            {
                count=0;
                try
                {
                    for(i=0; i<20;i++)
                    {
                        if((product_name[i]).equalsIgnoreCase(s))
                        {
                            count = 1;
                            System.out.println("------------------------------------------------------------------------------------");
                            System.out.printf("%-20s %-20s %-20s %-20s %n","Product Number","Product Name","Product Price","Quantity Available");
                            System.out.println("------------------------------------------------------------------------------------");
                            System.out.printf("%-20s %-20s %-20s %-20s %n",i+1,product_name[i],product_price[i],stock_product_qty[i]);   
                            break;
                        }
                    }
                }
                catch(Exception e)
                {
                    invalid_count++;
                }
                if(count == 0 )
                {
                    invalid_count++;
                    System.out.println("Product not Found!!");
                    continue;
                }
            }
            System.out.print("Do you want to Search another Product? y(Yes): ");
            x4 = sc.nextLine();
        }
    }
}