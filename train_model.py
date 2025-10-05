import lightgbm as lgb
import joblib
from sklearn.metrics import mean_squared_error
import pandas as pd
from preprocess import build_features

def train_and_save(airnow_df,weather_df,tempo_df=None):
    X_train,X_test,y_train,y_test,merged=build_features(airnow_df,weather_df,tempo_df)
    dtrain=lgb.Dataset(X_train,y_train)
    params={"objective":"regression","metric":"rmse","verbosity":-1}
    model=lgb.train(params,dtrain,num_boost_round=200)
    preds=model.predict(X_test)
    rmse=mean_squared_error(y_test,preds,squared=False)
    joblib.dump(model,"model.pkl")
    return rmse

if __name__=="__main__":
    print("train stub")
