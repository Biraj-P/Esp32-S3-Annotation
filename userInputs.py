def collect_and_store_user_input():
    name = input("Enter your first name: ")
    speed_options = ['Normal', 'Fast', 'Slow']
    gesture_options = ['True', 'FPG1', 'FPG2', 'FPG3', 'FPG4', 'FPG5', 'FPG6', 'FPG7']

    speed = input(f"Enter Speed ({'/'.join(speed_options)}): ")
    while speed not in speed_options:
        speed = input(f"Invalid choice. Enter Speed ({'/'.join(speed_options)}): ")

    gesture = input(f"Enter Gesture ({'/'.join(gesture_options)}): ")
    while gesture not in gesture_options:
        gesture = input(f"Invalid choice. Enter Gesture ({'/'.join(gesture_options)}): ")

    # Store the collected data in a text file
    with open("user_data.txt", "w") as file:
        file.write(f"Name: {name}\n")
        file.write(f"Speed: {speed}\n")
        file.write(f"Gesture: {gesture}\n")

    print("User data has been saved to 'user_data.txt'.")
if __name__ == "__main__":
    collect_and_store_user_input()