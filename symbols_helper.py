from my_database import db, SymbolCategory, Symbol


def pre_populate_forex_symbols():
    """
    Pre-populate Forex trading instrument if the `symbol` table is empty.
    """
    result = db.session.execute(db.select(SymbolCategory)).first()
    if result is None:
        forex_category = SymbolCategory(
            category_name="Forex"
        )
        db.session.add(forex_category)
        db.session.commit()

        forex_symbols = [
            # Major symbols (USD involved)
            "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "NZD/USD", "USD/CHF",

            # Minor (cross) symbols (no USD)
            "EUR/GBP", "EUR/JPY", "GBP/JPY", "AUD/JPY", "NZD/JPY", "CAD/JPY", "CHF/JPY",
            "EUR/AUD", "EUR/NZD", "GBP/AUD", "GBP/NZD", "GBP/CAD", "AUD/CAD", "AUD/NZD",
            "AUD/CHF", "CAD/CHF", "EUR/CAD", "EUR/CHF", "GBP/CHF", "NZD/CAD", "NZD/CHF",

            # Exotic symbols (less commonly traded currencies)
            "USD/TRY", "EUR/TRY", "GBP/TRY", "USD/ZAR", "USD/HKD", "USD/SGD", "USD/MXN",
            "USD/PLN", "USD/DKK", "USD/SEK", "USD/NOK", "USD/CZK", "USD/HUF", "USD/THB",
            "USD/INR", "USD/RUB", "USD/CNH", "USD/KRW", "USD/MYR", "USD/TWD", "USD/IDR",
            "USD/PHP", "USD/ILS", "USD/CLP", "USD/BRL", "USD/ARS", "EUR/PLN", "EUR/ZAR",
            "EUR/HUF", "EUR/CZK", "EUR/SEK", "EUR/NOK", "EUR/DKK", "EUR/RUB", "GBP/ZAR",
            "GBP/PLN", "AUD/SGD", "NZD/SGD", "SGD/JPY"
        ]
        for symbol_name in forex_symbols:
            new_symbol = Symbol(
                name=symbol_name,
                category=db.session.execute(db.select(SymbolCategory).filter_by(category_name="Forex")).scalar()
            )
            db.session.add(new_symbol)
        db.session.commit()
        print("Forex category and symbols pre-populated.")
