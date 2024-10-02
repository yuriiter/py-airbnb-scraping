import re

def extract_listing_info(item, encoded_params):
    listing = item.get('listing', {})
    price_info = item.get('pricingQuote', {}).get('structuredStayDisplayPrice', {}).get('primaryLine', {})

    avgRatingLocalized = listing.get('avgRatingLocalized')

    if avgRatingLocalized:
        parts = avgRatingLocalized.split(' ')
        if len(parts) >= 2:
            avg_rating, num_of_rates_unprocessed = parts[0], ' '.join(parts[1:])
        else:
            avg_rating, num_of_rates_unprocessed = parts[0], ""
    else:
        avg_rating, num_of_rates_unprocessed = "", ""

    num_of_rates_match = re.search(r'\((\d+)\)', num_of_rates_unprocessed)
    num_of_rates = num_of_rates_match.group(1) if num_of_rates_match else None

    coordinate = listing.get('coordinate', {})

    if '__typename' in coordinate:
        coordinate.pop('__typename')

    discounted_price = price_info.get('discountedPrice')
    original_price = price_info.get('originalPrice')
    price = discounted_price if discounted_price else price_info.get('price')

    return {
        'id': listing.get('id'),
        'url': f"https://airbnb.com/rooms/{listing.get('id')}?{encoded_params}",
        'name': listing.get('name'),
        'title': listing.get('title'),
        'avg_rating': avg_rating,
        'num_of_rates': num_of_rates,
        'room_type': listing.get('roomTypeCategory'),
        'price': price,
        'original_price': original_price,
        'discounted_price': discounted_price,
        'price_qualifier': price_info.get('qualifier'),
        # 'pictures': " - ".join([pic.get('picture') for pic in item.get('contextualPictures', [])]),
        'badges': " - ".join([badge.get('text') for badge in item.get('badges', [])]),
        **coordinate
    }

def extract_airbnb_listings(data, encoded_params):
    map_search_results = data.get('presentation', {}).get('staysSearch', {}).get('results', {}).get('searchResults', [])

    listings = [extract_listing_info(i, encoded_params) for i in map_search_results]

    return listings

def handle_response(response, encoded_params, listings):
    """Handle the response for listings."""
    if "operationName=StaysSearch" in response.url:
        json_response = response.json()
        new_listings = extract_airbnb_listings(json_response.get('data', {}), encoded_params)
        listings.extend(new_listings)
