"""
Simulation of Query Tree Protocol

@author Sunil
@date 25.06.2021
"""

import random
import matplotlib.pyplot as pyplot


class Message(object):
    """
    A message or packet that is send and from RFID tag
    """
    def __init__(self, prefix):
        self.__len = len(prefix)
        self.__prefix = prefix

    def len(self):
        return self.__len

    def prefix(self):
        return self.__prefix

    def match(self, tag_id):
        if (self.__len > len(tag_id)):
            return False

        for i in range(self.__len):
            if (self.__prefix[i] != tag_id[i]):
                return False

        return True


class Stack(object):
    """ 
    Maintain a LIFO structure for prefix that will 
    used to identify RFID tags
    """
    def __init__(self):
        self.__stack = []

    def push(self, obj):
        self.__stack.append(obj)

    def pop(self):
        if self.empty():
            return None
        return self.__stack.pop()

    def empty(self):
        return len(self.__stack) == 0


def transmit(prefix):
    message = Message(prefix)
    return message


def respond(message, tag_ids):
    response = []
    for tag_id in tag_ids:
        if message.match(tag_id):
            response.append(tag_id)

    return response


def generateTags(tags):
    sample = random.sample(range(0, 2 ** 32 - 1), tags)
    return ['0' * (32 - len(bin(int_id)[2:])) + bin(int_id)[2:] for int_id in sample]


def efficiency(total_tag, average_time):
    return [total_tag[i] / average_time[i] * 100 for i in range(len(total_tag))]


def unmatch_bit(id1, id2, start, last):
    for i in range(start, last):
        if id1[i] != id2[i]:
            return i 
    return last


def main():
    # Ask for total tags
    total_tags = int(input("Enter the number of tags: "))

    # Array or list that store number of tags we are simulating i.e. 10, 20, 30, ..., total_tags // 10 * 10
    total_tag = []

    # Store average time for tags 10, 20, 30, ..., total // 10 * 10
    average_time = []

    for tags in range(10, total_tags + 1, 10):
        total_tag.append(tags)

        # Reapating experiment multiple times so can average
        trails = 1

        total_time = 0

        for trail in range(trails):
            # Generating 'tags' randomly for experiment
            tag_ids = generateTags(tags)

            # Pushing initial prefix in stack
            prefix = ""
            stack = Stack()
            stack.push(prefix)

            # Storing number of requests made by reader to read all tags
            # Assuming a request take one unit of time
            requests = 0
            while not stack.empty():
                prefix = stack.pop()

                message = transmit(prefix)
                response = respond(message, tag_ids)
                
                # Finding collision bit
                if len(response) > 1:
                    tmp = response.pop()
                    start = len(prefix)
                    last = 32
                    for curr_id in response:
                        last = unmatch_bit(curr_id, tmp, start, last)
                    
                    stack.push(prefix + tmp[start:last] + '0')
                    stack.push(prefix + tmp[start:last] + '1')

                requests += 1

            total_time += requests

        average_time.append(total_time / trails)

    print(f"Efficiency: {sum(efficiency(total_tag, average_time)) / len(total_tag)}")

    pyplot.plot(total_tag, average_time)
    pyplot.xlabel("Number of Tags")
    pyplot.ylabel("Number of Transmission")
    pyplot.title("Tags Vs Transmission")
    pyplot.show()

    return


if __name__ == "__main__":
    main()