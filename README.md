# Project Ephesus

Interpret textual data generated from medical vocal memos

In the Library of Celsus in Ephesus, built in the 2nd century, there are four statues depicting wisdom (Sophia), knowledge (Episteme), intelligence (Ennoia) and excellence (Arete). Our project is named after this city and the goddess Sophia.

# What it's all about

After visiting a patient nurses and doctors need to quickly and easily send information

So they record a vocal memo after each visit

Today these memos are read by humans and the infos are manually entered in the database

We want to ease their work by automatically extracting informations from the vocal memos and pre-filling the informations to be entered in the database

This repo is the front end demo website for the [Project Ephesus](https://github.com/GeoffroyGit/ephesus/)

# Demo

## Try it yourself

You can play around with our demo [here](https://ephesus-web.herokuapp.com/)

In this demo, we let you try your own sentences and see the results from our models

# Run our code yourself

## Install the Ephesus package

Clone the project:

```bash
git clone git@github.com:JulianBreaud/ephesusWeb.git
```

We recommend you to create a fresh virtual environment

Create a python3 virtualenv and activate it:

```bash
cd ephesusWeb
pyenv virtualenv ephesusWeb
pyenv local ephesusWeb
```

Upgrade pip if needed:

```bash
pip install --upgrade pip
```

Install the package:

```bash
pip install -r requirements.txt
pip install -e .
```

## Run the website locally

Run the website on your machine:

```bash
make streamlit
```

## Run the website on Heroku

Create the app on Heroku:

```bash
make heroku_create
```

Deploy and run the website:

```bash
make heroku_deploy
```

# You're done

Congratulations!
