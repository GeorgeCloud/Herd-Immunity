import random
import sys
from person import Person
from logger import Logger
from virus import Virus

random.seed(42)

def random_number(start, end):
    return random.randrange(start, end)

class Simulation(object):
    def __init__(self, virus, pop_size, vacc_percentage, initial_infected=1):
        """ Logger object logger records all events during the simulation. """
        self.pop_size = int(pop_size)
        self.next_person_id = 0
        self.virus = virus  # <virus_obj>
        self.initial_infected = int(initial_infected)
        self.encounters = 0
        self.total_infected = int(initial_infected)  # Int
        self.current_infected = 0  # Int
        self.vacc_percentage = float(vacc_percentage)
        self.file_name = f"{virus.name}_simulation_pop_{pop_size}_vp_{vacc_percentage}_infected_{initial_infected}.txt"
        self.logger = Logger(self.file_name)
        self.population = []
        self._create_population()
        self.dead_population = []
        self.newly_infected = []
        self.infected = []

    def __str__(self):
        return f'''
    Simulation Stats
        Population Size: {str(self.pop_size)}
        Initial Infected: {float(self.initial_infected)}
        Vaccinated % = {float(self.vacc_percentage)}
        '''

    def _create_population(self):
        num_of_infected = self.initial_infected
        num_people_vax = round(self.vacc_percentage * (self.pop_size - num_of_infected)) # Don't count infected as part of pop. Doesn't make sense what if everyone is vacinated and 1 person is intially infected?

        for idx in range(self.pop_size):
            if num_of_infected > 0:
                person = Person(idx, False, self.virus)  # People infected from start
                num_of_infected -= 1

            elif num_people_vax > 0:
                person = Person(idx, True)  # People vaccinated
                num_people_vax -= 1

            else:
                person = Person(idx, False)  # People vaccinated

            self.population.append(person)

    def _simulation_should_continue(self):
        if self.pop_size == 0:
            return False

        for person in self.population:
            if person.infection:
                return True

        print('infection dies')
        return False  # Infection is dead

    def run(self):
        """ Run the simulation until all requirements for ending the simulation are met. """
        self.logger.write_metadata(self)

        time_step_counter = 0
        should_continue = True
        self.infected = [i for i in self.population[:self.initial_infected]]

        while should_continue:
            time_step_counter += 1
            print(f'The simulation turns {time_step_counter}.')
            self.time_step()
            should_continue = self._simulation_should_continue()

    def time_step(self):
        interactions = 0
        for infected_person in self.infected:
            self.population.remove(infected_person)
            for _ in range(100):
                random_person = self.population[random_number(0, self.pop_size-1)]
                self.interaction(infected_person, random_person)
                interactions += 1
            self.population.append(infected_person)

        self.population_health_check()
        self.infected = self.newly_infected
        self.newly_infected = []

    def interaction(self, person, random_person):
        """ Only pass infection to healthy person who is unvaccinated. """
        assert person.is_alive is True
        assert random_person.is_alive is True

        chance_of_survival = random.uniform(0, 1)
        if not random_person.is_vaccinated and random_person.infection is None:
            if chance_of_survival < person.infection.repro_rate:
                random_person.infection = person.infection
                self.newly_infected.append(random_person)
                self.current_infected += 1

        self.encounters += 1

    def population_health_check(self):
        for person in self.infected:
            if not person.did_survive_infection():
                self.population.remove(person)
                self.pop_size -= 1
                self.dead_population.append(person)

if __name__ == "__main__":
    params = sys.argv[1:]
    virus_name, repro_num, mortality_rate = params[0], params[1], params[2]

    pop_size, vacc_percentage, initial_infected = params[3], params[4], params[5]

    virus = Virus(virus_name, repro_num, mortality_rate)

    sim = Simulation(virus, pop_size, vacc_percentage, initial_infected)

    sim.run()

    # "Ebola" 0.50 0.50 10 0.50 1