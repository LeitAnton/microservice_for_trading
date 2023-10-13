from schemas.actions import Subscribe, Unsubscribe


async def subscribe_serializer(subscribe: Subscribe):
    list_of_symbols = [f'{symbol}-USD' for symbol in subscribe.symbols]
    request = {
        'type': subscribe.action,
        'product_ids': list_of_symbols,
        'channels': [
            {
                'name': 'ticker',
                'product_ids': list_of_symbols
            }
        ]
    }
    print(request)
    return request


async def unsubscribe_serializer(unsubscribe: Unsubscribe):
    request = {
        'type': unsubscribe.action,
        'channels': [
            {
                'name': 'ticker',
                'product_ids': [f'{symbol}-USD' for symbol in unsubscribe.symbols]
            }
        ]
    }
    return request
