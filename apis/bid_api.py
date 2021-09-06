import pytz
import json
from datetime import datetime
from django.http import JsonResponse
from .models import BidData, Users, Shares
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def process_bid_data(request):
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

        data = validate_schema(input_data)
        if not data.get("result"):
            return JsonResponse(data, status=400)

        user_id = input_data["user_id"]
        user_obj = Users.objects.filter(user_id=user_id).first()
        if not user_obj:
            Users.objects.create(user_id=user_id)
            user_obj = Users.objects.filter(user_id=user_id).first()

        share_exists = Shares.objects.filter(share_code=input_data["share_code"]).first()
        if not share_exists:
            all_sharescode = [share.share_code for share in Shares.objects.all()]
            return JsonResponse({
                "data": None,
                "result": False,
                "message": f"share does not exist. Here is the list of available shares {all_sharescode}",
            }, status=400)

        if input_data.get("no_of_shares") <= 0:
            return JsonResponse({
                "data": None,
                "result": False,
                "message": f"Number of shares cannot be less than 1",
            }, status=400)

        bid_start_time = share_exists.bid_start_time
        bid_end_time = share_exists.bid_end_time

        if bid_start_time <= pytz.UTC.localize(datetime.utcnow()) <= bid_end_time:
            input_data["user_pk"] = user_obj.id
            input_data["bid_status"] = "pending"
            BidData.objects.create(**input_data)
            return JsonResponse({
                "data": None,
                "result": True,
                "message": "bid has been successfully received!",
            }, status=200)
        else:
            return JsonResponse({
                "data": None,
                "result": False,
                "message": "The time frame to buy the stock has expired",
            }, status=400)
    else:
        return JsonResponse({
            "data": None,
            "result": False,
            "message": "method not allowed!",
        }, status=405)


def validate_schema(data):
    key_object_type = {
        "user_id": str,
        "share_code": str,
        "no_of_shares": int,
        "bidding_price": (float, int),
    }

    for k, v in data.items():
        if k not in key_object_type:
            return {"result": False, "data": None, "message": f"{k} is a additional key"}
        elif not isinstance(v, key_object_type.get(k)):
            return {"result": False, "data": None, "message": f"{k} should be a {key_object_type[k]}!"}
    return {"result": True, "data": data}
