""" Functionality for real-time data processing.
utils/realtime.py

This module contains functionality for real-time data processing.
For example for procession orders, so that the bar can get orders easily.
"""

class OrderQueue:
    
    """A queue for orders.
    
    This is supposed to be used for the bar to get orders from and 
    for the announcement board to get the order information from.
    
    Usage:
    # Create a new queue:
    >>> queue = OrderQueue()
    
    # Add an order/cart to the queue:
    >>> queue.add(1)
    
    # Get the first order in the queue:
    >>> queue.get()
    1
    
    # Resolve the order when it is finished.
    >>> queue.resolve()
    
    """
    
    __orders: list[int]
    
    def __init__(self) -> None:
        self.__orders = []
    
    def get(self) -> int | None:
        if len(self) == 0:
            return None
        else:
            return self.__orders[0]
    
    def resolve(self) -> None:
        self.__orders.pop(0)
        
    def add(self, cart_id: int) -> None:
        self.__orders.append(cart_id)
    
    def __len__(self) -> int:
        return len(self.__orders)