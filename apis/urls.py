from django.urls import path
from .bid_api import process_bid_data
from .shares_seed_data import populate_seed_shares_data, get_all_shares
from .auction_api import get_all_successful_bids, get_all_unsuccessful_bids


urlpatterns = [
    path("process-bid", process_bid_data, name='bid-api'),
    path("get-all-shares", get_all_shares, name='get-all-shares'),
    path("create-shares", populate_seed_shares_data, name='create-shares'),
    path("get-successful-bids", get_all_successful_bids, name='successful-bids'),
    path("get-unsuccessful-bids", get_all_unsuccessful_bids, name='unsuccessful-bids'),
]
