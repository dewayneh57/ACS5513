# Stacking Model

_A model detailing the experiment using a Stacking ensemble regressor, one of several models evaluated._

## Analytic Approach

- Target variable: **SalePrice** (the sale price of homes)
- Inputs:
  - Features (X): A set of engineered raw predictors (living area, basement area, overall quality, age/remodel features, various quality x size interactions, garage attributes, bath counts, encoded categorical variables).
  - Label (y): Continuous sale price values

## Model Description

A Stacking Regressor is an ensemble that learns to combine the predictions of three base learners (Random Forest, XGBoost, Elastic‑NetCV) via a second‑level meta‑learner (Elastic‑NetCV), with passthrough of original features.

**RandomForestRegressor (sklearn):**

- Key Hyper-parameters:
  - n_estimators=400 for the number of boosted trees
  - random_state=42, the seed for Random Forest internal random number generator. Fixing this ensures you get identical results each time you train.
  - n_jobs=-1, setting this to use all available cores in the CPU threads, speeding up training.

**XGBRegressor (xgboost):**

- Key Hyper-parameters:
  - n_estimators=400
  - learning_rate=0.05 which scales each trees contribution before adding it into the ensemble

**Elastic-NetCV (sklearn) via pipeline:**

- Key Hyper-parameters:

  - alphas=10⁻³–10²
  - l1_ratio= [0.1,0.5,.9]

- (Imputation & Scaling):

  - cv=5
  - max_iter=50000

- (Meta-Learner):

  - default alphas
  - cv=5
  - max_iter=50000

- Passthrough=True
- cv=5
- n_jobs=-1

**Data Flow:**

- Train/Test Split into 80% train and 20% test (random_state=42)
- Preprocessing:
  - Imputation: Mean imputation for missing values on all pipelines
  - Standard scaling only for Elastic-Net pipelines
- Base Learner Training: Each base model fits on the full training set
- 5-fold CV to generate “level one” features from base learners.
- Meta-learner training: Receives base-learner predictions plus the original features.
- The Meta-Learner training outputs the stacked prediction on the test set.

## Results (Model Performance)

**Model Performance Comparison Table Across All 9 Evaluated Models**

| Model             | RMSE        | R²       |
| ----------------- | ----------- | -------- |
| Stacking          | 20141.86235 | 0.872104 |
| CatBoost          | 20223.46376 | 0.871065 |
| XGBoost           | 20591.84538 | 0.866325 |
| Random Forest     | 20632.43312 | 0.865798 |
| LightGBM          | 20820.81834 | 0.863336 |
| HistGBR           | 20854.05774 | 0.862899 |
| Elastic-NetCV     | 20924.66392 | 0.861969 |
| Linear Regression | 21017.19852 | 0.860746 |
| Ridge             | 21047.27663 | 0.860347 |

## Model Understanding

The stacking ensemble delivers a test `RMSE` of approximately $20,141 and an `R²` of 0.872 which is marginally better than the next‑best base learner, CatBoost (RMSE ≈ $20,223, R² ≈ 0.871). While this might look like a small absolute gain (ΔRMSE ≈ $100–200, ΔR² ≈ 0.001), stacking’s strength lies in its ability to learn optimal, data‑driven combination of predictors, thereby reducing bias and variance.

By combining multiple models whose errors aren’t perfectly correlated, stacking reduces the overall “spread” of predictions. If one model overreacts to noise in the data, the others can pull the ensemble prediction back toward the truth. The meta‑learner automatically down‑weights any base model whose predictions tend to fluctuate wildly.

Each base learner (Random Forest, XGBoost, Elastic‑Net) has its own systematic tendencies, one might under-predict expensive homes; another might over-predict lower‑end properties. The stacking meta‑learner sees these patterns in their out‑of‑fold predictions and learns to compensate, effectively ironing out biases that any single model retains.

The final estimator is a regularized linear model. It enforces sparsity and shrinks extreme weights, preventing the stack from leaning too heavily on any one component. This keeps the ensemble from overfitting the training sets quirks while still capturing the predominant signals.

## Conclusion and Discussions for Next Steps

The Stacking Regressor demonstrated impressive performance for predicting home sale prices, marginally outperforming strong gradient‑boosted and forest‑based models. Its ability to learn blends of disparate algorithms makes it a robust choice for deployment if computation cost and complexity are acceptable. Continuous monitoring, feature updates, and periodic retraining will ensure sustained accuracy in production.

To further boost performance, it might be possible to engineer additional features from the existing dataset, but we are clearly in the territory of diminishing returns. Interaction terms that combine categorical groups (like house style × neighborhood), ratio features (such as living area per bedroom), and temporal deltas (for instance, the time elapsed since the last sale). Beyond our current variables, incorporating external data sources—public real‑estate indices, local demographic or school‑district performance metrics, and regional economic indicators (like employment rates and median income)—could add valuable context and drive even more accurate price predictions.
