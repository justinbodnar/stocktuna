# QUICK START

git clone https://github.com/justinbodnar/stock-tuna.git

cd stock-tuna

pip3 install -r requirements.txt

wget https://stocktuna.com/datasets/kaggle-stock-etf-dataset.zip

unzip kaggle-stock-etf-dataset.zip

rm kaggle-stock-etf-dataset.zip

mkdir models

mkdir datasets

python3 cli-menu.py

OR

pydocs3 stocktuna

# MENU OPTIONS

1. Create new data sets
2. Extend data set
3. List and analyze available data sets
4. Train a model on a data set
5. View a random data point and tag
6. Graph a random data point and tag (uses MatPlotLib)
6. Watch model make 10,000 predictions

# MORE INFORMATION

Read ABOUT.md for more information about the code

Read DATA.md for information about how the data is structured
