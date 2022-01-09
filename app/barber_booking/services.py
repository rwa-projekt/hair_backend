import json
from .models import *
from django.shortcuts import get_object_or_404
from .serializers import *


def get_json_data_from_formdata(formdata):
    data = json.loads(formdata['data'])
    return data


def add_hair_style(formdata, files=None):
    data = get_json_data_from_formdata(formdata)
    print(data)

    file = files[0] if files else None

    hair_style = HairStyle.objects.create(
        avatar = file,
        **data
    )

    return hair_style

class HairStyleService:
    def __init__():
        pass

    @classmethod
    def set_avatar(self, pk, files):
        print("Postavljanje avatara")
        file = files[0] if files else None

        obj = get_object_or_404(HairStyle, id=pk)
        obj.avatar = file
        obj.save()
        return obj