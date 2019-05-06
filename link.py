import requests, sys

class ELink:
    def __init__(self, server='http://rest.ensembl.org'):
        self.server = server

    def do_query(self, ext):
        print(self.server + ext)
        r = requests.get(self.server + ext, headers={"Content-Type": "application/json"})

        if not r.ok:
            r.raise_for_status()
            return {}

        decoded = r.json()
        return decoded


    def list_species(self, limit):
        json = self.do_query("/info/species")

        species = json["species"]
        names = []
        for s in species:
            names.append(s["display_name"])

        if limit > 0:
            names = names[:limit]

        print(names, limit)
        return names

    def karyotype(self, specie):
        json = self.do_query("/info/assembly/" + specie)

        print(json["karyotype"])
        return json["karyotype"]

    def chromosome_Length(self, specie, chromo):
        json = self.do_query("/info/assembly/" + specie)
        top = json["top_level_region"]
        for obj in top:
            if obj['name'] == chromo:
                return obj['length']

        print(json['karyotype'])
        return -1
