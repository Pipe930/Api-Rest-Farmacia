def discount(product_price, discount) -> int:

    discount_decimal = discount / 100
    price_discount = product_price * discount_decimal

    result = product_price - price_discount

    return result
