# coding=utf-8
from otlmow_model.OtlmowModel.BaseClasses.KeuzelijstField import KeuzelijstField


# Generated with OTLEnumerationCreator. To modify: extend, do not edit
class KlOptischeWegdeksensorModelnaam(KeuzelijstField):
    """Optische wegdeksensor modelnamen."""
    naam = 'KlOptischeWegdeksensorModelnaam'
    label = 'Optische wegdeksensor modelnaam'
    objectUri = 'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#KlOptischeWegdeksensorModelnaam'
    definition = 'Optische wegdeksensor modelnamen.'
    status = 'ingebruik'
    codelist = 'https://wegenenverkeer.data.vlaanderen.be/id/conceptscheme/KlOptischeWegdeksensorModelnaam'
    options = {
    }

    @classmethod
    def create_dummy_data(cls):
        return cls.create_dummy_data_keuzelijst(cls.options)

