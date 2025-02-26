# coding=utf-8
from otlmow_model.OtlmowModel.BaseClasses.OTLObject import OTLAttribuut
from ...Classes.Abstracten.SerienummerObject import SerienummerObject
from ...Classes.ImplementatieElement.AIMNaamObject import AIMNaamObject
from otlmow_model.OtlmowModel.BaseClasses.BooleanField import BooleanField
from ...Datatypes.KlContactpuntMerk import KlContactpuntMerk
from ...Datatypes.KlContactpuntModelnaam import KlContactpuntModelnaam
from ...Datatypes.KlContactpuntType import KlContactpuntType
from otlmow_model.OtlmowModel.GeometrieTypes.PuntGeometrie import PuntGeometrie


# Generated with OTLClassCreator. To modify: extend, do not edit
class Contactpunt(SerienummerObject, AIMNaamObject, PuntGeometrie):
    """Techniek voor het meten van een aan- of afwezigheid van contact tussen de onderdelen waaraan deze bevestigd is."""

    typeURI = 'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Contactpunt'
    """De URI van het object volgens https://www.w3.org/2001/XMLSchema#anyURI."""

    def __init__(self):
        super().__init__()

        self.add_valid_relation(relation='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Bevestiging', target='https://wegenenverkeer.data.vlaanderen.be/ns/abstracten#Behuizing', direction='u')  # u = unidirectional
        self.add_valid_relation(relation='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Bevestiging', target='https://wegenenverkeer.data.vlaanderen.be/ns/abstracten#Toegangselement', direction='u')  # u = unidirectional
        self.add_valid_relation(relation='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Bevestiging', target='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Afsluiting', direction='u')  # u = unidirectional
        self.add_valid_relation(relation='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Bevestiging', target='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Bovenbouw', direction='u', deprecated='2.1.0')  # u = unidirectional
        self.add_valid_relation(relation='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Bevestiging', target='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Brandblusser', direction='u')  # u = unidirectional
        self.add_valid_relation(relation='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Bevestiging', target='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#PutBovenbouw', direction='u')  # u = unidirectional
        self.add_valid_relation(relation='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Bevestiging', target='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Toegangsluik', direction='u')  # u = unidirectional
        self.add_valid_relation(relation='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#HoortBij', target='https://wegenenverkeer.data.vlaanderen.be/ns/installatie#Vluchtganginrichting', direction='o')  # o = direction: outgoing
        self.add_valid_relation(relation='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Sturing', target='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#IOKaart', direction='u')  # u = unidirectional
        self.add_valid_relation(relation='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Sturing', target='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Toegangscontroller', direction='u')  # u = unidirectional

        self._isBuiten = OTLAttribuut(field=BooleanField,
                                      naam='isBuiten',
                                      label='is buiten',
                                      objectUri='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Contactpunt.isBuiten',
                                      definition='Geeft aan of het contactpunt zich binnen of buiten bevindt.',
                                      owner=self)

        self._isOpbouw = OTLAttribuut(field=BooleanField,
                                      naam='isOpbouw',
                                      label='is opbouw',
                                      objectUri='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Contactpunt.isOpbouw',
                                      definition='Geeft aan of het contactpunt door middel van opbouw gerealiseerd is.',
                                      owner=self)

        self._isWisselcontact = OTLAttribuut(field=BooleanField,
                                             naam='isWisselcontact',
                                             label='is wisselcontact',
                                             objectUri='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Contactpunt.isWisselcontact',
                                             definition="Geeft aan of het contactpunt een wisselcontact is. Bij een wisselcontact kan men zelf instellen het contact 'normaal open' of 'normaal toe' is bij een stroompanne.",
                                             owner=self)

        self._merk = OTLAttribuut(field=KlContactpuntMerk,
                                  naam='merk',
                                  label='merk',
                                  objectUri='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Contactpunt.merk',
                                  definition='Het merk van het contactpunt.',
                                  owner=self)

        self._modelnaam = OTLAttribuut(field=KlContactpuntModelnaam,
                                       naam='modelnaam',
                                       label='modelnaam',
                                       objectUri='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Contactpunt.modelnaam',
                                       definition='De modelnaam van het contactpunt.',
                                       owner=self)

        self._type = OTLAttribuut(field=KlContactpuntType,
                                  naam='type',
                                  label='type contactpunt',
                                  objectUri='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Contactpunt.type',
                                  definition='Typering van de gebruikte techniek op basis waarvan de aan- of afwezigheid van een contact vastgesteld wordt.',
                                  owner=self)

    @property
    def isBuiten(self) -> bool:
        """Geeft aan of het contactpunt zich binnen of buiten bevindt."""
        return self._isBuiten.get_waarde()

    @isBuiten.setter
    def isBuiten(self, value):
        self._isBuiten.set_waarde(value, owner=self)

    @property
    def isOpbouw(self) -> bool:
        """Geeft aan of het contactpunt door middel van opbouw gerealiseerd is."""
        return self._isOpbouw.get_waarde()

    @isOpbouw.setter
    def isOpbouw(self, value):
        self._isOpbouw.set_waarde(value, owner=self)

    @property
    def isWisselcontact(self) -> bool:
        """Geeft aan of het contactpunt een wisselcontact is. Bij een wisselcontact kan men zelf instellen het contact 'normaal open' of 'normaal toe' is bij een stroompanne."""
        return self._isWisselcontact.get_waarde()

    @isWisselcontact.setter
    def isWisselcontact(self, value):
        self._isWisselcontact.set_waarde(value, owner=self)

    @property
    def merk(self) -> str:
        """Het merk van het contactpunt."""
        return self._merk.get_waarde()

    @merk.setter
    def merk(self, value):
        self._merk.set_waarde(value, owner=self)

    @property
    def modelnaam(self) -> str:
        """De modelnaam van het contactpunt."""
        return self._modelnaam.get_waarde()

    @modelnaam.setter
    def modelnaam(self, value):
        self._modelnaam.set_waarde(value, owner=self)

    @property
    def type(self) -> str:
        """Typering van de gebruikte techniek op basis waarvan de aan- of afwezigheid van een contact vastgesteld wordt."""
        return self._type.get_waarde()

    @type.setter
    def type(self, value):
        self._type.set_waarde(value, owner=self)
