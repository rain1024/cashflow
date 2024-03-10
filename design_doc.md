# Class Diagram 

```
classDiagram
  class StockExchange{
    +get_stock_prices(self, ticker, start_year, end_year)
  }
  class Trader{
    +dca_investment(ticker, start_year=2010, end_year=2018, monthly_investment=20000000)
  }
```

# Database Diagrams

Table stock_prices {
  id INTEGER [pk]
  ticker TEXT [not null]
  price REAL [not null]
  date TIMESTAMP [not null]
  Indexes {
    (ticker, date) [unique]
  }
}