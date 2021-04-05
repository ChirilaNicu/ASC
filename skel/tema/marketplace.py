"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import multiprocessing
from threading import currentThread


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """

        self.producer_queue = queue_size_per_producer
        # numarul de carucioare in utilizare
        self.num_carts = 0
        # numarul de produse in coada
        self.producer_quantity = list()
        # coada ce contine toate produsele
        self.products = list()
        # dictionar ce contine carucioare pentru fiecare client
        self.carts = dict()
        # dictionar pt produse si producatori
        self.producers = dict()

        self.lock = multiprocessing.Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.lock.acquire()
        try:
            # id este indexul producatorului din lista producer_quantity
            id_product = len(self.producer_quantity)
            self.producer_quantity.append(0)
        finally:
            self.lock.release()
        return id_product

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        # creste numarul de produse generate de producator si le
        # afiseaza in magazin pentru a fi vandute
        if self.producer_quantity[int(producer_id)] >= self.producer_queue:
            return False

        self.producer_quantity[int(
            producer_id)] = self.producer_quantity[int(producer_id)] + 1
        # append is thread safe
        self.products.append(product)
        self.producers[product] = int(producer_id)
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer.

        @returns an int representing the cart_id
        """
        self.lock.acquire()
        try:
            self.num_carts = self.num_carts + 1
            cart_id = self.num_carts
        finally:
            self.lock.release()
            self.carts[cart_id] = list()

        # fiecare carucior nou primeste un nou id pentru entrarile din dictionar
        return cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it
        should wait and then try again
        """
        # adauga produsul in cos, eliminandu-l din lista de produse si
        # decrementeaza cantitatea acestuia din  lista de cantitati
        self.lock.acquire()
        try:
            if product not in self.products:
                return False

            self.producer_quantity[self.producers[product]
                                   ] = self.producer_quantity[
                                       self.producers[product]] - 1

            self.products.remove(product)
        finally:
            self.lock.release()
        self.carts[cart_id].append(product)

        return True

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        # elimina produsul din cos, adaugandu-l in lista de produse si
        # incrementeaza cantitatea acestuia in lista de cantitati
        self.carts[cart_id].remove(product)
        self.products.append(product)

        self.lock.acquire()
        try:
            self.producer_quantity[self.producers[product]
                                   ] = self.producer_quantity[
                                       self.producers[product]] + 1
        finally:
            self.lock.release()

    def place_order(self, cart_id):
        """
        Returns a list with all the products in the cart.

        @type cart_id: Int
        @param cart_id: id cart
        """
        prod_list = self.carts.pop(cart_id)

        for prod in enumerate(prod_list):
            self.lock.acquire()
            try:
                # printeaza continutul din output
                print(f"{currentThread().getName()} bought {prod[1]}")
            finally:
                self.lock.release()

        return prod_list
