# Diopsis Annotation Aid 
## Taxonomic Tree Visualization

This Flask-based web application provides an interactive visualization of a taxonomic tree, allowing users to explore different taxonomic classes and view images associated with each taxon. Each taxon is linked to a dedicated page that displays its child taxonomic classes and a sample of images, enhancing both educational and research-oriented functionalities.

## Features

- Hierarchical display of taxonomic classes.
- Dedicated pages for each taxon with links to their child classes.
- Displays a sample of up to 100 images for each taxon, randomly selected.
- Breadcrumb navigation for easy tracing of the taxonomic path.

## Installation
To set up this project locally, follow these steps:

### Dataset
Download the data for this project here: https://drive.google.com/file/d/1-CeDtEaAeljRU-NTVnJ3N6peQVJJz3gi/view?usp=drive_link
Unzip and add the folder "diopsis_public_classification" and it's contents in the main folder of this project.

To properly cite the dataset use: https://zenodo.org/records/10853097

### Prerequisites

- Python 3.6+
- pip

### Setup Environment

```bash
# Clone the repository
git clone gh repo clone jacob-kamminga/Diopsis_labeling_aid
cd Diopsis_labeling_aid

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

