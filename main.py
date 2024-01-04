"""
As a freelance video editor and tutor, it has been been a challenge to effeciently track and manage multiple 
projects with multiple clients. Due to this, deadlines for projects and receival of payments have become difficult
to keep track of. I wish to create a program that displays a comprehensive overview of my clients, their projects, 
and my offered services. This comprehensive overview must include a chart of clients that includes their names, all projects
assigned to that name, the service I am providing them, the time I am putting into the project, and the
cost of the project. I must be able to add and remove clients entriely as well as add or remove individual projects 
to their name. It is also essential that I must be able to save and load my data so that I can view it as a text file 
to view my current projects whereever I am and then also edit the data when I am able to run the program. 
"""



import re

BLUE = '\033[94m'
RED = '\033[91m'
END_COLOR = '\033[0m'

OUTPUT_FILE_PATH = "cps109_a1_output.txt"
data_file_path = "client_data.txt"
services_file_path = "services_data.txt"

def read_client_data():
    """
    Reads client data from a file, storing it in a dictionary with the name of the clients as keys and the values as their projects.
    Returns:
    Example structure of the 'clients' dictionary:
        clients = 
        {
            'Client1': 
            {
                'Projects': 
                [
                    {'FOOPROJECT1': 'Project1', 'Service': 'POW SERVICE1', 'Hours': 5.0, 'Price': 100.0},
                    {'FOO2': 'Project2', 'Service': 'COOL SERVICE', 'Hours': 8.0, 'Price': 111},
                ]
            }
            ,
            'Client2': {
                'Projects':
                [
                    {'ProjectWIK': 'ProjectA', 'Service': 'ServiceDSF', 'Hours': 3.0, 'Price': 99},
                    {'ProjectCOCO': 'ProjectB', 'Service': 'ServiceASd', 'Hours': None, 'Price': 44.0},
                ]
            }
        }
    """
    try:
        with open(data_file_path, "r") as client_file:
            
            lines = client_file.readlines()
            clients = {}
            
            for line in lines:
                
                name_and_projects = line.strip().split(":", 1) # Seperates current line into a list containing a name and the corresponding projects
                name = name_and_projects[0]
                projects_string = name_and_projects[1]
                projects = eval(projects_string) # Converts the string containing a list of dictionaries into a list object that contains dictionary objects
                
                clients[name] = {"Projects": projects} # Adds a new key value pair to clients dictionary, containing client name and corresponding projects
    except FileNotFoundError:
        clients = {}
        
    return clients


def read_services_data():
    """
    Try to read service data from a file, storing it in a dictionary with service names as keys and hourly status as values.
    
    Example Services File Format:
    service1:True
    service2:False
    service3:True

    Returns:
        dict: A dictionary where keys are service names and values are dictionaries containing the hourly status.
              For example:
              {
                  'service1': {'hourly': True},
                  'service2': {'hourly': False},
                  'service3': {'hourly': True}
              }
    """
    try:
        with open(services_file_path, "r") as services_file:
            
            services_lines = services_file.readlines()
            Services = {}
            
            for line in services_lines:
                
                name_and_hourly = line.strip().split(":", 1)  # Separates the current line into a list containing a name and hourly status
                Service_name = name_and_hourly[0]
                hourly_string = name_and_hourly[1]
                
                # Converts the hourly status string to a boolean
                if hourly_string.lower() == "true":
                    hourly = True
                else:
                    hourly = False
                
                Services[Service_name] = {"hourly": hourly}  # Adds a new key-value pair to Services dictionary, containing service name and hourly status
    except FileNotFoundError:
        Services = {}
    return Services


# Saves client data to client_file in readable format 
def save_data():
    with open(data_file_path, "w") as client_file:
        for name, info in clients.items():
            projects_str = str(info["Projects"])
            client_file.write(f"{name}:{projects_str}\n")

def add_project(client_name):
    """
    Requests project details and appends project to defined client 

    Args:
        client_name (_str_): The name of the client that the project is being added too 
    """
    
    print(f"\nEnter project details for {client_name}:")
    project = input("Project Name: ")


    # Iterates through service names and indices (starting at 1), creating a menu 
    menu_items = []
    service_names = list(Services.keys())
    
    for i, name in enumerate(service_names, start=1):
        menu_item = f"[{i}] {name}"
        menu_items.append(menu_item)
    services_menu = "\n".join(menu_items) # combines the menu_items into a string seperated by new lines
    service_input = input(f"Select a service:\n{services_menu}\nService number: ")

    # Obtains user menu selection
    try:
        service_number = int(service_input)
        # Retrieve the selected service using the entered number
        selected_service = service_names[service_number - 1] # -1 to account for 0th index 
    except (ValueError, IndexError):
        print("Invalid selection. Please enter a valid service number.")
        return None
    

    price = None
    hours = None
    # Check if selected service has an hourly rate
    if Services[selected_service]["hourly"]:
        while hours is None:
            try:
                hours = float(input("Hours: "))
            except ValueError:
                print("Invalid input. Please enter a valid number for hours.")
    else:
        hours = None

    while price is None:
        try:
            price = float(input("Price: $"))
        except ValueError:
            print("Price must be a numeric value.")

    # Creates a dictionary with project details in reedable format
    new_project = {"Project": project, "Service": selected_service, "Hours": hours, "Price": price}

    if client_name in clients:
        clients[client_name]["Projects"].append(new_project)
    else:
        clients[client_name] = {"Projects": [new_project]}

def add_client():
    """
    Adds a client to the clients dictionary and calls add_project() function on the newly added client
    """
    print("\nEnter client details:")
    name = input("Name: ")
    clients[name] = {"Projects": []}
    add_project(name)


def delete_client():
    """
    Deletes a client from the clients dictionary 
    """
    # Iterates through client names and indices (starting at 1), creating a menu 
    print("\nExisting Clients:")
    for i, client_name in enumerate(clients.keys(), start=1):
        print(f"[{i}] {client_name}")

    try:
        choice = int(input("Select the number of the client to delete: "))

        client_names = list(clients.keys())
        
        if 1 <= choice and choice <= len(client_names): # Ensures that user selection is within the range of clients
            client_name = client_names[choice - 1]
            del clients[client_name]
            print(f"Client '{client_name}' deleted successfully.")
        else:
            print("Invalid selection. Please enter a valid client number.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def delete_client_project():
    """
    Allows the user to delete a specified project from the list of projects associated with a selected client.

    Deletes a specified project (value) from the projects dictionary (key and value) of a specified client dictionary (key) 
    after prompting the user to choose the client and project interactively.
    """
    print("\nCurrent Clients:")
    client_iterator = iter(clients.keys())
    i = 1
    n = len(clients)
    # Iterate through client names, print them with an index, and continue until all names have been printed
    while i <= n:
        client_name = next(client_iterator)
        print(f"[{i}] {client_name}")
        i += 1

    try:
        choice = int(input("Please enter the client number: "))
        client_name = list(clients.keys())[choice - 1]

        if client_name in clients:
            
            # Displays the projects associated with a specific client 
            projects = clients[client_name]["Projects"]
            print(f"\nProjects for client '{client_name}':")
            for i, project in enumerate(projects, start=1):
                print(f"[{i}] {project['Project']}")

            try:
                project_choice = int(input("Select the number of the project to delete: "))

                del projects[project_choice - 1]  # Deletes the selected project from the list of projects for the selected client
                
                print(f"Project deleted successfully from client '{client_name}'.")
            except (ValueError, IndexError):
                print("Invalid project selection. Please enter a valid project number.")
        else:
            print(f"Client '{client_name}' not found.")
    except (ValueError, IndexError):
        print("Invalid client selection. Please enter a valid client number.")
        
def display_clients():
    """
    Displays all client information in a chart format. 
    """
    global Completed_Chart
    headers = ["Client Name", "Project", "Service", "Hours", "Price ($)", "Total Cost ($)"]

    if not Services:
        print("No services available. Please add services first.")
        return

    if not clients:
        print("No clients available. Please add clients first.")
        return

    # Calculate column widths
    # Initialize the widths of each column as the length of each header in the headers
    column_widths = [len(header) for header in headers]

    # Iterate over each client in the clients dictionary
    for name, info in clients.items():
        # Updates the first column width to the length of the width of the name if it is larger
        column_widths[0] = max(column_widths[0], len(str(name)))

        # Iterate over each project in the list of projects for the current client
        for project in info.get("Projects", []):
            # Enumerate over each header in the headers list, starting from the second header ("Project")
            for i, header in enumerate(headers[1:], start=1):
                # Updates the curent column width to the length of the width of the project information if it is larger
                column_widths[i] = max(column_widths[i], len(str(project.get(header, ""))))

    # Display header
    
    # Create an empty list to store formatted headers
    formatted_headers = []

    # Iterate over the headers along with their indices
    for i, header in enumerate(headers):
        # Calculate the width for the current header based on the precalculated column widths
        width = column_widths[i]

        # Format the header with ANSI color codes and left-justify to the calculated width
        formatted_header = f'{BLUE}{header.ljust(width)}{END_COLOR}'

        # Add the formatted header to the list
        formatted_headers.append(formatted_header)

    header_str = "\t|\t".join(formatted_headers)

    print(header_str)

    Completed_Chart += header_str + "\n"
    # Display client information
# Iterate over each client in the clients dictionary
    for name, info in clients.items():
        # Iterate over each project in the list of projects for the current client
        for project in info.get("Projects", []):
            hours = project.get("Hours")

            # Ensure total cost is only calculated if the service has the hours property
            if hours is not None:
                total_cost = project["Price"] * hours
            else:
                total_cost = project["Price"]

            # Format the row data
            formatted_name = f'{RED}{name.ljust(column_widths[0])}{END_COLOR}'
            formatted_project = project.get("Project", "").ljust(column_widths[1])
            formatted_service = str(project.get("Service", "")).ljust(column_widths[2])

            # Format hours
            if hours is not None:
                formatted_hours = str(hours).ljust(column_widths[3])
            else:
                formatted_hours = "None".ljust(column_widths[3])

            formatted_price = str(project.get("Price", "")).ljust(column_widths[4])


            if total_cost is not None:
                formatted_total_cost = str(total_cost).ljust(column_widths[5])
            else:
                formatted_total_cost = "None".ljust(column_widths[5])

            # Create a list of data for the current project containing  all the formatted data 
            row = [formatted_name, formatted_project, formatted_service, formatted_hours, formatted_price, formatted_total_cost]
            row_str = "\t|\t".join(row) # Combine formatted data with tabs and | character to ensure chart formatting 
            Completed_Chart += row_str + "\n"
            print(row_str)





def manage_services():
    """
    Creates a visual menu for service management, prompts user input, and calls respective function. 
    """
    while True:
        print("\nService Management:")
        print("[1] Add a new service")
        print("[2] Modify an existing service")
        print("[3] Exit service management")

        choice = input("Select an option (1, 2, 3): ")

        if choice == "1":
            add_new_service()
        elif choice == "2":
            modify_existing_service()
        elif choice == "3":
            save_services()
            break
        else:
            print("Please select a valid option.")

def add_new_service():
    """
    Add a new service to the "Services" dictionary by prompting user for service details.
    """
    service_name = input("Enter the new service name: ")
    hourly = input("Is the service hourly-based? (yes/no): ").lower() == "yes"
    Services[service_name] = {"hourly": hourly}
    print(f"Service '{service_name}' added successfully.")

def modify_existing_service():
    """
    Displays a list of existing services with their corresponding numbers, prompting the user to select a service.
    Asks if the service is hourly-based and updates the hourly status variable in the Services dictionary.
    """
    print("\nExisting Services:")
    
    # Displays menu of services by enumerating through the names of the services, starting with and index value of 1
    for i, service_name in enumerate(Services.keys(), start=1):
        print(f"[{i}] {service_name}")

    try:
        choice = int(input("Select the number of the service to modify: "))
        service_name = list(Services.keys())[choice - 1] # -1 to account for 0th index
        hourly = input("Is the service hourly-based? (yes/no): ").lower() == "yes"
        Services[service_name]["hourly"] = hourly
        print(f"Service '{service_name}' modified successfully.")
    except (ValueError, IndexError):
        print("Invalid selection. Please enter a valid service number.")

def save_services():
    """
    Saves service information to services file in correct format.

    Example File Format:
    service1:True
    service2:False
    service3:True
    """
    with open(services_file_path, "w") as services_file:
        for name, service_info in Services.items():
            services_file.write(f"{name}:{service_info['hourly']}\n")
def main():
    """
    Main function to run freelance project manager. 
    Creates a main menu loop, displaying a menu an prompting a user for a choice.
    User choice calls various functions to faciliate request.
    """
    global Completed_Chart
    # Save Completed_Chart to a text file
    display_clients()
    with open(OUTPUT_FILE_PATH, "w") as output_file:
        output_file.write(re.sub(r'\033\[\d+m', '', Completed_Chart))
    while True:
        print("Menu:")
        print("[1] Manage Clients")
        print("[2] Manage Services")
        print("[3] Display Clients")
        print("[4] Save & Exit")

        choice = input("Select an option (1, 2, 3, 4): ")

        if choice == "1":
            while True:
                print("\nManage Clients:")
                print("[1] Add a new client")
                print("[2] Add a project to an existing client")
                print("[3] Delete a project from an existing client")
                print("[4] Delete a client")
                print("[5] Exit Manage Clients")

                manage_clients_choice = input("Select an option (1, 2, 3, 4): ")

                if manage_clients_choice == "1":
                    add_client()
                elif manage_clients_choice == "2":
                    display_clients()
                    client_name = input("Enter the name of the client to add a project to: ")
                    if client_name in clients:
                        add_project(client_name)
                    else:
                        print(f"Client '{client_name}' not found.")
                elif manage_clients_choice == "3":
                    delete_client_project()
                elif manage_clients_choice == "4":
                    delete_client()
                elif manage_clients_choice == "5":
                    break
                else:
                    print("Invalid option. Please select a valid option.")
        elif choice == "2":
            manage_services()
        elif choice == "3":
            display_clients()
        elif choice == "4":
            save_data()
            
            # Save Completed_Chart to a text file
            with open(OUTPUT_FILE_PATH, "w") as output_file:
                output_file.write(re.sub(r'\033\[\d+m', '', Completed_Chart))
            break
        else:
            print("Invalid option. Please select a valid option.")

if __name__ == "__main__":
    Completed_Chart = ""
    clients = read_client_data()
    Services = read_services_data()
    main()