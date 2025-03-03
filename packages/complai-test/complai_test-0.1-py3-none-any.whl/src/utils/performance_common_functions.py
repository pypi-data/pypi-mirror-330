from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score, roc_auc_score

def model_performance_report(y_val, y_pred_lab, performance_metric):
    '''
    Show Model Performance Report
    Args:
        model (sklearn model): Pretrained Model
        x_val (pandas dataframe): Validation Dataset
        y_val (numpy array): True Labels
        y_pred_lab (numpy array): Predicted Labels
    Returns:
        Displays Streamit Metric Row consisting of All Model performance metric
    '''
    pr = precision_score(y_val, y_pred_lab, average='weighted')
    rc = recall_score(y_val, y_pred_lab, average='weighted')
    ac = accuracy_score(y_val, y_pred_lab)
    f1 = f1_score(y_val, y_pred_lab, average='weighted')
    # roc = roc_auc_score(y_val, model.predict_proba(x_val)[:,1])
    d = {}
    d['Accuracy'] = ac
    d['Misclass Rate'] = 1 - ac
    d['F1 Score'] = f1
    d['Precision'] = pr
    d['Recall'] = rc
    d["performance_score"] = d[performance_metric]

    return d