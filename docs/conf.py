import os
import sys
sys.path.insert(0, os.path.abspath('../src'))

project = 'Dynamic Factor-Tilted Portfolio with Macro Stress Testing'
author = 'Aben Carrington'
release = '1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.mathjax'  # Add support for math equations
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Enable raw HTML in RST files for Plotly integration
html_js_files = [
    'https://cdn.plot.ly/plotly-latest.min.js',
]

# Add custom CSS
html_css_files = [
    'custom.css',
]

# Configure the theme
html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
    'sticky_navigation': True,
    'titles_only': False
}

# Auto-generate API documentation
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'

# Tell Sphinx to copy Plotly HTML files to static directory
html_extra_path = []

def setup(app):
    """
    Setup function for sphinx documentation
    """
    # Create custom.css file if it doesn't exist
    css_dir = os.path.join(os.path.dirname(__file__), '_static')
    os.makedirs(css_dir, exist_ok=True)
    css_path = os.path.join(css_dir, 'custom.css')
    
    if not os.path.exists(css_path):
        with open(css_path, 'w') as f:
            f.write("""
/* Custom CSS for documentation */
.plotly-graph-div {
    margin-bottom: 2em;
    margin-top: 1em;
}

/* Improve chart responsiveness */
.plotly-graph-div.js-plotly-plot {
    width: 100% !important;
}

/* Add a border to charts */
iframe {
    border: 1px solid #ddd;
    border-radius: 5px;
}
""")