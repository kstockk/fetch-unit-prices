# Fetch-Unit-Prices

Additonal price source for Bean-Price.

Fetches unit prices using APIR codes from the IOOF website (Australia).

'https://www.ioof.com.au/performance/unit-prices'

## Installation

```bash
python setup.py install
```

## Usage

```
bean-price -e 'AUD:my_sources.ioof:APIR_CODE'

bean-price -e 'AUD:my_sources.ioof:APIR_CODE' -d 2020-07-01
```

As unit prices are delayed, unlike listed securities, I have a bash script which fetches the unit-prices for the last 5 days, as just using the get_latest_price will not look at what prices were missing from your prices.beancount
