
from classify import classify, classifier
from pytest import raises
from uuid import UUID, uuid4

def test_using_non_default_type_without_extending():
    class A:
        id = UUID

    with raises(TypeError):
        classify(A, {
            'id': '70d074b4-416a-4563-8236-842ceb497584'
        })


def test_using_non_default_type_with_extending():

    @classifier(UUID)
    def uuid_classifier(data, model):
        try:
            return UUID(data)
        except TypeError:
            raise TypeError('{} does not match Type {}'.format(
                data,
                model.__name__
            ))

    class A:
        id = UUID

    a = classify(A, {
        'id': '70d074b4-416a-4563-8236-842ceb497584'
    })
    assert isinstance(a.id, UUID)
    assert a.id == UUID('70d074b4-416a-4563-8236-842ceb497584')
