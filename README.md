# Flappy Bird AI with NEAT
This repository contains a Flappy Bird game simulation where the bird is controlled by neural networks evolved using the NEAT (NeuroEvolution of Augmenting Topologies) algorithm. The objective is to evolve AI agents to master the game and achieve high scores.

# Introduction
In this project, we use NEAT to train neural networks that play Flappy Bird. The neural networks are evolved over multiple generations to improve their performance in navigating through pipes.

# Features
1. Neural Network Training: Utilizes NEAT to evolve neural networks.
2. Flappy Bird Simulation: Classic Flappy Bird game implemented with Pygame.
3. Dynamic Difficulty: Increasing difficulty as the game progresses.
4. Interactive Visualization: Real-time display of neural network performance.

# Requirements
1. Python 3.x
2. Pygame
3. NEAT-Python

# Installation
1. Clone the Repository: git clone https://github.com/Hamadabcn/flappy-birdAI.git
2. cd flappy-birdAI
3. Install Dependencies: pip install pygame neat-python

# Configuration
The NEAT algorithm's behavior is controlled via the config.txt file. This file contains parameters that influence the training process, including fitness criteria, population size, and mutation rates.

# Configuration File Overview
# NEAT
1. fitness_criterion: Criterion for evaluating fitness (max).
2. fitness_threshold: Threshold for fitness to reach (100).
3. pop_size: Population size (15).
4. reset_on_extinction: Whether to reset on extinction (False).

# DefaultGenome
1. activation_default: Default activation function (tanh).
2. num_inputs: Number of input nodes (3).
3. num_outputs: Number of output nodes (1).

# DefaultSpeciesSet
1. compatibility_threshold: Threshold for species compatibility (3.0).

# DefaultStagnation
1. species_fitness_func: Fitness function for species (max).
2. max_stagnation: Maximum stagnation allowed (20).

# DefaultReproduction
1. elitism: Number of elite genomes to keep (2).
2. survival_threshold: Threshold for genome survival (0.2).

# Usage
To start the simulation and train the neural networks:

1. Ensure you are in the project directory.
2. Run the main script: python main.py
This will initialize the NEAT algorithm, start the Flappy Bird simulation, and evolve the neural networks over generations.

# License
This project is licensed under the MIT License. See the LICENSE file for details.

# Contributing
Contributions are welcome! Please submit a pull request or open an issue to suggest improvements.
