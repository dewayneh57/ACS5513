# Project Charter

## Business Background

The process of home valuation is complex and multi-faceted, so much so that there are entire research firms dedicated to providing market intelligence to real estate companies, developers, and to end-users via Zillow and Redfin. **A Home Valuing Company Inc. **is a residential property valuation intelligence firm that provides data and analytics to appraisers and real-estate agents via proprietary APIs and custom-built SaaS web applications maintained by the client. The firm also provides an in-house, subscription-based web portal for homeowners to understand real estate comps based on home characteristics, as well as keep track of their home’s value over time.

## Business Problem

Underwriters use rule-of-thumb comparable and simplistic regression tools that miss nonlinear interactions between a house and its characteristics, such as neighborhoods, age, and structural components. This can create valuation errors that cost lenders & customers thousands of dollars in losses.

## Business Goal

Reduce appraisal error for residential properties by 10% to save lenders and homeowners money.

## Scope

An end-to-end ML service that ingests the Ames, IA housing CSV (~2,900 rows) from a version-controlled source and logs ingestion metadata to a notebook. Raw data is cleaned by dropping high-missing columns and taming unusually large or small values, so they don’t skew the results. We then crate 4 new measures: house age, years since last remodel, total living area and a “quality” size score and put every number on the same scale so the model can learn effectively.

Next, we split the homes into a “teach” group and “check” group. The model learns patterns from the teach group, like how square footage and overall quality relate to the price and then we confirm its accuracy on the check group, tracking how close its guesses are to real sale price.

Finally, a simple web form lets users enter home details and instantly get a price estimate. Each query is recorded in a table where you can copy any row, tweak one feature and see side-by-side of a “what-if” comparisons. All requests are logged so we can monitor its performance.

## Personnel

- Project Lead – Sean Miller
- PM – Farhan Hassan
- Data scientist(s) - Dewayne Hafenstein, Sean Miller
- Account Manager – Farhan Hassan
- Data Administrator – Sean Miller
- Business contact – Dewayne Hafenstein

## Metrics

- Predict the selling price within +/- 2% of its actual selling price 90% of the time.
- Improve the prediction of sale prices to maximize revenue for sellers and listing agents.
- The current national list-to-sale ratio is about 97% but varies by locality. In tight markets, this ratio exceeds 100% with sale prices exceeding the list price. This tool will account for these ratio differences and provide an estimate of what the actual selling price would be. The current list-to-sell pricing in Ames Iowa (2025) shows that 71.4% of the properties sell below their listing price (Zillow). The discounted rate appears to be about –1.9% on average in Ames Iowa.
- The data set will be split into training and test data. The training data will be used to create and train the initial model, and the test data will be used to verify the model's accuracy.

## Plan

**Phase 1**: Establish the problem, set our Goal(s) to accomplish, explore the data set, perform correlation analysis among the features to determine which features to focus on, and determine the target architecture.

**Phase 2**: Determine the exact model to use. At the time of Phase 1 we suspect it will be Logistic Regression or multiple linear regression. Data analysis will determine the actual algorithm used.

**Phase 3: **Operationalize a limited API and connect to a proof-of-concept web application.

## Architecture

We build on the Ames; IA housing dataset downloaded either directly via Kaggle or pulled from the Git repo and load it straight into memory with no external data movement tools. The entire solution is written in Python and deployed as two isolated Flask applications: one hosts the machine learning engine and model artifacts, and the other serves the user-facing web interface. By splitting these responsibilities, we give the model its own dedicated runtime (maximizing memory and compute for retraining or batch analysis) while shielding its complexity behind a clean RESTful API.

On the front end, an HTML/CSS/JavaScript form captures the 11 property features and submits them as JSON to the /predict end point. The backend service validates, and preprocesses inputs, runs the trained model and returns a price estimate. Each requests original inputs and predicted value are then logged to a results table in the browser.

## Communication

- The team stays in communication via Microsoft Teams, as well as virtual zoom meetings to ensure deliverables are equally distributed and progress is made across all fronts.
