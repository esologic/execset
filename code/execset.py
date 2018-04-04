from code.library_python.logger import logger


class Element(object):
    pass


class SetOfElements(object):

    # init the command list object
    def __init__(self):

        # the actual command list
        self.element_list = []

    def __iter__(self):
        """
        Makes this thing an iterable
        :return: the list of nodes
        """
        return iter(self.element_list)

    def __len__(self):
        return len(self.element_list)

    # returns the oldest element in the set and then removes that element from the set
    def dequeue_element(self):
        try:
            output = self.get_element(0, True)
        except IndexError:
            raise IndexError("Couldn't dequeue element, set is empty!")
        return output

    # adds a new element to the back of the list
    def enqueue_element(self, element):
        self.element_list.append(element)

    # append the command list with our new commands
    def enqueue_elements(self, elements):
        self.element_list = self.element_list + elements

    # add incoming set to the end of this map set. The new elements will be AFTER the existing ones
    def append_with_set(self, incoming_element_set):
        new_element_list = incoming_element_set.get_element_list()

        logger.info("Appending with set, current count [" + str(len(self.element_list)) + "] incoming length [" + str(len(new_element_list)) + "]")

        self.enqueue_elements(new_element_list)

        logger.info("Set appended, new count [" + str(len(self.element_list)) + "]")

    # return the entire list of elements stored in this set of elements
    def get_element_list(self):
        return self.element_list

    # return the final element in the list
    def get_final_element(self):
        return self.get_element(self.get_number_of_remaining_elements() - 1, False)

    # this is a function to return a given element from the set of elements
    # if delete is True, it will delete the element after it has been gotten
    # if there is no element in the location, it will return false
    def get_element(self, location, delete=False):

        # check and see if an element exists at the location
        try:
            # output = copy(self.element_list[location])
            output = self.element_list[location]

            if delete:
                del self.element_list[location]

        # it will throw an error if it doesn't
        except IndexError as e:
            raise IndexError("The element could not be retrieved")

        return output

    # a function to return the remaining elements in the list
    def get_number_of_remaining_elements(self):
        return len(self.element_list)

    # replaces an element in the existing element list, returns true of it works, false if it fails
    def replace_element_at_location(self, element_location, element):

        try:
            del self.element_list[element_location]
            self.element_list.insert(element_location, element)
            return True

        except IndexError as e:
            logger.info("The element could not be replaced")
            return False

    # gets a chunk of elements out of the list based on the two locations given
    # a chunk implies that the elements are REMOVED from the list once they are extracted
    # the result is returned as an elementlist itself
    def get_chunk_of_elements(self, start_location, end_location, delete=True):

        try:
            self.element_list[start_location]
        except IndexError as e:
            raise ValueError("No element at chunk starting location")

        try:
            self.element_list[end_location]
        except IndexError as e:
            raise ValueError("No element at chunk ending location")

        elements = self.element_list[start_location: end_location]

        if delete:
            del self.element_list[start_location: end_location]

        out_set = SetOfElements()

        out_set.element_list = elements

        return out_set

    def print_set(self):

        out = "["
        for element in self.element_list:
            out += str(element) + ", "
        out += "]"

        logger.info("" + out)


class PriorityElement(Element):

    def __init__(self, priority):
        self.priority = priority


class PrioritySetOfElements(SetOfElements):

    def __init__(self):
        super(PrioritySetOfElements, self).__init__()

    def enqueue_element(self, incoming_element):

        new_priority = incoming_element.priority

        insert_location = len(self.element_list)
        element_number = 0

        for element_number, element in enumerate(self.element_list):

            priority = element.priority

            if priority > new_priority:
                insert_location = element_number
                break

        elements_prior_to = self.element_list[:insert_location]
        elements_after_insert = self.element_list[insert_location:]

        self.element_list = elements_prior_to + [incoming_element] + elements_after_insert


