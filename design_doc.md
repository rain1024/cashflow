# Class Diagram 
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