import storage
from functions.search import binary_search
from functions.sort import quick_sort
from functions.type_validation import is_integer
from functions.generate import db_id
from functions.navigation.navigator import go_to

PLACES_PATH = "data/data.json"  # the file path for places
ACCOMMODATION_TYPES = quick_sort(["Hotel", "Hostel", "Bed and breakfast", "Apartment", "Guest house", "Dormitory", "Campsite", "Motel", "Cottage", "Resort", "Villa", "Inn", "Chalet", "Lodge", "Homestay", "Log cabin", "Glamping"])
AREAS = ['bassett', 'swaything', 'highfield', 'portswood', 'woolston', 'freemantle', 'milbrook', 'shirley', 'city center']
HUBS = ['railway station', 'bus station']


class Place:
    def __init__(self, name):
        self.name = name

    def _place_type(self, place_id, accom_type, area, rooms, price):
        # for type safety for db storage
        return {
            'place_id': place_id,
            'name': self.name,
            'accom_type': accom_type,
            'area': area,
            'available_rooms': rooms,
            'cost_per_night': price
        }

    def _add_to_db(self, place_id, accom_type, area, rooms, price):
        place_data = self._place_type(place_id, accom_type, area, rooms, price)
        storage.save_data(place_data, 'places')

    def _change_rooms_available(self, place_data, new_rooms_available):
        new_place_data = self._place_type(place_data['place_id'], place_data['accom_type'], place_data['area'], new_rooms_available, place_data['cost_per_night'])
        storage.update_data('places', 'name', self.name, new_place_data)

    def _get_self_data(self):
        place_data = quick_sort(storage.load_data('places'), 'name')
        place_data = binary_search(place_data, self.name, 'name')
        return place_data

    def reserve_room(self, place_data):
        # reduces rooms available by 1
        num = int(place_data['available_rooms'])
        self._change_rooms_available(place_data, num - 1)

        print("Successfully completed booking!")

    def show_bookings(self):
        pass

    def unreserve_room(self):
        # increases rooms available by 1
        place_data = self._get_self_data()
        num = int(place_data['available_rooms'])
        self._change_rooms_available(place_data, num + 1)

        print("\nSuccessfully removed booking!")

    @staticmethod
    def _get_area(area_index):
        return quick_sort(AREAS)[area_index - 1]

    @staticmethod
    def _print_areas():
        cur_index = 0
        areas = quick_sort(AREAS)

        for area in areas:
            print(f'{cur_index + 1}. {area.capitalize()}')
            cur_index += 1

        return areas

    @staticmethod
    def _print_hubs():
        # transportation hubs for navigation either bus or train station
        cur_index = 0
        hubs = quick_sort(HUBS)

        for hub in hubs:
            print(f'{cur_index + 1}. {hub.capitalize()}')
            cur_index += 1

        return hubs

    @staticmethod
    def create():
        # prompts user to enter the name, accommodation type, area, available rooms, and cost per night of stay for a new place they want to add

        # initial prompt to prepare the user
        input("We will need a few details about the place\nlike name, accommodation type, area, available rooms, and cost per night of stay.\nPress enter to continue")
        print("\n")

        # to get a valid name longer than 1 char and that does not already exist
        np_name = input("Please enter a name for this new place:\n")

        while len(np_name) < 2:
            np_name = input("The name you entered is not valid, try another:\n")
        # to print out a list of valid accommodation types and prompt the user to select
        Place._print_accom_types()
        print(f"What type of place would {np_name} be?")
        np_type = ""
        while not Place._is_valid_accommodation_type(np_type):
            np_type = input("*Select a valid accommodation type from list (enter number)*: ")

        # to get an area for the accommodation
        print('\n')
        areas = Place._print_areas()
        print(f"Where would {np_name} be located within Southampton?")
        np_area = ''
        while not is_integer(np_area, [1, len(areas)]):
            np_area = input(f"*Select from list of areas in Southampton*: ")

        # to set the initial available rooms for the accommodation
        np_available_rooms = input(f"How many rooms will be available initially?:\n")
        while not is_integer(np_available_rooms):
            np_available_rooms = input(f"Please enter a number greater than 0 for initial rooms available at {np_name}:\n")

        # to set the price per night of the accommodation
        np_price_per_night = input(f"Lastly, how much would {np_name} cost per night:\n")
        while not is_integer(np_price_per_night):
            np_price_per_night = input(f"Please enter a number greater than 0 for {np_name}'s price per night\n")

        # to store the new accommodation
        new_place = Place(np_name.lower())
        new_place._add_to_db(db_id('places', 'place_id'), np_type, int(np_area), np_available_rooms, np_price_per_night)

        print(f"Successfully added {np_name} to list")

    @staticmethod
    def show_all(show_opt=False):
        # show_booking_opt=true will add a number and a prompt to the accommodation prints for user to enter and book that accommodation
        places = Place._get_sorted_places()
        if len(places) < 1:
            print(f"There are no accommodations yet!")
            return

        current_index = 0
        for i in places:
            Place._print(place=i, show_place_id=not show_opt, additional_print_line=f'*[Enter {current_index + 1} to select this place.]*' if show_opt is True else None)
            current_index += 1

        return places

    @staticmethod
    def search():
        # THIS FUNC RETURNS A PLACE AND ALL ITS DETAILS IF id USER PROVIDED MATCHES AN ID IN DB
        # ELSE FUNC RETURNS 'None'
        existing_places = Place._get_sorted_places('place_id')
        if len(existing_places) < 1:
            print(f"There are no places yet!")
            return

        retry = 'y'
        while retry.lower() == 'y':
            place_id = input("Please enter the id of the place you want to search for:\n")
            while not is_integer(place_id):
                place_id = input("Please enter a VALID id for the place you want to search for:\n")
            place_found = binary_search(existing_places, int(place_id), 'place_id', True)

            if place_found != -1:
                print(f"FOUND:\n")
                for places in place_found:
                    Place._print(places)
                retry = input(f"\nDo you want to search again? (Y/N)")
            else:
                retry = input("No results!\nTry again (Y/N)")

    @staticmethod
    def search_by_type():
        if len(storage.load_data('places')) < 1:
            print(f"There are no places yet!")
            return

        choice = 'y'

        input("To search for places by type, select accommodation type number from list.\nPress enter to continue.")
        Place._print_accom_types()
        while choice.lower() == 'y':
            search_term = input("Select an accommodation type from list to search for\n")
            while not Place._is_valid_accommodation_type(search_term):
                search_term = input("Select a VALID accommodation type from list to search for\n")

            num_found = Place._search_by(search_term, 'accom_type')
            choice = input('No result.\nSearch again? (Y/N)') if num_found < 1 else input('Search again? (Y/N)')

    @staticmethod
    def let_user_select(initial_prompt, print_func, enter_prompt=None):
        # allows user to select a place
        # then it returns the place selected along with the list of places that was available for user to select

        input("Press enter to see a list of places, then enter the number of the place you want to select." if enter_prompt is None else enter_prompt)
        places = print_func(True)

        sel_place = input(initial_prompt)
        while not is_integer(sel_place, [1, len(places)]):
            sel_place = input(f"Please enter a VALID NUMBER between 1 and {len(places)} to select corresponding place!\n")

        return {'places': places, 'sel_place': places[int(sel_place) - 1]}

    @staticmethod
    def _search_by(search_term, attr='accom_type'):
        places = Place._get_sorted_places()
        num_found = 0
        for i in places:
            if i[attr] == search_term:
                Place._print(i)
                num_found += 1

        return num_found

    @staticmethod
    def _print(place, show_place_id=False, additional_print_line=None):
        print(f"* {place['name'].upper()} *")
        print(f"area: {Place._get_area(place['area']).capitalize()}")
        print(f"type: {ACCOMMODATION_TYPES[int(place['accom_type']) - 1]}")
        print(f"rooms available: {place['available_rooms']}")
        print(f"Price per night: {place['cost_per_night']}")
        if show_place_id:
            print(f'id: {place["place_id"]}')
        if additional_print_line is not None:
            print(f'{additional_print_line}')

        print('')

    @staticmethod
    def _print_accom_types():
        type_index = 0
        for t in ACCOMMODATION_TYPES:
            type_index += 1
            print(f"{type_index}. {t}")

    @staticmethod
    def _get_sorted_places(sort_by='name'):
        return quick_sort(storage.load_data("places"), sort_by)

    @staticmethod
    def _is_valid_accommodation_type(user_input):
        # CHECKS IF THE ACCOMMODATION TYPE THE USERS HAS ENTERED CORRESPONDS WITH ANY VALID ACCOM. TYPE

        # type validation
        user_input = is_integer(user_input)
        if user_input is False:
            return False

        # index range validation
        if user_input < 1 or user_input > len(ACCOMMODATION_TYPES):
            return False

        # assign accommodation type
        chosen_type = ACCOMMODATION_TYPES[user_input - 1]
        return binary_search(ACCOMMODATION_TYPES, chosen_type) != -1

    @staticmethod
    def navigate_to():
        if len(storage.load_data('places')) < 1:
            print(f"There are no places available to navigate to!")
            return

        input('Press enter to choose starting point\n')

        hubs = Place._print_hubs()
        choice = input('Enter the number of the starting point you want to select: ')
        while not is_integer(choice, [1, len(hubs)]):
            choice = input(f'Enter a VALID number from 1 to {len(hubs)} for the starting point: ')
        sel_hub = hubs[int(choice) - 1]

        print(f'You selected {hubs[int(choice) - 1]}')

        choice = Place.let_user_select("Please enter the number of the place you want to navigate to:\n", Place.show_all, 'Press enter to select end point from list of places.\n')
        sel_place = choice['sel_place']

        input(f"Press enter to navigate from {sel_hub.capitalize()} to *{sel_place['name'].upper()}*")

        sel_area_index = sel_place['area']
        sel_area = Place._get_area(sel_area_index)
        nav_route = go_to(sel_area.lower(), sel_hub.lower())

        cur_index = 0
        for point in nav_route:
            if cur_index == len(nav_route) - 1:  # if this is last point in list of routes
                print(f"-*{sel_place['name'].upper()}* ({point})")
                return
            print(f'-{point.capitalize()}')
            cur_index += 1
