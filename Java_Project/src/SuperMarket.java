import java.util.Scanner;

public class SuperMarket 
{
    public static void main(String[] args) 
    {
        String user_id = "admin";
        String password = "login";
        String u,p;
        int x=1,ch,i=0; //ch-choice menu, x= login credentials
        String x1 = "y"; // loop variable for menu
        String x2 = "y";
        Scanner sc = new Scanner(System.in);
        System.out.println("ENTER LOGIN CREDENTIALS");
        while(x==1)
        {
            System.out.print("User Id: ");
            u = sc.nextLine();
            System.out.print("Password: ");
            p = sc.nextLine();
            if(u.equals(user_id) && p.equals(password))
            {
                break;
            }
            else
            {
                System.out.print("Wrong Login Credentials!\nPress 1. To Try Again\t2.To Exit: ");
                x = sc.nextInt();
                sc.nextLine();
                if(x==1)
                {
                    continue;
                }
                else if(x==2)
                {
                    return;
                }
                else 
                {
                    System.out.println("Invalid Input!!");
                }
            }
        }
        admin a1 = new admin();
        user u1 = new user();
        System.out.print("\033[H\033[2J"); // clear the output screen
        while(x1.equalsIgnoreCase("y"))
        {
            System.out.println("SUPERMARKET MANAGEMENT SYSTEM");
            System.out.println();
            System.out.println("---Selection Menu---");
            System.out.println("1. Add Stock");
            System.out.println("2. Display Stock");
            System.out.println("3. Update Stock");
            System.out.println("4. Delete Stock");
            System.out.println("5. Search product");
            System.out.println("6. Take order & Display Bill");
            System.out.println("7. Exit");
            System.out.print("Enter your choice: ");
            ch = sc.nextInt();
            switch (ch) 
            {
                case 1:
                {
                    a1.add_stock();
                    break;
                }
                case 2:
                {
                    a1.display_stock();
                    break;
                }
                case 3:
                {
                    a1.update_stock();
                    break;
                }
                case 4:
                {
                    a1.delete_stock();
                    break;
                }
                case 5:
                {
                    a1.search_stock();
                    break;
                }
                case 6:
                {
                    while (x2.equalsIgnoreCase("y"))
                    {
                        System.out.println("Enter Data for Customer "+(i+1));
                        u1.take_order(a1);
                        sc.nextLine();
                        System.out.print("Do you want to continue for another customer? Y(yes)/N(no) ");
                        x2 = sc.nextLine();
                        System.out.print("\033[H\033[2J");
                        i++;                       
                    }
                    break;
                }
                case 7:
                {
                    System.out.println("Program Executed succesfully!!");
                    return;
                }
                default:
                    break;
            }
            sc.nextLine();
            System.out.print("To Continue to Main Menu, Press Y(yes)/N(no): ");
            x1 = sc.nextLine();
            System.out.print("\033[H\033[2J");

        }
    }
    
}