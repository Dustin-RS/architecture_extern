
from decimal import Decimal
import uuid

from catalog.registry import CategoryRegistry
from catalog.factories import BookFamilyFactory, ClothingFamilyFactory, ElectronicsFamilyFactory
from events.bus import AnalyticsHandler, EmailNotifier, EventBus, OrderPlacedEvent, SellerNotifier
from listings.dto import ListingDTO
from listings.repository import ListingRepository, ListingRepositoryCacheProxy
from listings.service import ListingService
from money import Money
from orders.commands import CommandBus, PlaceOrderCommand
from orders.context import OrderContext
from orders.handlers import CartValidationHandler, FraudCheckHandler, PaymentValidationHandler, StockReservationHandler
from orders.models import Item, Order
from payments.gateways import StripeAdapter
from payments.proxy import PaymentGatewayProxy, RetryPolicy
from payments.strategies import StripeStrategy
from pricing.calculators import BasePriceCalculator, PromotionDecorator, TaxDecorator



if __name__ == "__main__":
    registry = CategoryRegistry()
    registry.register_factory("electronics", ElectronicsFamilyFactory())
    registry.register_factory("clothing", ClothingFamilyFactory())
    registry.register_factory("books", BookFamilyFactory())

    # create repository and service
    repo = ListingRepository()
    repo_proxy = ListingRepositoryCacheProxy(repo)
    service = ListingService(registry, repo_proxy)

    # create listing DTO
    dto = ListingDTO(title="Smartphone",
                     price=Money(Decimal("399.99"), "USD"),
                     category_code="electronics",
                     attributes={"brand": "Acme", "model": "X1", "warranty_months": 24},
                     seller_id=uuid.uuid4())

    listing = service.create_listing(dto)
    print("Created listing:", listing)

    # create an order
    item = Item(listing_id=listing.get_id(), quantity=1, price_per_unit=Money(Decimal("399.99"), "USD"))
    order = Order(items=[item], buyer_id=uuid.uuid4())
    ctx = OrderContext(order)

    # handlers chain
    cart_h = CartValidationHandler()
    stock_h = StockReservationHandler()
    pay_h = PaymentValidationHandler()
    fraud_h = FraudCheckHandler()
    cart_h.set_next(stock_h).set_next(pay_h).set_next(fraud_h)
    ok = cart_h.handle(ctx)
    print("Handlers passed:", ok)

    # payments
    stripe = StripeAdapter(api_key="sk_test")
    proxy = PaymentGatewayProxy(stripe, RetryPolicy(attempts=2))
    strategy = StripeStrategy(proxy)
    res = strategy.execute_payment(order, {})
    print("Payment result:", res.success, res.tx_id)

    # event bus
    bus = EventBus()
    bus.subscribe(OrderPlacedEvent, EmailNotifier())
    bus.subscribe(OrderPlacedEvent, SellerNotifier())
    bus.subscribe(OrderPlacedEvent, AnalyticsHandler())

    # place order command
    place_cmd = PlaceOrderCommand(order, event_bus=bus)
    bus_cmd = CommandBus()
    bus_cmd.enqueue(place_cmd)
    r = bus_cmd.execute_next()
    print("Place command result:", r.success, r.message)

    # pricing example
    base_calc = BasePriceCalculator()
    promo = PromotionDecorator(base_calc)
    taxed = TaxDecorator(promo, tax_rate=0.2)
    price = taxed.calculate(listing, {"promotion_discount": Decimal("10.00")})
    print("Final price:", price)
