# QUICK START

git clone https://github.com/justinbodnar/stocktuna.git

cd stocktuna

pip3 install -r requirements.txt

wget https://stocktuna.com/datasets/kaggle-stock-etf-dataset.zip

unzip kaggle-stock-etf-dataset.zip

rm kaggle-stock-etf-dataset.zip

mkdir models

mkdir datasets

python3 cli-menu.py

OR

pydoc3 stocktuna

# CLI MENU OPTIONS

1. Create new data sets
2. Extend data set
3. List and analyze available data sets
4. Train a model on a data set
5. View a random data point and tag
6. Graph a random data point and tag (uses MatPlotLib)
6. Watch model make 10,000 predictions

# MORE INFORMATION

Read DATA.md for information about how the data is structured
