from enum import Enum
# todo: think about really wanting this, since this change will cause a big refactoring
class FECategory(Enum):
    HAUSHALTSGERAETE = "Haushaltsgeraete"
    KAFFEE_ZUBEHOER = "Kaffee & Zubehoer"
    REINIGUNG_WASCHMITTEL = "Reinigung & Waschmittel"
    BATTERIEN_AKKUS = "Batterien & Akkus"
    BELEUCHTUNG = "Beleuchtung"
    ELEKTRONIK = "Elektronik"
    ERSATZTEILE_ZUBEHOER = "Ersatzteile & Zubehoer"
    SERVICE = "Service"
    LIEFERSERVICE = "Lieferservice"
    KUECHENGERAETE = "Kuechengeraete"
    OTHERS = "others"
