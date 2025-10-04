from flask import Flask, render_template, request, jsonify
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import numpy as np
import os

app = Flask(__name__)

class ChestXrayAnalyzer:
    def __init__(self):
        self.data = None
        self.transactions = None
        self.frequent_itemsets = None
        self.rules = None
    
    def load_data(self, file_path):
        """Load and preprocess chest X-ray data"""
        try:
            self.data = pd.read_csv(file_path)
            # Process the Finding Labels column to create transactions
            self.data['Finding Labels'] = self.data['Finding Labels'].fillna('No Finding')
            
            # Split multiple findings and create transaction format
            transactions = []
            for findings in self.data['Finding Labels']:
                if findings != 'No Finding':
                    # Split by '|' and clean up
                    items = [item.strip() for item in findings.split('|')]
                    transactions.append(items)
                else:
                    transactions.append(['No Finding'])
            
            self.transactions = transactions
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def find_frequent_itemsets(self, min_support=0.01):
        """Apply Apriori algorithm to find frequent itemsets"""
        if not self.transactions:
            return None
        
        # Convert to binary matrix format
        te = TransactionEncoder()
        te_ary = te.fit(self.transactions).transform(self.transactions)
        df = pd.DataFrame(te_ary, columns=te.columns_)
        
        # Apply Apriori algorithm
        self.frequent_itemsets = apriori(df, min_support=min_support, use_colnames=True)
        return self.frequent_itemsets
    
    def generate_association_rules(self, metric='confidence', min_threshold=0.5):
        """Generate association rules from frequent itemsets"""
        if self.frequent_itemsets is None or len(self.frequent_itemsets) == 0:
            return None
        
        try:
            self.rules = association_rules(
                self.frequent_itemsets, 
                metric=metric, 
                min_threshold=min_threshold
            )
            return self.rules
        except Exception as e:
            print(f"Error generating rules: {e}")
            return None

# Initialize analyzer
analyzer = ChestXrayAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'})
    
    if file and file.filename.endswith('.csv'):
        file_path = os.path.join('uploads', file.filename)
        os.makedirs('uploads', exist_ok=True)
        file.save(file_path)
        
        if analyzer.load_data(file_path):
            return jsonify({'success': 'File uploaded and processed successfully'})
        else:
            return jsonify({'error': 'Error processing file'})
    
    return jsonify({'error': 'Invalid file format'})

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    min_support = float(data.get('support', 0.01))
    metric = data.get('metric', 'confidence')
    min_threshold = float(data.get('threshold', 0.5))
    
    # Find frequent itemsets
    frequent_itemsets = analyzer.find_frequent_itemsets(min_support)
    if frequent_itemsets is None or len(frequent_itemsets) == 0:
        return jsonify({'error': 'No frequent itemsets found with given support'})
    
    # Generate association rules
    rules = analyzer.generate_association_rules(metric, min_threshold)
    
    # Prepare results
    itemsets_result = []
    for _, row in frequent_itemsets.iterrows():
        itemsets_result.append({
            'itemsets': list(row['itemsets']),
            'support': round(row['support'], 4)
        })
    
    rules_result = []
    if rules is not None and len(rules) > 0:
        for _, row in rules.iterrows():
            rules_result.append({
                'antecedents': list(row['antecedents']),
                'consequents': list(row['consequents']),
                'support': round(row['support'], 4),
                'confidence': round(row['confidence'], 4),
                'lift': round(row['lift'], 4)
            })
    
    return jsonify({
        'frequent_itemsets': itemsets_result,
        'association_rules': rules_result,
        'total_transactions': len(analyzer.transactions) if analyzer.transactions else 0
    })

@app.route('/stats')
def get_stats():
    if analyzer.data is None:
        return jsonify({'error': 'No data loaded'})
    
    # Get basic statistics
    total_images = len(analyzer.data)
    unique_findings = set()
    
    for findings in analyzer.data['Finding Labels']:
        if findings != 'No Finding' and pd.notna(findings):
            items = [item.strip() for item in findings.split('|')]
            unique_findings.update(items)
    
    return jsonify({
        'total_images': total_images,
        'unique_findings': len(unique_findings),
        'findings_list': sorted(list(unique_findings))
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)