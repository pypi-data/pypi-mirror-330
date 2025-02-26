# coding=utf-8
from otlmow_model.OtlmowModel.BaseClasses.KeuzelijstField import KeuzelijstField


# Generated with OTLEnumerationCreator. To modify: extend, do not edit
class KlTypeHoogtebegrenzer(KeuzelijstField):
    """De mogelijke types van een hoogtebegrenzer."""
    naam = 'KlTypeHoogtebegrenzer'
    label = 'type hoogtebegrenzer'
    objectUri = 'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#KlTypeHoogtebegrenzer'
    definition = 'De mogelijke types van een hoogtebegrenzer.'
    status = 'ingebruik'
    codelist = 'https://wegenenverkeer.data.vlaanderen.be/id/conceptscheme/KlTypeHoogtebegrenzer'
    options = {
    }

    @classmethod
    def create_dummy_data(cls):
        return cls.create_dummy_data_keuzelijst(cls.options)

