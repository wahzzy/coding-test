class LinkedList:
    def __init__(self, head, tail):
        self.head = head
        self.tail = tail


def cons(head, tail=None):
    return LinkedList(head, tail)


def listToString(list):
    if list is None:
        return ""
    if list.tail is None:
        return str(list.head)
    return str(list.head) + " " + listToString(list.tail)


def myMap(fn, list):
    if list is None:
        return None
    return cons(fn(list.head), myMap(fn, list.tail))


def myReduce(fn, accm, list):
    if list is None:
        return accm
    return myReduce(fn, fn(accm, list.head), list.tail)


def myReduceRight(fn, accm, list):
    """
    This is similar to myReduce, with the difference that it calls the reducer function fn from the end of the list to the beginning.
    For example, if the list is cons(1, cons(2, cons(3))), myReduceRight(fn, accm, list) should return the result of evaluating fn(1, fn(2, fn(3, accm))).
    """
    if list is None:
        return accm
    return fn(list.head, myReduceRight(fn, accm, list.tail))


if __name__ == "__main__":
    example_list = cons(1, cons(2, cons(3, cons(4))))

    # myReduceRight(xTimeTwoPlusY, 0, exampleList) should evalute to 20
    assert myReduceRight(lambda x, y: x * 2 + y, 0, example_list) == 20

    # myReduceRight(unfoldCaculation, "accm", exampleList) should evalute to fn(1, fn(2, fn(3, fn(4, accm)))).
    assert (
        myReduceRight(lambda x, accm: f"fn({x}, {accm})", "accm", example_list)
        == "fn(1, fn(2, fn(3, fn(4, accm))))"
    )

    # myReduceRight(printXAndReturnY, 0, exampleList) should print out the content of the list in the reverse order.
    def printXAndReturnY(x, y):
        print(x)
        return y

    myReduceRight(printXAndReturnY, 0, example_list) # Output 4 3 2 1
