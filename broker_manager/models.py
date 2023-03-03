from django.db import models

# Create your models here.
from broker_manager.enums import PositionTypeChoice, PositionSideChoice, Broker


class PositionManager(models.Model):
    coin_name = models.CharField(max_length=50)
    position_type = models.IntegerField(choices=PositionTypeChoice.choices, db_index=True)
    position_side = models.IntegerField(choices=PositionSideChoice.choices, db_index=True)
    quantity = models.FloatField()
    price = models.FloatField()
    candle_datetime = models.DateTimeField()
    start_send_to_broker_datetime = models.DateTimeField()
    end_send_to_broker_datetime = models.DateTimeField()
    broker = models.IntegerField(choices=Broker.choices, db_index=True)
    broker_response_status_code = models.IntegerField()
    broker_response_message = models.TextField(null=True)
    request_from = models.CharField(max_length=50)
    request_id = models.IntegerField()
    position_related = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE,
                                         related_name="base_position")

    constraints = [
        models.UniqueConstraint(fields=['request_id', 'candle_datetime'], name='unique_candle_request_id')
    ]
