import os
import pandas as pd
import warnings
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
warnings.simplefilter("ignore")
def tachcamp(str):
    arr = str.split("_")
    max=arr[0]
    for i in range(0,len(arr)):
        if len(arr[i])>len(max):
            max=arr[i]
    return max
def SKU(str):
    result = str.replace('_Nga', '')
    result = result.replace('_Thuy', '')
    result = result.replace('_Thuan', '')
    result = result.replace('_Thienco', '')
    result = result.replace('_Hieu', '')
    arr=result.split("_")
    return arr[len(arr)-2]
def UTM(input_string):
    index = input_string.find("_", 15)
    result = input_string[index + 1:]
    
    result = result.replace('_Nga', '')
    result = result.replace('_Thuy', '')
    result = result.replace('_Thuan', '')
    result = result.replace('_Thienco', '')
    result = result.replace('_Hieu', '')
    return result
df = pd.read_excel('My-ngày-copy.xlsx')
df = df.rename(columns={'Campaign Delivery': 'Campaign delivery'})
df.to_excel('My-ngày-copy.xlsx', index=False)



df1 = pd.read_excel('My-ngày-copy.xlsx')
df2 = pd.read_excel('TC-ngày-copy.xlsx')
df3 = pd.read_excel('Yino-ngày-copy.xlsx')
df4 = pd.read_excel('Yino-Tech-ngày-copy.xlsx')
merged_df = pd.concat([df1, df2, df3, df4], axis=0, ignore_index=True)
merged_df.to_excel('Chi-phí-1-ngày.xlsx', index=False)
newdf = pd.read_excel('Chi-phí-1-ngày.xlsx')
newdf['Reach'] = newdf['Campaign name'].apply(tachcamp)
newdf['Impressions']=newdf['Campaign name'].apply(UTM)
newdf['Frequency']=newdf['Campaign name'].apply(SKU)

for index, row in newdf.iterrows():
    newdf.at[index, 'Reporting starts'] =  "Camp tốt" if row['Cost per purchase']<=15 and row['Purchases']>=2 and row['Amount spent (USD)']>=50 else "Camp bình thường"
   
newdf.to_excel('Chi-phí-1-ngày.xlsx', index=False)

filtered_df = newdf[newdf['Reporting starts'] == 'Camp tốt']
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE)-> None:
    for index, row in filtered_df.iterrows():
        message = f"Account name: {row['Account name']}\nAdset name: {row['Ad set name']}\nCPA: {row['Cost per purchase']}"
        await context.bot.send_message(chat_id=update.message.chat_id, text=message)
    


app = ApplicationBuilder().token("7154330748:AAGOkvwaduLSJVlFyOBjeHq7fACQGQ7LHdI").build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("report", report))
app.run_polling()