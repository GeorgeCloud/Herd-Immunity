from person import Person
from logger import Logger
from virus import Virus
import random, sys

random.seed(42)


class Simulation(object):
    def __init__(self, virus, pop_size, vacc_percentage, initial_infected=1):
        self.pop_size = int(pop_size)
        self.virus = virus
        self.step_counter = 0
        self.current_infected = 0
        self.initial_infected = int(initial_infected)
        self.vacc_percentage = float(vacc_percentage)
        self.total_infected = 0
        self.current_vacc = 0
        self.population = []
        self.newly_infected = []
        self.infected = []
        self._create_population()
        self.file_name = f"{virus.name}_simulation_pop_{pop_size}_vp_{vacc_percentage}_infected_{initial_infected}.txt"
        self.logger = Logger(self.file_name, pop_size)
        self.total_vacc = 0
        self.current_dead = 0
        self.total_dead = 0
        self.current_encounters = 0

    def __str__(self):
        return f'''
    Simulation Stats
        Population Size: {str(self.pop_size)}
        Initial Infected: {float(self.initial_infected)}
        Vaccinated % = {float(self.vacc_percentage)}
        '''

    def _create_population(self):
        num_of_infected = self.initial_infected
        num_people_vax = round(self.vacc_percentage * (self.pop_size - num_of_infected))

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
            self.logger.log_results('Population Died', self.total_dead, self.total_vacc)
            return False

        for person in self.population:
            if person.infection:
                return True

        self.logger.log_results('Infection Died', self.total_dead, self.total_vacc)
        return False

    def run(self):
        self.logger.write_metadata(self.__str__(), virus.__str__())
        should_continue = True

        self.infected = [i for i in self.population if i.infection]

        while should_continue:
            self.step_counter += 1
            print(f'\n- The simulation turns {self.step_counter}')
            self.time_step()
            self.total_dead += self.current_dead
            self.logger.log_step(self.step_counter, self.current_encounters, self.current_infected, self.current_dead,
                                 self.current_vacc)

            self.current_encounters = 0
            self.current_dead = 0
            self.total_vacc += self.current_vacc
            self.current_vacc = 0
            self.total_infected += self.current_infected
            self.current_infected = 0

            should_continue = self._simulation_should_continue()

    def time_step(self):
        for person in self.infected:
            for _ in range(100):
                random_person = self.population[
                    random.randrange(0, self.pop_size - 1)]
                self.interaction(person, random_person)
                self.current_encounters += 1
        self._infect_newly_infected()
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

    def _infect_newly_infected(self):
        for person in self.infected:
            self.current_infected += 1
            if not person.did_survive_infection():
                self.current_dead += 1
                self.population.remove(person)
                self.pop_size -= 1
            else:
                self.current_vacc += 1


if __name__ == "__main__":
    params = sys.argv[1:]
    virus_name, repro_num, mortality_rate = str(params[0]), float(params[1]), float(params[2])
    pop_size, vacc_percentage, initial_infected = int(params[3]), float(params[4]), float(params[5])

    virus = Virus(virus_name, repro_num, mortality_rate)
    sim = Simulation(virus, pop_size, vacc_percentage, initial_infected)

    sim.run()
