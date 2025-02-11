from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn.model_selection import train_test_split
import pandas as pd
import os
from datetime import datetime

class ModelEvaluation:
    def __init__(self, model, data, target_column, test_size=0.2, random_state=42):
        """
        Initializes the ModelEvaluation class.

        Parameters:
            model: The machine learning model to evaluate.
            data: The dataset to use for evaluation (DataFrame).
            target_column: The name of the target column in the dataset.
            test_size: Proportion of the data to use for testing.
            random_state: Random seed for reproducibility.
        """
        self.model = model
        self.data = data
        self.target_column = target_column
        self.test_size = test_size
        self.random_state = random_state

        # Split the data into training and testing sets
        self.X = self.data.drop(columns=[self.target_column])
        self.y = self.data[self.target_column]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=self.test_size, random_state=self.random_state)

    def fit(self):
        """
        Fits the model to the training data.
        """
        self.model.fit(self.X_train, self.y_train)

    def evaluate(self):
        """
        Evaluates the model on the test data using various metrics.

        Returns:
            dict: A dictionary containing evaluation metrics.
        """
        # Make predictions
        y_pred = self.model.predict(self.X_test)

        # Calculate metrics
        accuracy = accuracy_score(self.y_test, y_pred)
        precision = precision_score(self.y_test, y_pred, average='binary')  # assuming binary classification
        recall = recall_score(self.y_test, y_pred, average='binary')
        f1 = f1_score(self.y_test, y_pred, average='binary')

        # Generate classification report
        report = classification_report(self.y_test, y_pred)

        # Create a summary of metrics
        evaluation_metrics = {
            'Accuracy': accuracy,
            'Precision': precision,
            'Recall': recall,
            'F1 Score': f1,
            'Classification Report': report
        }

        return evaluation_metrics

    def save_report(self, output_folder="evaluation_reports"):
        """
        Saves the evaluation report to a file with a dynamic name.

        Parameters:
            output_folder (str): Folder to save the report.
        """
        metrics = self.evaluate()
        
        # Generate a dynamic file name using model name and timestamp
        model_name = type(self.model).__name__
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{model_name}_evaluation_{timestamp}.txt"
        output_path = os.path.join(output_folder, filename)

        # Ensure the output folder exists
        os.makedirs(output_folder, exist_ok=True)

        # Write the evaluation metrics to the file
        with open(output_path, 'w') as f:
            f.write(f"Evaluation Report for {model_name} Model\n")
            f.write(f"Timestamp: {timestamp}\n\n")
            f.write(f"Accuracy: {metrics['Accuracy']:.4f}\n")
            f.write(f"Precision: {metrics['Precision']:.4f}\n")
            f.write(f"Recall: {metrics['Recall']:.4f}\n")
            f.write(f"F1 Score: {metrics['F1 Score']:.4f}\n")
            f.write("\nClassification Report:\n")
            f.write(metrics['Classification Report'])

        print(f"Evaluation report saved to {output_path}")

# Example Usage:
if __name__ == "__main__":
    # Sample dataset for classification (you can replace this with your dataset)
    from sklearn.datasets import load_breast_cancer
    data = load_breast_cancer()
    df = pd.DataFrame(data=data.data, columns=data.feature_names)
    df['target'] = data.target

    # Example model (Random Forest Classifier)
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier()

    # Create the evaluation object
    evaluator = ModelEvaluation(model, df, target_column='target')

    # Fit the model
    evaluator.fit()

    # Save the evaluation report
    evaluator.save_report()
