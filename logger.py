from datetime import datetime


class Logger(object):
    """ Utility class responsible for logging all interactions during the simulation. """
    def __init__(self, file_name, pop_size):
        self.total_dead = 0
        self.total_vaccinated = 0
        self.pop_size = pop_size
        self.file = open(file_name, 'w')

    def write_metadata(self, simulation_string, virus_string):
        """ Log Simulation Inputs to text file. """
        self.file.write(f'Running Simulation: {datetime.now()} \n')
        self.file.write(simulation_string)
        self.file.write(virus_string)

    def log_step(self, step, interactions, new_infections, total_death, vaccinations):
        """ Log Every Step """
        self.file.write(f'\nstep: {step}\n\t')
        self.file.write(f'Interactions: {interactions} | New Infections: {new_infections} | deaths: {total_death} | '
                        f'vaccinations: {vaccinations}')

    def log_results(self, reason, num_of_dead, num_vaccinated):
        self.file.write(f'\n\nPopulation count: {self.pop_size} | Dead: {num_of_dead} | Vaccinated: {num_vaccinated}')
        self.file.write(f'\n\nSimulation Ended: {reason}\n')
