import re
from pathlib import Path
from typing import Dict, Set

from scheduling_environment.job import Job
from scheduling_environment.machine import Machine
from scheduling_environment.operation import Operation
import random


def parse_fjsp_conthereum(JobShop, instance, from_absolute_path=False):
    JobShop.set_instance_name(instance)

    if not from_absolute_path:
        base_path = Path(__file__).parent.parent.absolute()
        data_path = base_path.joinpath('data' + instance)
    else:
        data_path = instance

    with open(data_path, "r") as data:
        total_jobs, total_machines, max_operations, job_conflicting_percentage, random_seed = re.findall(
            '\S+', data.readline())
        number_total_jobs, number_total_machines, number_max_operations, number_job_conflicting_percentage, \
        number_random_seed = int(total_jobs), int(total_machines), int(float(max_operations)), \
                             int(job_conflicting_percentage), int(random_seed)

        JobShop.set_nr_of_jobs(number_total_jobs)
        JobShop.set_nr_of_machines(number_total_machines)

        precedence_relations = {}
        job_id = 0
        operation_id = 0

        for key, line in enumerate(data):
            if key >= number_total_jobs:
                break
            # Split data with multiple spaces as separator
            parsed_line = re.findall('\S+', line)

            # Current item of the parsed line
            i = 1
            job = Job(job_id)

            while i < len(parsed_line):
                # Total number of operation options for the operation
                operation_options = int(parsed_line[i])
                # Current activity
                operation = Operation(job, job_id, operation_id)

                for operation_options_id in range(operation_options):
                    machine_id = int(parsed_line[i + 1 + 2 *
                                                 operation_options_id]) - 1
                    duration = int(
                        parsed_line[i + 2 + 2 * operation_options_id])
                    operation.add_operation_option(machine_id, duration)
                job.add_operation(operation)
                JobShop.add_operation(operation)
                if i != 1:
                    precedence_relations[operation_id] = [
                        JobShop.get_operation(operation_id - 1)]

                i += 1 + 2 * operation_options
                operation_id += 1

            JobShop.add_job(job)
            job_id += 1

    # add also the operations without precedence operations to the precedence relations dictionary
    for operation in JobShop.operations:
        if operation.operation_id not in precedence_relations.keys():
            precedence_relations[operation.operation_id] = []
        operation.add_predecessors(
            precedence_relations[operation.operation_id])

    sequence_dependent_setup_times = [[[0 for r in range(len(JobShop.operations))] for t in range(len(JobShop.operations))] for
                                      m in range(number_total_machines)]

    # Precedence Relations & sequence dependent setup times
    JobShop.add_precedence_relations_operations(precedence_relations)
    JobShop.add_sequence_dependent_setup_times(sequence_dependent_setup_times)

    # Machines
    for id_machine in range(0, number_total_machines):
        JobShop.add_machine((Machine(id_machine)))

    # Conflicts
    conflicting_jobs: Dict[int, Set[int]] = {}
    generate_random_conflicts(conflicting_jobs, number_total_jobs, number_job_conflicting_percentage,
                              number_random_seed)
    JobShop.add_conflicting_jobs(conflicting_jobs)

    for job in JobShop.jobs:
        job.add_conflicting_jobs(conflicting_jobs.get(job.job_id))

    return JobShop


def add_conflict(conflicting_jobs: Dict[int, Set[int]] , id1: int, id2: int):
    conflicting_jobs.setdefault(id1, set()).add(id2)
    conflicting_jobs.setdefault(id2, set()).add(id1)


def generate_random_conflicts(conflicting_jobs, total_jobs: int, percentage: float, seed: int):
    random.seed(seed)
    num_conflicts = int((total_jobs * (total_jobs - 1) // 2) * (percentage / 100))
    pairs = random.sample([(i, j) for i in range(total_jobs) for j in range(i + 1, total_jobs)], num_conflicts)
    for id1, id2 in pairs:
        add_conflict(conflicting_jobs, id1, id2)


# if __name__ == "__main__":
#     from scheduling_environment.jobShop import JobShop
#     jobShopEnv = JobShop()
#     jobShopEnv = parse_fjsp(jobShopEnv, '/fjsp/1_brandimarte/Mk01.fjs')
#     jobShopEnv.update_operations_available_for_scheduling()
#     print(jobShopEnv.operations_available_for_scheduling)