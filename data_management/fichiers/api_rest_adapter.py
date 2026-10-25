import json
from urllib.request import urlopen

from .file_adapter import FileAdapter
from .unified_data import UnifiedData

class ApiRestThirdPartyAdapter(FileAdapter):

    def __init__(self, url):
        self.url = url

    def adapt(self):

        with urlopen(self.url) as response:

            contenu = response.read()

            donnees = json.loads(
                contenu.decode("utf-8")
            )

        resultat = {
            "source": "API REST",
            "url": self.url,
            "donnees": donnees
        }

        return UnifiedData(resultat)