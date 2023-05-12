# Anki Clone

Anki Clone is a simple flashcard application, currently a work in progress. It is being developed as part of a job interview process. The primary purpose of this application is to help users learn and review new words and their definitions effectively using spaced repetition.

## Technologies

![Django](https://img.shields.io/badge/Django-4.2.1-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11.3-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15.2-blue)

## Features

* **Admin Interface**: Allows administrators to manage flashcards. They can create, view, update, and delete words and
  definitions. It also provides a validation to warn against the creation of duplicate words (but still allows it).
* **View Cards Tool**: Displays all flashcards and their current status (bin, time to next appearance, number of times
  answered incorrectly). Cards are sorted by their ID for easy navigation.
* **Flashcard Logic**: Moves cards between bins based on the user's responses and manages review sessions.
* **Reviewing Words**: Words can be reviewed based on time and priority, with a focus on words that are due for review
  or have been answered incorrectly.
* **Forgetting Words Feature**: Moves words that have been answered incorrectly 10 times to a "hard to remember" bin.
* **ID Display for Duplicate Words**: In the case of duplicate words, their IDs are displayed next to them for
  differentiation.

## Getting Started

Please note that this project is still under development and may not be ready for production use. Instructions for
setting up the development environment will be provided once the project reaches a more stable state.

## Acknowledgments

This project was created with the guidance of ChatGPT, model GPT-4.