""" Database functionality for interacting with orders.
/db/ordering.py
"""

from src.db.schemas import Cart, CartItem, Product
from sqlalchemy.orm import Session as DBSession


def create_cart(db_session: DBSession, user_id: int) -> Cart:
    """Create a cart for a user."""
    cart = Cart(user=user_id, payed=False, ready=False, delivered=False)
    db_session.add(cart)
    db_session.commit()
    return cart


def get_cart_by_user(db_session: DBSession, user_id: int) -> Cart:
    """Get a cart by its ID."""
    return db_session.query(Cart).filter(Cart.user == user_id).first()


def user_has_cart(db_session: DBSession, user_id: int) -> bool:
    """Check if a user has a cart that is not payed, ready or delivered."""
    return (
        db_session.query(Cart)
        .filter(
            Cart.user == user_id,
            Cart.payed == False,
            Cart.ready == False,
            Cart.delivered == False,
        )
        .first()
        is not None
    )


def add_to_cart(db_session: DBSession, cart_id: int, product_id: int) -> None:
    """Add a product to a cart."""
    cart_item = CartItem(cart=cart_id, product=product_id)
    db_session.add(cart_item)
    db_session.commit()
    return


def get_cart_total(db_session: DBSession, cart_id: int) -> int:
    """Get the total price of a cart."""
    cart_items = db_session.query(CartItem).filter(CartItem.cart == cart_id).all()
    total = 0
    for cart_item in cart_items:
        product = (
            db_session.query(Product).filter(Product.id == cart_item.product).first()
        )
        if product is not None:
            total += product.price
        else:
            print("User has a cart item with a product that does not exist.")
    return total


def get_cart_items(db_session: DBSession, cart_id: int) -> list[CartItem]:
    """Get the items in a cart."""
    return db_session.query(CartItem).filter(CartItem.cart == cart_id).all()


def remove_cart_item(db_session: DBSession, cart_item_id: int) -> None:
    """Remove a cart item from the database."""
    cart_item = db_session.query(CartItem).filter(CartItem.id == cart_item_id).first()
    # TODO What if the cart item does not exist?
    db_session.delete(cart_item)
    db_session.commit()
    return


def set_cart_is_ready(db_session: DBSession, cart_id: int) -> None:
    """Set that the cart is ready for pickup."""
    cart = db_session.query(Cart).filter(Cart.id == cart_id).first()
    if cart is None:
        print("Tried to set a cart to ready, but the cart does not exist.")
        return
    cart.ready = True
    db_session.commit()
    return


def set_cart_is_delivered(db_session: DBSession, cart_id: int) -> None:
    """Set that the cart has been delivered."""
    cart = db_session.query(Cart).filter(Cart.id == cart_id).first()
    if cart is None:
        print("Tried to set a cart to delivered, but the cart does not exist.")
        return
    cart.delivered = True
    db_session.commit()
    return