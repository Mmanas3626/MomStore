#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import telebot
from telebot import types
import random
from tkinter import *
from prettytable import PrettyTable

# Set up the bot with your token
TOKEN = '5901938908:AAGGKpG3_cpjqoLv_6rXrOn9uONNGV79Qeo'
bot = telebot.TeleBot(TOKEN)
total_price=0
# Define the list of items in inventory
inventory = [
    {"name": "Chocolates", "price": 10, "quantity": 500, "weight": "500g", "type": "food", "brand": "Eco-clairs"},
    {"name": "Biscuits", "price": 20, "quantity": 100, "weight": "500g", "type": "food", "brand": "MARI-GOLD"},
    {"name": "Soaps", "price": 30, "quantity": 200, "weight": "10g", "type": "personal", "brand": "LUX"},
    {"name": "Brush", "price": 40, "quantity": 800, "weight": "3g", "type": "personal", "brand": "COLGATE"},
    {"name": "Television", "price": 50, "quantity": 60, "weight": "1kg", "type": "electronics", "brand": "TCL"},
    {"name": "Mixture", "price": 60, "quantity": 40, "weight": "2kg", "type": "food", "brand": "BOONDHI"},
    {"name": "Oil", "price": 70, "quantity": 30, "weight": "3kg", "type": "food", "brand": "COCONUT"},
    {"name": "Shirt", "price": 80, "quantity": 120, "weight": "0.5g", "type": "Clothing", "brand": "OTTO"},
    {"name": "Maidha", "price": 90, "quantity": 100, "weight": "5kg", "type": "food", "brand": "AASHIRVAD"},
    {"name": "haldirams", "price": 100, "quantity": 700, "weight": "6kg", "type": "food", "brand": "HALDI"}
]


# Define the headings for the table
headers = ["Name", "Price", "Quantity", "Weight", "Type", "Brand"]

# Create a new table with the specified headers
table = PrettyTable(headers)

# Add the data from the inventory to the table
for item in inventory:
    table.add_row([item["name"], item["price"], item["quantity"], item["weight"], item["type"], item["brand"]])
# Print the table
print(table)

# Define a dictionary to keep track of the user's cart
cart = {}

# Define a handler for the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the MomStore Bot! How can I help you today? To order from our store click on /help command")
    bot.reply_to(message,"heyy,Are you worrying about how to enter commands? here we are with solution just click on the blue letter wordsi.e /help which will enter the commands")

    
    
# Define a handler for the /help command
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = "Here are some things I can do:\n\n"                "/start - Start the bot\n"                "/help - Show this help message\n"                "/myusername - please click on this command to register your name for further order process\n"                "/inventory - Display the list of items in the store\n"                "/add [item] [quantity] - Add an item to your cart\n"                "/remove [item] - Remove an item from your cart\n"                "/cart - Display your cart\n"                "/coupons - list of discounts available\n"                "/apply_coupon - Apply Discounts\n"                "/checkout - Place your order\n"                "/cancel - Cancel your order\n"                "/socialmedia - For advertising about our bot\n"                "/feedback - To get feedback from users\n"                "/view_feedback - To view feedbacks\n"                "/delivery - select delivery option\n"                
               
    bot.reply_to(message, help_text)
    bot.reply_to(message,"Are you ready for shopping? click on /inventory to see the list of items available")
    
@bot.message_handler(commands=['myusername'])
def get_username(message):
    username = message.chat.username
    if username:
        bot.reply_to(message, f"Your username is @{username}.")
    else:
        bot.reply_to(message, "You don't have a username set.")

        
        
# Define a handler for the /inventory command
@bot.message_handler(commands=['inventory'])
def show_inventory(message):
    from prettytable import PrettyTable
    
    table = PrettyTable()
    table.field_names = ["Name", "Price", "Quantity", "Weight", "Type", "Brand"]
    
    for item in inventory:
        table.add_row([item['name'], item['price'], item['quantity'], item['weight'], item['type'], item['brand']])
    
    bot.reply_to(message, "Here's what we have in stock:\n\n" + str(table))
    
    bot.reply_to(message,"What you are waiting for ? To add the items into the cart click /add")
    
    
# Define a handler for the /add command
@bot.message_handler(commands=['add'])
def add_to_cart(message):
    # Extract the item name and quantity from the message text
    command_text = message.text.split()
    if len(command_text) != 3:
        bot.reply_to(message, "Please enter the item name and quantity in the format /add [item] [quantity].")
        bot.reply_to(message,"For example : /add Brush 2")
        return
    item_name = command_text[1]
    quantity = int(command_text[2])
    
    # Find the item in the inventory
    item = next((item for item in inventory if item['name'].lower() == item_name.lower()), None)
    
    if item is None:
        bot.reply_to(message, f"Sorry, we don't have {item_name} in stock.")
    elif item['quantity'] < quantity:
        bot.reply_to(message, f"Sorry, we only have {item['quantity']} {item_name} in stock.")
    else:
        # Add the item to the cart
        if item_name in cart:
            cart[item_name]['quantity'] += quantity
        else:
            cart[item_name] = {
                'name': item_name,
                'price': item['price'],
                'quantity': quantity,
                'weight': item['weight'],
                'type': item['type'],
                'brand': item['brand']
            }
        bot.reply_to(message, f"Added {quantity} {item_name} to your cart.")
        bot.reply_to(message,"To know bill till now click on ---->  /cart")
        
        
# Define a handler for the /remove command
@bot.message_handler(commands=['remove'])
def remove_from_cart(message):
    # Extract the item name from the message text
    command_text = message.text.split()
    item_name = command_text[1]
    
    # Check if the item is in the cart
    if item_name in cart:
        # Remove the item from the cart
        del cart[item_name]
        bot.reply_to(message, f"Removed {item_name} from your cart.")
    else:
        bot.reply_to(message, f"{item_name} is not in your cart.")
        
        
# Define a handler for the /cart command
@bot.message_handler(commands=['cart'])
def show_cart(message):
    if not cart:
        bot.reply_to(message, "Your cart is empty.")
    else:
        cart_text = "Here's what's in your cart:\n\n"
        total_price = 0
        for item in cart.values():
            item_cost = item['price'] * item['quantity']
            cart_text += f"{item['name']} - {item['quantity']} - {item_cost}\n"
            total_price += item_cost
            
        cart_text += f"\nTotal price: {total_price}"
        bot.reply_to(message, cart_text)
        bot.reply_to(message,"Wanna add some more items click on /add")
        bot.reply_to(message,"Heyy Shopping Completed? We have exciting discounts for you click on /coupons")
        
@bot.message_handler(commands=['coupons'])
def coupons_discounts(message):
    bot.reply_to(message,"The Amazing Discounts for you :\n NEW10 # 10% off\n DAILY20 #20% off \n WOMEN30 #30% off")
    bot.reply_to(message,"To avail the discount click on /apply_coupon")
            
@bot.message_handler(commands=['apply_coupon'])
def apply_coupon(message):
    # Prompt user to enter coupon code
    bot.reply_to(message, "Please enter your coupon code:")
    bot.reply_to(message,"For example WOMEN30")
    bot.register_next_step_handler(message, check_coupon)
    
def check_coupon(message):
    coupon_code = message.text.strip().upper()
    
    # Check if coupon code is valid
    coupons = {
    "NEW10": 0.1,  # 10% off
    "DAILY20": 0.2,  # 20% off
    "WOMEN30": 0.3,  # 30% off
       } 
    total_price=0
    if coupon_code in coupons:
        # Apply discount to cart
        discount = coupons[coupon_code]
        for item in cart.values():
            total_price += item['price'] * item['quantity']
            discount = total_price * coupons[coupon_code]
            total_price -= discount        
        bot.reply_to(message, f"Coupon code {coupon_code} applied successfully.")
        bot.reply_to(message, f"Your total is {total_price:.2f} dollars. Thank you for your order!")
        owner_id = "5835745759"
        bot.send_message(owner_id, f"New order received from {message.chat.username}:\nTotal price: {total_price:.2f} dollars.")
    
        bot.reply_to(message,"To continue with payment process click on /checkout")
    else:
        bot.reply_to(message,"The coupon code is not available")
        if not cart:
            bot.reply_to(message, "Your cart is empty.")
            bot.reply_to(message,"Click on /add to add items into the cart")
        else:
            total_price = sum(item['price'] * item['quantity'] for item in cart.values())
            order_summary = ""
            for item in cart:
                order_summary += f"{item}: {cart[item]['quantity']}\n"
        
            bot.reply_to(message, f"Your total is {total_price:.2f} dollars. Thank you for your order!")
            owner_id = "5835745759"
            bot.send_message(owner_id, f"New order received from {message.chat.username}:\nTotal price: {total_price:.2f} dollars.")
    
            bot.reply_to(message,"To continue with payment process click on /checkout")
# Define a handler for the /checkout command
@bot.message_handler(commands=['checkout'])
def checkout(message):
    
    owner_id = "5835745759"
    # Prompt user for payment
    payment_message = bot.send_message(message.chat.id, f"Please make a payment to 1234567890 (example mobile payment service number).\n and send the transaction id in the format TXN123456")
    bot.reply_to(message,"After payment enter transaction id for example : enter TXN123456")
    # Store transaction ID in cart
    transaction_id = f"TXN{random.randint(10000, 99999)}"
    cart['transaction_id'] = transaction_id
    
    # Clear cart
  
    
    # Handle transaction ID from user
    @bot.message_handler(func=lambda message: message.text.startswith("TXN"))
    def handle_transaction_id(message):
        # Send transaction ID to owner for confirmation
        bot.forward_message(owner_id, message.chat.id, message.message_id)
        
        # Send payment confirmation to user
        bot.reply_to(payment_message, "Payment received. Thank you for your purchase!")
        bot.reply_to(payment_message, "Now for delivery option click on /delivery command")
        
        # Handle payment confirmation from owner
        @bot.message_handler(func=lambda message: message.text == transaction_id and message.chat.id == owner_id)
        def handle_payment_confirmation(message):
            # Send payment confirmation to user
            bot.send_message(payment_message.chat.id, "Payment confirmed by the owner. Thank you for your purchase!")


   
        
# Define a handler for the /cancel command
@bot.message_handler(commands=['cancel'])
def cancel_order(message):
    global cart
    cart = {}
    bot.reply_to(message, "Your order has been cancelled.")
feedback_messages = []

@bot.message_handler(commands=['feedback'])
def get_feedback(message):
    bot.reply_to(message, "Please leave your feedback below:")
    bot.register_next_step_handler(message, save_feedback)

def save_feedback(message):
    feedback_messages.append(message.text)
    bot.reply_to(message, "Thank you for your feedback!")

@bot.message_handler(commands=['view_feedback'])
def view_feedback(message):
    if feedback_messages:
        bot.reply_to(message, "Here are the latest feedback messages:")
        for feedback in feedback_messages:
            bot.send_message(message.chat.id, feedback)
    else:
        bot.reply_to(message, "No feedback messages yet.")
        
@bot.message_handler(commands=['socialmedia'])
def socialmedia(message):
    bot.reply_to(message,"Heyy,Hope you enjoyed our bot")
    bot.reply_to(message,"Share your order details in various social media platforms mentioning our bot name MomStore_bot\nFor this you will get exciting offers in your next order")
    bot.reply_to(message,"Thank you so much and enjoy your order")
    
@bot.message_handler(commands=['delivery'])
def handle_delivery_command(message):
    # Create a reply keyboard with delivery options
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    delivery_option_1 = types.KeyboardButton('DELIVERY')
    delivery_option_2 = types.KeyboardButton('PICK UP')
    keyboard.add(delivery_option_1, delivery_option_2)

    # Ask the user to choose a delivery option
    bot.reply_to(message, "Please choose a delivery option:", reply_markup=keyboard)

    # Wait for the user to choose an option
    @bot.message_handler(func=lambda message: True, content_types=['text'])
    def handle_delivery_option(message):
        if message.text == 'DELIVERY':
        # Add your code for handling delivery option 1
        # For example, you could ask the user to enter their address
           
            bot.reply_to(message, "And by the way we are providing free delivery service and the chance to deliver your items will be given only to the poor and trusted rikshaws and autos to help them")
            bot.reply_to(message,"So it may take few minutes to reach you.Please cooperate with us")
            bot.reply_to(message, "Please enter your delivery address: \nfor example enter : vizag")
        # Then, you could register a new handler to handle the user's response
            bot.register_next_step_handler(message, handle_delivery_address)
        elif message.text == 'PICK UP':
        # Add your code for handling delivery option 2
        # For example, you could display a message letting the user know that delivery option 2 is not currently available
            bot.reply_to(message, "Okay you can come and take your delivery for address contact: 1234567890")
        else:
            # If the user sends an invalid option, ask them to choose again
            bot.reply_to(message, "Invalid option. Please choose a delivery option:", reply_markup=keyboard)
def handle_delivery_address(message):
    # Store the user's delivery address
    delivery_address = message.text

    # Add your code for handling the user's delivery address
    # For example, you could confirm the address and ask the user to confirm their order
    bot.reply_to(message, f"Thank you for your order! Your items will be delivered to {delivery_address}.")
    bot.reply_to(message,"Please give your valuable feedback by clicking on /feedback \n can also view feedback of other users /view_feedback")
    bot.reply_to(message,"Please spare some of your valuable time by clicking on /socialmedia")
 

# Start the bot
bot.polling()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




