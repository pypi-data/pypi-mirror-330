# imports for family relations and templates
from .constants import FAMILY_RELATION_DIFFICULTY

FAMILY_RELATION_EASY = [k for k, v in FAMILY_RELATION_DIFFICULTY.items() if v < 2]
FAMILY_RELATION_HARD = [k for k, v in FAMILY_RELATION_DIFFICULTY.items() if v >= 2]

from importlib.resources import files

FAMILY_RULES_BASE_PATH = files("phantom_wiki").joinpath("facts/family/rules_base.pl")
FAMILY_RULES_DERIVED_PATH = files("phantom_wiki").joinpath("facts/family/rules_derived.pl")

import logging

# imports for family generation
from argparse import ArgumentParser

# Create parser for family tree generation
fam_gen_parser = ArgumentParser(description="Family Generator", add_help=False)
fam_gen_parser.add_argument(
    "--max-branching-factor",
    type=int,
    default=5,
    help="The maximum number of children that any person in a family tree may have. (Default value: 5.)",
)
fam_gen_parser.add_argument(
    "--max-tree-depth",
    type=int,
    default=5,
    help="The maximum depth that a family tree may have. (Default value: 5.)",
)
fam_gen_parser.add_argument(
    "--max-tree-size",
    type=int,
    # default=26,
    default=25,
    help="The maximum number of people that may appear in a family tree. (Default value: 26.)",
)
fam_gen_parser.add_argument(
    "--num-samples", type=int, default=1, help="The size of the dataset to generate. (Default value: 1.)"
)
fam_gen_parser.add_argument(
    "--stop-prob",
    type=float,
    default=0.0,
    help="The probability of stopping to further extend a family tree after a person has been added. "
    "(Default value: 0.)",
)
fam_gen_parser.add_argument(
    "--duplicate-names",
    type=bool,
    default=False,
    help="Used to allow/prevent duplicate names in the generation. (Default value: False.)",
)

fam_gen_parser.add_argument(
    "--test",
    action="store_true",
    help="Whether or not in test-mode, if yes, can allow unhashed or uncommitted changes.",
)
# wrapper for family tree generation

import os
import random

from .generate import Generator, PersonFactory, create_dot_graph, family_tree_to_facts


def db_generate_family(db, args: ArgumentParser):
    """Generates family facts for a database.

    args:
        db: Database
        num_people: number of people to generate
        seed: random seed
    """
    # set the random seed
    random.seed(args.seed)
    # Get the prolog family tree
    pf = PersonFactory(args.duplicate_names)

    gen = Generator(pf)
    family_trees = gen.generate(args)

    for i, family_tree in enumerate(family_trees):
        logging.debug(f"Adding family tree {i+1} to the database.")

        # Obtain family tree facts
        facts = family_tree_to_facts(family_tree)
        db.add(*facts)

        #############
        # Debugging #
        #############
        if args.debug:
            # Create a unique filename for each tree
            output_file_path = os.path.join(args.output_dir, f"family_tree_{i+1}.pl")
            os.makedirs(args.output_dir, exist_ok=True)

            # Write the Prolog family tree to the file
            with open(output_file_path, "w") as f:
                f.write("\n".join(facts))

            # Generate family graph plot and save it
            family_graph = create_dot_graph(family_tree)
            output_graph_path = os.path.join(args.output_dir, f"family_tree_{i+1}.png")
            family_graph.write_png(output_graph_path)

    logging.debug(f"Saved family trees in {args.output_dir} as .png and .pl.")
