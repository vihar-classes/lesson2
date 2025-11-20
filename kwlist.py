import keyword
count = 0

while True:
    message = input("Enter> ")
    message_lower = message
    
    if message_lower == "count":
      print(f"You used {count} keywords this time.")
    
    if message_lower in keyword.kwlist:
        print("KEYWORD!")
        count += 1
        print(f"You used keywords {count} so far.")
        
    else:
        print("Good.")
    
    
    if message_lower == 'exit':
        print("Exiting program.")
        break
