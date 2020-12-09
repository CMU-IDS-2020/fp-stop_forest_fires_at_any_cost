install.packages("tidyverse")
library(tidyverse)
library(dplyr)
library(forecast)

#Load Data Set
dataset = read.csv('merged_acre_predict_human.csv', stringsAsFactors = FALSE)
dataset$Year <- as.numeric(dataset$YEAR_)
dataset$Acres <- dataset$TOTALACRES

#National Data Time Series
national_ts <- ts(dataset$Acres, start=2005, end=2016, freq=1)
national_model <- window(x = national_ts, start = c(2005), end = c(2016))
national_ets_auto <- ets(national_model)
national_ets_fc <- forecast(national_ets_auto, h=5)

national_ets_fc_df <- cbind("Year" = rownames(as.data.frame(national_ets_fc)), as.data.frame(national_ets_fc))
names(national_ets_fc_df) <- gsub(" ", "_", names(national_ets_fc_df))  
national_ets_fc_df$Date <- as.Date(paste("", national_ets_fc_df$Year, sep = ""), format = "%Y")
national_ets_fc_df$Model <- rep("NationalETS")

national_ets_fc_df %>% filter(Year == "2017") %>% select(Year, "Point_Forecast")

#merge the data
write.csv(national_ets_fc_df, 'human_prediction_results.csv')

#Load Data Set
dataset = read.csv('merged_acre_predict_natural.csv', stringsAsFactors = FALSE)
dataset$Year <- as.numeric(dataset$YEAR_)
dataset$Acres <- dataset$TOTALACRES

#National Data Time Series
national_ts <- ts(dataset$Acres, start=2005, end=2016, freq=1)
national_model <- window(x = national_ts, start = c(2005), end = c(2016))
national_ets_auto <- ets(national_model)
national_ets_fc <- forecast(national_ets_auto, h=5)

national_ets_fc_df <- cbind("Year" = rownames(as.data.frame(national_ets_fc)), as.data.frame(national_ets_fc))
names(national_ets_fc_df) <- gsub(" ", "_", names(national_ets_fc_df))  
national_ets_fc_df$Date <- as.Date(paste("", national_ets_fc_df$Year, sep = ""), format = "%Y")
national_ets_fc_df$Model <- rep("NationalETS")

national_ets_fc_df %>% filter(Year == "2017") %>% select(Year, "Point_Forecast")

#merge the data
write.csv(national_ets_fc_df, 'natural_prediction_results.csv')
