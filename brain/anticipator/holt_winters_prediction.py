import matplotlib.pyplot as plt

from scipy.optimize import minimize
import numpy as np
from seasonal import fit_seasons, adjust_seasons


class HoltWintersPrediction:
    def __init__(self, raw_data, forecast_len=0, forecast_method="auto"):
        """

        :param raw_data:
        :param forecast_len:
        :param forecast_method: could be "auto", "additive", "multiplicative",
               if new data is based on the last one, use "additive",
               if new data is a factor of the last one, use "multiplicative",
               you can also use "auto", but it will be twice slower
        """
        self.raw_data = raw_data
        self.season, self.trend = fit_seasons(self.raw_data)
        self.season_period = len(self.season)
        self.adjusted = adjust_seasons(self.raw_data, seasons=self.season)
        self.residual = self.adjusted - self.trend
        self.forecast_len = forecast_len
        self.forecast_method = forecast_method

    def holt_winters_additive(self, x):
        y = x[:]
        init_values = np.array([0.5, 0.5, 0.5])
        boundaries = [(0, 1), (0, 1), (0, 1)]

        parameters = minimize(self.rmse_holt_winters_additive, x0=init_values,
                              args=(y, self.season_period), bounds=boundaries)
        alpha, beta, gamma = parameters.x

        level = [sum(y[0:self.season_period]) / float(self.season_period)]
        trend = [(sum(y[self.season_period:2 * self.season_period])
                  - sum(y[0:self.season_period])) / self.season_period ** 2]
        season = [y[i] - level[0] - trend[0] for i in range(self.season_period)]
        forecast = [level[0] + trend[0] + season[0]]

        for i in range(len(y) + self.forecast_len):
            if i == len(y):
                y.append(level[-1] + trend[-1] + season[-self.season_period])

            level.append(alpha * (y[i] - season[i]) +
                         (1 - alpha) * (level[i] + trend[i]))
            trend.append(beta * (level[i + 1] - level[i]) + (1 - beta) * trend[i])
            season.append(gamma * (y[i] - level[i] - trend[i])
                          + (1 - gamma) * season[i])
            forecast.append(level[i + 1] + trend[i + 1] + season[i + 1])

        return forecast

    def rmse_holt_winters_additive(self, params, *args):
        Y = args[0]
        self.season_period = args[1]

        train_forecast_len = len(Y) - self.season_period
        y_train = Y[0:train_forecast_len]

        alpha, beta, gamma = params
        level = [sum(y_train[0:self.season_period]) / float(self.season_period)]
        trend = [(sum(y_train[self.season_period:2 * self.season_period]) -
                  sum(Y[0:self.season_period])) / self.season_period ** 2]
        season = [y_train[i] - level[0] - trend[0] for i in range(self.season_period)]
        forecast = [level[0] + trend[0] + season[0]]

        for i in range(len(y_train) + self.season_period):
            if i == len(y_train):
                y_train.append(level[-1] + trend[-1] + season[-self.season_period])

            level.append(alpha * (y_train[i] - season[i]) + (1 - alpha)
                         * (level[i] + trend[i]))
            trend.append(beta * (level[i + 1] - level[i]) + (1 - beta) * trend[i])
            season.append(gamma * (y_train[i] - level[i] - trend[i]) +
                          (1 - gamma) * season[i])
            forecast.append(level[i + 1] + trend[i + 1] + season[i + 1])

        rmse = np.sqrt(sum([(k - n) ** 2 for k, n in zip(Y, forecast)]) / len(Y))
        return rmse

    def holt_winters_multiplicative(self, x):
        y = x[:]
        init_values = np.array([0.5, 0.5, 0.5])
        boundaries = [(0, 1), (0, 1), (0, 1)]

        parameters = minimize(self.rmse_holt_winters_multiplicative, x0=init_values,
                              args=(y, self.season_period), bounds=boundaries)
        alpha, beta, gamma = parameters.x

        level = [sum(y[0:self.season_period]) / float(self.season_period)]
        trend = [(sum(y[self.season_period:2 * self.season_period])
                  - sum(y[0:self.season_period]))
                 / self.season_period ** 2]
        season = [y[i] / (level[0] + trend[0]) for i in range(self.season_period)]
        forecast = [(level[0] + trend[0]) * season[0]]

        for i in range(len(y) + self.forecast_len):
            if i == len(y):
                y.append((level[-1] + trend[-1]) * season[-self.season_period])

            if season[i] < 10 ** 8:
                level.append(alpha * (y[i]) + (1 - alpha) * (level[i] + trend[i]))
            else:
                level.append(alpha * (y[i] / season[i]) + (1 - alpha) *
                             (level[i] + trend[i]))
            trend.append(beta * (level[i + 1] - level[i]) + (1 - beta) * trend[i])
            season.append(gamma * (y[i] / (level[i] + trend[i])) +
                          (1 - gamma) * season[i])
            forecast.append((level[i + 1] + trend[i + 1]) * season[i + 1])

        return forecast

    def rmse_holt_winters_multiplicative(self, params, *args):
        Y = args[0]
        self.season_period = args[1]

        train_forecast_len = len(Y) - self.season_period
        y_train = Y[0:train_forecast_len]

        alpha, beta, gamma = params
        level = [sum(y_train[0:self.season_period]) / float(self.season_period)]
        trend = [(sum(y_train[self.season_period:2 * self.season_period]) -
                  sum(Y[0:self.season_period])) / self.season_period ** 2]
        season = [Y[i] / (level[0] + trend[0]) for i in range(self.season_period)]
        forecast = [(level[0] + trend[0]) * season[0]]

        for i in range(len(y_train) + self.season_period):
            if i == len(y_train):
                y_train.append((level[-1] + trend[-1]) * season[-self.season_period])

            if season[i] < 10 ** 8:
                level.append(alpha * (y_train[i]) + (1 - alpha) *
                             (level[i] + trend[i]))
            else:
                level.append(alpha * (y_train[i] / season[i]) + (1 - alpha) *
                             (level[i] + trend[i]))

            trend.append(beta * (level[i + 1] - level[i]) + (1 - beta) * trend[i])
            season.append(gamma * (y_train[i] / (level[i] + trend[i])) +
                          (1 - gamma) * season[i])
            forecast.append((level[i + 1] + trend[i + 1]) * season[i + 1])

        rmse = np.sqrt(sum([(k - n) ** 2 for k,
                                             n in zip(Y[:], forecast[:])]) / len(Y))
        return rmse

    def predict(self, x):
        if self.forecast_method == "auto":
            fa = self.holt_winters_additive(x)
            fm = self.holt_winters_multiplicative(x)

            rmsea = np.sqrt(sum([(k - n) ** 2 for k, n in zip(x, fa)]) / len(x))
            rmsem = np.sqrt(sum([(k - n) ** 2 for k, n in zip(x, fm)]) / len(x))

            if rmsea < rmsem:
                forecast = self.holt_winters_additive(x)
                print('additive season')
            else:
                forecast = self.holt_winters_multiplicative(x)
                print('multiplicative season')

            return forecast
        elif self.forecast_method == "additive":
            return self.holt_winters_additive(x)
        elif self.forecast_method == "multiplicative":
            return self.holt_winters_multiplicative(x)


if __name__ == "__main__":
    x = []
    y_additive = []
    y_multiplicative = []

    season = [0.0000, 0.0003, 0.0111, 0.1353, 0.6065, 1.0000, 0.6065, 0.1353,
              0.0111, 0.0003, 0.0000]
    noise = 0 * np.random.randn(200)

    for i in range(-100, 100):
        x.append(float(i) / 10)
        y_additive.append(1.3 ** x[-1])
        y_multiplicative.append(1.3 ** x[-1])

    for i in range(len(x)):
        y_additive[i] = y_additive[i] + season[i % 10] + noise[i]
        y_multiplicative[i] = y_multiplicative[i] * season[i % 10] + noise[i]

    hw = HoltWintersPrediction(y_additive, forecast_len=50, forecast_method="additive")

    forecast_1 = hw.predict(y_additive)
    forecast_2 = hw.predict(y_multiplicative)
    plt.plot(forecast_1, label='forecast')
    plt.plot(y_additive, label='noisy')
    plt.legend()

    plt.figure(2)
    plt.plot(forecast_2)
    plt.plot(y_multiplicative)
    plt.show()
