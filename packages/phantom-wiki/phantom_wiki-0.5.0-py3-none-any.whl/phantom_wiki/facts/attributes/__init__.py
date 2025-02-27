# standard imports
import logging
import time
from argparse import ArgumentParser

# resource containing the attribute rules
from importlib.resources import files

# phantom wiki functionality
from ..database import Database
from .generate import generate_hobbies, generate_jobs

ATTRIBUTE_RULES_PATH = files("phantom_wiki").joinpath("facts/attributes/rules.pl")

# TODO: add functionality to pass in CLI arguments


#
# Functionality to generate attributes for everyone in the database.
#
def db_generate_attributes(db: Database, args: ArgumentParser):
    """
    Generate attributes for each person in the database.

    Args:
        db (Database): The database containing the facts.
        args (ArgumentParser): The command line arguments.
    """
    start_time = time.time()
    names = db.get_person_names()
    jobs = generate_jobs(names, args.seed)
    hobbies = generate_hobbies(names, args.seed)

    # add the facts to the database
    facts = []
    for name in names:
        # add jobs
        job = jobs[name]
        facts.append(f'job("{name}", "{job}")')
        facts.append(f'attribute("{job}")')

        # add hobbies
        hobby = hobbies[name]
        facts.append(f'hobby("{name}", "{hobby}")')
        facts.append(f'attribute("{hobby}")')

    logging.info(f"Generated attributes for {len(names)} individuals in {time.time()-start_time:.3f}s.")
    db.add(*facts)
