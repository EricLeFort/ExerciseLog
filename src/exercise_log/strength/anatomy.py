from exercise_log.utils import StrEnum


class MuscleGroup(StrEnum):
    # Major
    ABS = "Abs"
    BICEPS = "Biceps"
    CALVES = "Calves"
    DELTS = "Deltoids"
    FOREARMS = "Forearms"
    GLUTES = "Gluteus"
    HAMSTRINGS = "Hamstrings"
    LATS = "Latissimus Dorsi"
    PECS = "Pectorals"
    QUADS = "Quadriceps"
    TRAPS = "Trapezius"
    TRICEPS = "Triceps"

    # Minor
    HIP_ABDUCTORS = "Hip Abductors"
    HIP_ADDUCTORS = "Hip Adductors"
    HIP_FLEXORS = "Hip Flexors"
    NECK = "Neck"
    RHOMBOIDS = "Rhomboids"
    ROTATOR_CUFF = "Rotator Cuff"
    SERRATUS = "Serratus"
    SPINAL_ERECTORS = "Spinal Erectors"


class Muscle(StrEnum):
    # Abs
    OBLIQUES = "Obliques"  # Encompasses both the Internal and External muscles since they work in tandem
    PYRAMIDALIS = "Pyramidalis"  # Only present in 80% of people
    RECTUS_ABDOMINUS = "Rectus Abdominus"
    TRANSVERSE_ABDOMINUS = "Transverse Abdominus"

    # Biceps
    BICEPS_BRACHII_SHORT = "Short-Head Biceps Brachii"  # Both heads belong to the same muscle but can train separately
    BICEPS_BRACHII_LONG = "Long-Head Biceps Brachii"
    BRACHIALIS = "Brachialis"

    # Calves
    POPLITEUS = "Popliteus"
    TIBIALIS_ANTERIOR = "Tibialis Anterior"
    TIBIALIS_POSTERIOR = "Tibialis Posterior"
    GASTROCNEMIUS_LATERAL = "Gastrocnemius Lateral"  # Both heads belong to the same muscle but can train separately
    GASTROCNEMIUS_MEDIAL = "Gastrocnemius Medial"
    SOLEUS = "Soleus"
    FIBULARIS = "Fibularis"  # Encompasses both the Longus and Brevis muscles since they work in tandem
    FIBULARIS_TERTIUS = "Fibularis Tertius"  # Lot of overlap with the EDL below, might be redundant to include
    EXTENSOR_DIGITORUM_LONGUS = "Extensor Digitorum Longus"
    EXTENSOR_HALLUCIS_LONGUS = "Extensor Hallucis Longus"
    FLEXOR_DIGITORUM_LONGUS = "Flexor Digitorum Longus"
    FLEXOR_HALLUCIS_LONGUS = "Flexor Hallucis Longus"

    # Delts
    DELTOID_ANTERIOR = "Deltoid Anterior"
    DELTOID_MEDIAL = "Deltoid Medial"
    DELTOID_POSTERIOR = "Deltoid Posterior"

    # Forearms (Anterior)
    FLEXOR_CARPI_ULNARIS = "Flexor Carpi Ulnaris"
    FLEXOR_CARPI_RADIALIS = "Flexor Carpi Radialis"
    # Skipping Palmaris Longus since it's absent in at least one arm in ~30% of the population and not very relevant
    PRONATOR_TERES = "Pronator Teres"
    FLEXOR_DIGITORUM_SUPERFICIALIS = "Flexor Digitorum Superficialis"
    FLEXOR_POLLICIS_LONGUS = "Flexor Pollicis Longus"
    FLEXOR_DIGITORUM_PROFUNDUS = "Flexor Digitorum Profundus"
    PRONATOR_QUADRATUS = "Pronator Quadratus"  # Works in tandem with the Pronator Teres

    # Forearms (Posterior)
    # Omitting Anconeus since it's functionally similar to the triceps
    EXTENSOR_CARPI_RADIALIS_BREVIS = "Extensor Carpi Radialis Brevis"
    EXTENSOR_DIGITORUM = "Extensor Digitorum"  # AKA Extensor Digitorum Communis
    EXTENSOR_CARPI_ULNARIS = "Extensor Carpi Ulnaris"
    EXTENSOR_CARPI_MINIMI = "Extensor Carpi Minimi"
    EXTENSOR_CARPI_RADIALIS_LONGUS = "Extensor Carpi Radialis Longus"
    BRACHIORADIALIS= "Brachioradialis"
    SUPINATOR = "Supinator"
    ABDUCTOR_POLLICIS = "Abductor Pollicis"  # Encompasses both the Longus and Brevis muscles since they work in tandem
    EXTENSOR_POLLICIS_LONGUS = "Extensor Pollicis Longus"
    EXTENSOR_INDICIS = "Extensor Indicis"  # AKA Extensor Indicis Propius

    # Glutes
    GLUTEUS_MAXIMUS = "Gluteus Maximus"
    GLUTEUS_MEDIUS = "Gluteus Medius"
    GLUTEUS_MINIMUS = "Gluteus Minimus"  # Virtually identical function as medius

    # Hamstrings
    BICEP_FEMORIS_SHORT = "Bicep Femoris Short"
    BICEP_FEMORIS_LONG = "Bicep Femoris Long"
    SEMIMEMBRANOSUS = "Semimembranosus"
    SEMITENDINOSUS = "Semitendinosus"

    # Hip Abductors
    TENSOR_FASCIAE_LATAE = "Tensor Fasciae Latae"  # 
    PIRIFORMUS = "Piriformis"
    OBTURATOR = "Obturator" # Encompasses both the Internus and Externus muscles since they work in tandem
    GEMELLUS = "Gemellus"  # Encompasses Superior and Inferiror muscles since they work in tandem

    # Hip Adductors
    ADDUCTOR_LONGUS = "Adductor Longus"
    ADDUCTOR_BREVIS = "Adductor Brevis"
    ADDUCTOR_MAGNUS = "Adductor Magnus"
    GRACILLIS = "Gracillis"
    QUADRATUS_FEMORIS = "Quadratis Femoris"

    # Hip Flexors
    ILIACUS = "Iliacus"
    PSOAS = "Psoas"
    PECTINEUS = "Pectineus"
    SARTORIUS = "Sartorius"

    # Lats
    LATISSIMUS_DORSI = "Latissimus Dorsi"

    # Pecs
    PECTORALIS_MAJOR_CLAVICULAR = "Pectoralis Major Clavicular"
    PECTORALIS_MAJOR_STERNOCOSTAL = "Pectoralis Major Sternocostal"
    PECTORALIS_MINOR = "Pectoralis Minor"
    SUBCLAVIUS = "Subclavius"  # Adding for completion's sake, not the most relevant muscle

    # Quads
    RECTUS_FEMORIS = "Rectus Femoris"
    VASTUS_LATERALIS = "Vastus Lateralis"
    VASTUS_MEDIALIS = "Vastus Medialis"
    VASTUS_INTERMEDIUS = "Vastus Intermedius"

    # Traps
    TRAPEZIUS_UPPER = "Trapezius Upper"  # Technically all the same muscle but are worked separately
    TRAPEZIUS_MIDDLE = "Trapezius Middle"
    TRAPEZIUS_LOWER = "Trapezius Lower"

    # Triceps
    TRICEPS_BRACHII_LONG = "Triceps Brachii Long"
    TRICEPS_BRACHII_LATERAL = "Triceps Brachii Lateral"
    TRICEPS_BRACHII_MEDIAL = "Triceps Brachii Medial"  # Virtually identical function as Lateral, more type I fibers

    # Skipping Neck; too complicated, doesn't matter enough

    # Rhomboids
    RHOMBOID_MAJOR = "Rhomboid Major"
    RHOMBOID_MINOR = "Rhomboid Minor"

    # Rotator Cuff
    SUPRASPINOUS = "Supraspinous"
    INFRASPINOUS = "Infraspinous"
    TERES_MINOR = "Teres Minor"
    SUBSCAPULARIS = "Subscapularis"

    # Serratus
    SERRATUS_ANTERIOR = "Serratus Anterior"
    SERRATUS_POSTERIOR_SUPERIOR = "Serratus Posterior Superior"  # The Posteriors are (maybe?) just breathing related
    SERRATUS_POSTERIOR_INFERIOR = "Serratus Posterior Inferior"

    # Spinal Erectors
    ILIOCOSTALIS_CERVICIS = "Iliocostalis Cervicis"
    ILIOCOSTALIS_THORACIS = "Iliocostalis Thoracis"
    ILIOCOSTALIS_LUMBORUM = "Iliocostalis Lumborum"

    muscle_group_map = {
        Muscle.OBLIQUES: MuscleGroup.ABS,
        Muscle.PYRAMIDALIS: MuscleGroup.ABS,
        Muscle.RECTUS_ABDOMINUS: MuscleGroup.ABS,
        Muscle.TRANSVERSE_ABDOMINUS: MuscleGroup.ABS,
        Muscle.BICEPS_BRACHII_SHORT: MuscleGroup.BICEPS,
        Muscle.BICEPS_BRACHII_LONG: MuscleGroup.BICEPS,
        Muscle.BRACHIALIS: MuscleGroup.BICEPS,
        Muscle.POPLITEUS: MuscleGroup.CALVES,
        Muscle.TIBIALIS_ANTERIOR: MuscleGroup.CALVES,
        Muscle.TIBIALIS_POSTERIOR: MuscleGroup.CALVES,
        Muscle.GASTROCNEMIUS_LATERAL: MuscleGroup.CALVES,
        Muscle.GASTROCNEMIUS_MEDIAL: MuscleGroup.CALVES,
        Muscle.SOLEUS: MuscleGroup.CALVES,
        Muscle.FIBULARIS: MuscleGroup.CALVES,
        Muscle.FIBULARIS_TERTIUS: MuscleGroup.CALVES,
        Muscle.EXTENSOR_DIGITORUM_LONGUS: MuscleGroup.CALVES,
        Muscle.EXTENSOR_HALLUCIS_LONGUS: MuscleGroup.CALVES,
        Muscle.FLEXOR_DIGITORUM_LONGUS: MuscleGroup.CALVES,
        Muscle.FLEXOR_HALLUCIS_LONGUS: MuscleGroup.CALVES,
        Muscle.DELTOID_ANTERIOR: MuscleGroup.DELTS,
        Muscle.DELTOID_MEDIAL: MuscleGroup.DELTS,
        Muscle.DELTOID_POSTERIOR: MuscleGroup.DELTS,
        Muscle.FLEXOR_CARPI_ULNARIS: MuscleGroup.FOREARMS,
        Muscle.FLEXOR_CARPI_RADIALIS: MuscleGroup.FOREARMS,
        Muscle.PRONATOR_TERES: MuscleGroup.FOREARMS,
        Muscle.FLEXOR_DIGITORUM_SUPERFICIALIS: MuscleGroup.FOREARMS,
        Muscle.FLEXOR_POLLICIS_LONGUS: MuscleGroup.FOREARMS,
        Muscle.FLEXOR_DIGITORUM_PROFUNDUS: MuscleGroup.FOREARMS,
        Muscle.PRONATOR_QUADRATUS: MuscleGroup.FOREARMS,
        Muscle.EXTENSOR_CARPI_RADIALIS_BREVIS: MuscleGroup.FOREARMS,
        Muscle.EXTENSOR_DIGITORUM: MuscleGroup.FOREARMS,
        Muscle.EXTENSOR_CARPI_ULNARIS: MuscleGroup.FOREARMS,
        Muscle.EXTENSOR_CARPI_MINIMI: MuscleGroup.FOREARMS,
        Muscle.EXTENSOR_CARPI_RADIALIS_LONGUS: MuscleGroup.FOREARMS,
        Muscle.BRACHIORADIALIS: MuscleGroup.FOREARMS,
        Muscle.SUPINATOR: MuscleGroup.FOREARMS,
        Muscle.ABDUCTOR_POLLICIS 
        Muscle.EXTENSOR_POLLICIS_LONGUS: MuscleGroup.FOREARMS,
        Muscle.EXTENSOR_INDICIS: MuscleGroup.FOREARMS,
        Muscle.GLUTEUS_MAXIMUS: MuscleGroup.GLUTES,
        Muscle.GLUTEUS_MEDIUS: MuscleGroup.GLUTES,
        Muscle.GLUTEUS_MINIMUS: MuscleGroup.GLUTES,
        Muscle.BICEP_FEMORIS_SHORT: MuscleGroup.HAMSTRINGS,
        Muscle.BICEP_FEMORIS_LONG: MuscleGroup.HAMSTRINGS,
        Muscle.SEMIMEMBRANOSUS: MuscleGroup.HAMSTRINGS,
        Muscle.SEMITENDINOSUS: MuscleGroup.HAMSTRINGS,
        Muscle.TENSOR_FASCIAE_LATAE: MuscleGroup.HIP_ABDUCTORS,
        Muscle.PIRIFORMUS: MuscleGroup.HIP_ABDUCTORS,
        Muscle.OBTURATOR: MuscleGroup.HIP_ABDUCTORS,
        Muscle.GEMELLUS: MuscleGroup.HIP_ABDUCTORS,
        Muscle.ADDUCTOR_LONGUS: MuscleGroup.HIP_ADDUCTORS,
        Muscle.ADDUCTOR_BREVIS: MuscleGroup.HIP_ADDUCTORS,
        Muscle.ADDUCTOR_MAGNUS: MuscleGroup.HIP_ADDUCTORS,
        Muscle.GRACILLIS: MuscleGroup.HIP_ADDUCTORS,
        Muscle.QUADRATUS_FEMORIS: MuscleGroup.HIP_ADDUCTORS,
        Muscle.ILIACUS: MuscleGroup.HIP_FLEXORS,
        Muscle.PSOAS: MuscleGroup.HIP_FLEXORS,
        Muscle.PECTINEUS: MuscleGroup.HIP_FLEXORS,
        Muscle.SARTORIUS: MuscleGroup.HIP_FLEXORS,
        Muscle.LATISSIMUS_DORSI: MuscleGroup.LATS,
        Muscle.PECTORALIS_MAJOR_CLAVICULAR: MuscleGroup.PECS,
        Muscle.PECTORALIS_MAJOR_STERNOCOSTAL: MuscleGroup.PECS,
        Muscle.PECTORALIS_MINOR: MuscleGroup.PECS,
        Muscle.SUBCLAVIUS: MuscleGroup.PECS,
        Muscle.RECTUS_FEMORIS: MuscleGroup.QUADS,
        Muscle.VASTUS_LATERALIS: MuscleGroup.QUADS,
        Muscle.VASTUS_MEDIALIS: MuscleGroup.QUADS,
        Muscle.VASTUS_INTERMEDIUS: MuscleGroup.QUADS,
        Muscle.TRAPEZIUS_UPPER: MuscleGroup.TRAPS,
        Muscle.TRAPEZIUS_MIDDLE: MuscleGroup.TRAPS,
        Muscle.TRAPEZIUS_LOWER: MuscleGroup.TRAPS,
        Muscle.TRICEPS_BRACHII_LONG: MuscleGroup.TRICEPS,
        Muscle.TRICEPS_BRACHII_LATERAL: MuscleGroup.TRICEPS,
        Muscle.TRICEPS_BRACHII_MEDIAL: MuscleGroup.TRICEPS,
        Muscle.RHOMBOID_MAJOR: MuscleGroup.RHOMBOIDS,
        Muscle.RHOMBOID_MINOR: MuscleGroup.RHOMBOIDS,
        Muscle.SUPRASPINOUS: MuscleGroup.ROTATOR_CUFF,
        Muscle.INFRASPINOUS: MuscleGroup.ROTATOR_CUFF,
        Muscle.TERES_MINOR: MuscleGroup.ROTATOR_CUFF,
        Muscle.SUBSCAPULARIS: MuscleGroup.ROTATOR_CUFF,
        Muscle.SERRATUS_ANTERIOR: MuscleGroup.SERRATUS,
        Muscle.SERRATUS_POSTERIOR_SUPERIOR: MuscleGroup.SERRATUS,
        Muscle.SERRATUS_POSTERIOR_INFERIOR: MuscleGroup.SERRATUS,
        Muscle.ILIOCOSTALIS_CERVICIS: MuscleGroup.SPINAL_ERECTORS,
        Muscle.ILIOCOSTALIS_THORACIS: MuscleGroup.SPINAL_ERECTORS,
        Muscle.ILIOCOSTALIS_LUMBORUM: MuscleGroup.SPINAL_ERECTORS,
    }

    def get_muscle_group(self):
        return Muscle.muscle_group_map[self]
