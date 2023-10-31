import pandas as pd

# Create a sorted and filtered csv file
dataStream = pd.read_csv('output/output3.csv', index_col="landmark")

leftKneeDataStream = dataStream.loc['LEFT_KNEE']
leftKneeDataStream.to_csv('./data/leftKneeData.csv')

rightKneeDataStream = dataStream.loc['RIGHT_KNEE']
rightKneeDataStream.to_csv('./data/rightKneeData.csv')

leftHipDataStream = dataStream.loc['LEFT_HIP']
leftHipDataStream.to_csv('./data/leftHipData.csv')

rightHipDataStream = dataStream.loc['RIGHT_HIP']
rightHipDataStream.to_csv('./data/rightHipData.csv')

