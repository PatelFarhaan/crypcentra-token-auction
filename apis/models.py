from django.db import models
from datetime import datetime


class BidData(models.Model):
    user_pk = models.IntegerField(models.ForeignKey('users.id', on_delete=models.CASCADE))
    timestamp = models.DateTimeField(default=datetime.utcnow)
    number_of_tokens = models.IntegerField(default=0)
    bid_status = models.CharField(max_length=15)
    share_code = models.CharField(max_length=30)
    id = models.IntegerField(primary_key=True)
    user_id = models.CharField(max_length=30)
    no_of_shares = models.IntegerField()
    bidding_price = models.FloatField()

    def __repr__(self):
        return self.user_id

    def serialize(self):
        return {
            "user_id": self.user_id,
            "timestamp": self.timestamp,
            "share_code": self.share_code,
            "bid_status": self.bid_status,
            "no_of_shares": self.no_of_shares,
            "bidding_price": self.bidding_price,
            "number_of_tokens": self.number_of_tokens,
        }


class Users(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.CharField(max_length=30)

    def __repr__(self):
        return self.user_id


class Shares(models.Model):
    share_quantity = models.IntegerField(default=0)
    share_name = models.CharField(max_length=30)
    share_code = models.CharField(max_length=30)
    id = models.IntegerField(primary_key=True)
    bid_start_time = models.DateTimeField()
    bid_end_time = models.DateTimeField()
    share_price = models.FloatField()

    def __repr__(self):
        return self.share_name

    def serialize(self):
        return {
            "share_code": self.share_code,
            "share_name": self.share_name,
            "share_price": self.share_price,
            "bid_end_time": self.bid_end_time,
            "bid_start_time": self.bid_start_time,
            "share_quantity": self.share_quantity
        }
