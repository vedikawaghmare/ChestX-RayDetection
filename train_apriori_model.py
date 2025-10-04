import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import pickle
import os

class ChestXrayAprioriTrainer:
    def __init__(self):
        self.frequent_itemsets = None
        self.rules = None
        self.feature_rules = None
        
    def load_chest_xray_data(self, csv_path):
        """Load NIH Chest X-ray dataset"""
        print("Loading chest X-ray dataset...")
        df = pd.read_csv(csv_path)
        
        # Clean and process the data
        df['Finding Labels'] = df['Finding Labels'].fillna('No Finding')
        
        # Create transactions from findings
        transactions = []
        for findings in df['Finding Labels']:
            if findings != 'No Finding':
                # Split multiple findings
                items = [item.strip() for item in findings.split('|')]
                transactions.append(items)
            else:
                transactions.append(['No Finding'])
        
        print(f"Processed {len(transactions)} patient records")
        return transactions
    
    def create_synthetic_training_data(self):
        """Create comprehensive synthetic training data if CSV not available"""
        print("Creating synthetic training dataset...")
        
        # Realistic chest X-ray findings combinations based on medical literature
        training_data = []
        
        # Generate realistic patient combinations
        conditions = {
            'Pneumonia': ['Consolidation', 'Pleural_Effusion', 'Infiltration'],
            'Cardiomegaly': ['Edema', 'Pleural_Effusion', 'Atelectasis'],
            'Atelectasis': ['Pneumonia', 'Pleural_Effusion'],
            'Mass': ['Nodule', 'Atelectasis'],
            'Nodule': ['Mass', 'Fibrosis'],
            'Pneumothorax': ['Atelectasis'],
            'Consolidation': ['Pneumonia', 'Infiltration'],
            'Infiltration': ['Pneumonia', 'Edema'],
            'Effusion': ['Cardiomegaly', 'Pneumonia', 'Edema'],
            'Emphysema': ['Fibrosis', 'Atelectasis'],
            'Fibrosis': ['Emphysema', 'Pleural_Thickening'],
            'Pleural_Thickening': ['Fibrosis', 'Effusion']
        }
        
        # Generate 5000 synthetic patient records
        for _ in range(5000):
            # Random primary condition
            primary = np.random.choice(list(conditions.keys()))
            patient_conditions = [primary]
            
            # Add associated conditions based on medical patterns
            if primary in conditions:
                # 70% chance of having associated conditions
                if np.random.random() < 0.7:
                    num_additional = np.random.randint(1, 3)
                    additional = np.random.choice(
                        conditions[primary], 
                        size=min(num_additional, len(conditions[primary])), 
                        replace=False
                    )
                    patient_conditions.extend(additional)
            
            # 30% chance of having completely random additional condition
            if np.random.random() < 0.3:
                random_condition = np.random.choice(list(conditions.keys()))
                if random_condition not in patient_conditions:
                    patient_conditions.append(random_condition)
            
            training_data.append(patient_conditions)
        
        # Add some "No Finding" cases
        for _ in range(1000):
            training_data.append(['No Finding'])
        
        print(f"Generated {len(training_data)} synthetic patient records")
        return training_data
    
    def train_apriori_model(self, transactions, min_support=0.01):
        """Train Apriori model on chest X-ray data"""
        print("Training Apriori model...")
        
        # Convert to binary matrix
        te = TransactionEncoder()
        te_ary = te.fit(transactions).transform(transactions)
        df = pd.DataFrame(te_ary, columns=te.columns_)
        
        # Find frequent itemsets
        self.frequent_itemsets = apriori(df, min_support=min_support, use_colnames=True)
        print(f"Found {len(self.frequent_itemsets)} frequent itemsets")
        
        # Generate association rules
        if len(self.frequent_itemsets) > 0:
            self.rules = association_rules(
                self.frequent_itemsets, 
                metric="confidence", 
                min_threshold=0.3
            )
            print(f"Generated {len(self.rules)} association rules")
        
        return self.frequent_itemsets, self.rules
    
    def create_feature_based_rules(self, transactions):
        """Create rules linking image features to conditions"""
        print("Creating feature-based rules...")
        
        # Simulate feature-condition relationships
        feature_conditions = []
        
        for transaction in transactions:
            # Simulate image features for each transaction
            features = {}
            
            if 'Pneumonia' in transaction or 'Consolidation' in transaction:
                features['low_brightness'] = True
                features['high_contrast'] = True
            
            if 'Cardiomegaly' in transaction:
                features['high_edge_density'] = True
                features['low_symmetry'] = True
            
            if 'Mass' in transaction or 'Nodule' in transaction:
                features['very_high_contrast'] = True
                features['medium_brightness'] = True
            
            if 'Pneumothorax' in transaction:
                features['very_high_edge_density'] = True
                features['high_brightness'] = True
            
            if 'No Finding' in transaction:
                features['normal_brightness'] = True
                features['normal_contrast'] = True
            
            # Create feature-condition pairs
            for feature, present in features.items():
                if present:
                    feature_conditions.append(transaction + [feature])
        
        # Train Apriori on feature-condition data
        te = TransactionEncoder()
        te_ary = te.fit(feature_conditions).transform(feature_conditions)
        df = pd.DataFrame(te_ary, columns=te.columns_)
        
        feature_itemsets = apriori(df, min_support=0.05, use_colnames=True)
        
        if len(feature_itemsets) > 0:
            self.feature_rules = association_rules(
                feature_itemsets, 
                metric="confidence", 
                min_threshold=0.4
            )
            print(f"Generated {len(self.feature_rules)} feature-based rules")
        
        return self.feature_rules
    
    def save_model(self, model_path='chest_xray_apriori_model.pkl'):
        """Save trained model"""
        model_data = {
            'frequent_itemsets': self.frequent_itemsets,
            'rules': self.rules,
            'feature_rules': self.feature_rules
        }
        
        with open(model_path, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"Model saved to {model_path}")
    
    def load_model(self, model_path='chest_xray_apriori_model.pkl'):
        """Load trained model"""
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            self.frequent_itemsets = model_data['frequent_itemsets']
            self.rules = model_data['rules']
            self.feature_rules = model_data['feature_rules']
            
            print(f"Model loaded from {model_path}")
            return True
        return False

def main():
    trainer = ChestXrayAprioriTrainer()
    
    # Try to load real data first, fallback to synthetic
    csv_path = 'Data_Entry_2017.csv'
    
    if os.path.exists(csv_path):
        print("Using real NIH Chest X-ray dataset")
        transactions = trainer.load_chest_xray_data(csv_path)
    else:
        print("Real dataset not found, using synthetic data")
        transactions = trainer.create_synthetic_training_data()
    
    # Train the model
    frequent_itemsets, rules = trainer.train_apriori_model(transactions)
    
    # Create feature-based rules
    feature_rules = trainer.create_feature_based_rules(transactions)
    
    # Save the trained model
    trainer.save_model()
    
    # Print some statistics
    print("\n=== TRAINING COMPLETE ===")
    print(f"Frequent Itemsets: {len(frequent_itemsets)}")
    print(f"Association Rules: {len(rules)}")
    print(f"Feature Rules: {len(feature_rules) if feature_rules is not None else 0}")
    
    # Show top rules
    if rules is not None and len(rules) > 0:
        print("\nTop 5 Association Rules:")
        top_rules = rules.nlargest(5, 'confidence')
        for _, rule in top_rules.iterrows():
            antecedents = list(rule['antecedents'])
            consequents = list(rule['consequents'])
            print(f"{antecedents} → {consequents} (confidence: {rule['confidence']:.3f})")

if __name__ == "__main__":
    main()