from django.urls import path
from .bid_api import process_bid_data
from .auction_api import process_auction_data
from .shares_seed_data import populate_seed_shares_data, get_all_shares


urlpatterns = [
    path("process-bid", process_bid_data, name='bid-api'),
    path("get-all-shares", get_all_shares, name='get-all-shares'),
    path("create-shares", populate_seed_shares_data, name='create-shares'),
    path("get-auction-details", process_auction_data, name='auction-detials'),
]
