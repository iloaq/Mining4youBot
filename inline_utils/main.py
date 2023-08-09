from aiogram import types
from keyboards import inline_result_miners

def create_inline_results(products,chat_id):
    results = []

    for product in products:
        # Combine the name and price of the product in the description
        description = f"{product['price']}"

        # Get the product image URL, or use None if not available
        image_url = None
        try:
            image_url = product['images'][0]['src']
        except (TypeError, IndexError):
            pass

        # Create InlineQueryResultPhoto for each product
        photo_result = types.InlineQueryResultArticle(
            id=str(product['id']),
            # photo_url=image_url,
            thumb_url=image_url,
            # photo_width=1,  # Adjust the width as needed
            # photo_height=1,  # Adjust the height as needed
            title=product['name'],
            description=description,
            input_message_content=types.InputMessageContent(
                message_text=f"{product['name']} {description}",
            ),
            reply_markup=inline_result_miners.return_button(chat_id,product['id'],auth=True)
        )
        results.append(photo_result)

    return results