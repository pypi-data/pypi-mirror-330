"""
This module tests the unilateral exclusion semantics, providing a means by which
to evaluate the logical relationships in a language with an exclusion operator
and comparing the result to the bilateral semantics.

Module Structure:
----------------
1. Imports:
   - Local semantic and operator definitions
   - Core model checker primitives
   - System utilities

2. Semantic Theories: include semantics, proposition theory, operators, and translation dictionary. 
   - exclusion_theory: Implements exclusion logic with unilateral operators
   - default_theory: Classical logic implementation for comparison
   - default_dictionary: Translates from unilateral to bilateral sentences

3. Example Types:
   - Countermodels (EX_CM_*): Examples demonstrating invalid inferences
   - Logical Consequences (EX_TH_*): Examples of valid logical relationships

4. Settings Configuration:
   - general_settings: Global settings for output and computation
   - example_settings: Default parameters for individual examples
   - Each example can override these with custom settings

Configuration:
-------------
- semantic_theories: Dictionary of semantic theories to test with
- example_range: Dictionary of example cases to evaluate

Example Format:
--------------
Each example is structured as a list: [premises, conclusions, settings]
- premises: List of formulas that serve as assumptions
- conclusions: List of formulas to be tested
- settings: Dictionary of specific settings for this example

Settings Options:
----------------
- N: Number of atomic propositions (default: 3)
- contingent: Whether to use contingent valuations
- disjoint: Whether to enforce disjoint valuations
- non_empty: Whether to enforce non-empty valuations
- non_null: Whether to enforce non-null valuations
- max_time: Maximum computation time in seconds

Development:
------
- From the 'model_checker/Code/' directory, run:
    python3 -m src.model_checker.cli path/to/theory_lib/exclusion/examples.py

Usage:
------
1. From project directory, run the following in the terminal:
    model-checker examples.py

2. To modify which examples run:
   - Edit the example_range dictionary
   - Comment/uncomment specific examples
   - Modify semantic_theories to change which theories to compare

3. To add new examples:
   - Follow the naming convention (CF_CM_*, CF_TH_*, CL_CM_*, CL_TH_*)
   - Define premises, conclusions, and settings
   - Add to example_range dictionary

Notes:
------
- At least one semantic theory must be included in semantic_theories
- At least one example must be included in example_range
- Some examples may require adjusting the settings to produce good models

Help:
-----
More information can be found in the README.md for the exclusion theory.
"""

##########################
### DEFINE THE IMPORTS ###
##########################

import os
import sys
# Add the current directory to sys.path
sys.path.append(os.path.dirname(__file__))

# Exclusion
from semantic import (
    ExclusionSemantics,
    UnilateralProposition,
    ExclusionStructure,
)
from operators import exclusion_operators

# Default + Utils
try: # Try local imports first (for development)
    from src.model_checker.theory_lib.default import (
        Semantics,
        Proposition,
        ModelStructure,
        default_operators,
    )
except ImportError:
    # Fall back to installed package imports
    from model_checker.theory_lib.default import (
        Semantics,
        Proposition,
        ModelStructure,
        default_operators,
    )

__all__ = [
    'general_settings',
    'example_settings',
    'exclusion_theory',
    'semantic_theories',
    'example_range',
]

####################################
### DEFINE THE SEMANTIC THEORIES ###
####################################

exclusion_theory = {
    "semantics": ExclusionSemantics,
    "proposition": UnilateralProposition,
    "model": ExclusionStructure,
    "operators": exclusion_operators,
    # base theory does not require a translation dictionary for comparison
    # since the examples are stated in the language of the default theory
}

default_dictionary = {
    "\\exclude" : "\\neg",
    "\\uniwedge" : "\\wedge",
    "\\univee" : "\\vee",
    "\\uniequiv" : "\\equiv",
}

default_theory = {
    "semantics": Semantics,
    "proposition": Proposition,
    "model": ModelStructure,
    "operators": default_operators,
    "dictionary": default_dictionary,
}

#######################
### DEFINE SETTINGS ###
#######################

general_settings = {
    "print_constraints": False,
    "print_impossible": False,
    "print_z3": False,
    "save_output": False,
    "maximize": False,
}

example_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'disjoint' : False,
    'non_empty' : False,
    'non_null' : False,
    'fusion_closure' : False,
    'max_time' : 1,
    'expectation' : True,
}

# premises = ['\\exclude (A \\univee B)']
# conclusions = ['(\\exclude A \\uniwedge \\exclude B)']

# premises = ['\\exclude (A \\uniwedge B)']
# conclusions = ['(\\exclude A \\univee \\exclude B)']

# premises = ['(A \\uniequiv B)']

# premises = []
# conclusions = ["(\\exclude (A \\uniwedge B) \\uniequiv (\\exclude A \\univee \\exclude B))"]
# settings['N'] = 4

# premises = []
# conclusions = ["(\\exclude (A \\univee B) \\uniequiv (\\exclude A \\uniwedge \\exclude B))"]

# premises = []
# conclusions = ["((A \\univee (B \\uniwedge C)) \\uniequiv ((A \\univee B) \\uniwedge (A \\univee C)))"]
# settings['N'] = 4

# premises = []
# conclusions = ["((A \\uniwedge (B \\univee C)) \\uniequiv ((A \\uniwedge B) \\univee (A \\uniwedge C)))"]

# premises = ['(A \\uniwedge (B \\univee C))']
# conclusions = ['((A \\univee B) \\uniwedge (A \\univee C))']

# premises = ['\\exclude (A \\uniwedge B)']
# conclusions = ['(\\exclude A \\univee \\exclude B)']




#####################
### COUNTERMODELS ###
#####################

# DOUBLE NEGATION ELIMINATION IDENTITY
EX_CM_1_premises = []
EX_CM_1_conclusions = ['(A \\uniequiv \\exclude \\exclude A)']
EX_CM_1_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
    'expectation' : True,
}
EX_CM_1_example = [
    EX_CM_1_premises,
    EX_CM_1_conclusions,
    EX_CM_1_settings,
]

# REVERSE DISTRIBUTION: DISJUNCTION OVER CONJUNCTION
EX_CM_9_premises = []
EX_CM_9_conclusions = ['(A \\uniwedge (B \\univee C)) \\uniequiv ((A \\univee B) \\uniwedge (A \\univee C))']
EX_CM_9_settings = { # agree
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
    'expectation' : True,
}
EX_CM_9_example = [
    EX_CM_9_premises,
    EX_CM_9_conclusions,
    EX_CM_9_settings,
]

# REVERSE DISTRIBUTION: DISJUNCTION OVER CONJUNCTION
EX_CM_8_premises = ['(A \\uniwedge (B \\univee C))']
EX_CM_8_conclusions = ['((A \\univee B) \\uniwedge (A \\univee C))']
EX_CM_8_settings = { # agree
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
    'expectation' : True,
}
EX_CM_8_example = [
    EX_CM_8_premises,
    EX_CM_8_conclusions,
    EX_CM_8_settings,
]

# REVERSE DISTRIBUTION: DISJUNCTION OVER CONJUNCTION
EX_CM_2_premises = ['((A \\univee B) \\uniwedge (A \\univee C))']
EX_CM_2_conclusions = ['(A \\uniwedge (B \\univee C))']
EX_CM_2_settings = { # agree
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
    'expectation' : True,
}
EX_CM_2_example = [
    EX_CM_2_premises,
    EX_CM_2_conclusions,
    EX_CM_2_settings,
]

# DOUBLE NEGATION ELIMINATION
EX_CM_3_premises = ['\\exclude \\exclude A']
EX_CM_3_conclusions = ['A']
EX_CM_3_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
    'expectation' : True,
}
EX_CM_3_example = [
    EX_CM_3_premises,
    EX_CM_3_conclusions,
    EX_CM_3_settings
]

# TRIPLE NEGATION ENTAILMENT
EX_CM_4_premises = ['\\exclude \\exclude \\exclude A']
EX_CM_4_conclusions = ['\\exclude A']
EX_CM_4_settings = { # TODO: print discrepancies
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
    'expectation' : True,
}
EX_CM_4_example = [
    EX_CM_4_premises,
    EX_CM_4_conclusions,
    EX_CM_4_settings
]

# TRIPLE NEGATION IDENTITY
EX_CM_5_premises = []
EX_CM_5_conclusions = ['(\\exclude A \\uniequiv \\exclude \\exclude \\exclude A)']
EX_CM_5_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : True,
    'non_null' : True,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
    'expectation' : True,
}
EX_CM_5_example = [
    EX_CM_5_premises,
    EX_CM_5_conclusions,
    EX_CM_5_settings, # these can be customized by example
]

# QUADRUPLE NEGATION
EX_CM_6_premises = ['\\exclude \\exclude \\exclude \\exclude A']
EX_CM_6_conclusions = ['\\exclude \\exclude A']
EX_CM_6_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
    'expectation' : True,
}
EX_CM_6_example = [
    EX_CM_6_premises,
    EX_CM_6_conclusions,
    EX_CM_6_settings
]

# # CONJUNCTION DEMORGANS
# EX_CM_7_settings = {
#     'N' : 3,
#     'possible' : False,
#     'contingent' : False,
#     'non_empty' : False,
#     'non_null' : False,
#     'disjoint' : False,
#     'fusion_closure' : False,
#     'max_time' : 1,
# }
# EX_CM_7_example = [ # TODO: fix example
#     ['\\exclude \\exclude \\exclude \\exclude A']
#     ['\\exclude \\exclude A']
#     EX_CM_7_settings
# ]



############################
### LOGICAL CONSEQUENCES ###
############################

# DISJUNCTIVE SYLLOGISM
EX_TH_1_premises = ['(A \\univee B)', '\\exclude B']
EX_TH_1_conclusions = ['A']
EX_TH_1_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
    'expectation' : False,
}
EX_TH_1_example = [
    EX_TH_1_premises,
    EX_TH_1_conclusions,
    EX_TH_1_settings
]

# CONJUNCTION DEMORGANS LR
EX_TH_2_premises = ['\\exclude (A \\uniwedge B)']
EX_TH_2_conclusions = ['(\\exclude A \\univee \\exclude B)']
EX_TH_2_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
    'expectation' : False,
}
EX_TH_2_example = [
    EX_TH_2_premises,
    EX_TH_2_conclusions,
    EX_TH_2_settings
]

# CONJUNCTION DEMORGANS RL
EX_TH_3_premises = ['(\\exclude A \\univee \\exclude B)']
EX_TH_3_conclusions = ['\\exclude (A \\uniwedge B)']
EX_TH_3_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
    'expectation' : False,
}
EX_TH_3_example = [
    EX_TH_3_premises,
    EX_TH_3_conclusions,
    EX_TH_3_settings
]

# DISJUNCTION DEMORGANS LR
EX_TH_3_premises = ['\\exclude (A \\univee B)']
EX_TH_3_conclusions = ['(\\exclude A \\uniwedge \\exclude B)']
EX_TH_3_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
    'expectation' : False,
}
EX_TH_3_example = [
    EX_TH_3_premises,
    EX_TH_3_conclusions,
    EX_TH_3_settings
]

# DISJUNCTION DEMORGANS RL
EX_TH_4_premises = ['(\\exclude A \\uniwedge \\exclude B)']
EX_TH_4_conclusions = ['\\exclude (A \\univee B)']
EX_TH_4_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
    'expectation' : False,
}
EX_TH_4_example = [
    EX_TH_4_premises,
    EX_TH_4_conclusions,
    EX_TH_4_settings
]

# DISJUNCTION DISTRIBUTION LR
EX_TH_5_premises = ['(A \\univee (B \\uniwedge C))']
EX_TH_5_conclusions = ['((A \\univee B) \\uniwedge (A \\univee C))']
EX_TH_5_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
    'expectation' : False,
}
EX_TH_5_example = [
    EX_TH_5_premises,
    EX_TH_5_conclusions,
    EX_TH_5_settings
]

# DISJUNCTION DISTRIBUTION RL
EX_TH_6_premises = ['((A \\univee B) \\uniwedge (A \\univee C))']
EX_TH_6_conclusions = ['(A \\univee (B \\uniwedge C))']
EX_TH_6_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
    'expectation' : False,
}
EX_TH_6_example = [
    EX_TH_6_premises,
    EX_TH_6_conclusions,
    EX_TH_6_settings
]

# CONJUNCTION DISTRIBUTION LR
EX_TH_7_premises = ['(A \\uniwedge (B \\univee C))']
EX_TH_7_conclusions = ['((A \\uniwedge B) \\univee (A \\uniwedge C))']
EX_TH_7_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
    'expectation' : False,
}
EX_TH_7_example = [
    EX_TH_7_premises,
    EX_TH_7_conclusions,
    EX_TH_7_settings
]

# CONJUNCTION DISTRIBUTION RL
EX_TH_8_premises = ['((A \\uniwedge B) \\univee (A \\uniwedge C))']
EX_TH_8_conclusions = ['(A \\uniwedge (B \\univee C))']
EX_TH_8_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
    'expectation' : False,
}
EX_TH_8_example = [
    EX_TH_8_premises,
    EX_TH_8_conclusions,
    EX_TH_8_settings
]

# CONJUNCTION ABSORPTION RL
EX_TH_9_premises = ['(A \\uniwedge (A \\univee B))']
EX_TH_9_conclusions = ['A']
EX_TH_9_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
    'expectation' : False,
}
EX_TH_9_example = [
    EX_TH_9_premises,
    EX_TH_9_conclusions,
    EX_TH_9_settings
]

# CONJUNCTION ABSORPTION LR
EX_TH_10_premises = ['A']
EX_TH_10_conclusions = ['(A \\uniwedge (A \\univee B))']
EX_TH_10_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
    'expectation' : False,
}
EX_TH_10_example = [
    EX_TH_10_premises,
    EX_TH_10_conclusions,
    EX_TH_10_settings
]

# DISJUNCTION ABSORPTION RL
EX_TH_11_premises = ['(A \\univee (A \\uniwedge B))']
EX_TH_11_conclusions = ['A']
EX_TH_11_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
    'expectation' : False,
}
EX_TH_11_example = [
    EX_TH_11_premises,
    EX_TH_11_conclusions,
    EX_TH_11_settings
]

# DISJUNCTION ABSORPTION LR
EX_TH_12_premises = ['A']
EX_TH_12_conclusions = ['(A \\univee (A \\uniwedge B))']
EX_TH_12_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
    'expectation' : False,
}
EX_TH_12_example = [
    EX_TH_12_premises,
    EX_TH_12_conclusions,
    EX_TH_12_settings
]

# CONJUNCTION ASSOCIATIVITY RL
EX_TH_13_premises = ['((A \\uniwedge B) \\uniwedge C)']
EX_TH_13_conclusions = ['(A \\uniwedge (B \\uniwedge C))']
EX_TH_13_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
    'expectation' : False,
}
EX_TH_13_example = [
    EX_TH_13_premises,
    EX_TH_13_conclusions,
    EX_TH_13_settings
]

# CONJUNCTION ASSOCIATIVITY LR
EX_TH_14_premises = ['(A \\uniwedge (B \\uniwedge C))']
EX_TH_14_conclusions = ['((A \\uniwedge B) \\uniwedge C)']
EX_TH_14_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
    'expectation' : False,
}
EX_TH_14_example = [
    EX_TH_14_premises,
    EX_TH_14_conclusions,
    EX_TH_14_settings
]

# DISJUNCTION ASSOCIATIVITY RL
EX_TH_15_premises = ['((A \\univee B) \\univee C)']
EX_TH_15_conclusions = ['(A \\univee (B \\univee C))']
EX_TH_15_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
    'expectation' : False,
}
EX_TH_15_example = [
    EX_TH_15_premises,
    EX_TH_15_conclusions,
    EX_TH_15_settings
]

# DISJUNCTION ASSOCIATIVITY LR
EX_TH_16_premises = ['(A \\univee (B \\univee C))']
EX_TH_16_conclusions = ['((A \\univee B) \\univee C)']
EX_TH_16_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
    'expectation' : False,
}
EX_TH_16_example = [
    EX_TH_16_premises,
    EX_TH_16_conclusions,
    EX_TH_16_settings
]

# UNIEQUIV DEMORGANS
uniequiv_demorgans_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : True,
    'non_null' : True,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
}
UNIEQUIV_PLAYGROUND = [
    # [], # premises
    # ["(\\exclude (A \\uniwedge B) \\uniequiv (\\exclude A \\univee \\exclude B))"], # conclusions
    # ["(A \\uniequiv (A \\uniwedge B))"],
    ["(A \\uniequiv \\exclude A)"],
    [],
    uniequiv_demorgans_settings
]



###############################################
### DEFINE EXAMPLES AND THEORIES TO COMPUTE ###
###############################################

# NOTE: at least one theory is required, multiple are permitted for comparison
semantic_theories = {
    "ChampollionBernard" : exclusion_theory,
    # "Brast-McKie" : default_theory,
}

# NOTE: at least one example is required, multiple are permitted for comparison
example_range = {
    # Countermodels
    "EX_CM_1" : EX_CM_1_example, # disagree
    "EX_CM_2" : EX_CM_2_example,
    "EX_CM_3" : EX_CM_3_example, # disagree
    "EX_CM_4" : EX_CM_4_example, # disagree
    "EX_CM_5" : EX_CM_5_example, # disagree
    "EX_CM_6" : EX_CM_6_example, # disagree
    # "EX_CM_7" : EX_CM_7_example, # disagree

    # Theorems
    "EX_TH_1" : EX_TH_1_example,
    "EX_TH_2" : EX_TH_2_example,
    "EX_TH_3" : EX_TH_3_example,
    "EX_TH_4" : EX_TH_4_example,
    "EX_TH_5" : EX_TH_5_example,
    "EX_TH_6" : EX_TH_6_example,
    "EX_TH_7" : EX_TH_7_example,
    "EX_TH_8" : EX_TH_8_example,
    "EX_TH_9" : EX_TH_9_example,
    "EX_TH_10" : EX_TH_10_example,
    "EX_TH_11" : EX_TH_11_example,
    "EX_TH_12" : EX_TH_12_example,
    "EX_TH_13" : EX_TH_13_example,
    "EX_TH_14" : EX_TH_14_example,
    "EX_TH_15" : EX_TH_15_example,
    "EX_TH_16" : EX_TH_16_example,

    # Testing
    # "UNIEQUIV PLAYGROUND" : UNIEQUIV_PLAYGROUND
}


