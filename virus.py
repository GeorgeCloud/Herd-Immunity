class Virus(object):
    def __init__(self, name, repro_rate, mortality_rate):
        self.name = str(name)
        self.repro_rate = float(repro_rate)
        self.mortality_rate = float(mortality_rate)

    def __str__(self):
        return f'''
    Virus Stats
        name: {str(self.name)}
        Repro Rate: {float(self.repro_rate)}
        Mortality Rate: {float(self.mortality_rate)}
        '''


def test_virus_instantiation():
    virus = Virus("HIV", 0.8, 0.3)
    assert virus.name == "HIV"
    assert virus.repro_rate == 0.8
    assert virus.mortality_rate == 0.3
