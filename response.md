# Response
## A. Required Information
### A.1. Requirement Completion Rate
- [V] List all pharmacies open at a specific time and on a day of the week if requested.
  - Implemented endpoint `/pharmacies/open`.
  - Example input
  ![](docs/pharmacies_open.png)
- [V] List all masks sold by a given pharmacy, sorted by mask name or price.
  - Implemented at endpoint `/pharmacies/{pharmacy_name}/masks`.
  - Example input
  ![](docs/pharmacyies_name.png)
- [V] List all pharmacies with more or less than x mask products within a price range.
  - Implemented at endpoint `/pharmacies/masks/by-price-range`.
  - Example input
  ![](docs/masks-by-price.png)
- [V] The top x users by total transaction amount of masks within a date range.
  - Implemented at endpoint `/users/top-by-amount`.
  - Example input
  ![](docs/user-top-by-amount.png)
- [V] The total number of masks and dollar value of transactions within a date range.
  - Implemented at endpoint `/users/transactions/summary`.
  - Example input
  ![](docs/transactions-summary.png)
- [V] Search for pharmacies or masks by name, ranked by relevance to the search term.
  - Implemented at endpoint `/search/fuzzy/pharmacy-or-mask`.
  - Example input
  ![](docs/serch-pharmacies.png)
- [V] Process a user purchases a mask from a pharmacy, and handle all relevant data changes in an atomic transaction.
  - Implemented at endpoint `/transactions/purchase`.
  - Example input
  ![](docs/transactions-purchase.png)

### A.2. API Document
After using `docker-compose.yml`, you should be able to open the following swagger docs
[swagger](http://localhost:9789/docs).
![swagger example](docs/swagger.png)

### A.3. Import Data Commands
Data import is implemented in [start.sh](start.sh), once the API is started, data import will be done

## B. Bonus Information

### B.1. Dockerized
Please check my [Dockerfile](docker/Dockerfile) / [docker-compose.yml](docker/docker-compose.yml).

On the local machine, please follow the commands below to build it.
After building image, you should be able to use docker-compose to have DB and API service
```bash
$ docker build -t fastapi:test -f docker/Dockerfile .  
$ docker-compose up -d
```
