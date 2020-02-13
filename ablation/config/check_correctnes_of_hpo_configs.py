# -*- coding: utf-8 -*-

"""Validates the HPO configs."""

import os
from typing import Iterable

HERE = os.path.abspath(os.path.dirname(__file__))

MODEL_DIRECTORIES = [
    'complex',
    'conve',
    'convkb',
    'distmult',
    'ermlp',
    'hole',
    'kg2e',
    'ntn',
    'proje',
    'rescal',
    'rgcn',
    'rotate',
    'simple',
    'structuredembedding',
    'transd',
    'transe',
    'transh',
    'transr',
    'tucker',
    'um',
]

DATASET_NAMES = ['fb15k237', 'kinships', 'wn18rr', 'yago310', 'examples']

NUM_LCWA_CONFIGS = 1
NUM_OWA_CONFIGS = 4


def iterate_config_paths(root_directory: str) -> Iterable[str]:
    """Iterate over all configuration paths."""
    root_directory = os.path.join(HERE, root_directory)
    for model in os.listdir(root_directory):
        # Check, whether model is valid
        if model.startswith('.'):
            break

        assert model in MODEL_DIRECTORIES, f'Model {model} is unknown'
        model_directory = os.path.join(root_directory, model)

        # Check, whether required datasets are defined
        datasets = os.listdir(model_directory)

        assert len(datasets) == len(DATASET_NAMES) and [dataset in datasets for dataset in DATASET_NAMES], \
            f'It is excepted that configurations for \'examples\', \'fb15k237\', \'kinships\', \'wn18rr\' and' \
                f' \'yago310\' are prvovided, but got' \
                f' {datasets[0]}, {datasets[1]}, {datasets[2]}, {datasets[3]} and {datasets[4]}.'

        for dataset in datasets:
            if dataset not in DATASET_NAMES and dataset != 'examples':
                raise Exception(f"Dataset {dataset} is unknown.")

            if dataset == 'examples':
                continue

            # Check, whether correct HPO approach is defined
            hpo_approach_directory = os.path.join(root_directory, model_directory, dataset)
            hpo_approach = os.listdir(hpo_approach_directory)

            assert len(
                hpo_approach) == 1 and hpo_approach[0] == 'random', \
                "Currently, only random search is allowed as HPO approach."

            # Check, whether correct training assumptions are defined
            training_assumption_directory = os.path.join(
                root_directory,
                model_directory,
                dataset,
                hpo_approach[0],
            )
            training_assumptions = os.listdir(training_assumption_directory)
            assert len(training_assumptions) == 2 and 'lcwa' in training_assumptions and 'owa' in training_assumptions, \
                f'It is expected that only configurations for LCWA and OWA are provided, but got ' \
                    f'{training_assumptions[0]} and {training_assumptions[1]}'

            for training_assumption in training_assumptions:
                configs_directory = os.path.join(
                    root_directory,
                    model_directory,
                    dataset,
                    hpo_approach[0],
                    training_assumption,
                )
                configs = os.listdir(configs_directory)

                # Check, whether correct number of configurations are defined
                if training_assumption == 'lcwa':
                    assert len(configs) == NUM_LCWA_CONFIGS, "More than one LCWA config provided."
                else:
                    assert training_assumption == 'owa' and len(
                        configs) == NUM_OWA_CONFIGS, f'For owa exactly {NUM_OWA_CONFIGS} configurations' \
                        f' are required, but {len(configs)} were provided'

                for config in configs:
                    yield model, dataset, hpo_approach, training_assumption, config


if __name__ == '__main__':
    iterator = iterate_config_paths(root_directory='reduced_search_space')

    for model, dataset, hpo_approach, training_assumption, config in iterator:
        pass
