# StockTuna Documentation

#### Sections

- [~Overview](README.md)
- [\_\_init\_\_( )](./__init__.md)
- [sma( bars, period )](./sma.md)
- [sma_graph( bars, periods, symbol)](sma_graph.md)
- [ema( bars, period )](ema.md)
- [ema_graph( bars, periods, symbol)](ema_graph.md)
- [rsi( bars, period )](rsi.md)
- [rsi_graph( bars, period, symbol)](rsi_graph.md)
- 
Developed by Justin Bodnar  
Website: [justinbodnar.com](http://justinbodnar.com)  
Email: [contact@justinbodnar.com](mailto:contact@justinbodnar.com)

### StockTuna Superclass

- `StockTuna`- holds all methods and data definitions.

### StockTuna Subclasses

- `PaperTuna` - child class that uses the Alpaca paper trading API.
- `LiveTuna` - child class that uses the Alpaca live trading API.