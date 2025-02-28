import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

from tqdm import tqdm
import os
from datetime import datetime

from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN, HDBSCAN, AgglomerativeClustering, MiniBatchKMeans
from sklearn.mixture import GaussianMixture
from sklearn.metrics import mean_squared_error, silhouette_score, calinski_harabasz_score, davies_bouldin_score, r2_score, mean_absolute_error, mean_absolute_percentage_error
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA, FactorAnalysis
from sklearn.manifold import TSNE

import umap
try:
    import torch
except:
    pass

from scipy.spatial.distance import pdist, squareform
from scipy import stats
from scipy.stats import spearmanr, gaussian_kde
 
from kneed import KneeLocator
from typing import Dict, List, Tuple, Union, Optional, Any

from sage_lib.miscellaneous.math_tools import *
import joblib

# Definición de la clase GPUKMeansAuto
class GPUKMeansAuto:
    def __init__(self, max_clusters=10, max_iter=100):
        self.max_clusters = max_clusters
        self.max_iter = max_iter
        self.labels_ = None
        self.n_clusters_ = None

    def fit_predict(self, data):
        labels, n_clusters = self.kmeans_auto_pytorch(data, self.max_clusters, self.max_iter)
        self.labels_ = labels
        self.n_clusters_ = n_clusters
        return labels

    def kmeans_pytorch(self, data, num_clusters, max_iter=100):
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        data_tensor = torch.tensor(data, device=device)

        # Inicializar centroides aleatoriamente
        indices = torch.randperm(data_tensor.size(0))[:num_clusters]
        centroids = data_tensor[indices]

        for _ in range(max_iter):
            # Asignar puntos al cluster más cercano
            distances = torch.cdist(data_tensor, centroids)
            labels = torch.argmin(distances, dim=1)

            # Recalcular centroides
            new_centroids = torch.stack([data_tensor[labels == i].mean(0) for i in range(num_clusters)])

            # Verificar convergencia
            if torch.allclose(centroids, new_centroids):
                break
            centroids = new_centroids

        return labels.cpu().numpy(), centroids.cpu().numpy()

    def kmeans_auto_pytorch(self, data, max_clusters=10, max_iter=100):
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        data_tensor = torch.tensor(data, device=device)

        best_score = -1
        best_labels = None
        best_num_clusters = 2

        for num_clusters in range(2, max_clusters + 1):
            labels, _ = self.kmeans_pytorch(data, num_clusters, max_iter)
            if len(np.unique(labels)) > 1:
                score = silhouette_score(data, labels)
                if score > best_score:
                    best_score = score
                    best_labels = labels
                    best_num_clusters = num_clusters

        return best_labels, best_num_clusters

# PLOTs
def correlation_plot(data, feature_names=None, figsize=(15, 15), output_file='correlation_plot.png'):
    """
    Generate a correlation plot with distributions on the diagonal, improved scatter plots 
    on the upper triangle, and correlation coefficients on the lower triangle, then save it to a file.
    
    Parameters:
    data (np.ndarray): Input data matrix with shape [samples, features].
    feature_names (list): List of feature names (optional).
    figsize (tuple): Figure size (width, height) in inches.
    output_file (str): Output filename for saving the plot.
    
    Returns:
    matplotlib.figure.Figure: The generated figure object.
    """
    directory = os.path.dirname(output_file)
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    if feature_names is None:
        feature_names = [f'Feature_{i}' for i in range(data.shape[1])]
    
    n_features = data.shape[1]
    
    # Create figure and axes objects
    fig, axes = plt.subplots(n_features, n_features, figsize=figsize)
    
    # Create a custom colormap similar to 'coolwarm'
    colors = ['blue', 'white', 'red']
    n_bins = 100
    cmap = LinearSegmentedColormap.from_list('custom_diverging', colors, N=n_bins)
    
    for i in range(n_features):
        for j in range(n_features):
            ax = axes[i, j]
            
            if i == j:
                # Diagonal: Distribution plot
                ax.hist(data[:, i], bins=20, density=True, alpha=0.7)
                kde = gaussian_kde(data[:, i])
                x_range = np.linspace(data[:, i].min(), data[:, i].max(), 100)
                ax.plot(x_range, kde(x_range))
                ax.set_title(feature_names[i], fontsize=10)
                ax.tick_params(axis='both', which='major', labelsize=8)
            elif i < j:
                # Upper triangle: Scatter plot
                ax.scatter(data[:, j], data[:, i], alpha=0.3, s=10)  # Smaller, more transparent points
                ax.set_xlabel(feature_names[j], fontsize=8)
                ax.set_ylabel(feature_names[i], fontsize=8)
                ax.tick_params(axis='both', which='major', labelsize=6)
            else:
                # Lower triangle: Correlation coefficient
                corr = np.corrcoef(data[:, i], data[:, j])[0, 1]
                ax.text(0.5, 0.5, f"{corr:.2f}", ha="center", va="center", fontsize=12)
                ax.set_facecolor(cmap((corr + 1) / 2))
                ax.set_xticks([])
                ax.set_yticks([])
    
    plt.tight_layout()
    
    # Save the figure to a file
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f" >> Plot saved as {output_file}")
    
    return fig

class LinearAnalysis:
    def __init__(self, X:np.array=None, y:np.array=None, linear_methods:dict=None, force_negative:bool=None, X_labels:list=None,
                zero_intercept:bool=None, regularization:float=None, verbose:bool=None):
        self.X = X
        self.X_scale = None

        self.y = y
        self.y_scale = None
    
        self.X_labels = X_labels
        self.residuals = None
        
        self.results = {}
        self.analysis_results = {}

        self.linear_methods = {
            'sensitivity': self.sensitivity_analysis,
            'cross_validation': self.cross_validation,
            'bootstrap': self.bootstrap_analysis,
            'regularization': self.regularization_analysis,
            'multicollinearity': self.multicollinearity_analysis,
            'residuals_analysis': self.residuals_analysis, 
            'dynamic_permutation': self.evaluate_dynamic_permutation_impact, 
            'parity': self.calculate_fit_metrics, 
            } if not type(linear_methods) is dict else linear_methods

        self.force_negative = False if not force_negative is bool else force_negative
        self.zero_intercept = True if not zero_intercept is bool else zero_intercept
        self.regularization = 1e-5 if not regularization is float else regularization
        self.verbose = True if not verbose is bool else verbose

    def linear_predict(self, X: np.ndarray=None, y: np.ndarray=None, 
                       regularization: float = 1e-8, verbose: bool = False, 
                       force_negative: bool = False, zero_intercept: bool = False,
                       method: str = 'ridge', save:bool=True,
                       ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Ajusta un modelo lineal usando varios métodos, con opciones de regularización,
        forzar coeficientes negativos y hacer cero el término independiente.
        
        Args:
        X (np.ndarray): Matriz de características de entrada.
        y (np.ndarray): Vector de valores objetivo.
        regularization (float): Parámetro de regularización (por defecto 1e-8).
        verbose (bool): Si es True, imprime información adicional.
        force_negative (bool): Si es True, fuerza los coeficientes a ser no positivos usando NNLS.
        zero_intercept (bool): Si es True, fuerza el término independiente a ser cero.
        method (str): Método de resolución ('ridge', 'ols', o 'nnls').
        
        Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray]: Coeficientes, predicciones y residuos.
        """
        X = self.X if type(X) is type(None) else X
        y = self.y if type(y) is type(None) else y

        if zero_intercept:
            X_model = X
        else:
            X_model = np.column_stack([np.ones(X.shape[0]), X])
        
        n_features = X_model.shape[1]

        def solve_nnls(A, b):
            try:
                return nnls(A, b)
            except RuntimeError:
                if verbose:
                    print("NNLS no convergió. Usando solución de mínimos cuadrados con proyección.")
                coeffs, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
                coeffs[coeffs < 0] = 0  # Proyectar a no-negativos
                return coeffs, None

        if method == 'ls':
            if force_negative:
                X_aug = np.vstack([X_model, np.sqrt(regularization) * np.eye(n_features)])
                y_aug = np.concatenate([y, np.zeros(n_features)])
                coefficients, _ = solve_nnls(X_aug, -y_aug)
                coefficients = -coefficients

            else:
                coefficients, _, _, _ = np.linalg.lstsq(X_model, y, rcond=None)

        else:  # default to ridge regression
            if force_negative:
                X_aug = np.vstack([X_model, np.sqrt(regularization) * np.eye(n_features)])
                y_aug = np.concatenate([y, np.zeros(n_features)])
                coefficients, _ = solve_nnls(X_aug, -y_aug)
                coefficients = -coefficients
            else:
                XTX = X_model.T @ X_model
                XTy = X_model.T @ y
                coefficients = np.linalg.solve(XTX + regularization * np.eye(n_features), XTy)
        
        predictions = X_model @ coefficients
        residuals = y - predictions

        if verbose:
            print(f"Método utilizado: {method}")
            print(f"Coeficientes: {coefficients.shape}")
            print(f"Error cuadrático medio: {np.mean(residuals**2)}")
        
        if zero_intercept:
            coefficients = np.insert(coefficients, 0, 0)

        if save:
            self.result = {
                'coefficients': coefficients,
                'Method': method,
                'y': predictions,
                'residuals': residuals,
                'ECM': np.mean(residuals**2),
                'regularization': regularization,
                'force_negative': force_negative, 
                'zero_intercept': zero_intercept,
                     } 

        return coefficients, predictions, residuals

    def save_output(self, output_dir: str):
        """
        Saves all input and output information to a plain text file.
        
        Args:
        output_dir (str): Name of the path where the information will be saved.
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        with open(output_dir+'/linear_model.dat', 'w') as f:
            f.write("Analysis Results\n")
            f.write("================\n\n")
            
            f.write(f"Date and time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write("Input parameters:\n")
            f.write(f"  X shape: {self.X.shape if hasattr(self, 'X') else None}\n")
            f.write(f"  y shape: {self.y.shape if hasattr(self, 'y') else None}\n")
            f.write(f"  regularization: {self.result.get('regularization')}\n")
            f.write(f"  force_negative: {self.result.get('force_negative')}\n")
            f.write(f"  zero_intercept: {self.result.get('zero_intercept')}\n")
            f.write(f"  method: {self.result.get('method')}\n\n")
            
            f.write("Results:\n")
            f.write(f"  coefficients: {self.result.get('coefficients')}\n")
            f.write(f"  MSE: {self.result.get('MSE')}\n\n")
            
            if hasattr(self, 'sensitivity_result'):
                f.write("Sensitivity analysis:\n")
                f.write("  Mean coefficients:\n")
                for i, coeff in enumerate(self.sensitivity_result['mean_coefficients']):
                    f.write(f"    Noise level {i}: {coeff}\n")
                f.write("\n  Std coefficients:\n")
                for i, std in enumerate(self.sensitivity_result['std_coefficients']):
                    f.write(f"    Noise level {i}: {std}\n")
                f.write("\n  Mean absolute noise levels:\n")
                for i, noise in enumerate(self.sensitivity_result['mean_abs_noise_levels']):
                    f.write(f"    Level {i}: {noise}\n")
        
        print(f"Results saved in {output_dir+'/linear_model.dat'}")

    def n_fold_cross_validation(self, compositions: np.ndarray, energies: np.ndarray, 
                                k: int = 20, output_path: str = None, 
                                verbose: bool = False) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Perform N-fold cross-validation on the dataset.

        Args:
            compositions (np.ndarray): Array of composition data.
            energies (np.ndarray): Array of energy data.
            k (int): Number of nearest neighbors for local linear regression.
            output_path (str, optional): Path to save output files.
            verbose (bool): If True, print detailed information.

        Returns:
            Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Arrays of errors, predicted energies, 
                                                                   composition data, and coefficients.
        """
        print(f"Performing {k}-fold cross-validation...")

        unique_compositions = np.unique(compositions, axis=0)
        errors = []
        real_E = []
        predicted_E = []
        composition_data = []
        coeffs_data = []

        for i, comp in enumerate(unique_compositions):
            if verbose:
                print(f"Processing unique composition {i+1}/{len(unique_compositions)}: {comp}")
            
            mask = np.all(compositions == comp, axis=1)
            train_compositions = compositions[~mask]
            train_energies = energies[~mask]
            test_compositions = compositions[mask]
            test_energies = energies[mask]

            for test_comp, real_energy in zip(test_compositions, test_energies):
                coefficients, predictions, residuals = self.linear_predict(
                                            train_compositions, train_energies,
                                            regularization = 1e-8, verbose = False, 
                                            zero_intercept = True, force_negative = True,
                                            save=False, )

                predicted_energy = np.sum(test_comp*coefficients[1:])
                error = predicted_energy - real_energy

                coeffs_data.append(coefficients[1:])
                errors.append(error / np.sum(test_comp))
                predicted_E.append(predicted_energy)
                real_E .append(real_energy)
                composition_data.append(test_comp)
            
        data = np.array([np.concatenate((c, [e], [Ep], [Er], Mu)) for e, c, Ep, Er, Mu in zip(errors, composition_data, predicted_E, real_E, coeffs_data)])

        if verbose:
            print(f"Processing {len(unique_compositions)} unique composition : error {np.sum(errors)}")
            print(f" Mean Coefficients { '  '.join([f'mu({ual})={cd:.3f}' for cd, ual in zip( np.mean(coeffs_data,axis=0), self.uniqueAtomLabels ) ]) } ")

        if output_path:
            self.save_array_to_csv(data, column_names=np.concatenate((self.uniqueAtomLabels, ['error', 'predicted e', 'E', *[f'Coeff {ua}' for ua in self.uniqueAtomLabels] ])), 
                                   sample_numbers=True, file_path=output_path)
            print(f"Cross-validation results saved to {output_path}")

        print(f"Cross-validation completed. RMSE: {np.sqrt(np.mean(np.array(errors)**2)):.4f}")
        return np.array(errors), np.array(predicted_E), np.array(composition_data), np.array(coeffs_data)

    def find_optimal_k(self, composition_data: Dict[str, np.ndarray], initial_step: int = 10, 
                       refinement_step: int = 1, verbose: bool = False) -> Tuple[int, List, List, np.ndarray]:
        """
        Find the optimal value of k for locally linear regression.

        Args:
            composition_data (Dict[str, np.ndarray]): Dictionary containing composition and energy data.
            initial_step (int): Step size for initial broad search.
            refinement_step (int): Step size for refined search.
            verbose (bool): If True, print detailed information.

        Returns:
            Tuple[int, List, List, np.ndarray]: Optimal k value, initial errors, refined errors, and coefficients.
        """
        print("Finding optimal k for locally linear regression...")

        compositions = composition_data['composition_data']
        energies = composition_data['energy_data']
        n_samples = int(compositions.shape[0] * 0.9)

        k_values = range(compositions.shape[1], n_samples, initial_step)
        initial_errors = []
        error_history = []
        coeffs_history = []

        for idx, k in enumerate(k_values):
            errors, _, _, coeffs = self.n_fold_cross_validation(compositions, energies, k=k, verbose=False)
            current_rmse = np.mean(errors**2)**0.5
            initial_errors.append((k, current_rmse))
            error_history.append(current_rmse)
            coeffs_history.append(coeffs)

            if verbose:
                print(f"Initial search - k: {k}, RMSE: {current_rmse:.4f}, Progress: {100*(idx+1)/len(k_values):.2f}%")

            if len(error_history) > 4 and abs(error_history[-1] - error_history[-2]) < 1e-4:
                if verbose:
                    print(f"Early stopping at k: {k} due to minimal change in error.")
                break

        initial_best_k = min(initial_errors, key=lambda x: x[1])[0]
        print(f"Best k after initial search: {initial_best_k}")

        refined_range = range(max(1, initial_best_k - initial_step), 
                              min(n_samples, initial_best_k + initial_step), 
                              refinement_step)
        refined_errors = []
        for idx, k in enumerate(refined_range):
            errors, _, _, coeffs = self.n_fold_cross_validation(compositions, energies, k=k, verbose=False)
            current_rmse = np.mean(errors**2)**0.5
            refined_errors.append((k, current_rmse))
            coeffs_history.append(coeffs)

            if verbose:
                print(f"Refined search - k: {k}, RMSE: {current_rmse:.4f}, Progress: {100*(idx+1)/len(refined_range):.2f}%")

        best_k = min(refined_errors, key=lambda x: x[1])[0]
        print(f"Optimal k after refined search: {best_k}")

        return best_k, initial_errors, refined_errors, np.array(coeffs_history)

    def get_coefficients(self, data):
        return self.result.get('coefficients', None)

    def plot_results(self, plot, output_dir):
        pass

    def save_results(self, output_dir):
        pass

    def analysis(self, methods:list=None, plot:bool=True, output_dir:str='./'):

        if not type(methods) == list:
            methods = self.linear_methods.keys()

        prediction_method, X, y = self.linear_predict, self.X, self.y

        if 'sensitivity' in methods:
            self.analysis_results['sensitivity'] = self.sensitivity_analysis(prediction_method, X, y)
            self.plot_sensitivity_analysis(self.analysis_results['sensitivity'], output_file=f'{output_dir}/sensitivity_analysis.png')

        if 'cross_validation' in methods:        
            self.analysis_results['cross_validation'] = self.cross_validation(prediction_method, X, y)
            self.plot_coefficients_distribution(self.analysis_results['cross_validation']['coefficients'], 'Cross-Validation Coefficients', output_file=f'{output_dir}/Cross-Validation Coefficients.png')

        if 'bootstrap' in methods:          
            self.analysis_results['bootstrap'] = self.bootstrap_analysis(prediction_method, X, y)
            self.plot_coefficients_distribution(self.analysis_results['bootstrap']['coefficients'], 'Cross-Validation Coefficients', output_file=f'{output_dir}/Cross-Validation Coefficients.png')

        if 'regularization' in methods:
            self.analysis_results['regularization'] = self.regularization_analysis(prediction_method, X, y)
            self.plot_regularization_path(self.analysis_results['regularization']['coefficients'], self.analysis_results['regularization']['reg_range'], output_file=f'{output_dir}/regularization_results.png')

        if 'multicollinearity' in methods:
            self.analysis_results['multicollinearity'] = self.multicollinearity_analysis(X)
            self.plot_correlation_matrix(self.analysis_results['multicollinearity'], output_file=f'{output_dir}/multicollinearity_results.png')

        if 'multicollinearity' in methods:         
            self.analysis_results['residuals'] = self.residuals_analysis(prediction_method, X, y)
            self.plot_residuals(self.analysis_results['residuals']['residuals'], output_file=f'{output_dir}/residuals_results.png')

        if 'dynamic_permutation' in methods:         
            self.analysis_results['dynamic_permutation'] = self.evaluate_dynamic_permutation_impact(X=X, y=y, linear_predict=prediction_method)
            self.plot_dynamic_permutation_impact(self.analysis_results['dynamic_permutation']['mean_errors'], self.analysis_results['dynamic_permutation']['n_permutations'], output_file=f'{output_dir}/dynamic_permutation_impact.png')

        if 'parity' in methods:         
            self.analysis_results['parity'] = self.calculate_fit_metrics(X=X, y=y)
            self.plot_fit_analysis(self.analysis_results['parity'], output_file=f'{output_dir}/parity_plot.png')

        for m in methods:
            if not m in self.linear_methods:            
                print(f' (!) Method {m} is not recognizeble.')           


    def sensitivity_analysis(self, linear_predict, compositions, energies, noise_levels=np.logspace(-5, -3, num=30), n_iterations=300):
        """
        Perform sensitivity analysis by adding noise to the target values and save all coefficients.
        Args:
            linear_predict (function): The function used for linear prediction.
            compositions (np.array): Input features.
            energies (np.array): Target values.
            noise_levels (list): Levels of noise to add.
            n_iterations (int): Number of iterations for each noise level.
        Returns:
            dict: Dictionary containing all coefficients, mean and std of coefficients, and noise levels.
        """
        abs_max_energy = np.abs(np.max(energies))  # Precompute max energy
        n_coeffs = compositions.shape[1]  # Number of coefficients to track
        
        # Preallocate results
        all_coeffs = np.zeros((len(noise_levels), n_iterations, n_coeffs))
        mean_coeffs = np.zeros((len(noise_levels), n_coeffs))
        std_coeffs = np.zeros((len(noise_levels), n_coeffs))
        mean_abs_noise = np.zeros(len(noise_levels))

        for i, noise in enumerate(tqdm(noise_levels, desc="Processing noise levels")):
            noise_scale = abs_max_energy * noise
            coeffs_for_noise = np.zeros((n_iterations, n_coeffs))
            abs_noise_for_level = np.zeros(n_iterations)

            # Batch processing for efficiency
            noise_matrix = np.random.normal(0, noise_scale, size=(n_iterations, len(energies)))
            noisy_energies_matrix = energies + noise_matrix

            for j in range(n_iterations):
                noisy_energies = noisy_energies_matrix[j]
                coeffs, _, _ = linear_predict(compositions, noisy_energies, regularization=1e-5, verbose=False, zero_intercept=True, force_negative=False, save=False,)
                coeffs_for_noise[j] = coeffs[1:]  # Exclude intercept
                abs_noise_for_level[j] = np.std(noise_matrix[j])

            # Store results for this noise level
            all_coeffs[i] = coeffs_for_noise
            mean_coeffs[i] = np.mean(coeffs_for_noise, axis=0)
            std_coeffs[i] = np.std(coeffs_for_noise, axis=0)
            mean_abs_noise[i] = np.mean(abs_noise_for_level)

        return {
            "all_coeffs": all_coeffs,
            "mean_coeffs": mean_coeffs,
            "std_coeffs": std_coeffs,
            "mean_abs_noise": mean_abs_noise,
            "noise_levels": noise_levels,
        }

    def cross_validation(self, 
                                       linear_predict, X: np.ndarray, y: np.ndarray, 
                                       regularization: float = 1e-6, 
                                       force_negative: bool = False, 
                                       zero_intercept: bool = True, 
                                       method: str = 'ridge', 
                                       n_splits: int = 5, 
                                       verbose: bool = False):
        """
        Realiza una predicción lineal con validación cruzada utilizando diferentes métodos y opciones de regularización.
        
        Args:
        X (np.ndarray): Matriz de características de entrada.
        y (np.ndarray): Vector de valores objetivo.
        regularization (float): Parámetro de regularización (por defecto 1e-8).
        force_negative (bool): Si es True, fuerza los coeficientes a ser no positivos usando NNLS.
        zero_intercept (bool): Si es True, fuerza el término independiente a ser cero.
        method (str): Método de resolución ('ridge', 'ols', o 'nnls').
        n_splits (int): Número de splits para la validación cruzada.
        verbose (bool): Si es True, imprime información adicional.

        Returns:
        dict: Contiene los coeficientes promedio, el error cuadrático medio promedio y los resultados de cada fold.
        """
        
        kf = KFold(n_splits=n_splits)
        fold_results = []
        all_coefficients = []
        all_mse = []

        for train_index, test_index in kf.split(X):
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]

            # Llamar a la función linear_predict dentro de cada fold
            coefficients, predictions, residuals = linear_predict(X=X_train, y=y_train, 
                                                                  regularization=regularization, 
                                                                  force_negative=force_negative, 
                                                                  zero_intercept=zero_intercept, 
                                                                  method=method, 
                                                                  verbose=verbose,
                                                                  save=False,)

            mse = mean_squared_error(y_test, X_test @ coefficients[1:]) 
            all_coefficients.append(coefficients)
            all_mse.append(mse)

            fold_results.append({
                'coefficients': coefficients,
                'mse': mse
            })

        avg_coefficients = np.mean(all_coefficients, axis=0)
        avg_mse = np.mean(all_mse)

        if verbose:
            print(f"Validación cruzada completada: {n_splits} folds.")
            print(f"Error cuadrático medio promedio: {avg_mse}")
            print(f"Coeficientes promedio: {avg_coefficients}")

        return {
            'coefficients': all_coefficients, 'mse': all_mse,
            'avg_coefficients': avg_coefficients,
            'avg_mse': avg_mse,
            'fold_results': fold_results
        }

    def bootstrap_analysis(self, linear_predict, compositions, energies, n_iterations=1000):
        """
        Perform bootstrap analysis.

        Args:
            linear_predict (function): The function used for linear prediction.
            compositions (np.array): Input features.
            energies (np.array): Target values.
            n_iterations (int): Number of bootstrap iterations.

        Returns:
            dict: Dictionary containing bootstrap coefficients and confidence intervals.
        """
        bootstrap_coeffs = []
        for _ in tqdm(range(n_iterations), desc="Processing bootstrap_analysis"):
            indices = np.random.choice(len(compositions), size=len(compositions), replace=True)
            X_boot, y_boot = compositions[indices], energies[indices]
            coeffs, _, _ = linear_predict(X_boot, y_boot, regularization=1e-5, verbose=False, zero_intercept=True, force_negative=False, save=False)
            bootstrap_coeffs.append(coeffs[1:])
        
        ci_lower = np.percentile(bootstrap_coeffs, 2.5, axis=0)
        ci_upper = np.percentile(bootstrap_coeffs, 97.5, axis=0)
        
        return {'coefficients': bootstrap_coeffs, 'ci_lower': ci_lower, 'ci_upper': ci_upper}

    def regularization_analysis(self,linear_predict, compositions, energies, reg_range=np.logspace(-10, 1, 1000)):
        """
        Perform regularization analysis.

        Args:
            linear_predict (function): The function used for linear prediction.
            compositions (np.array): Input features.
            energies (np.array): Target values.
            reg_range (np.array): Range of regularization values to test.

        Returns:
            dict: Dictionary containing coefficients for each regularization value and the reg_range.
        """
        reg_coeffs = []
        for reg in tqdm(reg_range):
            coeffs, _, _ = linear_predict(compositions, energies, regularization=reg, verbose=False, zero_intercept=True, force_negative=False, save=False)
            reg_coeffs.append(coeffs[1:])
        return {'coefficients': reg_coeffs, 'reg_range': reg_range}

    def multicollinearity_analysis(self, compositions, *wargs, **kwargs):
        """
        Analyze multicollinearity among input features.

        Args:
            compositions (np.array): Input features.

        Returns:
            np.array: Correlation matrix of input features.
        """
        return np.corrcoef(compositions.T)

    def residuals_analysis(self, linear_predict, X, y):
        """
        Analyze residuals of the linear fit.

        Args:
            linear_predict (function): The function used for linear prediction.
            X (np.array): Input features.
            y (np.array): Target values.

        Returns:
            dict: Dictionary containing residuals and normality test results.
        """
        if self.result.get('residuals', None) is None:
            _, predictions, residuals = linear_predict(X, y, regularization=1e-5, verbose=False, zero_intercept=True, force_negative=False, save=False)
        else:
            residuals = self.result['residuals'] 

        _, p_value = stats.normaltest(residuals)
        return {'residuals': residuals, 'normality_p_value': p_value}

    def evaluate_dynamic_permutation_impact(self, X, y, linear_predict, n_permutations=300, n_iterations=100):
        """
        Evaluates the impact of performing n permutations on the input feature matrix X
        and calculates the mean error for each permutation count.

        Parameters:
        - X (np.ndarray): Input feature matrix with shape (n_samples, n_features).
        - y (np.ndarray): Target vector of length n_samples.
        - linear_predict (callable): Function to perform linear prediction. It should return
                                     coefficients, predictions, and residuals.
        - n_permutations (list of int): List of permutation counts to evaluate.
        - n_iterations (int): Number of iterations for each permutation count.

        Returns:
        - dict: A dictionary containing:
            - 'n_permutations': The list of permutation counts.
            - 'mean_errors': The mean error for each permutation count.
        """
        mean_errors = []
        n_permutations = n_permutations if n_permutations < X.size else X.size
        n_permutations_list = [n for n in range(0, n_permutations, 10)]

        for n_perm in tqdm(n_permutations_list, desc="Evaluating permutations"):
            errors = []

            for _ in range(n_iterations):
                # Create a permuted copy of X
                X_permuted = np.copy(X)
                
                # Generate random indices for rows and columns in a single operation
                indices = np.random.choice(X.size, size=n_perm, replace=False)
                row_indices, col_indices = np.unravel_index(indices, X.shape)

                cols_add = np.random.randint(0, X.shape[1], size=n_perm)
                perturbations = np.random.choice([-10, 10], size=n_perm)

                X_permuted[row_indices, col_indices] += perturbations
                for i, n in enumerate(cols_add):
                    X_permuted[row_indices[i], n] -= perturbations[i]

                # Predict using the linear model
                _, predictions, _ = linear_predict(
                    X=X_permuted, y=y, regularization=1e-5, force_negative=False, zero_intercept=True, verbose=False
                )

                # Calculate the Mean Squared Error (MSE)
                mse = np.mean((predictions - y) ** 2)
                errors.append(mse)

            # Compute the mean error for this permutation count
            mean_errors.append(np.mean(errors))

        return {"n_permutations": n_permutations_list, "mean_errors": mean_errors}


    def calculate_fit_metrics(self, X=None, y=None):
        """
        Calculate fit metrics and predicted vs. nominal values.

        Args:
            compositions (np.array): Input features.
            energies (np.array): Target values.

        Returns:
            dict: Dictionary containing predicted values, nominal values, and fit metrics.
        """
        # Realizar predicción
        y_predict = self.result['y']

        # Cálculo de métricas
        mse = mean_squared_error(y, y_predict)
        rmse = np.sqrt(mse)
        r2 = r2_score(y, y_predict)
        mae = mean_absolute_error(y, y_predict)
        mape = mean_absolute_percentage_error(y, y_predict)
        
        # Cálculo de métricas adicionales, por ejemplo, error en regiones específicas
        max_error = np.max(np.abs(y - y_predict))
        min_error = np.min(np.abs(y - y_predict))
        std_dev_error = np.std(y - y_predict)

        metrics = {
            'predicted': y_predict,
            'nominal': y,
            'mse': mse,
            'rmse': rmse,
            'r2': r2,
            'mae': mae,
            'mape': mape,
            'max_error': max_error,
            'min_error': min_error,
            'std_dev_error': std_dev_error
        }
        
        return metrics

    # ============ Plotting functions ============ ============ Plotting functions =========== ============ Plotting functions ===========

    def plot_sensitivity_analysis(self, result, feature_names=None, output_file='coefficients_distribution.png'):
        """
        Plot the results of the sensitivity analysis with two subplots.
        Args:
            result (dict): The result from sensitivity_analysis function.
            feature_names (list): Names of the features (optional).
        """
        noise_levels = result['noise_levels']
        mean_coeffs = np.array(result['mean_coeffs'])
        std_coeffs = np.array(result['std_coeffs'])

        n_features = mean_coeffs.shape[1]
        
        if feature_names is None:
            feature_names = [f'Feature {i+1}' for i in range(n_features)]

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 16), sharex=True)

        # Plot 1: Mean coefficients with std area
        for i in range(n_features):
            ax1.plot(noise_levels, mean_coeffs[:, i], label=feature_names[i])
            ax1.fill_between(noise_levels, 
                             mean_coeffs[:, i] - std_coeffs[:, i], 
                             mean_coeffs[:, i] + std_coeffs[:, i], 
                             alpha=0.2)

        ax1.set_xscale('log')
        ax1.set_ylabel('Coefficient Value')
        ax1.set_title('Sensitivity Analysis: Mean Coefficients with Std. Dev.')
        ax1.legend()
        ax1.grid(True, which="both", ls="-", alpha=0.2)

        # Plot 2: Standard deviation for each noise level
        for i in range(n_features):
            ax2.plot(noise_levels, std_coeffs[:, i], label=feature_names[i])

        ax2.set_xscale('log')
        ax2.set_xlabel('Noise Level')
        ax2.set_ylabel('Standard Deviation')
        ax2.set_title('Sensitivity Analysis: Standard Deviation of Coefficients')
        ax2.legend()
        ax2.grid(True, which="both", ls="-", alpha=0.2)

        plt.tight_layout()
        # Save the figure to a file
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f" >> Plot saved as {output_file}")

    def plot_coefficients_distribution(self, coeff_list, title, output_file='coefficients_distribution.png'):
        """
        Plot the distribution of coefficients using a KDE with shaded area, and label the maximum points with feature names.

        Args:
            coeff_list (list): List of coefficient arrays.
            title (str): Title of the plot.
            output_file (str): Path to save the plot image.
        """
        directory = os.path.dirname(output_file)
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        plt.figure(figsize=(12, 7))
        num_coeffs = len(coeff_list[0])
        colors = plt.cm.viridis(np.linspace(0, 1, num_coeffs))
        
        for i in range(num_coeffs):
            coeff_values = [c[i] for c in coeff_list]

            # Agregar una pequeña perturbación aleatoria
            coeff_values = np.array(coeff_values) + np.random.normal(0, 1e-8, size=len(coeff_values))
            
            # Calcular la estimación de densidad gaussiana
            kde = gaussian_kde(coeff_values)
            x_vals = np.linspace(min(coeff_values), max(coeff_values), 1000)
            y_vals = kde(x_vals)
            
            # Graficar la curva de densidad con sombreado
            plt.plot(x_vals, y_vals, color=colors[i], label=f'Coefficient {i+1}')
            plt.fill_between(x_vals, y_vals, alpha=0.3, color=colors[i])
            
            # Encontrar el punto máximo de la curva
            max_idx = np.argmax(y_vals)
            max_x = x_vals[max_idx]
            max_y = y_vals[max_idx]

            # Añadir la etiqueta en el punto máximo
            label = self.X_labels[i] if hasattr(self, 'X_labels') and i < len(self.X_labels) else f'Coefficient {i+1}'
            plt.text(max_x, max_y, label, fontsize=10, color=colors[i], ha='center', va='bottom')

        plt.title(title, fontsize=16, fontweight='bold')
        plt.xlabel('Coefficient Value', fontsize=12)
        plt.ylabel('Density', fontsize=12)
        plt.legend(fontsize=10, bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()

        # Guardar la figura en un archivo
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f" >> Plot saved as {output_file}")


    def plot_regularization_path(self, reg_coeffs, reg_range, output_file='regularization_path.png'):
        """
        Plot the regularization path with an enhanced appearance.

        Args:
            reg_coeffs (list): List of coefficient arrays for different regularization values.
            reg_range (np.array): Range of regularization values.
        """
        directory = os.path.dirname(output_file)
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        plt.figure(figsize=(12, 7))
        num_coeffs = len(reg_coeffs[0])
        colors = plt.cm.viridis(np.linspace(0, 1, num_coeffs))
        
        for i in range(num_coeffs):
            plt.semilogx(reg_range, [c[i] for c in reg_coeffs], label=f'Coefficient {i+1}',
                         linewidth=2, color=colors[i], marker='o', markersize=4)
        
        plt.title('Regularization Path', fontsize=16, fontweight='bold')
        plt.xlabel('Regularization Parameter', fontsize=12)
        plt.ylabel('Coefficient Value', fontsize=12)
        plt.legend(fontsize=10, bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, which="both", linestyle='--', alpha=0.7)
        plt.tight_layout()

        # Save the figure to a file
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f" >> Plot saved as {output_file}")
        '''
        Interpretación:

        Estabilidad de coeficientes: Si los coeficientes cambian drásticamente con pequeños cambios en la regularización, esto podría indicar inestabilidad en el modelo o multicolinealidad entre las características.
        Shrinkage (reducción): A medida que aumenta la regularización, normalmente verás que los coeficientes se acercan a cero. Esto es el efecto de "shrinkage" de la regularización.
        Importancia de las características: Las características cuyos coeficientes se mantienen grandes incluso con alta regularización son probablemente más importantes para el modelo.
        Overfitting vs Underfitting:

        Con baja regularización (izquierda del gráfico), los coeficientes pueden ser grandes, lo que podría indicar overfitting.
        Con alta regularización (derecha del gráfico), los coeficientes tienden a cero, lo que podría llevar a underfitting.


        Punto de inflexión: Busca un punto donde los coeficientes comienzan a estabilizarse. Este podría ser un buen valor de regularización para tu modelo final.
        '''
    def plot_correlation_matrix(self, correlation_matrix, output_file='correlation_matrix.png'):
        """
        Plot the correlation matrix of input features with an enhanced appearance.

        Args:
            correlation_matrix (np.array): Correlation matrix to plot.
        """
        directory = os.path.dirname(output_file)
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        plt.figure(figsize=(10, 8))
        im = plt.imshow(correlation_matrix, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
        plt.colorbar(im, label='Correlation Coefficient')
        
        plt.title('Correlation Matrix of Predictors', fontsize=16, fontweight='bold')
        if type(self.X_labels) == list:
            try:
                plt.xticks( range(len(correlation_matrix)), [f'{i}' for i in self.X_labels], rotation=45)
                plt.yticks( range(len(correlation_matrix)), [f'{i}' for i in self.X_labels] )
            except:
                print(' (!) Can not read variable labels.')
                plt.xticks(range(len(correlation_matrix)), [f'X{i+1}' for i in range(len(correlation_matrix))], rotation=45)
                plt.yticks(range(len(correlation_matrix)), [f'X{i+1}' for i in range(len(correlation_matrix))])

        else:
            plt.xticks(range(len(correlation_matrix)), [f'X{i+1}' for i in range(len(correlation_matrix))], rotation=45)
            plt.yticks(range(len(correlation_matrix)), [f'X{i+1}' for i in range(len(correlation_matrix))])

        plt.tight_layout()

        # Save the figure to a file
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f" >> Plot saved as {output_file}")

    def plot_residuals(self, residuals, output_file='residuals.png'):
        """
        Plot the residuals of the linear fit with an enhanced appearance.

        Args:
            residuals (np.array): Residuals to plot.
        """
        directory = os.path.dirname(output_file)
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        plt.figure(figsize=(12, 7))
        plt.scatter(range(len(residuals)), residuals, alpha=0.7, color='#1f77b4', edgecolor='black', linewidth=0.5)
        
        plt.title('Residuals Plot', fontsize=16, fontweight='bold')
        plt.xlabel('Data Point', fontsize=12)
        plt.ylabel('Residual', fontsize=12)
        
        plt.axhline(y=0, color='r', linestyle='--', linewidth=2)
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Add mean and std annotations
        mean_residual = np.mean(residuals)
        std_residual = np.std(residuals)
        plt.annotate(f'Mean: {mean_residual:.4f}\nStd Dev: {std_residual:.4f}', 
                     xy=(0.05, 0.95), xycoords='axes fraction',
                     fontsize=10, ha='left', va='top',
                     bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                     )
        
        plt.tight_layout()

        # Save the figure to a file
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f" >> Plot saved as {output_file}")

    def plot_k_convergence(self, initial_errors: List[Tuple[int, float]], 
                           refined_errors: List[Tuple[int, float]], 
                           coeffs: np.ndarray, output_path: str = None, 
                           verbose: bool = False) -> None:
        """
        Plot the convergence of RMSE and coefficients with respect to k values.

        Args:
            initial_errors (List[Tuple[int, float]]): List of (k, RMSE) from initial search.
            refined_errors (List[Tuple[int, float]]): List of (k, RMSE) from refined search.
            coeffs (np.ndarray): Array of coefficients for different k values.
            output_path (str, optional): Path to save the plot.
            verbose (bool): If True, print additional information.
        """
        print("Plotting k convergence and coefficient trends...")

        initial_k, initial_rmse = zip(*initial_errors)
        refined_k, refined_rmse = zip(*refined_errors)
        
        fig, ax = plt.subplots(2, 1, figsize=(12, 14))

        # RMSE convergence plot
        ax[0].plot(initial_k, initial_rmse, 'o-', label='Initial Search', color='blue')
        ax[0].plot(refined_k, refined_rmse, 'x-', label='Refined Search', color='red')
        ax[0].set_xlabel('k value')
        ax[0].set_ylabel('RMSE')
        ax[0].set_title('Convergence of RMSE with Different k Values')
        ax[0].legend()
        ax[0].grid(True)
        
        # Coefficients plot
        N, samples, atom_types = coeffs.shape
        colors = plt.cm.viridis(np.linspace(0, 1, atom_types))
        
        for atom_type in range(atom_types):
            for n in range(samples):
                label = f'{self.uniqueAtomLabels[atom_type]}' if n == 0 else None
                ax[1].plot(initial_k + refined_k, coeffs[:, n, atom_type], 'o-', 
                           color=colors[atom_type], alpha=0.2, label=label)

        ax[1].set_xlabel('k value')
        ax[1].set_ylabel('Coefficient Value')
        ax[1].set_title('Coefficients Trend with k Values')
        ax[1].legend()

        plt.tight_layout()
        
        if output_path:
            plt.savefig(f'{output_path}/k_convergence_with_coeffs.png', dpi=300)
            if verbose:
                print(f"Convergence plot saved to {output_path}/k_convergence_with_coeffs.png")

    def plot_dynamic_permutation_impact(self, mean_errors, n_permutations_list, output_file):
        """
        Plots the relationship between the number of permutations and the corresponding mean prediction errors.

        Parameters:
        - mean_errors (list): A list of mean errors corresponding to each permutation count.
        - n_permutations_list (list): A list of integers representing the number of permutations.
        - output_file (str): File path to save the resulting plot.

        This function saves the plot to a file rather than displaying it directly, which is useful for 
        documentation and presentations.
        """
        # Creating a figure object with a specific size
        plt.figure(figsize=(10, 6))
        
        # Plotting the mean errors as a function of permutation counts
        plt.plot(n_permutations_list, mean_errors, marker='o', linestyle='-', color='blue', label='Mean Error')
        
        # Adding labels and title
        plt.xlabel('Number of Permutations', fontsize=14)
        plt.ylabel('Mean Error', fontsize=14)
        plt.title('Impact of Feature Permutations on Model Accuracy', fontsize=16)
        
        # Adding a grid for better readability
        plt.grid(True)
        
        # Adding a legend to explain the plot elements
        plt.legend()
        
        # Saving the plot to the specified file path
        plt.savefig(output_file, format='png', dpi=300)
        
        # Clearing the plot from memory after saving to file
        plt.close()

    def plot_fit_analysis(self, fit_metrics, output_file=None):
        """
        Plot fit analysis showing predicted vs nominal values and other metrics.

        Args:
            fit_metrics (dict): Dictionary containing predicted, nominal, and fit metrics.
            output_file (str): Path to save the output plot.

        Returns:
            None
        """
        predicted = fit_metrics['predicted']
        nominal = fit_metrics['nominal']
        
        # Crear el plot
        plt.figure(figsize=(10, 8))
        
        # Gráfico de dispersión (scatter plot) Predicho vs Nominal
        plt.scatter(nominal, predicted, label='Predicted vs. Nominal', color='blue', alpha=0.6)
        
        # Línea ideal de ajuste perfecto (y = x)
        plt.plot([min(nominal), max(nominal)], [min(nominal), max(nominal)], 'r--', label='Ideal Fit (y = x)', linewidth=2)
        
        # Líneas adicionales de error
        plt.plot([min(nominal), max(nominal)], [min(nominal) + fit_metrics['rmse'], max(nominal) + fit_metrics['rmse']], 'g:', label='RMSE Offset (+)', linewidth=1)
        plt.plot([min(nominal), max(nominal)], [min(nominal) - fit_metrics['rmse'], max(nominal) - fit_metrics['rmse']], 'g:', label='RMSE Offset (-)', linewidth=1)
        
        # Añadir texto con las métricas
        plt.text(0.05, 0.95, f"RMSE: {fit_metrics['rmse']:.3f}", transform=plt.gca().transAxes, fontsize=12, verticalalignment='top')
        plt.text(0.05, 0.90, f"R²: {fit_metrics['r2']:.3f}", transform=plt.gca().transAxes, fontsize=12, verticalalignment='top')
        plt.text(0.05, 0.85, f"MAE: {fit_metrics['mae']:.3f}", transform=plt.gca().transAxes, fontsize=12, verticalalignment='top')
        plt.text(0.05, 0.80, f"MAPE: {fit_metrics['mape']:.3f}", transform=plt.gca().transAxes, fontsize=12, verticalalignment='top')
        plt.text(0.05, 0.75, f"Max Error: {fit_metrics['max_error']:.3f}", transform=plt.gca().transAxes, fontsize=12, verticalalignment='top')
        plt.text(0.05, 0.70, f"Std Dev Error: {fit_metrics['std_dev_error']:.3f}", transform=plt.gca().transAxes, fontsize=12, verticalalignment='top')
        
        # Etiquetas y título del gráfico
        plt.xlabel('Nominal Values')
        plt.ylabel('Predicted Values')
        plt.title('Fit Analysis: Predicted vs. Nominal')
        plt.legend()
        plt.grid(True)

        # Guardar o mostrar el gráfico
        if output_file:
            plt.savefig(output_file)

# Example usage:
# sensitivity_results = sensitivity_analysis(linear_predict, compositions, energies)
# cv_results = cross_validation(linear_predict, compositions, energies)
# bootstrap_results = bootstrap_analysis(linear_predict, compositions, energies)
# regularization_results = regularization_analysis(linear_predict, compositions, energies)
# multicollinearity_results = multicollinearity_analysis(compositions)
# residuals_results = residuals_analysis(linear_predict, compositions, energies)

# Plot results:
# plot_coefficients_distribution(sensitivity_results['coefficients'], 'Sensitivity Analysis')
# plot_coefficients_distribution(cv_results['coefficients'], 'Cross-Validation Coefficients')
# plot_coefficients_distribution(bootstrap_results['coefficients'], 'Bootstrap Coefficients')
# plot_regularization_path(regularization_results['coefficients'], regularization_results['reg_range'])
# plot_correlation_matrix(multicollinearity_results)
# plot_residuals(residuals_results['residuals'])

#linear_analysis = LinearAnalysis(X=compositions, y=energies)
#coefficients, predictions, residuals = linear_analysis.linear_predict()
#linear_analysis.analysis()

# ============ ClusteringAnalysis ============ ============ ClusteringAnalysis =========== ============ ClusteringAnalysis ===========
class ClusteringAnalysis:
    def __init__(self):
        self.data = None
        self.data_scaled = None
        self.results = {}
        self.dim_reduction = {}
        self.clustering_methods = {
            'dbscan': lambda eps, min_samples: DBSCAN(eps=eps, min_samples=min_samples),
            'kmeans': lambda n_clusters: KMeans(n_clusters=n_clusters, random_state=42),
            'gpu-kmeans': lambda: GPUKMeansAuto(),
            'minibatch-kmeans': lambda n_clusters: MiniBatchKMeans(
                n_clusters=n_clusters, batch_size=1000, max_iter=100, n_init=10, random_state=42
            ),
            'agglomerative': lambda n_clusters: AgglomerativeClustering(n_clusters=n_clusters),
            'gmm': lambda n_components: GaussianMixture(n_components=n_components, random_state=42),
            'hdbscan': lambda min_cluster_size, min_samples: HDBSCAN(
                min_cluster_size=min_cluster_size, 
                min_samples=min_samples
            ),
        }

    def kmeans_pytorch(self, data, num_clusters, max_iter=100):
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        data = torch.tensor(data, device=device)

        # Inicializar centroides aleatoriamente
        indices = torch.randperm(data.size(0))[:num_clusters]
        centroids = data[indices]

        for _ in range(max_iter):
            # Asignar puntos al cluster más cercano
            distances = torch.cdist(data, centroids)
            labels = torch.argmin(distances, dim=1)

            # Recalcular centroides
            new_centroids = torch.stack([data[labels == i].mean(0) for i in range(num_clusters)])

            # Verificar convergencia
            if torch.allclose(centroids, new_centroids):
                break
            centroids = new_centroids

        return labels.cpu().numpy(), centroids.cpu().numpy()

    def kmeans_auto_pytorch(self, data, max_clusters=10):
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        data = torch.tensor(data, device=device)

        best_score = -1
        best_labels = None
        best_num_clusters = 2

        for num_clusters in range(2, max_clusters + 1):
            labels, _ = kmeans_pytorch(data.cpu().numpy(), num_clusters)
            score = silhouette_score(data.cpu().numpy(), labels)
            if score > best_score:
                best_score = score
                best_labels = labels
                best_num_clusters = num_clusters

        return best_labels, best_num_clusters

    def preprocess_data(self, data):
        scaler = StandardScaler()
        return scaler.fit_transform(data)

    def estimate_initial_params(self, data, k=5):
        """
        Estimates initial DBSCAN parameters using k-distance graph.
        
        Parameters:
        -----------
        data : array-like
            The input data.
        k : int
            The number of neighbors to consider.
        
        Returns:
        --------
        tuple
            Estimated (eps, min_samples) parameters.
        """
        neigh = NearestNeighbors(n_neighbors=k)
        nbrs = neigh.fit(data)
        distances, _ = nbrs.kneighbors(data)
        distances = np.sort(distances, axis=0)
        distances = distances[:, 1]
        kneedle = KneeLocator(range(len(distances)), distances, curve='convex', direction='increasing')
        eps = distances[kneedle.elbow]
        return eps, k

    def optimize_dbscan_params(self, data, k_range=(2, 5), eps_margin=0.5, min_samples_margin=5, n_jobs=-1, cluster_penalty=-0.0, outlier_penalty=0.0, max_outlier_fraction=0.1):
        """
        Optimizes DBSCAN parameters using a combination of initial estimation and refined grid search,
        with penalties for the number of clusters and the proportion of outliers.
        
        This function aims to find optimal DBSCAN parameters that balance clustering quality,
        number of clusters, and outlier reduction.
        
        Parameters:
        -----------
        data : array-like, shape (n_samples, n_features)
            The input data to be clustered.
        k_range : tuple, optional (default=(2, 5))
            Range of k values to consider for initial parameter estimation.
        eps_margin : float, optional (default=0.5)
            Margin around the estimated eps for grid search.
        min_samples_margin : int, optional (default=5)
            Margin around the estimated min_samples for grid search.
        n_jobs : int, optional (default=-1)
            The number of parallel jobs to run. -1 means using all processors.
        cluster_penalty : float, optional (default=0.1)
            Penalty factor for the number of clusters.
        outlier_penalty : float, optional (default=0.2)
            Penalty factor for the fraction of outliers.
        max_outlier_fraction : float, optional (default=0.1)
            Maximum allowed fraction of outliers.
        
        Returns:
        --------
        tuple or None
            A tuple containing the best (eps, min_samples) parameters if found, 
            or None if no valid parameters were found.
        """

        def score_clustering(data, labels, n_clusters, outlier_fraction, cluster_penalty=0.1, outlier_penalty=1.0, 
                             max_clusters=10, max_outlier_fraction=0.5, metrics_weights={'silhouette': 0.4, 'calinski': 0.3, 'davies': 0.3},
                             verbose:bool=False):
            """
            Calcula una puntuación para el resultado del clustering, considerando múltiples métricas,
            número de clusters y fracción de outliers.
            
            Parámetros:
            -----------
            data : array-like
                Los datos de entrada.
            labels : array-like
                Etiquetas de cluster para cada punto en los datos.
            n_clusters : int
                Número de clusters (excluyendo puntos de ruido).
            outlier_fraction : float
                Fracción de puntos etiquetados como ruido.
            cluster_penalty : float, opcional (default=0.1)
                Factor de penalización para el número de clusters.
            outlier_penalty : float, opcional (default=1.0)
                Factor de penalización para la fracción de outliers.
            max_clusters : int, opcional (default=10)
                Número máximo de clusters permitidos.
            max_outlier_fraction : float, opcional (default=0.5)
                Fracción máxima de outliers permitida.
            metrics_weights : dict, opcional
                Pesos para cada métrica en el cálculo del score final.
            
            Retorna:
            --------
            float
                La puntuación calculada. Mayor es mejor.
            """
            # Verificar condiciones básicas
            #if n_clusters <= 1 or n_clusters > max_clusters:
            #    return -np.inf
            #if outlier_fraction < 0 or outlier_fraction > max_outlier_fraction:
            #    return -np.inf
            
            # Calcular métricas
            silhouette = silhouette_score(data, labels)
            calinski = calinski_harabasz_score(data, labels)
            davies = davies_bouldin_score(data, labels)
            
            # Normalizar calinski y davies (mayor es mejor para todas las métricas)
            calinski_norm = 1 / (1 + np.exp(-calinski / 1000))  # Sigmoid normalization
            davies_norm = 1 / (1 + davies)  # Inverse normalization
            
            # Calcular score combinado 
            combined_score = (
                metrics_weights['silhouette'] * silhouette +
                metrics_weights['calinski'] * calinski_norm +
                metrics_weights['davies'] * davies_norm
            )
            
            # Aplicar penalizaciones
            cluster_penalty_score = cluster_penalty * n_clusters / max_clusters
            outlier_penalty_score = outlier_penalty * outlier_fraction / max_outlier_fraction
            
            final_score = combined_score - cluster_penalty_score - outlier_penalty_score
            
            if verbose:
                print(f"Silhouette: {silhouette:.4f}, Calinski: {calinski_norm:.4f}, Davies: {davies_norm:.4f}")
                print(f"Combined Score: {combined_score:.4f}, Cluster Penalty: {cluster_penalty_score:.4f}, Outlier Penalty: {outlier_penalty_score:.4f}")
                print(f"Final Score: {final_score:.4f}")
            
            return final_score

        # Initial parameter estimation
        best_score = -np.inf
        best_initial_params = None
        for k in range(k_range[0], k_range[1] + 1):
            eps, min_samples = self.estimate_initial_params(data, k)
            dbscan = DBSCAN(eps=eps, min_samples=min_samples, n_jobs=n_jobs)
            
            labels = dbscan.fit_predict(data)
            n_clusters = len(np.unique(labels)) - (1 if -1 in labels else 0)
            outlier_fraction = np.sum(labels == -1) / len(labels)
            if n_clusters > 1:
                score = score_clustering(data, labels, n_clusters, outlier_fraction, cluster_penalty, outlier_penalty)
                if score > best_score:
                    best_score = score
                    best_initial_params = (eps, min_samples)

        if best_initial_params is None:
            print("Could not find a valid initial estimation.")
            return None

        # Refined grid search
        eps_init, min_samples_init = best_initial_params
        eps_range = (max(0.01, eps_init - eps_margin), eps_init + eps_margin)
        min_samples_range = (max(2, min_samples_init - min_samples_margin), min_samples_init + min_samples_margin)
        eps_values = np.linspace(eps_range[0], eps_range[1], 20)
        min_samples_values = range(min_samples_range[0], min_samples_range[1] + 1)

        best_score = -np.inf
        best_params = None
        total_iterations = len(eps_values) * len(min_samples_values)
        
        with tqdm(total=total_iterations, desc="Optimizing DBSCAN") as pbar:
            for eps in eps_values:
                for min_samples in min_samples_values:
                    dbscan = DBSCAN(eps=eps, min_samples=min_samples, n_jobs=n_jobs)
                    labels = dbscan.fit_predict(data)
                    n_clusters = len(np.unique(labels)) - (1 if -1 in labels else 0)
                    outlier_fraction = np.sum(labels == -1) / len(labels)
                    if n_clusters > 1:
                        score = score_clustering(data, labels, n_clusters, outlier_fraction, cluster_penalty, outlier_penalty)
                        if score > best_score:
                            best_score = score
                            best_params = (eps, min_samples)
                    pbar.update(1)

        if best_params:
            print(f"Best DBSCAN parameters: eps={best_params[0]:.2f}, min_samples={best_params[1]}")
        else:
            print("Could not find optimal parameters.")
        return best_params
  
    def determine_optimal_clusters(self, data, max_clusters=10):
        max_clusters = min(max_clusters, data.shape[0] // 2)
        inertias = []
        for k in tqdm(range(2, max_clusters + 1), desc="Determining optimal clusters"):
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(data)
            inertias.append(kmeans.inertia_)

        kneedle = KneeLocator(range(2, max_clusters + 1), inertias, curve='convex', direction='decreasing')
        optimal_cluster_count = kneedle.elbow if not kneedle.elbow is None else max_clusters

        return optimal_cluster_count

    def vssovou_method(self, data, k_min=2, k_max=10, weight=0.5, seed=42):
        np.random.seed(seed)
        vssovou_scores = []

        for k in tqdm(range(k_min, k_max + 1), desc="Applying VSSOVOU method"):
            kmeans = KMeans(n_clusters=k, random_state=seed)
            labels = kmeans.fit_predict(data)
            centroids = kmeans.cluster_centers_

            ssb = np.sum([np.sum((data[labels == i] - np.mean(data, axis=0))**2) for i in range(k)])
            ssw = np.sum([np.sum((data[labels == i] - centroids[i])**2) for i in range(k)])

            vssovou = weight * (1 - 1/k) * ssb + (1 - weight) * (1 - 1/k) * ssw
            vssovou_scores.append(vssovou)

        optimal_k = np.argmin(vssovou_scores) + k_min
        return optimal_k

    def apply_clustering(self, data, methods, metrics:bool=False):
        results = {}
        for name, method in tqdm(methods.items(), desc="Applying clustering methods"):
            if name in ['kmeans', 'minibatch-kmeans']:
                with joblib.parallel_backend('loky', n_jobs=-1):
                    labels = method.fit_predict(data)
            else:
                labels = method.fit_predict(data)
            results[name] = labels

            if len(np.unique(labels)) > 1 and metrics:
                silhouette = silhouette_score(data, labels)
                ch = calinski_harabasz_score(data, labels)
                db = davies_bouldin_score(data, labels)
                results[f"{name}_metrics"] = {
                    "silhouette": silhouette,
                    "calinski_harabasz": ch,
                    "davies_bouldin": db
                }

        return results

    def apply_dim_reduction(self, data):
        dim_reduction = {}
        for name, method in tqdm([("PCA", PCA(n_components=2)),
                                  ("t-SNE", TSNE(n_components=2, random_state=42)),
                                  ("UMAP", umap.UMAP(random_state=42))],
                                 desc="Applying dimensionality reduction"):
            dim_reduction[name] = method.fit_transform(data)
        return dim_reduction

    def verify_and_load_results(self, output_dir='./cluster_results', methods=None):
        """
        Verify if previous results exist and load them if they do.

        Args:
            output_dir (str): Directory where results are stored.
            methods (list): List of clustering methods to check.

        Returns:
            tuple: (bool, dict, dict) indicating if all results were loaded, 
                   and dictionaries of loaded clustering and dim reduction results.
        """
        if methods is None:
            methods = ['dbscan', 'kmeans', 'agglomerative', 'gmm', 'kmeans_vssovou']

        all_loaded = True
        loaded_results = {}
        loaded_dim_reduction = {}

        for method in tqdm(methods, desc="Verifying existing results"):
            filename = f'{output_dir}/{method}_labels.txt'

            if os.path.exists(filename):
                loaded_results[method] = np.loadtxt(filename, dtype=int)
            else:
                all_loaded = False
                break

        if all_loaded:
            for dim_method in ['PCA', 't-SNE', 'UMAP']:
                filename = f'{output_dir}/{dim_method}_reduction.npy'
                if os.path.exists(filename):
                    loaded_dim_reduction[dim_method] = np.load(filename)
                else:
                    all_loaded = False
                    break

        if all_loaded:
            print("All previous results loaded successfully.")
        else:
            print("Some results are missing. Will perform new analysis.")

        return all_loaded, loaded_results, loaded_dim_reduction

    def cluster_analysis(
        self,
        data: np.ndarray,
        output_dir: str = './cluster_results',
        methods: Optional[List[str]] = None,
        max_clusters: int = 10,
        use_cache: bool = True,
        params: Optional[Dict[str, Any]] = None,
        save:bool=True,
    ) -> Dict[str, Any]:
        """
        Perform cluster analysis on the given data using specified methods.

        This function applies various clustering algorithms to the input data,
        optimizes parameters if necessary, and saves the results.

        Args:
            data (np.ndarray): Input data for clustering.
            output_dir (str): Directory to save output results.
            methods (List[str], optional): List of clustering methods to apply.
            max_clusters (int): Maximum number of clusters to consider.
            use_cache (bool): Whether to use cached results if available.
            params (Dict[str, Any], optional): Pre-defined parameters for clustering methods.

        Returns:
            Dict[str, Any]: Results of the clustering analysis.

        """
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Attempt to load cached results if use_cache is True
        if use_cache:
            all_loaded, loaded_results, loaded_dim_reduction = self.verify_and_load_results(output_dir, methods)
            if all_loaded:
                self.results = loaded_results
                self.dim_reduction = loaded_dim_reduction
                return self.results

        # Preprocess and scale the data
        self.data = data
        self.data_scaled = self.preprocess_data(data)
        n_samples, n_features = self.data.shape
        print(f"Number of samples: {n_samples}")
        print(f"Number of features: {n_features}")

        # Set default methods if None
        methods = methods or ['dbscan', 'kmeans', 'minibatch-kmeans', 'agglomerative', 'gmm']

        # Initialize parameters
        params = params or {}

        # Determine necessary parameters for each method
        params = self._determine_method_parameters(methods, params, max_clusters)

        # Create clustering methods dictionary
        clustering_methods = self._create_clustering_methods(params)

        # Select only the methods present in 'methods'
        selected_methods = {name: method() for name, method in clustering_methods.items() if name in methods}

        # Apply clustering methods
        self.results = self.apply_clustering(self.data_scaled, selected_methods)

        # Save and plot results
        if save:
            asd
            # Apply dimensionality reduction
            self.dim_reduction = self.apply_dim_reduction(self.data_scaled)

            self.save_results(output_dir)
            self.plot_results(output_dir)

        return self.results

    def _determine_method_parameters(self, methods: List[str], params: Dict[str, Any], max_clusters: int) -> Dict[str, Any]:
        """
        Determine and set parameters for each clustering method.

        Args:
            methods (List[str]): List of clustering methods to apply.
            params (Dict[str, Any]): Pre-defined parameters for clustering methods.
            max_clusters (int): Maximum number of clusters to consider.

        Returns:
            Dict[str, Any]: Updated parameters dictionary.
        """
        if any(method in methods for method in ['kmeans', 'minibatch-kmeans', 'agglomerative', 'gmm']):
            params['optimal_k'] = params.get('optimal_k', self.determine_optimal_clusters(self.data_scaled, max_clusters))
            print(f"Optimal number of clusters: {params['optimal_k']}")

        if 'kmeans_vssovou' in methods:
            params['vssovou_k'] = params.get('vssovou_k', self.vssovou_method(self.data_scaled, k_max=max_clusters))
            print(f"Optimal number of clusters (VSSOVOU): {params['vssovou_k']}")

        if 'dbscan' in methods:
            if 'optimize' in params:
                params['eps'], params['min_samples'] = self.optimize_dbscan_params(self.data_scaled)
            elif 'estimate' in params and params['optimize_dbscan']:
                params['eps'], params['min_samples'] = self.estimate_initial_params(self.data_scaled, k=5)
            elif not all(param in params for param in ['eps', 'min_samples']):
                print(params)
                params['eps'], params['min_samples'] = params['eps'], params['min_samples']

            print(f"DBSCAN parameters: eps={params['eps']}, min_samples={params['min_samples']}")

        if 'hdbscan' in methods:
            params['min_cluster_size'] = params.get('min_cluster_size', 5)
            params['min_samples'] = params.get('min_samples', 5)
            print(f"HDBSCAN parameters: min_cluster_size={params['min_cluster_size']}, min_samples={params['min_samples']}")

        return params

    def _create_clustering_methods(self, params: Dict[str, Any]) -> Dict[str, callable]:
        """
        Create a dictionary of clustering method callables with their respective parameters.

        Args:
            params (Dict[str, Any]): Parameters for clustering methods.

        Returns:
            Dict[str, callable]: Dictionary of clustering method callables.
        """
        return {
            'dbscan': lambda: self.clustering_methods['dbscan'](eps=params['eps'], min_samples=params['min_samples']),
            'hdbscan': lambda: self.clustering_methods['hdbscan'](min_cluster_size=params['min_cluster_size'], min_samples=params['min_samples']),
            'kmeans': lambda: self.clustering_methods['kmeans'](n_clusters=params['optimal_k']),
            'gpu-kmeans': lambda: self.clustering_methods['gpu-kmeans'](),
            'minibatch-kmeans': lambda: self.clustering_methods['minibatch-kmeans'](n_clusters=params['optimal_k']),
            'agglomerative': lambda: self.clustering_methods['agglomerative'](n_clusters=params['optimal_k']),
            'gmm': lambda: self.clustering_methods['gmm'](n_components=params['optimal_k']),
            'kmeans_vssovou': lambda: self.clustering_methods['kmeans'](n_clusters=params['vssovou_k'])

        }

    def plot_results(self, output_dir='./cluster_results'):
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Plot clustering results
        for name, labels in self.results.items():
            if not name.endswith('_metrics'):
                plt.figure(figsize=(10, 8))
                scatter = plt.scatter(self.data_scaled[:, 0], self.data_scaled[:, 1], c=labels, cmap='viridis')
                plt.colorbar(scatter)
                plt.title(f'Clustering with {name}')
                plt.savefig(f'{output_dir}/{name}_clusters.png')
                plt.close()

        # Plot dimensionality reduction results
        for name, reduced_data in self.dim_reduction.items():
            plt.figure(figsize=(10, 8))
            for cluster_name, labels in self.results.items():
                if not cluster_name.endswith('_metrics'):
                    scatter = plt.scatter(reduced_data[:, 0], reduced_data[:, 1], c=labels, cmap='viridis', alpha=0.7)
            plt.colorbar(scatter)
            plt.title(f'Dimensionality Reduction with {name}\nColored by {cluster_name}')
            plt.savefig(f'{output_dir}/{name}_reduction.png')
            plt.close()

    def save_results(self, output_dir='./cluster_results'):
        for name, labels in self.results.items():
            if not name.endswith('_metrics'):
                np.savetxt(f'{output_dir}/{name}_labels.txt', labels, fmt='%d')

        for name, reduced_data in self.dim_reduction.items():
            np.save(f'{output_dir}/{name}_reduction.npy', reduced_data)

        metrics = {name: metrics for name, metrics in self.results.items() if name.endswith('_metrics')}
        with open(f'{output_dir}/clustering_metrics.txt', 'w') as f:
            for method, metric_dict in metrics.items():
                f.write(f"{method}:\n")
                for metric_name, metric_value in metric_dict.items():
                    f.write(f"  {metric_name}: {metric_value}\n")
                f.write("\n")

        print(f"All results have been saved in {output_dir}")

# Usage example:
# analyzer = ClusteringAnalysis()
# results = analyzer.cluster_analysis(data, use_cache=True)
# ============ Compress Compress ============ ============ Compress Compress =========== ============ Compress Compress ===========
class Compress:
    def __init__(self, unique_labels, output_dir='./compression_output'):
        """
        Initialize the Compress class.

        Args:
            unique_labels (list): List of unique labels (e.g., species) in the data.
            output_dir (str): Directory to save the compressed data.
        """
        self.unique_labels = unique_labels
        self.output_dir = output_dir
        self.compression_methods = {
            'umap': self._umap_compression,
            'pca': self._pca_compression,
            'tsne': self._tsne_compression,
            'factor_analysis': self._factor_analysis_compression
        }
        self.models = {}  # Dictionary to store compression models

    def compress(self, data, n_components=2, method='umap', **kwargs):
        """
        Compress the data using the specified method.

        Args:
            data (dict): Dictionary containing data for each label.
            method (str): Compression method to use ('umap', 'pca', or 'tsne').
            **kwargs: Additional arguments for the compression method.

        Returns:
            dict: Dictionary containing compressed data for each label.
        """
        if method not in self.compression_methods:
            raise ValueError(f"Unsupported compression method: {method}")

        compressed_data = {}
        self.models[method] = {}
        for label, label_data in data.items():
            n_components_label = n_components.get(label, 2)  # Default to 2 if not specified
            compressed_data[label], self.models[method][label] = self.compression_methods[method](
                label_data, n_components=n_components_label, **kwargs
            )

        return compressed_data

    def _umap_compression(self, data, n_components=2, n_neighbors=15, min_dist=0.1, random_state=None):
        data = np.array(data)
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(data)
        reducer = umap.UMAP(n_components=n_components, n_neighbors=n_neighbors,
                            min_dist=min_dist, random_state=random_state)
        compressed = reducer.fit_transform(data_scaled)
        return compressed, reducer

    def _pca_compression(self, data, n_components=2, random_state=None):
        data = np.array(data)
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(data)
        pca = PCA(n_components=n_components, random_state=random_state)
        compressed = pca.fit_transform(data_scaled)
        return compressed, pca

    def _tsne_compression(self, data, n_components=2, perplexity=30, random_state=None):
        data = np.array(data)
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(data)
        tsne = TSNE(n_components=n_components, perplexity=perplexity, random_state=random_state)
        compressed = tsne.fit_transform(data_scaled)
        return compressed, tsne

    def _factor_analysis_compression(self, data, n_components=2, random_state=None):
        data = np.array(data)
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(data)
        fa = FactorAnalysis(n_components=n_components, random_state=random_state)
        compressed = fa.fit_transform(data_scaled)
        return compressed, fa

    def save_compression(self, compression_dict, method):
        method_dir = os.path.join(self.output_dir, method)
        if not os.path.exists(method_dir):
            os.makedirs(method_dir)

        for label, compressed_data in compression_dict.items():
            filename = os.path.join(method_dir, f"{method}_compressed_{label}.npy")
            np.save(filename, compressed_data)
            print(f"{method.upper()} compressed data for {label} saved to {filename}")

    def save_compression(self, compression_dict, method):
        """
        Save the compression results for each label.

        Args:
            compression_dict (dict): Dictionary containing compressed data for each label.
            method (str): Compression method used.
        """
        method_dir = os.path.join(self.output_dir, method)
        if not os.path.exists(method_dir):
            os.makedirs(method_dir)

        for label, compressed_data in compression_dict.items():
            filename = os.path.join(method_dir, f"{method}_compressed_{label}.npy")
            np.save(filename, compressed_data)
            print(f"{method.upper()} compressed data for {label} saved to {filename}")

    def load_compression(self, method):
        """
        Load the compression results for each label if they exist.

        Args:
            method (str): Compression method to load.

        Returns:
            dict or None: Dictionary containing compressed data for each label if all files exist,
                          None if any file is missing.
        """
        method_dir = os.path.join(self.output_dir, method)
        compression_dict = {}

        for label in self.unique_labels:
            filename = os.path.join(method_dir, f"{method}_compressed_{label}.npy")
            if not os.path.exists(filename):
                print(f"Missing {method.upper()} compressed data for label {label}")
                return None

            compression_dict[label] = np.load(filename)

        print(f"All {method.upper()} compressed data files found and loaded successfully.")
        return compression_dict

    def verify_and_load_or_compress(self, data, n_components=2, method='umap', load=True, save=True, **kwargs):
        """
        Verify if compression results exist, load them if they do, or compress the data if they don't.

        Args:
            data (dict): Dictionary containing data for each label.
            method (str): Compression method to use ('umap', 'pca', or 'tsne').
            **kwargs: Additional arguments for the compression method.

        Returns:
            dict: Dictionary containing compressed data for each label.
        """
        compressed_data = self.load_compression(method)
        if compressed_data is not None and load:
            print(f"Loaded existing {method.upper()} compression data.")
            return compressed_data

        print(f"Some {method.upper()} compression files are missing. Recalculating...")
        compressed_data = self.compress(data, n_components, method, **kwargs)
        if save:self.save_compression(compressed_data, method)
        return compressed_data

    def determine_optimal_factors(self, data, max_factors=40, save=True):
        """
        Determine the optimal number of factors using the elbow method.
        
        Args:
            data (dict): Dictionary of input data for each label to perform Factor Analysis on.
            max_factors (int): Maximum number of factors to consider.
            save (bool): Whether to save the elbow curve plots.
        
        Returns:
            dict: Optimal number of factors for each label.
        """
        method_dir = os.path.join(self.output_dir, 'factor_analysis')
        if save and not os.path.exists(method_dir):
            os.makedirs(method_dir)
        
        optimal_factors = {}
        for label, label_data in data.items():
            scaler = StandardScaler()
            data_scaled = scaler.fit_transform(label_data)
            
            explained_variances = []
            for n in range(1, max_factors + 1):
                fa = FactorAnalysis(n_components=n, random_state=None)
                fa.fit(data_scaled)
                
                # Calculate explained variance
                if hasattr(fa, 'explained_variance_ratio_'):
                    explained_var = np.sum(fa.explained_variance_ratio_)
                else:
                    # If explained_variance_ratio_ is not available, calculate it manually
                    X_transformed = fa.transform(data_scaled)
                    total_var = np.var(data_scaled, axis=0).sum()
                    explained_var = np.var(X_transformed, axis=0).sum() / total_var
                
                explained_variances.append(explained_var)
            
            # Use KneeLocator to find the elbow point
            kneedle = KneeLocator(
                range(1, max_factors + 1), 
                explained_variances, 
                S=1.0, 
                curve='concave', 
                direction='increasing'
            )
            optimal_factors[label] = kneedle.elbow
        
            if optimal_factors[label] is None:
                print(f"Warning: Could not determine optimal number of factors for {label}. Using maximum.")
                optimal_factors[label] = max_factors
            
            if save:
                self._save_elbow_plot(label, max_factors, explained_variances, optimal_factors[label], method_dir)
        
        return optimal_factors

    def _save_elbow_plot(self, label, max_factors, explained_variances, optimal_factor, save_dir):
        """
        Save the elbow plot for a given label.
        
        Args:
            label (str): The label for which the plot is being saved.
            max_factors (int): Maximum number of factors considered.
            explained_variances (list): List of explained variances for each number of factors.
            optimal_factor (int): The optimal number of factors determined.
            save_dir (str): Directory to save the plot.
        """
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, max_factors + 1), explained_variances, 'bo-')
        plt.xlabel('Number of Factors')
        plt.ylabel('Cumulative Explained Variance Ratio')
        plt.title(f'Elbow Method for Optimal Number of Factors - {label}')
        plt.vlines(optimal_factor, plt.ylim()[0], plt.ylim()[1], linestyles='dashed', colors='r', 
                   label=f'Optimal Factors: {optimal_factor}')
        plt.legend()
        plt.tight_layout()
        
        filename = os.path.join(save_dir, f"FA_compressed_{label}_optimal_factors.png")
        plt.savefig(filename)
        plt.close()
        print(f"Elbow plot for {label} saved to {filename}")

    def plot_compression(self, compressed_data, method, output_file=None):
        """
        Plot the compressed data in 2D.

        Args:
            compressed_data (dict): Dictionary containing compressed data for each label.
            method (str): Compression method used ('umap', 'pca', 'tsne', or 'factor_analysis').
            output_file (str, optional): File path to save the plot. If None, the plot will be displayed.

        Returns:
            None
        """
        plt.figure(figsize=(12, 8))
        
        for label, data in compressed_data.items():
            plt.scatter(data[:, 0], data[:, 1], label=label, alpha=0.7)
        
        plt.title(f'2D Projection using {method.upper()}')
        plt.xlabel('Factor 1' if method == 'factor_analysis' else 'Dimension 1')
        plt.ylabel('Factor 2' if method == 'factor_analysis' else 'Dimension 2')
        plt.legend()
        
        if output_file:
            plt.savefig(output_file)
            print(f"Plot saved to {output_file}")
        else:
            plt.show()
        
        plt.close()

    def plot_pca_explained_variance(self, data, n_components=10, output_file=None):
        """
        Plot the explained variance ratio for PCA components.

        Args:
            data (numpy.ndarray): The input data to perform PCA on.
            n_components (int): Number of components to calculate.
            output_file (str, optional): File path to save the plot. If None, the plot will be displayed.

        Returns:
            None
        """
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(data)
        pca = PCA(n_components=n_components)
        pca.fit(data_scaled)

        plt.figure(figsize=(10, 6))
        plt.bar(range(1, n_components + 1), pca.explained_variance_ratio_)
        plt.xlabel('Principal Component')
        plt.ylabel('Explained Variance Ratio')
        plt.title('Explained Variance Ratio by Principal Component')
        plt.tight_layout()

        if output_file:
            plt.savefig(output_file)
            print(f"PCA explained variance plot saved to {output_file}")
        else:
            plt.show()

        plt.close()

    def plot_factor_analysis_results(self, data, optimal_factors, output_dir=None):
        """
        Generate multiple figures to interpret Factor Analysis results.

        This function creates separate plots for different aspects of factor analysis,
        including factor loadings, explained variance, factor correlations, and feature importance.

        Args:
            data (dict): Dictionary containing data for each label.
            optimal_factors (dict): Dictionary containing optimal number of factors for each label.
            output_dir (str): Directory to save the output plots.

        Returns:
            None
        """
        output_dir = os.path.join(self.output_dir, 'factor_analysis')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if 'factor_analysis' not in self.models:
            raise ValueError("No Factor Analysis models found. Please run compression with 'factor_analysis' method first.")

        for label, label_data in data.items():
            if label not in self.models['factor_analysis']:
                print(f"No Factor Analysis model found for label: {label}. Skipping.")
                continue

            n_factors = optimal_factors.get(label)
            if n_factors is None:
                print(f"No optimal factor count found for label: {label}. Skipping.")
                continue

            model = self.models['factor_analysis'][label]
            compressed_data = model.transform(label_data)

            # 1. Factor Loadings Heatmap
            plt.figure(figsize=(12, 8))
            loadings = model.components_.T[:, :n_factors]
            im1 = plt.imshow(loadings, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
            plt.title(f'Factor Loadings Heatmap - {label}')
            plt.xlabel('Factors')
            plt.ylabel('Features')
            plt.xticks(range(n_factors), [f'F{i+1}' for i in range(n_factors)])
            plt.yticks(range(loadings.shape[0]), [f'Feature {i+1}' for i in range(loadings.shape[0])])
            plt.colorbar(im1)

            # Add text annotations
            #for i in range(loadings.shape[0]):
            #    for j in range(n_factors):
            #        plt.text(j, i, f'{loadings[i, j]:.2f}', ha='center', va='center', color='black')

            # Save the plot
            plt.savefig(os.path.join(output_dir, f"{label}_factor_loadings_heatmap.png"), dpi=300, bbox_inches='tight')
            plt.close()  # Close the plot to free up memory

            # 2. Explained Variance Plot
            plt.figure(figsize=(10, 6))
            explained_variance = np.sum(loadings**2, axis=0)
            explained_variance_ratio = explained_variance / np.sum(explained_variance)
            plt.bar(range(1, n_factors + 1), explained_variance_ratio)
            plt.title(f'Explained Variance Ratio - {label}')
            plt.xlabel('Factors')
            plt.ylabel('Explained Variance Ratio')
            plt.savefig(os.path.join(output_dir, f"{label}_explained_variance_ratio.png"), dpi=300, bbox_inches='tight')
            plt.close()

            # 3. Cumulative Explained Variance Plot
            plt.figure(figsize=(10, 6))
            cumulative_variance_ratio = np.cumsum(explained_variance_ratio)
            plt.plot(range(1, n_factors + 1), cumulative_variance_ratio, 'bo-')
            plt.title(f'Cumulative Explained Variance Ratio - {label}')
            plt.xlabel('Number of Factors')
            plt.ylabel('Cumulative Explained Variance Ratio')
            plt.axhline(y=0.8, color='r', linestyle='--', label='80% Threshold')
            plt.legend()
            plt.savefig(os.path.join(output_dir, f"{label}_cumulative_explained_variance.png"), dpi=300, bbox_inches='tight')
            plt.close()

            # 4. Correlation between factors
            plt.figure(figsize=(10, 8))
            factor_corr = spearmanr(compressed_data[:, :n_factors]).correlation
            im2 = plt.imshow(factor_corr, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
            plt.title(f'Factor Correlation Heatmap - {label}')
            plt.xlabel('Factors')
            plt.ylabel('Factors')
            plt.xticks(range(n_factors), [f'F{i+1}' for i in range(n_factors)])
            plt.yticks(range(n_factors), [f'F{i+1}' for i in range(n_factors)])
            plt.colorbar(im2)

            # Add text annotations
            #for i in range(n_factors):
            #    for j in range(n_factors):
            #        plt.text(j, i, f'{factor_corr[i, j]:.2f}', ha='center', va='center', color='black')

            plt.savefig(os.path.join(output_dir, f"{label}_factor_correlation_heatmap.png"), dpi=300, bbox_inches='tight')
            plt.close()

            # 5. Scatter plot of the two most important factors
            plt.figure(figsize=(10, 8))
            plt.scatter(compressed_data[:, 0], compressed_data[:, 1])
            plt.title(f'Scatter Plot of Two Most Important Factors - {label}')
            plt.xlabel('Factor 1')
            plt.ylabel('Factor 2')
            plt.savefig(os.path.join(output_dir, f"{label}_top_factors_scatter.png"), dpi=300, bbox_inches='tight')
            plt.close()

            # 6. Top features for each factor
            plt.figure(figsize=(12, 8))
            top_features = []
            for i in range(n_factors):
                factor_loadings = loadings[:, i]
                top_indices = np.argsort(np.abs(factor_loadings))[-5:]  # Top 5 features
                top_features.append([f"Feature {idx+1}" for idx in top_indices[::-1]])
            
            table_data = [[f"Factor {i+1}"] + top_features[i] for i in range(n_factors)]
            table = plt.table(cellText=table_data, loc='center', cellLoc='center', colLabels=['Factor', 'Top 1', 'Top 2', 'Top 3', 'Top 4', 'Top 5'])
            table.auto_set_font_size(False)
            table.set_fontsize(8)
            table.scale(1, 1.5)
            plt.axis('off')
            plt.title(f'Top 5 Features for Each Factor - {label}')
            plt.savefig(os.path.join(output_dir, f"{label}_top_features_table.png"), dpi=300, bbox_inches='tight')
            plt.close()

            print(f"Factor Analysis results plots for {label} saved to {output_dir}")

    def plot_umap_neighbor_graph(self, data, n_neighbors=15, min_dist=0.1, output_file=None):
        """
        Plot the UMAP neighbor graph.

        Args:
            data (numpy.ndarray): The input data to perform UMAP on.
            n_neighbors (int): Number of neighbors to consider for each point.
            min_dist (float): The minimum distance between points in the low-dimensional representation.
            output_file (str, optional): File path to save the plot. If None, the plot will be displayed.

        Returns:
            None
        """
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(data)
        reducer = umap.UMAP(n_neighbors=n_neighbors, min_dist=min_dist, random_state=None)
        embedding = reducer.fit_transform(data_scaled)

        plt.figure(figsize=(12, 10))
        plt.scatter(embedding[:, 0], embedding[:, 1], c=reducer.labels_, cmap='Spectral', s=5)
        plt.colorbar(boundaries=np.arange(11)-0.5).set_ticks(np.arange(10))
        plt.title('UMAP Projection with Neighbor Connectivity')
        plt.tight_layout()

        if output_file:
            plt.savefig(output_file)
            print(f"UMAP neighbor graph plot saved to {output_file}")
        else:
            plt.show()

        plt.close()
