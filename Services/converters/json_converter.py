import json
import simplejson


class JsonConverter:

    def convert(self, obj):
        data = ""
        try:
            data = obj
            data = simplejson.dumps(data,  indent=4, sort_keys=True, default=str)
            data = json.loads(data)
        except Exception as e:
            print(f"convert went wrong: {e}")

        return data
