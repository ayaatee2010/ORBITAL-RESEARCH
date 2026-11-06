from dataclasses import dataclass


@dataclass(frozen=True)
class Experiment:
    experiment_id: str
    asteroid: str
    model: str
    duration_days: int
    description: str


EXPERIMENTS = {
    "EXP-001": Experiment(
        experiment_id="EXP-001",
        asteroid="433 Eros",
        model="Sun-only",
        duration_days=7,
        description="Baseline prediction using solar gravity only.",
    ),

    "EXP-002": Experiment(
        experiment_id="EXP-002",
        asteroid="433 Eros",
        model="Sun-Earth-Jupiter",
        duration_days=7,
        description="Prediction including Earth and Jupiter perturbations.",
    ),

    "EXP-003": Experiment(
        experiment_id="EXP-003",
        asteroid="433 Eros",
        model="Solar-System",
        duration_days=30,
        description="Prediction including the eight major planets.",
    ),

    "EXP-004": Experiment(
        experiment_id="EXP-004",
        asteroid="433 Eros",
        model="Solar-System",
        duration_days=90,
        description="Longer-term prediction and error growth analysis.",
    ),
}


def get_experiment(experiment_id):
    try:
        return EXPERIMENTS[experiment_id]
    except KeyError:
        raise ValueError(
            f"Unknown experiment: {experiment_id}"
        )


def list_experiments():
    return list(EXPERIMENTS.values())
