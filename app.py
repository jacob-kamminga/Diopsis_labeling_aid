from collections import defaultdict
from flask import Flask, render_template, request, url_for
import pandas as pd
import random



# Original paths to the classification labels and images
classification_labels_path = 'diopsis_public_classification/classification_labels.csv'
images_path = 'diopsis_public_classification/images'

# Create app instance
app = Flask(__name__, static_folder=images_path, static_url_path='/images')

# Load and prepare data
name_to_ancestors_df = pd.read_csv('name_to_ancestors2.csv')
classification_labels_df = pd.read_csv(classification_labels_path)


# Build the taxonomic tree as shown previously
def build_tree(df):
    tree = defaultdict(list)
    for index, row in df.iterrows():
        name = row['name']
        ancestors = eval(row['ancestors'])
        if len(ancestors) > 1:
            parent = ancestors[1]
            tree[parent].append(name)
    return tree

taxonomic_tree = build_tree(name_to_ancestors_df)

def get_description(taxon):
    try:
        return name_to_ancestors_df[name_to_ancestors_df['name'] == taxon]["Description"].item()
    except:
        return ""

@app.route('/')
def main_page():
    # Display top-level taxa
    taxon_name = "Animalia"
    top_level_taxa = taxonomic_tree[taxon_name]  # Assuming 'Animalia' is the root if not change accordingly
    children_descriptions = {child: get_description(child) for child in top_level_taxa}
    current_description = get_description(taxon_name)
    return render_template('main_page.html', taxon_name = taxon_name, children_descriptions=children_descriptions, current_description=current_description)


@app.route('/taxon/<taxon_name>') # TODO figure out where to add description as part of the list of children and bread crumb
def taxon_page(taxon_name):
    # Display children of the current taxon
    children = taxonomic_tree.get(taxon_name, [])
    # Fetch images associated with this taxon
    images = classification_labels_df[classification_labels_df['deepest_name'] == taxon_name].head(100)
    # Randomly sample up to 100 images from those available
    sample_size = min(100, len(images))  # Adjust sample size if less than 100 images are available
    sampled_images = images.sample(n=sample_size)  # Randomly sample images , random_state=42
    image_files = [f"{image}.jpg" if not image.endswith('.jpg') else image for image in sampled_images['basename'].tolist()]

    # Generate breadcrumbs (assuming 'name_to_ancestors.csv' gives direct lineage to each taxon)
    ancestors = eval(name_to_ancestors_df.loc[name_to_ancestors_df['name'] == taxon_name, 'ancestors'].values[0])
    breadcrumbs = [{'name': anc, 'url': url_for('taxon_page', taxon_name=anc)} for anc in ancestors[::-1]]

    # Get the description of the current taxon
    current_description = get_description(taxon_name)

    # Get descriptions for children
    children_descriptions = {child: get_description(child) for child in children}

    return render_template('taxon_page.html', taxon_name=taxon_name, current_description=current_description, children_descriptions=children_descriptions, images=image_files,
                           breadcrumbs=breadcrumbs)

if __name__ == '__main__':
    app.run(debug=True)
