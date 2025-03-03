import numpy as np
from scipy.stats import norm
from .varinputs import RiskInputs


# Risk Metrics
class VaRMetrics:
    """
    Class to calculate various Value at Risk (VaR) metrics.

    Parameters
    ----------
    inputs : RiskInputs
        Object containing the following option parameters:
        - confidence_level : float
            The confidence level for the VaR calculation.
        - lookback_period : int
            The number of historical days for risk estimation.
        - num_simulations : int
            The number of Monte Carlo simulations.
        - portfolio_returns : pd.DataFrame
            Historical returns of portfolio assets or single stock.
        - is_single_stock : bool
            Flag to indicate single stock calculation.
        - portfolio_weights : list of float, optional
            Weights of assets in the portfolio (None for single stock).

    Attributes
    ----------
    parametric_var : float
        The parametric VaR value.
    historical_var : float
        The historical VaR value.
    monte_carlo_var : float
        The Monte Carlo VaR value.
    expected_shortfall : float
        The expected shortfall value.

    """

    def __init__(self, inputs: RiskInputs):
        self.confidence_level = inputs.confidence_level
        self.lookback_period = inputs.lookback_period
        self.num_simulations = inputs.num_simulations
        self.returns = inputs.portfolio_returns
        self.is_single_stock = inputs.is_single_stock

        # attributes
        self.parametric_var = self._parametric_var()
        self.historical_var = self._historical_var()
        self.monte_carlo_var = self._monte_carlo_var()
        self.expected_shortfall = self._expected_shortfall()

        if self.is_single_stock:
            self.weights = np.array([1.0])  # Single stock, full weight
        else:
            if inputs.portfolio_weights is None:
                raise ValueError(
                    "Portfolio weights must be provided for portfolio VaR calculation"
                )
            self.weights = np.array(inputs.portfolio_weights)
            if len(self.weights) != self.returns.shape[1]:
                raise ValueError("Portfolio weights must match the number of assets")

    def _parametric_var(self) -> float:
        mean_returns = np.mean(self.returns, axis=0)
        std = np.std(self.returns, axis=0)
        return self.weights @ norm.ppf(
            1 - self.confidence_level, loc=mean_returns, scale=std
        )

    def _historical_var(self) -> float:
        portfolio_returns = (
            self.returns if self.is_single_stock else self.returns @ self.weights
        )
        return np.percentile(portfolio_returns, 100 * (1 - self.confidence_level))

    def _monte_carlo_var(self) -> float:
        mean_returns = np.mean(self.returns, axis=0)
        cov_matrix = (
            np.cov(self.returns.T)
            if not self.is_single_stock
            else np.var(self.returns, axis=0)
        )

        simulated_returns = (
            np.random.normal(mean_returns, np.sqrt(cov_matrix), self.num_simulations)
            if self.is_single_stock
            else np.random.multivariate_normal(
                mean_returns, cov_matrix, self.num_simulations
            )
        )

        portfolio_simulated_returns = (
            simulated_returns
            if self.is_single_stock
            else simulated_returns @ self.weights
        )
        return np.percentile(
            portfolio_simulated_returns, 100 * (1 - self.confidence_level)
        )

    def _expected_shortfall(self) -> float:
        portfolio_returns = (
            self.returns if self.is_single_stock else self.returns @ self.weights
        )
        var = self._historical_var()
        return np.mean(portfolio_returns[portfolio_returns <= var])
