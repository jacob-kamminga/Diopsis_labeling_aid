from collections import defaultdict
from flask import Flask, render_template, request
import pandas as pd
import random

app = Flask(__name__, static_folder='diopsis_public_classification/images', static_url_path='/images')


# Load and prepare data
name_to_ancestors_df = pd.read_csv('diopsis_public_classification/name_to_ancestors.csv')
classification_labels_df = pd.read_csv('diopsis_public_classification/classification_labels.csv')


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


@app.route('/')
def main_page():
    # Display top-level taxa
    top_level_taxa = taxonomic_tree['Animalia']  # Assuming 'Animalia' is the root if not change accordingly
    return render_template('main_page.html', taxa=top_level_taxa)


@app.route('/taxon/<taxon_name>')
def taxon_page(taxon_name):
    # Display children of the current taxon
    children = taxonomic_tree.get(taxon_name, [])
    # Fetch images associated with this taxon
    images = classification_labels_df[classification_labels_df['deepest_name'] == taxon_name].head(100)
    image_files = [f"{image}.jpg" if not image.endswith('.jpg') else image for image in images['basename'].tolist()]
    return render_template('taxon_page.html', taxon_name=taxon_name, children=children, images=image_files)

if __name__ == '__main__':
    app.run(debug=True)
