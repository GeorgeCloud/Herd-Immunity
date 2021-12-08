import random
from virus import Virus

# random.seed(42)


class Person(object):
    def __init__(self, _id, is_vaccinated, infection=None):
        self._id = _id
        self.is_alive = True
        self.is_vaccinated = is_vaccinated
        self.infection = infection

    def did_survive_infection(self, is_test=None):
        if self.infection:
            chance_of_survival = is_test or random.uniform(0, 1)
            if self.infection.mortality_rate > chance_of_survival:
                self.is_alive = False
            else:
                self.is_vaccinated = True
                self.infection = None

        return self.is_alive


def test_vacc_person_instantiation():
    person = Person(1, True)
    assert person._id == 1
    assert person.is_alive is True
    assert person.is_vaccinated is True
    assert person.infection is None


def test_not_vacc_person_instantiation():
    person = Person(2, False)
    assert person._id == 2
    assert person.is_alive is True
    assert person.infection is None

    for _ in range(10):
        assert person.did_survive_infection() is True


def test_sick_person_instantiation():
    virus = Virus("Dysentery", 0.7, 0.2)
    person = Person(3, False, virus)

    assert person._id == 3
    assert person.is_alive is True
    assert isinstance(person.infection, Virus)

    chance_of_survival = 0.000001
    for _ in range(10):
        assert person.did_survive_infection(chance_of_survival) is False


def test_did_survive_infection():
    virus = Virus("Dysentery", 0.7, 0.2)
    person = Person(4, False, virus)
    survived = person.did_survive_infection()
    if survived:
        assert person.is_alive is True
    else:
        assert person.is_alive is False


if __name__ == "__main__":
    test_vacc_person_instantiation()
    test_not_vacc_person_instantiation()
    test_sick_person_instantiation()
    test_did_survive_infection()
