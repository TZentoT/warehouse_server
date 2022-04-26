

class StringConverter:

    def convert(self, string):
        result = ""
        try:
            result = str(string)
            result = result.replace("None", "null")
            result = result.replace("\'", "\"")
        except Exception as e:
            print(f"convert wrong: {e}")

        return result
