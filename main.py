import customtkinter as ctk
from tkinter import messagebox
import json
import os
from  geopy.distance import geodesic

class Page(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

class MainPage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        # widget initialisation
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)

        self.label = ctk.CTkLabel(self, text="Herzlich Willkommen")
        self.label.grid(row=1, column=0, padx=(2,2), sticky="nsew")

        btn_select_ticket = ctk.CTkButton(self, text="Ticket auswählen",
                                                    command=lambda: controller.show_frame("FindTicket"))
        btn_select_ticket.grid(row=2, column=0, pady=2 )


class FindTicket(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        # Define labels and entry fields
        self.label_schedule = ctk.CTkLabel(self, text='Fahrplan', anchor='w', font=('Roboto', 14))
        self.entry_start = ctk.CTkEntry(self, placeholder_text='Start eingeben')
        self.entry_destination = ctk.CTkEntry(self, placeholder_text='Ziel eingeben...')
        self.label_euro = ctk.CTkLabel(self, text='€', anchor='w', font=('Roboto', 14))
        self.label_price = ctk.CTkLabel(self, text='Preis: ', anchor='w', font=('Roboto', 14))
        self.button_find = ctk.CTkButton(self, text="Suchen", command=self.validate_entry, font=('Roboto', 14))
        self.button_confirm = ctk.CTkButton(self, text='Bestätigen', command=self.btn_confirm_click, state='disabled', font=('Roboto', 14))
        
        # self.button_back = ctk.CTkButton(self, text='<', width=10, command=lambda: controller.show_frame("MainPage"))

        self.listCities = self.load_cities()
        self.city_names = [city['name'] for city in self.listCities] if self.listCities else []
        
        # Grid placement with padding
        # self.button_back.grid(row=0, column=0, pady=(10, 2), padx=20, sticky='w')    
        self.label_schedule.grid(row=1, column=0, pady=(50, 10), padx=20, sticky='w')
        self.entry_start.grid(row=2, column=0, columnspan=2, pady=(2, 2), padx=20, sticky='we')
        self.entry_destination.grid(row=3, column=0, columnspan=2, pady=(2, 2), padx=20, sticky='we')
        self.button_find.grid(row=4, column=0, pady=(2,2), padx=(20), sticky='w')
        self.label_euro.grid(row=5, column=0, pady=(2,2), padx=10, sticky='w')
        self.label_price.grid(row=5, column=0, pady=(2, 2), padx=20, sticky='w')
        # self.label_sum.grid(row=5, column=1, pady=(2, 2), padx=20, sticky='e')
        self.button_confirm.grid(row=6, column=1, pady=(2, 20), padx=20, sticky='e')

        # Configure the grid layout behavior
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)

    def load_cities(self):
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, 'germany.json')
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print("Error reading file:", str(e))
        else:
            print("File does not exist.")

    def btn_confirm_click(self):
        if self.validate_entry() and self.controller.selected_start is None:
            self.controller.selected_start = self.entry_start.get()
            self.controller.selected_destination = self.entry_destination.get()
            self.controller.calculated_price = self.label_price.cget('text')
             # Create the AddTicketPage instance here
            add_ticket_page = self.controller.get_page("AddTicketPage")
            add_ticket_page.update_ui()

            # print(f'find ticket class {self.controller.selected_start}')
            self.controller.show_frame("AddTicketPage")
            

    def get_lat_long(self, city_name):
        for city in self.listCities:
            if city['name'] == city_name:
                return (city['coords']['lat'], city['coords']['lon'])

    def get_distance_price(self, start_city, destination_city):
        start_coords = self.get_lat_long(start_city)
        destination_coords = self.get_lat_long(destination_city)
        distance = geodesic(start_coords, destination_coords).kilometers
        if 0 < distance < 50:
            rate = 0.30
        elif 50 <= distance < 100:
            rate = 0.15
        else:
            rate = 0.10
        return distance * rate

    def validate_entry(self):
        start = self.entry_start.get()
        destination = self.entry_destination.get()
        if start and destination and start != destination:
            if start in self.city_names and destination in self.city_names:
                price = self.get_distance_price(start, destination)
                self.label_price.configure(text=f'{round(price, 2)}')
                self.button_confirm.configure(state='normal')
                return True
            else:
                messagebox.showerror("Ungültige Stadt", "Die eingegebene Stadt ist ungültig. Bitte geben Sie eine gültige Stadt ein.")
        else:
            messagebox.showerror("Leeres Feld", "Bitte geben Sie Start- und Zielstadt in die bereitgestellten Felder ein.")
        return False


class AddTicketPage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        # Define labels and entry fields
        self.btn_back = ctk.CTkButton(self, text='<', width=10, command=lambda: controller.show_frame("FindTicket"))
        self.btn_buy = ctk.CTkButton(self, text='Zur Zahlung', command=self.go_to_payment, font=('Roboto', 14))
       
        # Create a frame to hold the grid cells
        self.frame_card = ctk.CTkFrame(self)
        self.frame_card.grid(row=1, column=0, columnspan=6, padx=10, pady=(50,2), sticky='ew')

        # Ensure the window can accommodate two columns
        for i in range(6):
            self.columnconfigure(i, weight=1)
            
     
        self.btn_buy.grid(row=3, column=5, padx=10, pady=10, sticky='e')

        # Frame for card 1
        self.lb_card_1 = ctk.CTkLabel(self.frame_card, anchor='w', font=('Roboto', 14))
        self.btn_edit_card1 = ctk.CTkButton(self.frame_card, text='+', width=50, font=('Roboto', 14))
        self.lb_preis_1 = ctk.CTkLabel(self.frame_card, font=('Roboto', 14))

        # Frame grid configuration
        for i in range(3):
            self.frame_card.columnconfigure(i, weight=1)

        # Placement for card inside frame

        self.lb_card_1.grid(row=0, column=1, columnspan=3, padx=10, pady=10, sticky='w')
        self.lb_preis_1.grid(row=0, column=3, columnspan=3, padx=10, pady=10, sticky='w')

    def go_to_payment(self):
        zahlung_method_page = self.controller.get_page("PaymentMethod")
        zahlung_method_page.update_payment_page()
        self.controller.show_frame("PaymentMethod")

    def confirm_selection(self):
        # This method seems to be unused, consider removing it if it's not needed
        print("Bestätigung wurde geklickt")

    def update_ui(self):
        # Update the label with the latest price
        self.lb_card_1.configure(text=f'{self.controller.selected_start} nach {self.controller.selected_destination}')
        self.lb_preis_1.configure(text=f'€ {self.controller.calculated_price}')
   


class PaymentMethod(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.lb_payment = ctk.CTkLabel(self, text='Zahlungsmethoden', font=('Roboto', 14))
        self.lb_items = ctk.CTkLabel(self, text='', font=('Roboto', 14))
        self.lb_instruction = ctk.CTkLabel(self, text='Wählen Sie eine Zahlungsmethode aus', font=('Roboto', 14))
        self.btn_with_card = ctk.CTkButton(self, text='EC Karte', command=self.go_to_ec_card_page, font=('Roboto', 14))
        self.btn_cash = ctk.CTkButton(self, text='Bar', command=self.go_to_cash_update_ui, font=('Roboto', 14))
        self.btn_back = ctk.CTkButton(self, text='<', command= lambda: controller.show_frame('AddTicketPage'), width = 10, font=('Roboto', 14))

        # root column configuration
        self.columnconfigure(0, weight=1)

        # root widget placement
        self.btn_back.grid(row=0, column=0, pady=(10, 2), padx=20, sticky='w')
        self.lb_payment.grid(row=1, column=0, pady=(10, 2), padx=20, sticky='ew')
        self.lb_instruction.grid(row=2, column=0, pady=(10, 2), padx=20, sticky='ew')
        self.lb_items.grid(row=3, column=0, pady=(10, 2), padx=20, sticky='ew')
        self.btn_with_card.grid(row=4, column=0, pady=(10, 2), padx=20, sticky='ew')
        self.btn_cash.grid(row=5, column=0, pady=(10, 2), padx=20, sticky='ew')

    # for previous page
    def update_payment_page(self):
        self.lb_items.configure(text=f'{self.controller.selected_start} nach {self.controller.selected_destination}  {self.controller.calculated_price}')

    # go to ec card:
    def go_to_ec_card_page(self):
        ec_card_page = self.controller.get_page("EcCard")
        ec_card_page.update_ui_payment()
        self.controller.show_frame("EcCard")

    # call to update ui from cash
    def go_to_cash_update_ui(self):
        cash_page = self.controller.get_page("Cash")
        cash_page.update_ui_calculated_price()
        self.controller.show_frame("Cash")
        

class EcCard(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.columnconfigure(0, weight=1)

        self.lb_payment = ctk.CTkLabel(self, font=('Roboto', 14))
        self.lb_instruction = ctk.CTkLabel(self, text='Bitte Ihre EC Karte einscannen', font=('Roboto', 14))
        self.btn_ec_karte = ctk.CTkButton(self, text='EC Karte einscannen', font=('Roboto', 14), command=self.btn_ec_karte_click, state='normal')
        self.btn_fertig = ctk.CTkButton(self, text='Karte ausdrücken', command=self.go_to_print_start_countdown,font=('Roboto', 14))        
        self.btn_back = ctk.CTkButton(self, text='<', width = 10, command=lambda: controller.show_frame("PaymentMethod"), font=('Roboto', 14))
        
        # root widget placement
        self.lb_payment.grid(row=1, column=0, columnspan=2, pady=(10, 2), padx=20, sticky='ew')
        self.lb_instruction.grid(row=2, column=0, columnspan=2, pady=(10, 2), padx=20, sticky='ew')
        self.btn_ec_karte.grid(row=3, column=0, columnspan=2, pady=(10, 2), padx=20, sticky='ew')
        self.btn_back.grid(row=0, column=0, pady=(5, 2), padx=10, sticky='w')
   
    # zu PrintCard gehen und Countdown starten:
    def go_to_print_start_countdown(self):
        print_card_page = self.controller.get_page("PrintTicket")
        print_card_page.processing(5)
        self.controller.show_frame("PrintTicket")

    def check_card(self):
        self.lb_instruction.configure(text='Karte geprüft.')
        self.btn_fertig.grid(row=7, column=0, pady=10, padx=20, sticky='ew')
        self.btn_ec_karte.destroy()
        self.lb_payment.configure(text='')
    
    def btn_ec_karte_click(self):
        self.lb_instruction.configure(text='Bitte warten... Karte wird geprüft')
        self.btn_ec_karte.configure(state='disabled')
        self.after(3000, self.check_card)             

    # to be called from PaymentMethod, show calculated_price
    def update_ui_payment(self):
        self.lb_payment.configure(text=f'Zu zahlen : {self.controller.calculated_price}')
        

class PrintTicket(Page):
    def __init__(self,parent,controller):
        super().__init__(parent, controller)
        # configure root column
        self.columnconfigure(0, weight=2)
        self.rowconfigure(3, weight=2)
        self.loading_sign = '|/-\\'
        self.lb_message = ctk.CTkLabel(self, text="")
        self.lb_message.grid(row=1, column=0, pady=(100,20), sticky="ew")
        self.btn_back = ctk.CTkButton(self, text="Beenden", command=self.quit)

    def update_label(self,countdown):
        if countdown > 0:
            self.lb_message.configure(text=f"Bitte warten... \n Karte wird in {countdown} Sekunden gedruckt {self.loading_sign[countdown % len(self.loading_sign)]}")
            self.after(1000, self.update_label, countdown-1)
        else:
            self.lb_message.configure(text="Ihre Karte wurde ausgedruckt. Schöne Reise!")
            self.btn_back.grid(row=2, column=0, pady=5,  sticky="n")

    def processing(self,seconds):
        self.update_label(seconds)


class Cash(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.given_money = 0
        self.returned_money = 0

        # root column configuration
        self.columnconfigure(0, weight=1)
        self.frame_money = ctk.CTkFrame(self)
        self.frame_money.columnconfigure(0, weight=1)
        self.frame_money.columnconfigure(1, weight=1)
        self.frame_money.grid(row=6, column=0, pady=10, padx=20, sticky='ew')

        self.btn_back = ctk.CTkButton(self, text='<', width = 10, command=lambda: controller.show_frame("PaymentMethod"), font=('Roboto', 14))
        self.lb_payment = ctk.CTkLabel(self, font=('Roboto', 14))
        self.lb_beitrag = ctk.CTkLabel(self, text='Ihr Beitrag:', font=('Roboto', 14))
        self.lb_instruction = ctk.CTkLabel(self, text='Bitte werfen Sie Ihr Geld ein', font=('Roboto', 14))
        self.btn_five_euros= ctk.CTkButton(self.frame_money, text='5€', font=('Roboto', 14), command= lambda: self.calculate_remaining_amount(5))
        self.btn_ten_euros = ctk.CTkButton(self.frame_money, text='10€', font=('Roboto', 14), command= lambda: self.calculate_remaining_amount(10))
        self.btn_twenty_euros = ctk.CTkButton(self.frame_money, text='20€', font=('Roboto', 14), command= lambda: self.calculate_remaining_amount(20))
        self.btn_fifty_euros = ctk.CTkButton(self.frame_money, text='50€', font=('Roboto', 14), command= lambda: self.calculate_remaining_amount(50))
        self.btn_fertig = ctk.CTkButton(self, state='disabled', text='Karte ausdrücken', font=('Roboto', 14))

        # root widget placement
        self.btn_back.grid(row=0, column=0, pady=(5, 2), padx=10, sticky='w')
        self.lb_payment.grid(row=1, column=0, columnspan=2, pady=(10, 2), padx=10, sticky='ew')
        self.lb_instruction.grid(row=2, column=0, columnspan=2, pady=(10, 2), padx=10, sticky='ew')
        self.lb_beitrag.grid(row=3, column=0, pady=(5, 2), columnspan=2,padx=20, sticky='ew')
        self.btn_fertig.grid(row=7, column=0, pady=5, padx=5, sticky='ew')

        # frame_money widget placement
        self.btn_five_euros.grid(row=4, column=0, pady=5, padx=10, sticky='ew')
        self.btn_ten_euros.grid(row=4, column=1, pady=5, padx=10, sticky='ew')
        self.btn_twenty_euros.grid(row=5, column=0, pady=5, padx=10, sticky='ew')
        self.btn_fifty_euros.grid(row=5, column=1, pady=5, padx=10, sticky='ew')

        # update ui
    def update_ui_calculated_price(self):
        self.lb_payment.configure(text=f'Zu zahlen : {self.controller.calculated_price}')

    def given_money(self, money):
        given_money += money
        self.lb_beitrag.configure(text=f'Ihr Beitrag : {str(given_money)}')  

    def calculate_remaining_amount(self, amount):
        self.given_money += amount
        remaining = round((float(self.controller.calculated_price) - self.given_money),2)
        if remaining > 0:
            self.lb_payment.configure(text=f'Zu zahlen: {remaining}')
            self.lb_beitrag.configure(text=f'Ihr Beitrag: {self.given_money}')
        elif remaining < 0:
            self.returned_money = round((self.given_money - float(self.controller.calculated_price)),2)
            self.lb_payment.configure(text=f'Ihr Rückgeld {self.returned_money} ')
            self.lb_beitrag.configure(text=f'Ihr Beitrag: {self.controller.calculated_price}')
            self.lb_instruction.configure(text="")    
            self.btn_fertig.configure(state='enable', command=self.go_to_print_start_countdown)
            self.btn_five_euros.configure(state='disabled')
            self.btn_ten_euros.configure(state='disabled')
            self.btn_twenty_euros.configure(state='disabled')
            self.btn_fifty_euros.configure(state='disabled')
    
    def go_to_print_start_countdown(self):
        print_card_page = self.controller.get_page("PrintTicket")
        print_card_page.processing(5)
        self.controller.show_frame("PrintTicket")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Fahrkartenautomat")
        self.geometry("400x300")

        # Attributes to store ticket information
        self.selected_start = None
        self.selected_destination = None
        self.calculated_price = None

        self.frames = {}
        for F in (MainPage, FindTicket, AddTicketPage, PaymentMethod, EcCard, PrintTicket, Cash):
            frame = F(parent=self, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)    
        self.show_frame("MainPage")
       

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def get_page(self, page_class):
        return self.frames[page_class]

app = App()
app.mainloop()
