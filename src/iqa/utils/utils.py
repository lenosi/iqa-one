class Utils:
    @staticmethod
    def remove_prefix(string, prefix) -> str:
        if string.startswith(prefix):
            return string[len(prefix):]
        else:
            return string
