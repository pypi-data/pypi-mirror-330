
Quantmod Python package is inspired by the quantmod package for R. This new tool is designed to assist quantitative traders and data analysts with the development, testing, and rapid prototyping of trading strategies. quantmod features a straightforward and intuitive interface aimed at simplifying workflows and boosting productivity.


## Installation
The easiest way to install quantmod is using pip:

```bash
pip install quantmod
```


## Modules

* [markets](https://kannansingaravelu.com/docs/site/markets/)
* [models](https://kannansingaravelu.com/docs/site/models/)
* [risk](https://kannansingaravelu.com/docs/site/risk/) 
* [timeseries](https://kannansingaravelu.com/docs/site/timeseries/)
* [indicators](https://kannansingaravelu.com/docs/site/indicators/)
* [derivatives](https://kannansingaravelu.com/docs/site/derivatives/)
* [datasets](https://kannansingaravelu.com/docs/site/datasets/)


## Quickstart

```py
# Retrieves market data & ticker object 
from quantmod.markets import getData, getTicker

# Option price
from quantmod.models import OptionInputs, BlackScholesOptionPricing, MonteCarloOptionPricing

# Risk measures
from quantmod.risk import RiskInputs, ValueAtRisk, ConditionalVaR, VarBacktester

# Calculates price return of different time period.
from quantmod.timeseries import *

# Technical indicators
from quantmod.indicators import ATR

# Derivatives functions
from quantmod.derivatives import maxpain

# Datasets functions
from quantmod.datasets import fetch_historical_data
```
<br>
Note: quantmod is currently under active development, and anticipate ongoing enhancements and additions. The aim is to continually improve the package and expand its capabilities to meet the evolving needs of the community.


## Examples
Refer to the [examples](https://kannansingaravelu.com/) section for more details.


## Changelog
The list of changes to quantmod between each release can be found [here](https://kannansingaravelu.com/docs/site/changelog/)


## Community
[Join the quantmod server](https://discord.com/invite/DXQyezbJ) to share feature requests, report bugs, and discuss the package.


## Legal 
`quatmod` is distributed under the **Apache Software License**. See the [LICENSE.txt](https://www.apache.org/licenses/LICENSE-2.0.txt) file in the release for details.
