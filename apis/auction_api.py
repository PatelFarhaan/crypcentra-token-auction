from .models import BidData, Shares
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def process_pending_bids():
    bidding_data = process_bid_data(BidData.objects.filter(bid_status="pending").all())

    for share_code, share_price_obj in bidding_data.items():
        share_obj = get_share_details(share_code)
        if share_obj:
            share_details = share_obj.serialize()

            share_quantity = share_details.get("share_quantity")
            sorted_price_keys = sorted(share_price_obj, reverse=True)

            for price in sorted_price_keys:
                if share_quantity > 0:
                    user_object, share_quantity = distribute_token(share_price_obj[price], share_quantity)
                    share_obj.share_quantity = share_quantity
                    share_obj.save()
                    for user in user_object:
                        user.save()
            make_rest_bids_un_successful(share_price_obj)


def make_rest_bids_un_successful(bid_object: dict):
    for k, v in bid_object.items():
        for bid_data in v:
            if bid_data.number_of_tokens == 0:
                bid_data.bid_status = "failed"
                bid_data.save()


def distribute_token(bid_object, share_quantity):
    index = 0
    all_assigned = [False] * len(bid_object)

    while share_quantity > 0 and not all(all_assigned):
        if index == len(bid_object):
            index = 0

        current_bid = bid_object[index]
        if current_bid.number_of_tokens < current_bid.no_of_shares:
            current_bid.number_of_tokens += 1
            current_bid.bid_status = "success"
            share_quantity -= 1
        else:
            all_assigned[index] = True

        index += 1
    return bid_object, share_quantity


def get_share_details(share_code):
    share_obj = Shares.objects.filter(share_code=share_code).first()
    if not share_obj:
        return None
    return share_obj


def process_bid_data(bid_data):
    res = {}
    for share in bid_data:
        if share.share_code in res:
            res[share.share_code].append(share)
        else:
            res[share.share_code] = [share]

    for k, v in res.items():
        res[k] = process_share_price(v)

    return res


def process_share_price(object):
    res = {}
    for share in object:
        if share.bidding_price in res:
            res[share.bidding_price].append(share)
        else:
            res[share.bidding_price] = [share]

    for k in res:
        res[k] = sorted(res[k],
                        reverse=False,
                        key=lambda x: x.serialize()["timestamp"])
    return res


@csrf_exempt
def get_all_successful_bids(request):
    if request.method != "POST":
        return JsonResponse({
            "data": None,
            "result": False,
            "message": "method not allowed!",
        }, status=405)

    if request.body:
        return JsonResponse({
            "data": None,
            "result": False,
            "message": "this api does not take any input",
        }, status=400)

    if BidData.objects.filter(bid_status="pending").all():
        process_pending_bids()

    bd_object = BidData.objects.filter(bid_status="success").all()
    result = [bid_data.serialize() for bid_data in bd_object]
    return JsonResponse({
        "data": result,
        "result": True,
        "message": "success",
    }, status=200)


@csrf_exempt
def get_all_unsuccessful_bids(request):
    if request.method != "POST":
        return JsonResponse({
            "data": None,
            "result": False,
            "message": "method not allowed!",
        }, status=405)

    if request.body:
        return JsonResponse({
            "data": None,
            "result": False,
            "message": "this api does not take any input",
        }, status=400)

    if BidData.objects.filter(bid_status="pending").all():
        process_pending_bids()

    bd_object = BidData.objects.filter(bid_status="failed").all()
    result = [bid_data.serialize() for bid_data in bd_object]
    return JsonResponse({
        "data": result,
        "result": True,
        "message": "success",
    }, status=200)
