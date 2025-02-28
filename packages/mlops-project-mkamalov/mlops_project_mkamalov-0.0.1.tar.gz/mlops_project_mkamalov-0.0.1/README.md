# Technopark MLOps Project: Product URL Classifier

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

## Описание проекта
Данный проект представляет собой систему классификации товаров на основе их URL. Система получает на вход URL товара и относит его к одной из категорий, используя предопределенное дерево категорий.

## Дерево категорий
Категории задаются в формате JSON и выглядят следующим образом:
```json
{
  "Красота и уход": {
    "Уход за лицом": [],
    "Уход за волосами": [],
    "Средства по уходу за телом": [],
    "Личная гигиена": [],
    "Макияж": [],
    "Маникюр и педикюр": [],
    "Парфюмерия": [],
    "Подарочные наборы косметики и парфюмерии": [],
    "Косметические приборы": []
  },
  "Хобби и увлечения": {
    "Антиквариат и коллекционирование": [],
    "Моделизм": [],
    "Музыкальные инструменты": [],
    "Прикладное искусство": [],
    "Поделки и рукоделие": [],
    "Игры и головоломки": [],
    "Прочие хобби и увлечения": []
  }
}
```

## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         mlops_project_m.kamalov and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── mlops_project_m.kamalov   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes mlops_project_m.kamalov a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```

--------

### Создание и активация виртуального окружения (LINUX)
- python3.10 -m venv venv
- source ./venv/bin/activate 

### Создание и активация виртуального окружения (WINDOWS)
- py -3.10 -m venv venv 
- venv/Scripts/Activate.ps1 

