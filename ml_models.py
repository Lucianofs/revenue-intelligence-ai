from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

def modelo_churn(df):
    df['churn'] = (df['reservas'] < 50).astype(int)

    X = df[['cliques','custo','valor']]
    y = df['churn']

    X_train, X_test, y_train, y_test = train_test_split(X, y)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    df['churn_pred'] = model.predict(X)
    return df

def previsao_receita(df):
    df['t'] = range(len(df))

    X = df[['t']]
    y = df['valor']

    model = RandomForestRegressor()
    model.fit(X, y)

    df['forecast'] = model.predict(X)
    return df
