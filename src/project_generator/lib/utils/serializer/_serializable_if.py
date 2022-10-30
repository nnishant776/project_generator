'''
Serialization interface to be implemented by inheriting class
'''

from dataclasses import dataclass

from typing_extensions import Self

from ._serializer import Serializer


@dataclass(slots=True)
class Serializable:
    '''
    Serialization interface
    '''

    def serialize(self):
        '''
        Return a serialized representation of the object
        '''
        return Serializer().default(self, bypass=True)

    @classmethod
    def deserialize(cls, obj) -> Self:
        '''
        Construct the object with serialized values in `obj`
        '''


@dataclass(slots=True)
class DictSerializable(Serializable):
    '''
    Serialization interface which serializes objects into dicts
    '''

    def to_dict(self) -> dict:
        '''
        Return a `dict` representation of the class object
        '''
        return self.serialize()

    @classmethod
    def deserialize(cls, obj) -> Self:
        return cls.from_dict(obj)

    @classmethod
    def from_dict(cls, obj) -> Self:
        '''
        Construct the object from the dict values in `obj`
        '''
