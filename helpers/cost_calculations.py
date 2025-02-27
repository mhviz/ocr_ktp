# function for calculate gpt-model cost
def calculate_aoai_cost(model, prompt_tokens, completion_tokens):
    # Pricing per 1,000,000 tokens
    if model == 'gpt-4o':
        input_price_per_million = 2.5
        output_price_per_million = 10 
    elif model == 'gpt-4o-mini':
        input_price_per_million = 0.15
        output_price_per_million = 0.60

    # Convert pricing to per token
    input_price_per_token = input_price_per_million / 1_000_000
    output_price_per_token = output_price_per_million / 1_000_000

    # Calculate cost for each type of token
    prompt_cost = prompt_tokens * input_price_per_token
    completion_cost = completion_tokens * output_price_per_token

    # Total cost
    total_cost = prompt_cost + completion_cost

    return total_cost