"""
Main entry point for the yacht management system.

This script provides a command-line interface for users to search for base yachts,
create their own yachts from base yachts, and view or modify their yacht profiles.
It uses the orchestration Services class to manage all yacht data.

Example usage:
    $ python app.py
"""

from back_end.orchestration.services import Services


def main_menu():
    print("\nYacht Management System")
    print("1. Search for a base yacht")
    print("2. Create your own yacht from a base yacht")
    print("3. View or modify your yacht")
    print("4. Exit")
    return input("Choose an option: ")


def search_base_yachts(services):
    print("\nAvailable Base Yachts:")
    yachts = []
    # For demo, just list all base yachts (base_id is None)
    for yid in range(1, 100):
        row, columns = services.profile_service.db.get_by_yacht_id(yid)
        if row:
            yacht = services.profile_service.db.get_by_yacht_id(yid)[0]
            if yacht and columns[columns.index('base_id')] is None:
                yachts.append((yid, row, columns))
    if not yachts:
        print("No base yachts found.")
        return None
    for yid, row, columns in yachts:
        profile = services.profile_service.get_profile(yid)
        print(f"ID: {profile.yacht_id} | Class: {profile.yacht_class} | Model: {profile.model} | Designer: {profile.designer}")
    return yachts


def create_user_yacht(services, user_id):
    base_yachts = search_base_yachts(services)
    if not base_yachts:
        return
    base_id = int(input("Enter the ID of the base yacht to use: "))
    base_profile = services.profile_service.get_profile(base_id)
    if not base_profile:
        print("Base yacht not found.")
        return
    new_yacht_id = int(input("Enter a new yacht ID for your yacht: "))
    user_profile = type(base_profile)(
        yacht_id=new_yacht_id,
        base_id=base_profile.yacht_id,
        yacht_class=base_profile.yacht_class,
        model=base_profile.model,
        version=base_profile.version,
        builder=base_profile.builder,
        designer=base_profile.designer,
        year_introduced=base_profile.year_introduced,
        production_start=base_profile.production_start,
        production_end=base_profile.production_end,
        country_of_origin=base_profile.country_of_origin,
        notes=(base_profile.notes or "") + f" (User {user_id})"
    )
    services.profile_service.save_profile(user_profile)
    print(f"Created your yacht with ID {new_yacht_id} based on base yacht {base_id}.")
    # TODO: Call other services to initialize hull, rig, sails, etc.


def view_or_modify_yacht(services, user_id):
    yacht_id = int(input("Enter your yacht ID: "))
    profile = services.profile_service.get_profile(yacht_id)
    if not profile:
        print("Yacht not found.")
        return
    print(f"\nYour Yacht Profile:")
    for k, v in profile.__dict__.items():
        print(f"{k}: {v}")
    print("\n1. Modify notes\n2. Back")
    choice = input("Choose an option: ")
    if choice == "1":
        new_notes = input("Enter new notes: ")
        profile.notes = new_notes
        services.profile_service.save_profile(profile)
        print("Notes updated.")


def main():
    user_id = input("Enter your user ID: ")
    services = Services()
    while True:
        choice = main_menu()
        if choice == "1":
            search_base_yachts(services)
        elif choice == "2":
            create_user_yacht(services, user_id)
        elif choice == "3":
            view_or_modify_yacht(services, user_id)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")
    services.profile_service.close()


if __name__ == "__main__":
    main()