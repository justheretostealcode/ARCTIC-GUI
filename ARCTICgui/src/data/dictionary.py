"""File containing a custom class to store the dictionary"""
class Dictionary(dict):

    def __missing__(self, key: str) -> str:
        """Overwriting default behaviour to return the key as a string if the key can't be found inside the dictionary
        
        Args:
            key (str): the key who was looked up in the dictionary

        Returns:
            str: the key as a string 
        """
        return str(key)