# Demographic Fairness
This is for a research project to determine whether gender bias exists in Tweets related to computer science education, which affects fairness.

## Setup

1. Install [Anaconda](https://www.anaconda.com/products/individual).

2. Create and activate an environment:

   ```
   conda create -n <env name> python=3.10
   conda activate <env name>
   ```

3. Clone the repository and install the requirements:

   ```
   git clone https://github.com/butakow/demographic-fairness
   cd demographic-fairness
   pip install -r requirements.txt
   ```
   
4. Download the model:

   ```
   python download.py
   ```

5. Predict gender framework class probabilities:

   ```
   python predict.py
   ```

6. Analyze:

   ```
   python fairnessanalysis.py
   ```
