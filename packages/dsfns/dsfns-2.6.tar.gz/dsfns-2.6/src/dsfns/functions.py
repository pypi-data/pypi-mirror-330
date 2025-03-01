import pandas as pd
import numpy as np
from feature_engine.outliers import Winsorizer
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, LabelEncoder
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant
from sklearn import metrics

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from sklearn.base import BaseEstimator, TransformerMixin

from sklearn.pipeline import Pipeline
from imblearn.pipeline import Pipeline as ImbPipeline  # For imbalanced learning resampling
from sklearn.metrics import classification_report


# Version History
'''
    1.1  - Outlier handling - IQR method / Winsorizer / Clip
    1.2  - Missing value imputation - Simple Imputer / Mean, Median, Mode / Numerical data with mean and obj/cat with mode
    1.3  - Outlier Counter, Columns with Outlier and high frequency column finder (single value repeating over 50%)
    1.4  - Data Encoding (label, onehot) and Scaling (MinMax, Standard, Robust)
    1.5  - Fixed general code issues
    1.6  - Redundant Codes removed
    1.7  - Fixed general code issues / issues with return statement
    1.8  - Fixed general code issues / issues with df.sample()
    1.9  - Added Outlier replacement (using Mean, Median or Mode) and Low Variance columns (cols with IQR = 0)
    1.10 - Missing value Interpolation (use with Time series data, Continuous variables with trends etc)
    2.0  - Visualize data with Single and Multiple Line plots
    2.1  - Visualize data with Multiple Regression plots and VIF (Variance Inflation Factor)
    2.2  - Compare model accuracy of multiple models
    2.3  - Added function that outputs various metrics for model evaluation
    2.4  - Added a function that creates a reusable transformer from a custom function
    2.6  - Function added that can train, evaluate, and print results for any classifier, optionally using resampling.

'''



def Outlier_IQR(df,columns,whis=1.5):
    for i in columns:
        IQR = df[i].quantile(0.75) - df[i].quantile(0.25)
        UL = df[i].quantile(0.75) + (whis * IQR)
        LL = df[i].quantile(0.25) - (whis * IQR)

        df[i] = np.where(df[i] > UL, UL, np.where(df[i] < LL , LL, df[i]))
    return df



def Outlier_Winsorizer(df, column, capping_method='iqr', fold=1.5):
    winsor = Winsorizer(capping_method=capping_method,
                        tail='both',
                        fold=fold,
                        variables=[column])
    
    df[column] = winsor.fit_transform(df[[column]])
    return df



def Outlier_Clip(df,columns, perc=0.05):
    up = 1 - perc
    lw = 0 + perc
    for column in columns:
        df[column] = df[column].clip(lower=df[column].quantile(lw), upper=df[column].quantile(up))
    return df



def MissingVal_Repl(df, columns, type='mean'):
    for i in columns:
        if type == 'mean':
            value = df[i].mean()
        elif type == 'median':
            value = df[i].median()
        elif type == 'mode':
            value = df[i].mode()[0]  
        
        df[i] = df[i].replace(np.nan, value)
    return df



def MissingVal_Imputer(df,columns,strategy='mean'):
    if strategy == 'mode':
        strategy = 'most_frequent'

    imputer = SimpleImputer(missing_values=np.nan, strategy=strategy)
    for i in columns:
        df[i] = pd.DataFrame(imputer.fit_transform(df[[i]]))
    return df
    


def MissingVal_Fillna(df):
    num_cols = df.select_dtypes(include=['float', 'int']).columns
    for x in num_cols:
        df[x] = df[x].fillna(df[x].mean())

    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    for y in cat_cols:
        df[y] = df[y].fillna(df[y].mode()[0])
    return df



def outlierColumns(df, whis=1.5):
    outl_cols = []
    for i in df.columns:
        if pd.api.types.is_numeric_dtype(df[i]):
            IQR = df[i].quantile(0.75) - df[i].quantile(0.25)
            LLi = df[i].quantile(0.25) - (whis * IQR)
            ULi = df[i].quantile(0.75) + (whis * IQR)
            
            if ((df[i] < LLi) | (df[i] > ULi)).sum() > 0:
                outl_cols.append(i)
    return outl_cols



def outlierCount(df, columns):
    plt.ioff()
    for i in columns:
        oc = len(plt.boxplot(df[i])['fliers'][0].get_ydata())
        print(f"{i} = {oc}")



def highFrequency(df, perc=0.5):
    high_freq_columns = []
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            value_counts = df[col].value_counts()
            max_count = value_counts.max()
            total_count = len(df)
            
            if max_count / total_count > perc:
                high_freq_columns.append(col)
    return high_freq_columns



def Encoding(df,method='label'):
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    if method == 'label':
        label = LabelEncoder()
        for col in cat_cols:
            df[col] = label.fit_transform(df[col])
    elif method == 'onehot':
        df = pd.get_dummies(df, columns=cat_cols)
    return df



def Scaling(df, method='minmax'):
    if method == 'standard':
        scaler = StandardScaler()
    elif method == 'minmax':
        scaler = MinMaxScaler()
    elif method == 'robust':
        scaler = RobustScaler()
        
    df = pd.DataFrame(scaler.fit_transform(df),columns=df.columns)
    return df
    


def Outlier_MMM(df, columns, type='median'):
    for i in columns:
        IQR = df[i].quantile(0.75) - df[i].quantile(0.25)
        UL = df[i].quantile(0.75) + (1.5 * IQR)
        LL = df[i].quantile(0.25) - (1.5 * IQR)

        if type == 'mean':
            value = df[i].mean()
        elif type == 'median':
            value = df[i].median()
        elif type == 'mode':
            value = df[i].mode()[0]

        if df[i].dtype in ['int32', 'int64']:
            value = int(value)    
        
        df.loc[df[i] > UL, i] = value
        df.loc[df[i] < LL, i] = value

    return df



def LowVarianceCols(df):
    LowVar = []
    columns = df.describe(include = ['int','float']).columns
    for i in columns:
        IQR = df[i].quantile(0.75) - df[i].quantile(0.25)
        if IQR == 0:
            LowVar.append(i)
         
    return LowVar



def MissingVal_Interpolate(df,type='linear'):
    num_cols = df.select_dtypes(include=['float', 'int']).columns
    for i in num_cols:
        if type == 'linear':
            df[i] = df[i].interpolate(method='linear')
        elif type == 'polynomial':
            df[i] = df[i].interpolate(method='polynomial', order=2)
        elif type == 'spline':
            df[i] = df[i].interpolate(method='spline', order=3)
    return df


def Lineplot_Multi(df, inpCol, outCol, figsize=(15, 5)):

    n_plots = len(inpCol)
    n_rows = int(np.ceil(n_plots / 3))
    plt.figure(figsize=(figsize[0], figsize[1] * n_rows))
    
    for i, col in enumerate(inpCol, 1): 
        plt.subplot(n_rows, 3, i)  
        sns.lineplot(data=df, x=col, y=outCol)
        plt.title(col)  
        plt.xlabel(col)  
        plt.ylabel(outCol) 
        plt.grid(True)
    
    plt.tight_layout()
    plt.show()



def Lineplot_Single(df, inpCol, outCol):
    plt.figure(figsize=(10,9))
    
    for col in inpCol:
        sns.lineplot(data=df, x=col, y=outCol, label=col)
    
    plt.title(f"{outCol} vs Input Columns")
    plt.xlabel("Input Columns")
    plt.ylabel(outCol)
    plt.legend(title="Input Columns")
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()



def RegressionPlot_Multiple(df, inpCol, outCol, figsize=(15, 5)):
   
    n_plots = len(inpCol)
    n_rows = int(np.ceil(n_plots / 3))
    plt.figure(figsize=(figsize[0], figsize[1] * n_rows))
    
    for i, col in enumerate(inpCol, 1):
        plt.subplot(n_rows, 3, i) 
        sns.regplot(data=df, x=col, y=outCol, ci=None,line_kws={'color':'red'})    
        plt.title(f'Regression: {col} vs {outCol}')
        plt.xlabel(col)  
        plt.ylabel(outCol)  
        plt.grid(True)
    
    plt.tight_layout()
    plt.show()



def VIF(X):
    X = add_constant(X)
    vif_df = pd.DataFrame()
    vif_df["Variable"] = X.columns[1:]

    vif_values = []
    for i in range(1,X.shape[1]):
        vif = variance_inflation_factor(X.values, i)
        vif_values.append(vif)

    vif_df["VIF"] = vif_values
    return vif_df    



def CompareAccuracy(models, x_train, x_test, y_train, y_test):
    AccScore = []

    for name, model in models.items():
        
        model.fit(x_train, y_train)

        #TEST ACC
        testPreds = model.predict(x_test)
        teAcc = metrics.accuracy_score(y_test, testPreds)

        #TRAIN ACC
        trainPreds = model.predict(x_train)
        trAcc = metrics.accuracy_score(y_train, trainPreds)

        AccScore.append({
            "Model": name,
            "TestAcc":teAcc,
            "TrainAcc": trAcc
        })

    return pd.DataFrame(AccScore)   



def Metrics_Clf(y_train, y_pred_train, y_test, y_pred_test):
    # For training set
    train_accuracy = accuracy_score(y_train, y_pred_train)
    train_precision = precision_score(y_train, y_pred_train)
    train_recall = recall_score(y_train, y_pred_train)
    train_f1 = f1_score(y_train, y_pred_train)
    train_roc_auc = roc_auc_score(y_train, y_pred_train)

    # For testing set
    test_accuracy = accuracy_score(y_test, y_pred_test)
    test_precision = precision_score(y_test, y_pred_test)
    test_recall = recall_score(y_test, y_pred_test)
    test_f1 = f1_score(y_test, y_pred_test)
    test_roc_auc = roc_auc_score(y_test, y_pred_test)
    
    # Combine the results into a dictionary
    ClMetrics = {
        "Metric": ["accuracy", "precision", "recall", "f1", "roc_auc"],
        "Train_Values": [train_accuracy, train_precision, train_recall, train_f1, train_roc_auc],
        "Test_Values": [test_accuracy, test_precision, test_recall, test_f1, test_roc_auc]
    }
    
    return pd.DataFrame(ClMetrics)



def Metrics_Reg(y_train, y_pred_train, y_test, y_pred_test):
    # For training set
    train_mae = mean_absolute_error(y_train, y_pred_train)
    train_mse = mean_squared_error(y_train, y_pred_train)
    train_rmse = (train_mse)**0.5
    train_r2 = r2_score(y_train, y_pred_train)

    # For testing set
    test_mae = mean_absolute_error(y_test, y_pred_test)
    test_mse = mean_squared_error(y_test, y_pred_test)
    test_rmse = (test_mse)**0.5
    test_r2 = r2_score(y_test, y_pred_test)
    
    # Combine the results into a dictionary
    ReMetrics = {
        "Metric": ["MAE", "MSE", "RMSE", "R²"],
        "Train_Values": [train_mae, train_mse, train_rmse, train_r2],
        "Test_Values": [test_mae, test_mse, test_rmse, test_r2]
    }

    return pd.DataFrame(ReMetrics)



def RowTransformer(custom_transform_fn):
    class CustomTransformer(BaseEstimator, TransformerMixin):
        def fit(self, X, y=None):
            return self 
        
        def transform(self, X):
            return custom_transform_fn(X) 

    return CustomTransformer()



def TrainEvaluate_Classifier(model, x_train, y_train, x_test, y_test, preprocessor=None, resampler=None):
        
    if resampler:
        pipeline = ImbPipeline([
            ('preprocessor', preprocessor),  # Preprocessing step (if provided)
            ('resampler', resampler),        # Resampling step (if provided)
            ('classifier', model)            # The classifier
        ])
    else:
        pipeline = Pipeline([
            ('preprocessor', preprocessor),  
            ('classifier', model)            
        ])
    
    pipeline.fit(x_train, y_train)
    
    # Predict on the test set
    y_pred = pipeline.predict(x_test)
    
    # Print the results
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    print("ROC-AUC Score:", round(roc_auc_score(y_test, y_pred), 2))
    
    return pipeline
