#include<iostream>
#include<iomanip>
#include<fstream>
#include<string.h>
#include<stdlib.h>
using namespace std;
class admin
{
		private:
			int productno,product_qty;
			char product_name[20];
			float product_price;
		public:
			void add_product()
			{
				productno=productno+1;
				cout<<"Enter product name : ";
				cin>>product_name;
				cout<<"Enter product Qty : ";
				cin>>product_qty;
				cout<<"Enter product price : ";
				cin>>product_price;	
			}
			void display_products()
			{
				cout<<endl<<productno<<setw(15)<<product_name<<setw(15)<<product_qty<<setw(15)<<product_price;
			}
			int get_productno()
			{
				return productno;
			}	
			int get_qty()
			{
				return product_qty;
			}
			int get_product_price()
			{
				return product_price;
			}
			string get_pname()
			{
				return product_name;
			}
			void update_qty(int qty)
			{
				product_qty=qty;
			}
			void update_price(int price)
			{
				product_price=price;
			}	
			void new_qty(int qty)
			{
				product_qty=product_qty-qty;
			}		
};
		
admin a;
fstream f;
void write()
{
	f.open("supermarket.dat",ios::binary|ios::app);
	a.add_product();
	f.write((char*)&a,sizeof(a));
	f.close();
}
void read()
{
	f.open("supermarket.dat",ios::binary|ios::in);
	cout<<endl<<"SRNO."<<setw(15)<<"PRODUCT NAME"<<setw(15)<<"QUANTITY"<<setw(13)<<"PRICE";
	cout<<endl<<"-----------------------------------------------------------";
	while(f.read((char*)&a,sizeof(a)))
	{
		a.display_products();
	}	
	cout<<endl<<"------------------------------------------------------------";
	f.close();
}
void update_product()
{
	int flag=0,qty,price;
	int productno;
	f.open("supermarket.dat",ios::binary|ios::in|ios::out);
	if(!f)
	{
		cout<<endl<<" File Not Found ";
		return;                         
	}
	else
	{
		cout<<"Enter product no. : ";
		cin>>productno;
		while(f)
		{
			if(f.read((char*)&a,sizeof(a)))
			{
				int p=f.tellg();
				int uch;
				if(a.get_productno()==productno)
				{
					flag=1;
					cout<<"\n1.Quantity\n2.Price\n";
					cout<<"What do you want to update?";
					cin>>uch;
					if(uch==1)
					{
						cout<<endl<<"Enter qty to add: ";
						cin>>qty;
						a.update_qty(a.get_qty()+qty);
						cout<<endl<<"-----------------------------------------------------------";
						a.display_products();
						cout<<endl<<"-----------------------------------------------------------";
						cout<<endl<<"Successful ";
						f.seekp(p-sizeof(a));
						f.write((char*)&a,sizeof(a));
						break;
					}
					else if(uch==2)
					{
						cout<<endl<<"Enter new price : ";
						cin>>price;
						a.update_price(price);
						cout<<endl<<"-----------------------------------------------------------";
						a.display_products();
						cout<<endl<<"-----------------------------------------------------------";
						cout<<endl<<"Successful ";
						f.seekp(p-sizeof(a));
						f.write((char*)&a,sizeof(a));
						break;
					}
					else
					{
						cout<<"Invalid choice";
					}
				}
			}
		}
		if(flag==0)
		{
			cout<<endl<<"No Data Found ";
		}
		f.close();
	}
}

void delete_product()
{
	int productno;
	fstream file;
	cout<<endl<<"Enter product number of product you want delete: ";
	cin>>productno;
	f.open("supermarket.dat",ios::binary|ios::in);
	file.open("new.dat",ios::binary|ios::app);
	while(f)
		{
			if(f.read((char*)&a,sizeof(a)))
			{
				if(a.get_productno()!=productno)
				{
					file.write((char*)&a,sizeof(a));
				}
			}
		}
	f.close();
	file.close();
	remove("supermarket.dat");
	rename("new.dat","supermarket.dat");
}

void search_product()
{
	int productno,flag=0;
	cout<<"Enter product no. : ";
	cin>>productno;
	f.open("supermarket.dat",ios::binary|ios::in);
	if(!f)
	{
		cout<<endl<<"File Error";return;
	}
	else
	{
		while(f)
		{
			if(f.read((char*)&a,sizeof(a)))
			{
				if(a.get_productno()==productno)
				{
					cout<<"Record Found "<<endl;
					cout<<endl<<"-----------------------------------------------------------";
					a.display_products();
					cout<<endl<<"-----------------------------------------------------------";
					flag=1;
					break;
				}
			}
		}
		if(flag==0)
		{
			cout<<endl<<"No Data Found";
		}
		f.close();
	}
}

class user
{	
	private:
		float totalprice,netprice,discount,cgst,sgst,purchase_product_price[20],purchase_product_total_price[20];
		int qty,count=0,productno,purchase_product_no[20],purchase_product_qty[20],totalproducts;
		char c,product_name[20]={},purchase_product_name[20][20]={};
		char name[20];	
	public:
		void get()
		{
			cout<<endl<<"Enter customer name : ";
			cin>>name;
			while(1)
			{
				char product_name[20]={};
				int i,flag=0;
				read();
				f.open("supermarket.dat",ios::binary|ios::out|ios::in);
				cout<<"\nEnter product no. : ";
				cin>>productno;
				while(f.read((char*)&a,sizeof(a)))
				{
					int tell=f.tellp();
					if(productno==a.get_productno())
					{
						flag=1;
						cout<<"Enter quantity : ";
						cin>>qty;
						if(a.get_qty()>=qty)
						{
							a.new_qty(qty);
							f.seekp(tell-sizeof(a));
							f.write((char*)&a,sizeof(a));
							purchase_product_price[count]=a.get_product_price();
							purchase_product_total_price[count]=a.get_product_price()*qty;
						 	purchase_product_no[count]=a.get_productno();
							purchase_product_qty[count]=qty;
							string hh=a.get_pname();
							strcpy(purchase_product_name[count],hh.c_str());
							totalprice=totalprice+purchase_product_total_price[count];
							count++;
						}
						break;
					}	
				}
				f.close();
				cout<<endl<<"Do you want to continue y-yes,n-no : ";cin>>c;
				if(c=='n')
				{
					break;
				}
			}
			totalproducts=count;
			if(totalprice>=500)
			{
				discount=(totalprice*0.10);
				totalprice=totalprice-discount;
			}
			else
			{
				discount=0;
			}
			cgst=totalprice*0.025;
			sgst=totalprice*0.025;
			netprice=totalprice+cgst+sgst;
		}
		void display_bill()
		{
			cout<<endl<<"-----------------------------------------------------------";
			cout<<endl<<endl<<"CUSTOMER NAME : "<<name<<endl;
			cout<<endl<<"SRNO."<<setw(15)<<"PRODUCT NAME"<<setw(15)<<"QUANTITY"<<setw(15)<<"P PRICE"<<setw(15)<<"Total Price";
			cout<<endl<<"-----------------------------------------------------------";
			for(int i=0;i<totalproducts;i++)
			{
				cout<<endl<<purchase_product_no[i]<<setw(15)<<purchase_product_name[i]<<setw(15)<<purchase_product_qty[i]<<setw(15)<<purchase_product_price[i]<<setw(15)<<purchase_product_total_price[i];	
			}
			cout<<endl<<"-----------------------------------------------------------";
			cout<<endl<<"TOTALPRICE : "<<totalprice;
			cout<<endl<<"DISCOUNT : "<<discount;
			cout<<endl<<"CGST : "<<cgst;
			cout<<endl<<"SGST : "<<sgst;
			cout<<endl<<"NETPRICE : "<<netprice;
			cout<<endl<<"-----------------------------------------------------------";
		}	
		int get_tp()
		{
			return totalproducts;
		}
};

user u;
fstream file;
void write_u()
{
	file.open("BILL.dat",ios::binary|ios::app);
	u.get();
	u.display_bill();
	f.write((char*)&u,sizeof(u));
	f.close();
}

int main()
{
		
		char id[10],p[10];
		char userid[10]="admin";
		char password[10]="login";
		int ch,clr;
		cout<<"Enter correct credentials to login to the management system\n";
		cout<<"Enter Userid : ";
		cin>>id;
		cout<<"Enter password : ";
		cin>>p;
		if((strcmp(id,userid)==0) && (strcmp(p,password)==0))
		{
			system("cls");
			while(1)
			{
				cout<<"******WELCOME TO MODERN SUPERMARKET MANAGEMENT SYSTEM*****";
				cout<<"\n\n----SELECTION MENU----\n"<<endl;
				cout<<"1.ADD PRODUCT"<<endl;
				cout<<"2.DISPLAY PRODUCT"<<endl;
				cout<<"3.UPDATE PRODUCT DETAILS"<<endl;
				cout<<"4.SEARCH PRODUCT"<<endl;
				cout<<"5.DELETE PRODUCT"<<endl;
				cout<<"6.BILL"<<endl;
				cout<<"7.EXIT"<<endl;	
				cout<<endl<<"Enter your choice : ";
				cin>>ch;
				switch(ch)
				{
					case 1:
						write();
						break;
					case 2:
						cout<<endl<<"-----------------------------------------------------------";
						read();
						break;
					case 3:
						update_product();
						break;
					case 4:
						search_product();
						break;
					case 5:
						delete_product();
						break;
					case 6:
						write_u();
						break;
					case 7:
						cout<<"Exit!";
						exit(0);
						break;
					default:
						cout<<"Invalid choice";
						break;
				}
				cout<<"\nPress 1 to continue:";
				cin>>clr;
				if(clr==1)
				{
					system("cls");
				}
				else
				{
					exit(0);
				}
			}
		}
		else
		{
			cout<<"INVALID LOGIN CREDENTIALS!\nPLEASE TRY AGAIN";
		}
		return 0;
}
