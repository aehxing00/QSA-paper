import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
import warnings

warnings.filterwarnings('ignore')

# ==================== HYPERPARAMETER SETTINGS ====================
MIN_CORRELATION_TO_PLOT = 0.95         # Only plot connections with |r| > this value
NODE_RADIUS_SCALE = 0.5              # Node circle radius scaling factor
CIRCLE_RADIUS = 4                    # Layout circle radius
DIMENSION_LABEL_SIZE = 18            # Font size for dimension labels inside circles
MIN_SATURATION = 0.6                 # Minimum color saturation (light red)
MAX_SATURATION = 0.99                # Maximum color saturation (dark red)
BASE_LINE_WIDTH = 6.0                # Base line width
# ================================================================

print(f"Hyperparameter Settings:")
print(f"  Only plot connections with |r| > {MIN_CORRELATION_TO_PLOT}")
print(f"  Dimension label font size: {DIMENSION_LABEL_SIZE}")
print(f"  Color saturation range: {MIN_SATURATION} (light) to {MAX_SATURATION} (dark)")
print(f"  Base line width: {BASE_LINE_WIDTH}")

# 1. Read data
file_path = 'a1_alllll.xlsx'
df = pd.read_excel(file_path)

print("\nProcessing data...")
print(f"Total number of questions: {len(df)}")
print(f"Number of models: {len(df.columns) - 1}")

# 2. Parse question IDs to get major and minor category information
def parse_question_id(q_id):
    """Parse question ID, return (major_category, minor_category)"""
    if isinstance(q_id, str):
        major_category = q_id[0]
        minor_category = q_id[1]
        return major_category, minor_category
    return None, None

# Add category columns
df['Major_Category'] = df['Question_ID'].apply(lambda x: parse_question_id(x)[0])
df['Minor_Category'] = df['Question_ID'].apply(lambda x: parse_question_id(x)[1])

# 3. Group questions into 15 dimensions (5 major categories × 3 minor categories)
model_columns = [col for col in df.columns if col not in ['Question_ID', 'Major_Category', 'Minor_Category']]

# Assumed dimension order: 1A, 1B, 1C, 2A, 2B, 2C, 3A, 3B, 3C, 4A, 4B, 4C, 5A, 5B, 5C
expected_dimensions = []
for major in ['1', '2', '3', '4', '5']:
    for minor in ['A', 'B', 'C']:
        expected_dimensions.append(f"{major}{minor}")

dimensions = []
dimension_names = []

for dim_name in expected_dimensions:
    major, minor = dim_name[0], dim_name[1]
    mask = (df['Major_Category'] == major) & (df['Minor_Category'] == minor)
    dimension_questions = df[mask]
    
    if len(dimension_questions) > 0:
        dimension_names.append(dim_name)
        # Calculate average score for all questions in this dimension
        dimension_scores = [dimension_questions[model].mean() for model in model_columns]
        dimensions.append(dimension_scores)

print(f"\nTotal dimensions created: {len(dimensions)}")

# 4. Calculate correlation matrix
dimension_array = np.array(dimensions)
n_dimensions = len(dimensions)

# Calculate Spearman correlation coefficients
spearman_corr = np.ones((n_dimensions, n_dimensions))
for i in range(n_dimensions):
    for j in range(i+1, n_dimensions):
        corr, _ = spearmanr(dimension_array[i], dimension_array[j])
        spearman_corr[i, j] = corr
        spearman_corr[j, i] = corr

# 5. Prepare all correlation data
all_correlations = []
for i in range(n_dimensions):
    for j in range(i+1, n_dimensions):
        corr = spearman_corr[i, j]
        if abs(corr) > MIN_CORRELATION_TO_PLOT:
            all_correlations.append({
                'dim1': dimension_names[i],
                'dim2': dimension_names[j],
                'correlation': corr,
                'abs_correlation': abs(corr)
            })

print(f"  Total {len(all_correlations)} connections satisfy |r| > {MIN_CORRELATION_TO_PLOT}")

# 6. Create figure (adjust size, remove margins)
plt.figure(figsize=(16, 16), facecolor='white')

# Calculate positions of 15 points on the circle
angles = np.linspace(0, 2 * np.pi, n_dimensions, endpoint=False)
pos = {}
for i, (dim, angle) in enumerate(zip(dimension_names, angles)):
    x = CIRCLE_RADIUS * np.cos(angle)
    y = CIRCLE_RADIUS * np.sin(angle)
    pos[dim] = (x, y)

# Set colors for each major category (by first number)
major_colors = {
    '1': '#FF6B6B',  # Red - Major category 1
    '2': '#4ECDC4',  # Cyan - Major category 2
    '3': '#45B7D1',  # Blue - Major category 3
    '4': '#96CEB4',  # Green - Major category 4
    '5': '#FFEAA7',  # Yellow - Major category 5
}

def get_edge_color_saturation(corr_value, min_sat=MIN_SATURATION, max_sat=MAX_SATURATION):
    """
    Return red-based color based on correlation coefficient, with saturation indicating correlation strength
    
    Parameters:
    corr_value: Correlation coefficient value (0.95-1.0)
    min_sat: Minimum color saturation (0-1)
    max_sat: Maximum color saturation (0-1)
    
    Returns:
    RGBA color tuple
    """
    # Ensure correlation coefficient is within valid range
    abs_corr = abs(corr_value)
    
    # Map correlation coefficient to saturation range
    # Due to MIN_CORRELATION_TO_PLOT constraint, abs_corr should be between 0.95-1.0
    # We linearly map this range to min_sat-max_sat
    if abs_corr < MIN_CORRELATION_TO_PLOT:
        abs_corr = MIN_CORRELATION_TO_PLOT
    
    # Normalize to 0-1 range (relative to MIN_CORRELATION_TO_PLOT to 1.0)
    normalized = (abs_corr - MIN_CORRELATION_TO_PLOT) / (1.0 - MIN_CORRELATION_TO_PLOT)
    
    # Calculate saturation
    saturation = min_sat + normalized * (max_sat - min_sat)
    saturation = max(min_sat, min(max_sat, saturation))  # Ensure within range
    
    # Create red-based color, higher saturation means darker color
    # RGB format: red channel fixed high, green/blue channels vary with saturation
    red = 0.8  # Base red
    green_blue = 1.0 - saturation  # Higher saturation means lower green/blue components
    
    # Ensure green/blue components are not negative
    green_blue = max(0.0, min(1.0, green_blue))
    
    # Transparency also varies with saturation
    alpha = 0.5 + saturation * 0.3  # 0.5-0.8 transparency range
    
    return (red, green_blue, green_blue, alpha)

# 7. Draw connections (sorted by correlation strength, weak first, strong last)
if all_correlations:
    # Sort by absolute correlation
    all_correlations_sorted = sorted(all_correlations, key=lambda x: x['abs_correlation'])
    
    for corr_data in all_correlations_sorted:
        dim1, dim2, corr = corr_data['dim1'], corr_data['dim2'], corr_data['correlation']
        
        x1, y1 = pos[dim1]
        x2, y2 = pos[dim2]
        
        # Use color saturation to indicate correlation strength
        line_color = get_edge_color_saturation(corr)
        
        # Draw line (fixed width, color indicates strength)
        plt.plot([x1, x2], [y1, y2], 
                color=line_color,
                linewidth=BASE_LINE_WIDTH,
                solid_capstyle='round')

# 8. Draw node circles (colored by major category)
node_radius = NODE_RADIUS_SCALE * 1.2
for i, dim in enumerate(dimension_names):
    x, y = pos[dim]
    major = dim[0]  # Get major category number
    color = major_colors.get(major, '#888888')  # Get color by major category
    
    # Draw circle
    circle = plt.Circle((x, y), node_radius, 
                       facecolor=color, 
                       edgecolor='black',
                       linewidth=1.5,
                       alpha=0.9)
    plt.gca().add_patch(circle)
    
    # Display dimension name at circle center (using hyperparameter-controlled font size)
    plt.text(x, y, dim, 
             fontsize=DIMENSION_LABEL_SIZE, 
             fontweight='bold',
             ha='center', 
             va='center',
             color='black')

# 9. Set figure properties
plt.axis('equal')
plt.xlim(-CIRCLE_RADIUS*1.15, CIRCLE_RADIUS*1.15)
plt.ylim(-CIRCLE_RADIUS*1.15, CIRCLE_RADIUS*1.15)
plt.axis('off')

# Remove all margins
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

# 10. Display connection details in console
if all_correlations:
    # Sort by absolute correlation for display
    sorted_correlations = sorted(all_correlations, key=lambda x: x['abs_correlation'], reverse=True)
    print(f"\nConnection details (sorted by correlation strength):")
    print("-" * 70)
    print(f"Color saturation range: {MIN_SATURATION:.2f} (light) to {MAX_SATURATION:.2f} (dark)")
    print("-" * 70)
    
    for i, corr_data in enumerate(sorted_correlations[:15], 1):  # Show only top 15 strongest
        sign = "+" if corr_data['correlation'] > 0 else ""
        abs_corr = corr_data['abs_correlation']
        
        # Calculate corresponding color saturation
        if abs_corr < MIN_CORRELATION_TO_PLOT:
            norm_corr = MIN_CORRELATION_TO_PLOT
        else:
            norm_corr = abs_corr
            
        normalized = (norm_corr - MIN_CORRELATION_TO_PLOT) / (1.0 - MIN_CORRELATION_TO_PLOT)
        saturation = MIN_SATURATION + normalized * (MAX_SATURATION - MIN_SATURATION)
        saturation = max(MIN_SATURATION, min(MAX_SATURATION, saturation))
        
        # Determine strength category for display
        if saturation > (MIN_SATURATION + MAX_SATURATION) * 0.75:
            strength_desc = "Very Strong"
        elif saturation > (MIN_SATURATION + MAX_SATURATION) * 0.5:
            strength_desc = "Strong"
        elif saturation > (MIN_SATURATION + MAX_SATURATION) * 0.25:
            strength_desc = "Moderate"
        else:
            strength_desc = "Weak"
        
        print(f"{i:2d}. {corr_data['dim1']} ↔ {corr_data['dim2']}: "
              f"r = {sign}{corr_data['correlation']:.3f} "
              f"({strength_desc})")

plt.show()