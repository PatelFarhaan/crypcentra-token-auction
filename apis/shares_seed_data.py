import json
from .models import Shares
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt


def create_share_data(shares):
    all_shares = [(_share.share_name, _share.share_code) for _share in Shares.objects.all()]

    for share in shares:
        share_tuple = (share.get("share_name"), share.get("share_code"))
        if share_tuple in all_shares:
            continue

        bidding_time = share.pop("bidding_time")
        bid_start_time = datetime.utcnow()
        bid_end_time = bid_start_time + timedelta(minutes=bidding_time)

        share["bid_start_time"] = bid_start_time
        share["bid_end_time"] = bid_end_time
        Shares.objects.create(**share)


@csrf_exempt
def populate_seed_shares_data(request):
    if request.method == "POST":
        if not request.body:
            return JsonResponse({
                "data": None,
                "result": False,
                "message": "input cannot be None",
            }, status=400)

        try:
            input_data = json.loads(request.body)
        except:
            return JsonResponse({
                "data": None,
                "result": False,
                "message": "malformed input body!",
            }, status=400)

        data = validate_data(input_data)
        if not data.get("result"):
            return JsonResponse(data, status=400)

        unique_key_check = unique_share_code_validation(input_data)
        if not unique_key_check.get("result"):
            return JsonResponse(unique_key_check, status=400)

        create_share_data(input_data)
        return JsonResponse({
            "data": None,
            "result": True,
            "message": "Only new shares inserted in the database",
        }, status=200)
    else:
        return JsonResponse({
            "data": None,
            "result": False,
            "message": "method not allowed!",
        }, status=405)


@csrf_exempt
def get_all_shares(request):
    if request.method == "GET":
        try:
            all_shares = [share.serialize() for share in Shares.objects.all()]
            return JsonResponse({
                "result": True,
                "data": all_shares,
                "message": "success",
            }, status=200)
        except:
            return JsonResponse({
                "data": None,
                "result": True,
                "message": "failed",
            }, status=500)
    else:
        return JsonResponse({
            "data": None,
            "result": False,
            "message": "method not allowed!",
        }, status=405)


def unique_share_code_validation(data):
    unique_shares = []

    for share in data:
        share_name = share.get("share_name")
        share_code = share.get("share_code")
        share_tuple = (share_name, share_code)
        if not share_tuple in unique_shares:
            unique_shares.append(share_tuple)
        else:
            return {"result": False, "message": "no two shares can have the same name or code", "data": None}
    return {"result": True, "data": data}


def validate_data(data):
    key_validation = {
        "share_code": str,
        "share_name": str,
        "share_price": int,
        "bidding_time": int,
        "share_quantity": (float, int)
    }

    for share in data:
        for k, v in share.items():
            print(k, v)
            if k not in key_validation:
                return {"result": False, "message": "Additional key found in body", "data": None}
            elif not isinstance(v, key_validation.get(k)):
                return {"result": False, "data": None, "message": f"{k} should be a {key_validation[k]}!"}
        return {"result": True, "data": data}
