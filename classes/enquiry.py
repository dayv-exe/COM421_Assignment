import storage
from functions.sort import quick_sort
from functions.search import binary_search
from classes.place import Place
from functions import generate


class Enquiry:
    def __init__(self, enquiry_id):
        self.enquiry_id = enquiry_id

    def _get_self_data(self):
        # uses current enquiry id to get full data on current enquiry
        data = quick_sort(storage.load_data('enquiries'), 'enquiry_id')
        data = binary_search(data, self.enquiry_id, 'enquiry_id')

        return data

    def _enquiry_type(self, accom_name, enquiry, response):
        # to make sure required values are collected for db
        # i.e. all required parameters a parsed
        return {
            'enquiry_id': int(self.enquiry_id),
            'accom_name': accom_name,
            'enquiry': enquiry,
            'response': response
        }

    def _add_to_db(self, accom_name, enquiry):
        # adds new enquiry to db
        new_data = self._enquiry_type(accom_name, enquiry, None)
        storage.save_data(new_data, 'enquiries')

        print("Your query has been submitted, you will receive a response shortly.")

    def _add_response_to_db(self, enquiry_data, response):
        # adds a response to an already existing enquiry

        new_data = self._enquiry_type(
            # creates new data which is old enquiry data with response appended
            enquiry_data['accom_name'],
            enquiry_data['enquiry'],
            response
        )

        # update storage with new data
        storage.update_data('enquiries', 'enquiry_id', enquiry_data['enquiry_id'], new_data)

        print('Your response has been saved and is now visible to the enquirer.')

    @staticmethod
    def make():
        # select place to make enquiry on
        if len(storage.load_data('places')) < 1:
            print(f"There are no places available to enquire on!")
            return

        # allow user to select a place to enquire on
        choice = Place.let_user_select("Please enter the number of the place you want to make enquiries on:\n", Place.show_all)
        sel_place = choice['sel_place']

        print(f"You have selected *{sel_place['name'].upper()}*")

        # generates random enquiry id
        enquiry_id = generate.db_id('enquiries', 'enquiry_id')

        # allows user to input their enquiry
        enquiry = input("Please enter the enquiry you have about this place:\n")

        while len(enquiry) < 3:
            enquiry = input("Please enter a VALID enquiry you have about this place:\n")

        # adds the enquiry to database
        new_enquiry = Enquiry(enquiry_id)
        new_enquiry._add_to_db(sel_place['name'], enquiry)

    @staticmethod
    def show_all(show_opt=False):
        # to print all the enquiries
        enquiries = storage.load_data('enquiries')
        if len(enquiries) < 1:
            # return if there are no enquiries yet
            print(f"There are no enquiries yet!")
            return

        current_index = 0
        print('')
        for i in enquiries:
            Enquiry._print(i, None if not show_opt else f'*[enter {current_index + 1} to respond to this enquiry]*')
            current_index += 1

        return enquiries

    @staticmethod
    def respond():
        # allows user to respond to enquiries
        if len(storage.load_data('enquiries')) < 1:
            # if there are no enquireies in db
            print("There are no enquiries to respond to!")
            return

        # let user select place
        choice = Place.let_user_select("Please enter the number of the enquiry you want to respond to:\n", Enquiry.show_all, 'Press enter to see a list of enquires, then enter the number of the enquiry you want to select.')
        selected_enquiry = choice['sel_place']

        # let user enter response to enquiry
        response = input(f'Please enter your response to the enquiry: \n')
        while len(response) < 2:
            response = input(f'Please enter a VALID response to the enquiry: \n')

        # save enquiry to db
        res_enquiry = Enquiry(selected_enquiry['enquiry_id'])
        res_enquiry._add_response_to_db(selected_enquiry, response)

    @staticmethod
    # print enquiries
    def _print(enquiry, special_line):
        print(f"for: *{enquiry['accom_name'].upper()}*")
        print(f"Customer asked: {enquiry['enquiry']}")
        if enquiry['response'] is not None:
            print(f"host response: {enquiry['response']}")
        if special_line:
            print(special_line)

        print("")
