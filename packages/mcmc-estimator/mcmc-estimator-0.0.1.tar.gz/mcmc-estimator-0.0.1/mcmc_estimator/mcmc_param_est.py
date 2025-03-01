import numpy as np
import matplotlib.pyplot as plt

class MCMCParameterEstimator:
    """
    A general MCMC parameter estimator that uses the Metropolis-Hastings algorithm.
    Provide:
      - model_fn(params, x) -> y_pred
      - data x, data y (observations)
      - log_likelihood_fn(params, x, y) (optional, defaults to Gaussian errors with known sigma)
      - log_prior_fn(params) (optional, defaults to Gaussian priors N(0,10^2))
      - initial_params (array-like, initial guess)
      - step_size (float or array-like, controls proposal distribution)
      - n_iterations
      - burn_in fraction
    After run(), use get_samples() for the posterior chain or summary() for a quick stats summary.
    """
    def __init__(
        self,
        model_fn,
        x_data,
        y_data,
        initial_params,
        step_size=0.1,
        n_iterations=10_000,
        burn_in=0.2,
        sigma_obs=1.0,
        log_prior_fn=None,
        log_likelihood_fn=None,
        random_seed=None
    ):
        """
        Args:
            model_fn (callable): Function model_fn(params, x) -> predicted y
            x_data (array-like): Independent variable data
            y_data (array-like): Observed dependent variable data
            initial_params (array-like): Initial guess of parameters
            step_size (float or array-like): Standard deviation(s) for Gaussian proposal
            n_iterations (int): Number of total MCMC steps
            burn_in (float): Fraction of samples to discard as burn-in (0 <= burn_in < 1)
            sigma_obs (float): Standard deviation for Gaussian noise (if using default likelihood)
            log_prior_fn (callable): log_prior_fn(params) -> float (log of the prior)
                If None, a default Gaussian prior N(0,10^2) is used for each parameter.
            log_likelihood_fn (callable): log_likelihood_fn(params, x_data, y_data) -> float
                If None, a default Gaussian error model is used: 
                log p(y|params) = -0.5 sum( (y - model(params,x))/sigma_obs )^2 ...
            random_seed (int or None): Fix random seed for reproducibility
        """
        self.model_fn = model_fn
        self.x_data = np.array(x_data)
        self.y_data = np.array(y_data)
        self.initial_params = np.array(initial_params, dtype=float)
        self.n_params = len(self.initial_params)
        self.step_size = step_size if hasattr(step_size, "__len__") else np.repeat(step_size, self.n_params)
        self.n_iterations = n_iterations
        self.burn_in = burn_in
        self.sigma_obs = sigma_obs
        
        if random_seed is not None:
            np.random.seed(random_seed)
        
        # Set defaults if None
        self.log_prior_fn = log_prior_fn if log_prior_fn is not None else self._default_log_prior
        self.log_likelihood_fn = (
            log_likelihood_fn if log_likelihood_fn is not None else self._default_log_likelihood
        )
        
        # Will store chains
        self.chain = None
        self.acceptance_rate_ = None

    def _default_log_prior(self, params):
        """
        Default prior: Each parameter is ~ N(0, 10^2).
        log p(param) = -0.5 * (param/10)^2 - log(10 * sqrt(2 pi))
        Summed over all parameters.
        """
        sigma_p = 10.0
        const_term = -np.log(sigma_p * np.sqrt(2 * np.pi))  # constant per parameter
        lp = 0.0
        for p in params:
            lp += -0.5 * (p / sigma_p) ** 2 + const_term
        return lp

    def _default_log_likelihood(self, params, x_data, y_data):
        """
        Default likelihood: Gaussian errors with known sigma_obs.
        log p(y|params) = -0.5 * sum( ((y - model(params,x))/sigma_obs)^2 ) - ...
        """
        y_model = self.model_fn(params, x_data)
        residual = (y_data - y_model) / self.sigma_obs
        ll = -0.5 * np.sum(residual**2)  
        # minus constant term:
        ll -= 0.5 * len(x_data) * np.log(2 * np.pi * self.sigma_obs**2)
        return ll

    def log_posterior(self, params):
        """Compute log posterior = log prior + log likelihood."""
        lp = self.log_prior_fn(params)
        if np.isinf(lp) or np.isnan(lp):
            return -np.inf
        ll = self.log_likelihood_fn(params, self.x_data, self.y_data)
        if np.isinf(ll) or np.isnan(ll):
            return -np.inf
        return lp + ll

    def run(self):
        """
        Run Metropolis-Hastings MCMC to sample from the posterior distribution of parameters.
        """
        chain = np.zeros((self.n_iterations, self.n_params))
        chain[0] = self.initial_params
        
        current_lp = self.log_posterior(chain[0])
        n_accepted = 0
        
        for i in range(1, self.n_iterations):
            # Propose new parameters from a Gaussian around current
            proposal = chain[i-1] + np.random.normal(0, self.step_size, size=self.n_params)
            
            proposal_lp = self.log_posterior(proposal)
            accept_prob = np.exp(proposal_lp - current_lp)

            # Accept or reject
            if np.random.rand() < accept_prob:
                chain[i] = proposal
                current_lp = proposal_lp
                n_accepted += 1
            else:
                chain[i] = chain[i-1]
        
        self.chain = chain
        self.acceptance_rate_ = n_accepted / (self.n_iterations - 1)

    def get_samples(self):
        """
        Return the MCMC samples after burn-in.
        """
        if self.chain is None:
            raise RuntimeError("You must call run() before obtaining samples.")
        burn = int(self.burn_in * self.n_iterations)
        return self.chain[burn:]
    
    def summary(self, credible_interval=0.95):
        """
        Print summary statistics: mean, std, and optional credible intervals.
        """
        samples = self.get_samples()
        means = np.mean(samples, axis=0)
        stds = np.std(samples, axis=0)
        
        # For credible intervals, we'll do a percentile-based approach
        alpha = 0.5 * (1 - credible_interval)
        lower_percentile = 100 * alpha
        upper_percentile = 100 * (1 - alpha)
        lower_bounds = np.percentile(samples, lower_percentile, axis=0)
        upper_bounds = np.percentile(samples, upper_percentile, axis=0)
        
        print("Acceptance Rate = {:.3f}".format(self.acceptance_rate_))
        print("Parameter Estimates:")
        for i in range(self.n_params):
            print(
                f"Param {i}: mean={means[i]:.3f}, "
                f"std={stds[i]:.3f}, "
                f"{int(100*credible_interval)}% CI=({lower_bounds[i]:.3f}, {upper_bounds[i]:.3f})"
            )

    def plot_fit(self, x_range=None, num_points=100):
        """
        Plot the observed data alongside the model prediction using mean posterior parameters.
        
        Args:
            x_range (tuple): The range of x values for plotting the model. 
                             Defaults to the observed data range.
            num_points (int): Number of points to plot for the model curve.
        """
        if self.chain is None:
            raise RuntimeError("You must call run() before plotting the fit.")

        # Get mean parameter values from posterior samples
        samples = self.get_samples()
        mean_params = np.mean(samples, axis=0)

        # Define x_range for plotting if not provided
        if x_range is None:
            x_range = (min(self.x_data), max(self.x_data))
        x_plot = np.linspace(x_range[0], x_range[1], num_points)

        # Calculate model predictions
        y_model = self.model_fn(mean_params, x_plot)

        # Plot data and model
        plt.figure(figsize=(8, 6))
        plt.scatter(self.x_data, self.y_data, label="Observed Data", color="black", alpha=0.7)
        plt.plot(x_plot, y_model, label="Model Fit (Mean Parameters)", color="red", linewidth=2)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
        plt.title("Observed Data and Model Fit")
        plt.grid(True)
        plt.show()

    def plot_diagnostics(self, param_names=None):
        """
        Plot trace plots and posterior histograms for all parameters.
        
        Args:
            param_names (list of str): Optional names for the parameters.
                                       If None, uses generic names "Param 0", "Param 1", etc.
        """
        if self.chain is None:
            raise RuntimeError("You must call run() before plotting diagnostics.")

        samples = self.get_samples()
        n_params = samples.shape[1]

        # Set default parameter names if none provided
        if param_names is None:
            param_names = [f"Param {i}" for i in range(n_params)]

        # Create figure for trace plots and histograms
        fig, axes = plt.subplots(n_params, 2, figsize=(10, 3 * n_params))
        fig.tight_layout(pad=4)

        for i in range(n_params):
            # Trace plot
            axes[i, 0].plot(samples[:, i], alpha=0.7, color="blue")
            axes[i, 0].set_title(f"Trace Plot: {param_names[i]}")
            axes[i, 0].set_xlabel("Iteration")
            axes[i, 0].set_ylabel(param_names[i])

            # Posterior histogram
            axes[i, 1].hist(samples[:, i], bins=30, color="green", alpha=0.7)
            axes[i, 1].set_title(f"Posterior Distribution: {param_names[i]}")
            axes[i, 1].set_xlabel(param_names[i])
            axes[i, 1].set_ylabel("Frequency")

        plt.show()
