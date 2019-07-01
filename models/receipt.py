from models.base_model import BaseModel
import peewee as pw
from playhouse.hybrid import hybrid_property
from config import Config

class Receipt(BaseModel):
    receipt_image = pw.CharField(unique=False, null = False)

    @hybrid_property
    def receipt_image_url(self):
        if self.receipt_image:
            return Config.S3_LOCATION + self.receipt_image

