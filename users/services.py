import stripe
from forex_python.converter import CurrencyRates

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def convert_rub_to_dollars(amount):
    """Конвертирует рубли в доллары."""
    c = CurrencyRates()
    rate = c.get_rate("RUB", "USD")
    return int(amount * rate)


def create_stripe_product(name: str) -> dict:
    """Создает продукт в Stripe."""
    return stripe.Product.create(name="Payment")


# def create_stripe_price(product_id: str, amount: int, currency: str = "rub") -> dict:
def create_stripe_price(product_id: str, amount: int) -> dict:
    """Создает цену для продукта в Stripe."""
    return stripe.Price.create(
        product=product_id,
        currency="rub",
        unit_amount=amount * 100,
        # product_data={"name": "Payment"},
    )


def create_stripe_session(price):
    """Создает сессию оплаты в Stripe."""
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": price.get("id"),
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url="http://127.0.0.1:8000/",
    )
    return session.get("id"), session.get("url")
