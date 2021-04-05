"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.marketplace = marketplace
        self.carts = carts
        self.retry_wait_time = retry_wait_time

    def run(self):
        # Creează fiecare coș nou și efectuează operațiunile
        # specificate pe acesta
        for j in range(len(self.carts)):
            cart_id = self.marketplace.new_cart()

            for i in range(len(self.carts[j])):
                index = 0

                while self.carts[j][i]["quantity"] > index:
                    if self.carts[j][i]['type'] == 'add':
                        status = self.marketplace.add_to_cart(
                            cart_id, self.carts[j][i]['product'])
                    elif self.carts[j][i]['type'] == 'remove':
                        status = self.marketplace.remove_from_cart(
                            cart_id, self.carts[j][i]['product'])

                    if status:
                        index += 1
                    # daca status este null
                    elif status is None:
                        index += 1
                    else:
                        # Când o operațiune de carucior eșuează, consumatorul
                        # doarme pentru `retry_wait_time` secunde.
                        time.sleep(self.retry_wait_time)

            self.marketplace.place_order(cart_id)
