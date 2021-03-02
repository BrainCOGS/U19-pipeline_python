"""This module was auto-generated by datajoint from an existing schema"""


import datajoint as dj

schema = dj.schema('U19_subject')


vmod0 = dj.create_virtual_module('vmod0', 'U19_lab')


@schema
class Strain(dj.Lookup):
    definition = """
    strain_name          : varchar(32)                  # strain name
    ---
    strain_description="" : varchar(255)                 # description
    """


@schema
class Cage(dj.Lookup):
    definition = """
    cage                 : char(8)                      # name of a cage
    ---
    -> vmod0.User.proj(cage_owner="user_id")
    """


@schema
class SequenceType(dj.Lookup):
    definition = """
    sequence_type        : varchar(63)
    ---
    seq_type_description="" : varchar(255)
    """


@schema
class Sequence(dj.Lookup):
    definition = """
    sequence             : varchar(63)                  # informal name
    ---
    -> SequenceType
    base_pairs=""        : varchar(1023)                # base pairs
    sequence_description="" : varchar(255)
    """


@schema
class ActItem(dj.Lookup):
    definition = """
    act_item             : varchar(64)                  # possible act item
    """


@schema
class Species(dj.Lookup):
    definition = """
    binomial             : varchar(32)                  # binomial
    ---
    species_nickname     : varchar(32)                  # nickname
    """


@schema
class Line(dj.Lookup):
    definition = """
    line                 : varchar(128)                 # name
    ---
    -> Species
    -> Strain
    line_description=""  : varchar(2048)                # description
    target_phenotype=""  : varchar(255)                 # target phenotype
    is_active=1          : tinyint                      # is active
    """


@schema
class Subject(dj.Manual):
    definition = """
    -> vmod0.User
    subject_id           : char(8)                      # nickname
    ---
    genomics_id=null     : int                          # number from the facility
    sex="Unknown"        : enum('Male','Female','Unknown') # sex
    dob=null             : date                         # birth date
    head_plate_mark=null : blob                         # little drawing on the head plate for mouse identification
    -> vmod0.Location
    -> [nullable] vmod0.Protocol
    -> [nullable] Line
    subject_description="" : varchar(255)                 # description
    initial_weight=null  : float
    """


@schema
class Weaning(dj.Manual):
    definition = """
    -> Subject
    ---
    wean_date            : date
    """


@schema
class SubjectProject(dj.Manual):
    definition = """
    -> Subject
    -> vmod0.Project
    """


@schema
class SubjectActItem(dj.Manual):
    definition = """
    -> Subject
    -> ActItem
    """


@schema
class HealthStatus(dj.Manual):
    definition = """
    -> Subject
    status_date          : date
    ---
    normal_behavior=1    : tinyint
    bcs=-1               : tinyint                      # Body Condition Score, from 1 (emaciated i.e. very malnourished) to 5 (obese), 3 being normal
    activity=-1          : tinyint                      # score from 0 (moves normally) to 3 (does not move) -1 unknown
    posture_grooming=-1  : tinyint                      # score from 0 (normal posture + smooth fur) to 3 (hunched + scruffy) -1 unknown
    eat_drink=-1         : tinyint                      # score from 0 (normal amounts of feces and urine) to 3 (no evidence of feces or urine) -1 unknown
    turgor=-1            : tinyint                      # score from 0 (skin retracts within 0.5s) to 3 (skin retracts in more than 2 s) -1 unknown
    comments=null        : varchar(255)
    """


    class Action(dj.Part):
        definition = """
        -> HealthStatus
        action_id            : tinyint                      # id of the action
        ---
        action               : varchar(255)
        """


@schema
class GenotypeTest(dj.Manual):
    definition = """
    -> Subject
    -> Sequence
    genotype_test_id     : varchar(63)
    ---
    test_result          : enum('Present','Absent')
    """


@schema
class Death(dj.Manual):
    definition = """
    -> Subject
    ---
    death_date           : date
    """


@schema
class CagingStatus(dj.Manual):
    definition = """
    -> Subject
    ---
    -> Cage
    """


@schema
class BreedingPair(dj.Manual):
    definition = """
    breeding_pair        : varchar(63)                  # name
    ---
    -> Line
    -> Subject
    bp_description=""    : varchar(2047)                # description
    bp_start_date=null   : date                         # start date
    bp_end_date=null     : date
    """


@schema
class Litter(dj.Manual):
    definition = """
    litter               : varchar(63)
    ---
    -> BreedingPair
    -> Line
    litter_descriptive_name="" : varchar(255)                 # descriptive name
    litter_description="" : varchar(255)                 # description
    litter_birth_date=null : date
    """


@schema
class LitterSubject(dj.Manual):
    definition = """
    -> Subject
    ---
    -> Litter
    """


@schema
class Source(dj.Lookup):
    definition = """
    source               : varchar(32)                  # name of source
    ---
    source_description="" : varchar(255)
    """


@schema
class Allele(dj.Lookup):
    definition = """
    allele               : varchar(63)                  # informal name
    ---
    standard_name=""     : varchar(255)                 # standard name
    -> Source
    original_allele_source : varchar(255)                 # original source of the allele
    allele_description="" : varchar(1023)
    """


@schema
class Zygosity(dj.Manual):
    definition = """
    -> Subject
    -> Allele
    ---
    zygosity             : enum('Present','Absent','Homozygous','Heterozygous')
    """


@schema
class LineAllele(dj.Lookup):
    definition = """
    -> Line
    -> Allele
    """


@schema
class AlleleSequence(dj.Lookup):
    definition = """
    -> Allele
    -> Sequence
    """
