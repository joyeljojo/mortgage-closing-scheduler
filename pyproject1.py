# Mortgage Closing Scheduler
# Author: Joyel Jojo
# Description:
# A Python application that automates attorney assignment
# for mortgage closings based on state, county,
# closing type, DNU restrictions, and attorney rotation.

# Attorney Database
attorneys = {

    "Georgia": {

        "Kendra Robinson": {
            "counties": ["Fulton", "Dekalb", "Cobb"],
            "fee": 225,
            "type": "Physical"
        },

        "Leonid Sakson": {
            "counties": ["Cherokee", "Fulton", "Forsyth"],
            "fee": 225,
            "type": "Physical"
        },

        "Greg Stein": {
            "counties": ["Chatham", "Effingham"],
            "fee": 250,
            "type": "Physical"
        },

        "Conley Scott": {
            "counties": ["Camden"],
            "fee": 180,
            "type": "Physical"
        },

        "Jade Redmond": {
            "counties": ["Richmond", "McDuffie"],
            "fee": 200,
            "type": "Physical"
        },

        "Kimberly Arvelo": {
            "counties": ["All"],
            "fee": 50,
            "type": "Phone"
        }

    },

    "Massachusetts": {

        "Peter Engles": {
            "counties": ["Norfolk"],
            "fee": 175,
            "type": "Physical"
        },

        "Jesse Limanek": {
            "counties": ["Worcester", "Hampden"],
            "fee": 225,
            "type": "Physical"
        },

        "Alexander Joyal": {
            "counties": ["Bristol", "Plymouth"],
            "fee": 240,
            "type": "Physical"
        },

        "David DeMella": {
            "counties": ["Middlesex", "Essex", "Suffolk"],
            "fee": 230,
            "type": "Physical"
        },

        "Stephen Valente": {
            "counties": ["Norfolk", "Plymouth", "Essex", "Middlesex"],
            "fee": 170,
            "type": "Physical"
        },

        "Jesse Limanek": {
            "counties": ["All"],
            "fee": 30,
            "type": "Phone"
        }

    },

    "South Carolina": {

        "Christopher Jay": {
            "counties": ["Richland", "Lexington", "Kershaw"],
            "fee": 190,
            "type": "Physical"
        },

        "Lovee Watts": {
            "counties": ["Greenville", "Pickens", "Spartanburg"],
            "fee": 225,
            "type": "Physical"
        },

        "Harvey": {
            "counties": ["Greenville", "Oconee", "Greenwood"],
            "fee": 225,
            "type": "Physical"
        },

        "Melvin": {
            "counties": ["York", "Lancaster", "Chester"],
            "fee": 200,
            "type": "Physical"
        },

        "Douglas Laffin": {
            "counties": ["Berkeley", "Charleston", "Dorchester", "Aiken"],
            "fee": 250,
            "type": "Physical"
        },

        "David West": {
            "counties": ["All"],
            "fee": 30,
            "type": "Phone"
        }

    },

    "North Carolina": {

        "Justin Merritt": {
            "counties": ["Wake", "Johnston"],
            "fee": 150,
            "type": "Physical"
        },

        "Carlosha Easton": {
            "counties": ["Durham", "Wake"],
            "fee": 150,
            "type": "Physical"
        },

        "Anthony Dilon": {
            "counties": ["Guilford", "Forsyth"],
            "fee": 225,
            "type": "Physical"
        },

        "Paul Ryan": {
            "counties": ["All"],
            "fee": 30,
            "type": "Phone"
        }
    },

    "West Virginia": {

        "Ari Carver": {
            "counties": ["All"],
            "fee": 30,
            "type": "Phone"
        }
    }
}

# DNU Attorney Restrictions
dnu_attorneys = {

    "First American Title": [
        "Kendra Robinson",
        "Christopher Jay"
    ],

    "Liberty Title": [
        "Leonid Sakson",
        "Lovee Watts"
    ],

    "Old Republic Title": [
        "David DeMella",
        "Anthony Dilon"
    ],

    "Fidelity National Title": [
        "Stephen Valente",
        "Harvey"
    ]

}

# Attorney Rotation Tracking
attorney_rotation = {}

# Attorney Assignment Logic
def assign_attorney(property_state,
                    property_county,
                    closing_state,
                    closing_county,
                    title_company):

    # STATE NOT SUPPORTED
    if property_state not in attorneys:
        return {
            "name": "No attorney available",
            "fee": 0,
            "type": "N/A"
        }

    # WEST VIRGINIA = ALWAYS PHONE
    if property_state == "West Virginia":

        for attorney, details in attorneys[property_state].items():

            if details["type"] == "Phone":
                return {
                    "name": attorney,
                    "fee": details["fee"],
                    "type": details["type"]
                }

    # PHONE CLOSING
    if property_state != closing_state:

        for attorney, details in attorneys[property_state].items():

            if details["type"] == "Phone":
                return {
                    "name": attorney,
                    "fee": details["fee"],
                    "type": details["type"]
                }

        return {
            "name": "No attorney available",
            "fee": 0,
            "type": "N/A"
        }

    # PHYSICAL CLOSING
    
    restricted_attorneys = dnu_attorneys.get(title_company, [])

    eligible_attorneys = []

    for attorney, details in attorneys[property_state].items():
        if attorney in restricted_attorneys:
            continue

        if details["type"] == "Physical":
            
            if closing_county in details["counties"]:
                eligible_attorneys.append({
                    "name": attorney,
                    "fee": details["fee"],
                    "type": details["type"]
                })

    if len(eligible_attorneys) == 0 and property_state == "North Carolina":
        
        for attorney, details in attorneys[property_state].items():
            if details["type"] == "Phone":
                return {
                    "name": attorney,
                    "fee": details["fee"],
                    "type": details["type"]
                }
        
    if len(eligible_attorneys) == 0:
        return {
            "name": "No attorney available",
            "fee": 0,
            "type": "N/A"
        }

    rotation_key = f"{property_state}-{property_county}"

    if rotation_key not in attorney_rotation:
        attorney_rotation[rotation_key] = 0

    rotation_index = attorney_rotation[rotation_key]

    assigned_attorney = eligible_attorneys[
        rotation_index % len(eligible_attorneys)
    ]

    attorney_rotation[rotation_key] += 1

    return assigned_attorney

closing_requests = []
while True:
    print("\n---Mortgage Closing Scheduler---")
    print("1. Add Closing Task")
    print("2. View Tasks")
    print("3. Statistics")
    print("4. Search Borrower")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        borrower_name = input("Enter borrower name: ")
        title_company = input("Enter title company: ")
        property_state = input("Enter property state: ")
        closing_date = input("Enter closing date: ")
        closing_time = input("Enter closing time: ")
        property_county = input("Enter property county: ")
        closing_state = input("Enter closing state: ")
        closing_county = input("Enter closing county: ")
        assigned_attorney = assign_attorney(
            property_state,
            property_county,
            closing_state,
            closing_county,
            title_company
        )
        closings = {
            "attorney": assigned_attorney["name"],
            "fee": assigned_attorney["fee"],
            "type": assigned_attorney["type"],
            "borrower": borrower_name,
            "title_company": title_company,
            "property_state": property_state,
            "date": closing_date,
            "time": closing_time,
            "property_county": property_county,
            "closing_state": closing_state,
            "closing_county": closing_county
        }

        closing_requests.append(closings)
        print("Closing request added successfully!")

    elif choice == "2":

        if not closing_requests:
            print("No closing requests available.")
        else:
            for i, closings in enumerate(closing_requests):
                print(f"\n Closing #{i + 1}")
                print(f"Borrower: {closings['borrower']}")
                print(f"Title Company: {closings['title_company']}")
                print(f"Date: {closings['date']}")
                print(f"Time: {closings['time']}")
                print(f"Property State: {closings['property_state']}")
                print(f"Property County: {closings['property_county']}")
                print(f"Closing State: {closings['closing_state']}")
                print(f"Closing County: {closings['closing_county']}")
                print(f"Attorney: {closings['attorney']}")
                print(f"Fee: ${closings['fee']}")
                print(f"Type: {closings['type']} Closing")

    elif choice == "3":
        
        total_closings = len(closing_requests)
        phone_closings = 0
        physical_closings = 0
        total_fees = 0

        attorney_usage = {}

        for closing in closing_requests:
            total_fees += closing["fee"]

            if closing["type"] == "Phone":
                phone_closings += 1
                
            elif closing["type"] == "Physical":
                physical_closings += 1

            attorney_name = closing["attorney"]

            if attorney_name in attorney_usage:
                attorney_usage[attorney_name] += 1
            
            else:
                attorney_usage[attorney_name] = 1

        print("\n----- Statistics -----")
        print(f"Total Closings: {total_closings}")
        print(f"Phone Closings: {phone_closings}")
        print(f"Physical Closings: {physical_closings}")
        print(f"Total Attorney Fees: ${total_fees}")

        if total_closings > 0:
            print(f"Average Fee: ${total_fees / total_closings:.2f}")

        print("\nAttorney Usage:")
    
        for attorney, count in sorted(
            attorney_usage.items(),
            key=lambda item: item[1],
            reverse=True):
        
            print(f"{attorney}: {count} closings")

    elif choice == "4":
        borrower_name = input("Enter borrower name to search: ")

        found = False

        for closing in closing_requests:
            
            if closing["borrower"].lower() == borrower_name.lower():
                found = True

                print("\n----- Closing Found -----")
                print(f"Borrower: {closing['borrower']}")
                print(f"Title Company: {closing['title_company']}")
                print(f"Date: {closing['date']}")
                print(f"Time: {closing['time']}")
                print(f"Property State: {closing['property_state']}")
                print(f"Property County: {closing['property_county']}")
                print(f"Closing State: {closing['closing_state']}")
                print(f"Closing County: {closing['closing_county']}")
                print(f"Attorney: {closing['attorney']}")
                print(f"Fee: ${closing['fee']}")
                print(f"Type: {closing['type']} Closing")

        if found == False:
            print("No closing found for that borrower.")

    elif choice == "5":
        print("Exiting Program...")
        break

    else:
        print("Invalid Choice")