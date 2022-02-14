import json


class DataAbstract:
    """
    Args: 1) data 2) check_ser 3) pk 4)files 
    Kwargs: token
    """
    data = None
    files = None
    check_ser = None
    pk = None
    token = None
    user = None
    validated_data = None

    def __init__(self, *args, **kwargs):
        self.reset()
        self.token = kwargs.get('token', None)
        if len(args) >= 1:
            self.data = args[0]

            if len(args) >= 2:
                self.check_ser = args[1]

                if len(args) >= 3:
                    self.pk = args[2]

                    if len(args) >= 4:
                        self.files = args[3]
                        if 'data' in self.data:
                            self.data = json.loads(self.data['data'])
                        else:
                            self.data = {}
                        
        self.user = kwargs.get('user', None)
        
        self.check_request_data()
        print(self.data)

    def reset(self):
        self.data = None
        self.files = None
        self.check_ser = None
        self.pk = None
        self.token = None
        self.user = None
        self.validated_data = None

    def check_request_data(self):
        if self.check_ser:
            if self.pk: self.data['pk'] = self.pk
            print("Provjera podataka...")
            ser = self.check_ser(data = self.data)
            ser.is_valid(raise_exception=True)
            self.validated_data = ser.data
        return True