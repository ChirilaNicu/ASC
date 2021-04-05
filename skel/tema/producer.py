"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)

        # variabila pentru loop-ul infinit din funtia run
        self.producing = True

        # asignam valori
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time

        # Înregistrarea producătorului aici pentru comercializarea
        # produselor pe piață
        self.prod_id = self.marketplace.register_producer()

    def run(self):

        # Adaugă pe piață toate produsele stocate în producătorul actual
        # într-o buclă infinită.
        while self.producing:
            # EX: self.products= [["id", 2,0.18], ...]
            for j in range(len(self.products)):
                id_product = self.products[j][0]
                quantity = self.products[j][1]
                waiting_time = self.products[j][2]

                for index in range(quantity):
                    status = self.marketplace.publish(
                        str(self.prod_id), id_product)
                    # Solicitarea publicării articolului pe piață. Funcția va
                    # intoarce False dacă coada  este plină, altfel Adevarat.
                    if status:
                        time.sleep(waiting_time)
                    else:
                        # Nu vom incrementa bucla aici pentru că dorim să
                        # solicităm publicarea din nou a aceluiași produs
                        time.sleep(self.republish_wait_time)
