from datetime import datetime

class Logger(object):
    """ Utility class responsible for logging all interactions during the simulation. """

    def __init__(self, file_name):
        self.file = None
        self.file_name = file_name

    def write_metadata(self, simulation_obj):
        """ Log Simulation Inputs to text file. """
        with open(self.file_name, 'w') as file:
            file.write(f'Running Simulation: {datetime.now()} \n')
            file.write(simulation_obj.__str__())
            file.write(simulation_obj.__str__() + "\n")
            self.file = file

    def log_every_step(self):
        """ Log Every Step """
        self.file.write('step:', step)
        self.file.write(f'Interactions: {interactions} | New Infections: {new_infections} | deaths: {total_death} |'
                        f'vaccinations: {vaccinations}')

    def log_simulation_results(self, population_size, total_death, total_vaccinated):
        self.file.write(f'Total Population: {population_count}')
