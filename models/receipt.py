from models.base_model import BaseModel
import peewee as pw
from playhouse.hybrid import hybrid_property
from config import Config

class Receipt(BaseModel):
    receipt_image = pw.CharField(unique=False, null = False)
    receipt_width = pw.IntegerField(unique=False, null=True)
    receipt_height = pw.IntegerField(unique=False, null=True)

    @hybrid_property
    def receipt_image_url(self):
        if self.receipt_image:
            return Config.S3_LOCATION + self.receipt_image

