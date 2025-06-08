import java.util.Scanner;

public class user 
{
    String cust_name;
    double bill=0;
    double total_bill, cgst_bill, sgst_bill;
    int total_order_items;
    int[] order_product_no = new int[20];
    int[] order_product_qty = new int[20];
    int[] order_product_price = new int[20];
    String[] order_product_name = new String[20];
    int i;

    void take_order(admin a1)
    {
        a1.display_stock();
        System.out.println();
        Scanner sc = new Scanner(System.in);
        sc.nextLine();
        System.out.print("Enter Customer Name: ");
        cust_name = sc.nextLine();
        System.out.print("How many Products do you want to Order? ");
        total_order_items = sc.nextInt();
        if(total_order_items <= a1.j-1)
        {
            for(i=0; i<total_order_items; i++)
            {
                System.out.print("Enter Product Number of Item "+(i+1)+": ");
                order_product_no[i] = sc.nextInt();
                if(order_product_no[i]>20||order_product_no[i]<=0)
                {
                    System.out.println("Indvalid Product Number\nTry Again");
                    break;
                }
                System.out.print("Enter Quantity of Product: ");
                order_product_qty[i] = sc.nextInt();
                if(order_product_qty[i] > (a1.stock_product_qty[order_product_no[i]-1]) )
                {
                    System.out.print("Try Again!!\nInput Quantity Exceeds the Availabe Quantity");
                    break;
                }
                else if(order_product_qty[i]<=0)
                {
                    System.out.println("Invalid Product Quantity");
                    break;
                }
                order_product_name[i]= a1.product_name[order_product_no[i]-1];
                order_product_price[i]=a1.product_price[order_product_no[i]-1];
            }
            for(i=0; i<total_order_items; i++) //for Updation after ordering
            {
                a1.stock_product_qty[order_product_no[i]-1]-=order_product_qty[i];
            }
            for(i=0; i<total_order_items; i++)
            {
                bill += (order_product_price[i]*order_product_qty[i]);
                sgst_bill = bill*0.025;
                cgst_bill = bill*0.025;
                total_bill = bill + sgst_bill + cgst_bill; 
            }
            display_bill(a1);
        }
        else
        {
            System.out.println("Enough items are not available!!");
            return;
        }
    }
    void display_bill(admin a1)
    {
        System.out.println("---------------------------------------------------------------------------------");
        System.out.printf("%-20s %-20s %-20s %-20s %n","Sr No","Product Name","Order Price","Product Quantity");
        System.out.println("------------------------------------------------------------------------------------");
        for(i=0; i<total_order_items; i++)
        {
            System.out.printf("%-20s %-20s %-20s %-20s %n",i+1,order_product_name[i],order_product_qty[i],order_product_price[i]*order_product_qty[i]);
        }
        System.out.println("------------------------------------------------------------------------------------");
        System.out.println("Total Price: "+bill);
        System.out.println("CGST: "+cgst_bill);
        System.out.println("SGST: "+sgst_bill);
        System.out.println("Net Price: "+ total_bill);
        System.out.println("------------------------------------------------------------------------------------");
    }

}
