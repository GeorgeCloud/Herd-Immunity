import datetime

class Logger(object):
    """ Utility class responsible for logging all interactions during the simulation. """

    def __init__(self, file_name):
        self.file = None
        self.file_name = file_name

    def write_metadata(self, simulation_obj, virus_obj):
        """ Log Simulation Inputs to text file. """
        with open(self.file_name, 'w') as file:
            file.write(simulation_obj.__str__())
            file.write(virus_obj.__str__() + "\n")
            file.write(f'Running Simulation: {datetime.datime.now()} \n')
            self.file = file

    def log_interaction(self, step, interactions, new_infections, total_death, vaccinations):
        """ Log Every Step """
        self.file.write('step:', step)
        self.file.write(f'Interactions: {interactions} | New Infections: {new_infections} | deaths: {total_death} |'
                        f'vaccinations: {vaccinations}')

    def log_simulation_results(self, population_size, total_death, total_vaccinated):
        self.file.write(f'Total Population: {population_count}')