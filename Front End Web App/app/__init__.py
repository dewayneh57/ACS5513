from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages

# Store results in memory (for demo; not persistent)
results = []

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', results=results)

@app.route('/calculate', methods=['POST'])
def calculate():
    # Server-side validation
    overall_qual = request.form.get('overall_qual')
    if not overall_qual:
        flash('Please select an Overall Quality rating.', 'error')
        return redirect(url_for('home'))
    
    # Validate and convert numeric fields, ensuring no negative values
    try:
        # Year validation (must be reasonable year range)
        year_built = int(request.form.get('year_built') or 0)
        if year_built < 1800 or year_built > 2025:
            flash('Year Built must be between 1800 and 2025.', 'error')
            return redirect(url_for('home'))
        
        year_remod_add = request.form.get('year_remod_add')
        if year_remod_add:
            year_remod_add = int(year_remod_add)
            if year_remod_add < 1800 or year_remod_add > 2025:
                flash('Year Remodeled must be between 1800 and 2025.', 'error')
                return redirect(url_for('home'))
        
        # Square footage validation (must be non-negative)
        first_flr_sf = float(request.form.get('first_flr_sf') or 0)
        second_flr_sf = float(request.form.get('second_flr_sf') or 0)
        third_flr_sf = float(request.form.get('third_flr_sf') or 0)
        bsmt_living_sf = float(request.form.get('bsmt_living_sf') or 0)
        total_ground_sf = float(request.form.get('total_ground_sf') or 0)
        
        # Check for negative square footage values
        if any(val < 0 for val in [first_flr_sf, second_flr_sf, third_flr_sf, bsmt_living_sf, total_ground_sf]):
            flash('Square footage values cannot be negative.', 'error')
            return redirect(url_for('home'))
        
        # Bathroom validation (must be non-negative)
        half_baths = int(request.form.get('half_baths') or 0)
        full_baths = int(request.form.get('full_baths') or 0)
        if half_baths < 0 or full_baths < 0:
            flash('Number of bathrooms cannot be negative.', 'error')
            return redirect(url_for('home'))
        
        # Garage validation (must be non-negative)
        garage_size = float(request.form.get('garage_size') or 0)
        if garage_size < 0:
            flash('Garage size cannot be negative.', 'error')
            return redirect(url_for('home'))
        
    except (ValueError, TypeError):
        flash('Please enter valid numeric values for all fields.', 'error')
        return redirect(url_for('home'))
    
    total_sq_ft = first_flr_sf + second_flr_sf + third_flr_sf + bsmt_living_sf
    
    if total_sq_ft <= 0:
        flash('Please enter at least one square footage value. The total living area must be greater than 0.', 'error')
        return redirect(url_for('home'))
    
    # Collect all form inputs
    model_type = request.form.get('model_type', 'catboost')  # Default to catboost
    
    data = {
        'model_type': model_type,
        'overall_qual': overall_qual,
        'year_built': request.form.get('year_built'),
        'year_remod_add': request.form.get('year_remod_add'),
        'first_flr_sf': request.form.get('first_flr_sf'),
        'second_flr_sf': request.form.get('second_flr_sf'),
        'third_flr_sf': request.form.get('third_flr_sf'),
        'bsmt_living_sf': request.form.get('bsmt_living_sf'),
        'total_ground_sf': request.form.get('total_ground_sf'),
        'half_baths': request.form.get('half_baths'),
        'full_baths': request.form.get('full_baths'),
        'garage_cars': request.form.get('garage_cars'),
        'garage_finish': request.form.get('garage_finish', '0'),  # Default to 0 (No Garage)
        'garage_size': request.form.get('garage_size'),
        'kitchen_qual': request.form.get('kitchen_qual'),
        'exterior_qual': request.form.get('exterior_qual'),
        'heating_qual': request.form.get('heating_qual'),
        'basement_qual': request.form.get('basement_qual'),
        'fireplace_qual': request.form.get('fireplace_qual'),
    }
    # Placeholder for calculation result (replace with your model/prediction)
    # You can now use the model_type to determine which model to use
    data['result'] = f'TBD ({model_type.upper()})'
    results.append(data)
    flash(f'Calculation completed successfully using {model_type.upper()} model!', 'success')
    return redirect(url_for('home'))
