"""Legacy cost helper. Use current Azure pricing for billing; this is only an estimate."""


_PRICES_PER_MILLION_TOKENS = {
    "gpt-4o": (2.50, 10.00),
    "gpt-4o-mini": (0.15, 0.60),
    "gpt-4.1-mini": (0.40, 1.60),
}


def calculate_aoai_cost(model, prompt_tokens, completion_tokens):
    """Return a historical rough estimate; None for models without a configured rate."""
    prices = _PRICES_PER_MILLION_TOKENS.get(model)
    if prices is None:
        return None
    input_price, output_price = prices
    return (prompt_tokens * input_price + completion_tokens * output_price) / 1_000_000
