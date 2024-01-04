BLUE = '\033[94m'
RED = '\033[91m'
END_COLOR = '\033[0m'

data_file_path = "client_data.txt"
services_file_path = "services_data.txt"

try:
    with open(data_file_path, "r") as data_file:
        lines = data_file.readlines()
        clients = {}
        for line in lines:
            name, projects_str = line.strip().split(":", 1)
            projects = eval(projects_str)
            clients[name] = {"Projects": projects}
except FileNotFoundError:
    clients = {}

try:
    with open(services_file_path, "r") as services_file:
        services_lines = services_file.readlines()
        SERVICES = {}
        for line in services_lines:
            name, hourly_str = line.strip().split(":", 1)
            hourly = hourly_str.lower() == "true"
            SERVICES[name] = {"hourly": hourly}
except FileNotFoundError:
    SERVICES = {}

def save_data():
    with open(data_file_path, "w") as data_file:
        for name, info in clients.items():
            projects_str = str(info["Projects"])
            data_file.write(f"{name}:{projects_str}\n")

def add_project(client_name):
    print(f"\nEnter project details for {client_name}:")
    project = input("Project: ")

    services_menu = "\n".join([f"[{i}] {name}" for i, name in enumerate(SERVICES.keys(), start=1)])
    service_input = input(f"Select a service:\n{services_menu}\n")

    try:
        service_number = int(service_input)
        selected_service = list(SERVICES.keys())[service_number - 1]
    except (ValueError, IndexError):
        print("Invalid selection. Using the default service.")
        selected_service = "Default"

    if selected_service in SERVICES and SERVICES[selected_service]["hourly"]:
        hours = float(input("Hours: "))
    else:
        hours = None

    price = float(input("Price: $"))

    new_project = {"Project": project, "Service": selected_service, "Hours": hours, "Price": price}

    if client_name in clients:
        clients[client_name]["Projects"].append(new_project)
    else:
        clients[client_name] = {"Projects": [new_project]}

def add_client():
    print("\nEnter client details:")
    name = input("Name: ")
    clients[name] = {"Projects": []}

    add_project(name)

def delete_client():
    print("\nExisting Clients:")
    for i, client_name in enumerate(clients.keys(), start=1):
        print(f"[{i}] {client_name}")

    try:
        choice = int(input("Select the number of the client to delete: "))
        client_name = list(clients.keys())[choice - 1]
        del clients[client_name]
        print(f"Client '{client_name}' deleted successfully.")
    except (ValueError, IndexError):
        print("Invalid selection. Please enter a valid client number.")

def delete_client_project():
    print("\nExisting Clients:")
    for i, client_name in enumerate(clients.keys(), start=1):
        print(f"[{i}] {client_name}")

    try:
        choice = int(input("Select the number of the client to delete a project from: "))
        client_name = list(clients.keys())[choice - 1]

        if client_name in clients:
            display_client_projects(client_name)

            try:
                project_choice = int(input("Select the number of the project to delete: "))
                del clients[client_name]["Projects"][project_choice - 1]
                print(f"Project deleted successfully from client '{client_name}'.")
            except (ValueError, IndexError):
                print("Invalid project selection. Please enter a valid project number.")
        else:
            print(f"Client '{client_name}' not found.")
    except (ValueError, IndexError):
        print("Invalid client selection. Please enter a valid client number.")

def display_client_projects(client_name):
    projects = clients[client_name]["Projects"]
    print(f"\nProjects for client '{client_name}':")
    for i, project in enumerate(projects, start=1):
        print(f"[{i}] {project['Project']}")

def display_clients():
    headers = ["Client Name", "Project", "Service", "Hours", "Price ($)", "Total Cost ($)"]

    if not SERVICES:
        print("No services available. Please add services first.")
        return

    max_service_length = max(len(name) for name in SERVICES.keys())
    column_widths = [max(len(header), max(len(str(project.get(header, ""))) for info in clients.values() for project in info["Projects"])) for header in headers]
    column_widths[2] = max(column_widths[2], max_service_length)

    header_str = "\t|\t".join([f'{BLUE}{header.ljust(column_widths[i])}{END_COLOR}' for i, header in enumerate(headers)])
    print(header_str)

    for name, info in clients.items():
        for project in info["Projects"]:
            hours = project.get("Hours")
            total_cost = project["Price"] * hours if hours is not None else None
            row = [
                f'{RED}{name.ljust(column_widths[0])}{END_COLOR}',
                project["Project"].ljust(column_widths[1]),
                str(project["Service"]).ljust(column_widths[2]),
                str(hours).ljust(column_widths[3]) if hours is not None else "None",
                str(project["Price"]).ljust(column_widths[4]),
                str(total_cost).ljust(column_widths[5]) if total_cost is not None else "None"
            ]
            row_str = "\t|\t".join(row)
            print(row_str)

def manage_services():
    """
    
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
            print("Invalid option. Please select a valid option.")

def add_new_service():
    service_name = input("Enter the new service name: ")
    hourly = input("Is the service hourly-based? (yes/no): ").lower() == "yes"
    SERVICES[service_name] = {"hourly": hourly}
    print(f"Service '{service_name}' added successfully.")

def modify_existing_service():
    "
    
    "
    print("\nExisting Services:")
    for i, service_name in enumerate(SERVICES.keys(), start=1):
        print(f"[{i}] {service_name}")

    try:
        choice = int(input("Select the number of the service to modify: "))
        service_name = list(SERVICES.keys())[choice - 1]
        hourly = input("Is the service hourly-based? (yes/no): ").lower() == "yes"
        SERVICES[service_name]["hourly"] = hourly
        print(f"Service '{service_name}' modified successfully.")
    except (ValueError, IndexError):
        print("Invalid selection. Please enter a valid service number.")

def save_services():
    with open(services_file_path, "w") as services_file:
        for name, service_info in SERVICES.items():
            services_file.write(f"{name}:{service_info['hourly']}\n")

while True:
    print("\nMenu:")
    print("[1] Manage Clients")
    print("[2] Manage Services")
    print("[3] Display Clients")
    print("[4] Exit")

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
        break
    else:
        print("Invalid option. Please select a valid option.")
