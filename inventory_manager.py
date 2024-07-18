class CsvFiles:

    def __init__(self):
        self.file_name = "none"
        self.dict = {}

    def sorted_dict(self):
        import csv
        with open(self.file_name, "r") as csv_file:
            contents = csv.reader(csv_file, delimiter=",")
            for row in contents:
                for stuff in row:
                    if stuff != row[0]:
                        continue
                    else:
                        self.dict[stuff] = row[1:]
        sorted_dict = dict(sorted(self.dict.items(), key=sort_by_name))
        return sorted_dict

    def list_of_items(self):
        list_of_items = list(self.sorted_dict().items())
        return list_of_items

    def sorted_list_of_items(self):
        sorted_list_of_items = sorted(self.list_of_items(), key=sort_by_id)
        return sorted_list_of_items


def sort_by_name(name):
    return name[1]


def sort_by_date(date):
    from datetime import datetime
    return datetime.strptime(date[4], '%m/%d/%Y')


def sort_by_name_date(name_date):
    from datetime import datetime
    return name_date[1], datetime.strptime(name_date[4], '%m/%d/%Y')


def sort_by_id(i_d):
    return i_d[0]


def sort_by_price(price):
    return int(price[3])


# Combines all csv files and places all their contents with their respective ID's
def combined_list(list1, list2, list3):
    list1 = sorted(list1, key=sort_by_id)
    list2 = sorted(list2, key=sort_by_id)
    list3 = sorted(list3, key=sort_by_id)
    general_list = []
    for row_x, row_y, row_z in zip(list1, list2, list3):
        for item_x, item_y, item_z in zip(row_x, row_y, row_z):
            if item_x == item_y == item_z:
                general_list.append([item_x, row_x[1], row_y[1], row_z[1]])
    # Places items by order of: item id, manufacturer name, item type, price, service date, and situation
    formatted_items = []
    for row in general_list:
        formatted_items.append([row[0], row[1][0].strip(), row[1][1], row[2][0], row[3][0], row[1][2]])
    return formatted_items


# Splits the mm/dd/yyyy format into their respective positions of date and convert each to int
def get_current_date():
    import datetime
    current_date = datetime.date.today()
    current_date_formatted = current_date.strftime("%m/%d/%Y")

    year_now = int(current_date_formatted.split("/")[2])
    day_now = int(current_date_formatted.split("/")[1])
    month_now = int(current_date_formatted.split("/")[0])
    return month_now, day_now, year_now


def get_manufacturers_and_items(combined_inventory):
    # Stores manufacturer names from the full inventory list
    manufacturer_names = []
    for stuff in combined_inventory:
        manufacturer = stuff[1].strip()

        if manufacturer in manufacturer_names:
            continue
        else:
            manufacturer_names.append(manufacturer)

    # Stores item types from the full inventory list
    item_types = []
    for stuff in combined_inventory:
        item_type = stuff[2].strip()

        if item_type in item_types:
            continue
        else:
            item_types.append(item_type)

    return manufacturer_names, item_types


def allowed_list(combined_inventory):
    # Stores past service dates based on today's date into a new list
    current_month, current_day, current_year = get_current_date()
    past_service_date = []
    for stuff in combined_inventory:
        month = int(stuff[4].split("/")[0])
        day = int(stuff[4].split("/")[1])
        year = int(stuff[4].split("/")[2])
        if year < current_year:
            past_service_date.append(stuff)
        elif year <= current_year:
            if month < current_month:
                past_service_date.append(stuff)
            elif month <= current_month:
                if day < current_day:
                    past_service_date.append(stuff)
                else:
                    continue
    past_service_date = sorted(past_service_date, key=sort_by_id)

    # Retrieves items that are damaged
    damaged_inventory = []
    for stuff in full_inventory:
        if "damaged" in stuff:
            damaged_inventory.append(stuff)

    # Appends only items that do not exist in both Damaged Inventory and Past Service Date Inventory
    allowed_items = []
    for stuff in full_inventory:
        if (stuff not in past_service_date) and (stuff not in damaged_inventory):
            allowed_items.append(stuff)

    return allowed_items


if __name__ == "__main__":
    import csv

    # ManufacturerList.csv
    manufacturer_list = CsvFiles()
    manufacturer_list.file_name = "ManufacturerList.csv"

    # PriceList.csv
    price_list = CsvFiles()
    price_list.file_name = "PriceList.csv"

    # ServiceDatesList.csv
    service_dates_list = CsvFiles()
    service_dates_list.file_name = "ServiceDatesList.csv"

    full_inventory = combined_list(manufacturer_list.sorted_list_of_items(),
                                   price_list.sorted_list_of_items(),
                                   service_dates_list.sorted_list_of_items())

    appropriate_inventory = allowed_list(full_inventory)

    manufacturers, devices = get_manufacturers_and_items(full_inventory)

    while True:
        userInput = input("Enter the manufacturer's name and item type (Hit 'q' to quit): ")

        # if user hits the "q" button, the program will immediately end
        if userInput == 'q':
            break

        # stores user input manufacturer in a list. If multiple same word, only append one instance
        user_manufacturer = []
        for word in userInput.split(" "):
            if word in manufacturers:
                if word not in user_manufacturer:
                    user_manufacturer.append(word)

        # stores user input device in a list. If multiple same word, only append one instance
        user_device = []
        for word in userInput.split():
            if word in devices:
                if word not in user_device:
                    user_device.append(word)

        if (len(user_device) != 1) or (len(user_manufacturer) != 1):
            print("No such item in inventory\n")
        else:
            # Appends inventory items based on user choice
            user_item_pseudo = []
            for item in appropriate_inventory:
                if (user_manufacturer[0] in item[1]) and (user_device[0] in item[2]):
                    user_item_pseudo.append([item[0], item[1], item[2], item[3]])
            user_item = []
            for item in user_item_pseudo:
                user_item.append(item)

            # if an item, based on user choice, does not exist then it will output that there's no item
            # else, it will output an inventory item with the highest price to manipulate users into
            # buying the item with the highest price, despite having another inventory with lower prices
            if len(user_item) < 1:
                print("No such item in inventory\n")
            else:
                user_item = sorted(user_item, key=sort_by_price, reverse=True)
                recommended_item = user_item[0]
                print(f"Your item is: {', '.join(recommended_item)}")

                # Lists inventories that are ONLY from another manufacturer that holds the same item
                # as the user choice
                considered_items_pseudo = []
                for item in appropriate_inventory:
                    if (item[1] != user_manufacturer[0]) and (item[2] == user_device[0]):
                        considered_items_pseudo.append([item[0], item[1], item[2], item[3]])
                considered_items = []
                for item in considered_items_pseudo:
                    considered_items.append(item)
                considered_items = sorted(considered_items, key=sort_by_price, reverse=True)

                # Goes through the process of retrieving the item from a list of considered items
                # with the least amount of price difference between the user choice, based on items, and
                # considered item.
                try:
                    user_price = int(recommended_item[3])
                    closest_price = considered_items[0]
                    closest_price_difference = abs(int(closest_price[3]) - user_price)

                    for item in considered_items:
                        difference = abs(int(item[3]) - user_price)
                        if difference < closest_price_difference:
                            closest_price = item
                            closest_price_difference = difference

                    if len(closest_price) < 1:
                        print()
                    else:
                        print(f"You may, also, consider: {', '.join(closest_price)}")
                    print()

                except IndexError:
                    print()
