""" Functionality for real-time data processing.
utils/realtime.py

This module contains functionality for real-time data processing.
For example for procession orders, so that the bar can get orders easily.
"""

from sqlalchemy.orm import Session as DBSession
from src.db import ordering


class OrderQueue:

    """A queue for orders.

    This is supposed to be used for the bar to get orders from and
    for the announcement board to get the order information from.
    """

    __orders: list[int]
    __db_session: DBSession

    def __init__(self, db_session: DBSession) -> None:
        self.__orders = []
        self.__db_session = db_session

    def get_current_order_id(self) -> int | None:
        """Get the current order."""
        if len(self) == 0:
            return None
        else:
            return self.__orders[0]

    def order_ready(self) -> None:
        """Mark the current order as ready."""
        if len(self) == 0:
            return
        else:
            ordering.set_cart_is_ready(self.__db_session, self.__orders[0])

    def order_delivered(self) -> None:
        """Mark the current order as delivered."""
        if len(self) == 0:
            return
        else:
            ordering.set_cart_is_delivered(self.__db_session, self.__orders[0])
            self.__orders.pop(0)

    def add(self, cart_id: int) -> None:
        """Add an order to the queue.

        It assumes that the cart is already payed for.
        """
        self.__orders.append(cart_id)

    def move_order_to_top(self, cart_id: int) -> None:
        """Move an order to the top of the queue."""
        self.__orders.remove(cart_id)
        self.__orders.insert(0, cart_id)

    def all(self) -> list[int]:
        """Get all orders in the queue."""
        return self.__orders.copy()

    def __len__(self) -> int:
        return len(self.__orders)
