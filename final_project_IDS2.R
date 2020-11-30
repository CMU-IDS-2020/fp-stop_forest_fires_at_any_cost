install.packages("tidyverse")
library(tidyverse)
library(dplyr)
library(forecast)

#Load Data Set
dataset = read.csv('significant-fires.csv', stringsAsFactors = FALSE)
dataset$Start_Date = as.Date(dataset$Start_Date, format='%m/%d/%Y')
dataset$year = dataset$ï..Year
dataset$year <- as.numeric(dataset$year)
dataset$Acres <-as.numeric(gsub(",", "", dataset$Acres))

#Filter data for Texas
texas <- filter(dataset, State == 'Texas')
texas2 <- aggregate(Acres ~ year, texas, sum)
texas_ts <- ts(texas2$Acres, start=2015, end=2019, freq=1)
texas_model <- window(x = texas_ts, start = c(2016), end = c(2018))
texas_ets_auto <- ets(texas_model)
texas_ets_fc <- forecast(texas_ets_auto, h=5)

texas_ets_fc_df <- cbind("Year" = rownames(as.data.frame(texas_ets_fc)), as.data.frame(texas_ets_fc))
names(texas_ets_fc_df) <- gsub(" ", "_", names(texas_ets_fc_df))  
texas_ets_fc_df$Date <- as.Date(paste("", texas_ets_fc_df$Year, sep = ""), format = "%Y")
texas_ets_fc_df$Model <- rep("ets")

texas_ets_fc_df %>% 
  filter(Year == "2020") %>% 
  select(Year, "Point_Forecast")

#Filter data for Alaska 
alaska <- filter(dataset, State == 'Alaska')
alaska2 <- aggregate(Acres ~ year, alaska, sum)
alaska_ts <- ts(alaska2$Acres, start=2015, end=2019, freq=1)
alaska_model <- window(x = alaska_ts, start = c(2015), end = c(2019))
alaska_ets_auto <- ets(alaska_model)
alaska_ets_fc <- forecast(alaska_ets_auto, h=5)

alaska_ets_fc_df <- cbind("Year" = rownames(as.data.frame(alaska_ets_fc)), as.data.frame(alaska_ets_fc))
names(alaska_ets_fc_df) <- gsub(" ", "_", names(alaska_ets_fc_df))  
alaska_ets_fc_df$Date <- as.Date(paste("", alaska_ets_fc_df$Year, sep = ""), format = "%Y")
alaska_ets_fc_df$Model <- rep("ets")

alaska_ets_fc_df %>% filter(Year == "2020") %>% select(Year, "Point_Forecast")

#Filter data for Arizona
arizona <- filter(dataset, State == 'Arizona')
arizona2 <- aggregate(Acres ~ year, arizona, sum)
arizona_ts <- ts(arizona2$Acres, start=2015, end=2019, freq=1)
arizona_model <- window(x = arizona_ts, start = c(2015), end = c(2019))
arizona_ets_auto <- ets(arizona_model)
arizona_ets_fc <- forecast(arizona_ets_auto, h=5)

arizona_ets_fc_df <- cbind("Year" = rownames(as.data.frame(arizona_ets_fc)), as.data.frame(arizona_ets_fc))
names(arizona_ets_fc_df) <- gsub(" ", "_", names(arizona_ets_fc_df))  
arizona_ets_fc_df$Date <- as.Date(paste("", arizona_ets_fc_df$Year, sep = ""), format = "%Y")
arizona_ets_fc_df$Model <- rep("ets")

arizona_ets_fc_df %>% filter(Year == "2021") %>% select(Year, "Point_Forecast")

#Filter data for California
california <- filter(dataset, State == 'California')
california2 <- aggregate(Acres ~ year, california, sum)
california_ts <- ts(california2$Acres, start=2015, end=2019, freq=1)
california_model <- window(x = california_ts, start = c(2015), end = c(2019))
california_ets_auto <- ets(california_model)
california_ets_fc <- forecast(california_ets_auto, h=5)

california_ets_fc_df <- cbind("Year" = rownames(as.data.frame(california_ets_fc)), as.data.frame(california_ets_fc))
names(california_ets_fc_df) <- gsub(" ", "_", names(california_ets_fc_df))  
california_ets_fc_df$Date <- as.Date(paste("", california_ets_fc_df$Year, sep = ""), format = "%Y")
california_ets_fc_df$Model <- rep("ets")

california_ets_fc_df %>% filter(Year == "2021") %>% select(Year, "Point_Forecast")

#Filter data for Colorado
colorado <- filter(dataset, State == 'Colorado')
colorado2 <- aggregate(Acres ~ year, colorado, sum)
colorado_ts <- ts(colorado2$Acres, start=2018, end=2018, freq=1)
colorado_model <- window(x = colorado_ts, start = c(2018), end = c(2018))
colorado_ets_auto <- ets(colorado_model)
colorado_ets_fc <- forecast(colorado_ets_auto, h=5)

colorado_ets_fc_df <- cbind("Year" = rownames(as.data.frame(colorado_ets_fc)), as.data.frame(colorado_ets_fc))
names(colorado_ets_fc_df) <- gsub(" ", "_", names(colorado_ets_fc_df))  
colorado_ets_fc_df$Date <- as.Date(paste("", colorado_ets_fc_df$Year, sep = ""), format = "%Y")
colorado_ets_fc_df$Model <- rep("ets")

colorado_ets_fc_df %>% filter(Year == "2021") %>% select(Year, "Point_Forecast")

#Filter data for Florida
florida <- filter(dataset, State == 'Florida')
florida2 <- aggregate(Acres ~ year, florida, sum)
florida_ts <- ts(florida2$Acres, start=2018, end=2019, freq=1)
florida_model <- window(x = florida_ts, start = c(2018), end = c(2019))
florida_ets_auto <- ets(arizona_model)
florida_ets_fc <- forecast(florida_ets_auto, h=5)

florida_ets_fc_df <- cbind("Year" = rownames(as.data.frame(florida_ets_fc)), as.data.frame(florida_ets_fc))
names(florida_ets_fc_df) <- gsub(" ", "_", names(florida_ets_fc_df))  
florida_ets_fc_df$Date <- as.Date(paste("", florida_ets_fc_df$Year, sep = ""), format = "%Y")
florida_ets_fc_df$Model <- rep("ets")

florida_ets_fc_df %>% filter(Year == "2021") %>% select(Year, "Point_Forecast")

#Filter data for Georgia
georgia <- filter(dataset, State == 'Georgia')
georgia2 <- aggregate(Acres ~ year, georgia, sum)
georgia_ts <- ts(georgia2$Acres, start=2017, end=2017, freq=1)
georgia_model <- window(x = georgia_ts, start = c(2017), end = c(2017))
georgia_ets_auto <- ets(georgia_model)
georgia_ets_fc <- forecast(georgia_ets_auto, h=5)

georgia_ets_fc_df <- cbind("Year" = rownames(as.data.frame(georgia_ets_fc)), as.data.frame(georgia_ets_fc))
names(georgia_ets_fc_df) <- gsub(" ", "_", names(georgia_ets_fc_df))  
georgia_ets_fc_df$Date <- as.Date(paste("", georgia_ets_fc_df$Year, sep = ""), format = "%Y")
georgia_ets_fc_df$Model <- rep("ets")

georgia_ets_fc_df %>% filter(Year == "2021") %>% select(Year, "Point_Forecast")

#Filter data for Idaho
idaho <- filter(dataset, State == 'Idaho')
idaho2 <- aggregate(Acres ~ year, idaho, sum)
idaho_ts <- ts(idaho2$Acres, start=2015, end=2019, freq=1)
idaho_model <- window(x = idaho_ts, start = c(2015), end = c(2019))
idaho_ets_auto <- ets(idaho_model)
idaho_ets_fc <- forecast(idaho_ets_auto, h=5)

idaho_ets_fc_df <- cbind("Year" = rownames(as.data.frame(idaho_ets_fc)), as.data.frame(idaho_ets_fc))
names(idaho_ets_fc_df) <- gsub(" ", "_", names(idaho_ets_fc_df))  
idaho_ets_fc_df$Date <- as.Date(paste("", idaho_ets_fc_df$Year, sep = ""), format = "%Y")
idaho_ets_fc_df$Model <- rep("ets")

idaho_ets_fc_df %>% filter(Year == "2021") %>% select(Year, "Point_Forecast")

#Filter data for Montana
montana <- filter(dataset, State == 'Montana')
montana2 <- aggregate(Acres ~ year, montana, sum)
montana_ts <- ts(montana2$Acres, start=2015, end=2017, freq=1)
montana_model <- window(x = montana_ts, start = c(2015), end = c(2017))
montana_ets_auto <- ets(montana_model)
montana_ets_fc <- forecast(montana_ets_auto, h=5)

montana_ets_fc_df <- cbind("Year" = rownames(as.data.frame(montana_ets_fc)), as.data.frame(montana_ets_fc))
names(montana_ets_fc_df) <- gsub(" ", "_", names(montana_ets_fc_df))  
montana_ets_fc_df$Date <- as.Date(paste("", montana_ets_fc_df$Year, sep = ""), format = "%Y")
montana_ets_fc_df$Model <- rep("ets")

montana_ets_fc_df %>% filter(Year == "2021") %>% select(Year, "Point_Forecast")

#Filter data for Nevada
nevada <- filter(dataset, State == 'Nevada')
nevada2 <- aggregate(Acres ~ year, nevada, sum)
nevada_ts <- ts(nevada2$Acres, start=2016, end=2018, freq=1)
nevada_model <- window(x = nevada_ts, start = c(2016), end = c(2018))
nevada_ets_auto <- ets(nevada_model)
nevada_ets_fc <- forecast(nevada_ets_auto, h=5)

nevada_ets_fc_df <- cbind("Year" = rownames(as.data.frame(nevada_ets_fc)), as.data.frame(nevada_ets_fc))
names(nevada_ets_fc_df) <- gsub(" ", "_", names(nevada_ets_fc_df))  
nevada_ets_fc_df$Date <- as.Date(paste("", nevada_ets_fc_df$Year, sep = ""), format = "%Y")
nevada_ets_fc_df$Model <- rep("ets")

nevada_ets_fc_df %>% filter(Year == "2021") %>% select(Year, "Point_Forecast")

#Filter data for New Mexico
newmexico <- filter(dataset, State == 'New Mexico')
newmexico2 <- aggregate(Acres ~ year, newmexico, sum)
newmexico_ts <- ts(newmexico2$Acres, start=2016, end=2018, freq=1)
newmexico_model <- window(x = newmexico_ts, start = c(2016), end = c(2018))
newmexico_ets_auto <- ets(newmexico_model)
newmexico_ets_fc <- forecast(newmexico_ets_auto, h=5)

newmexico_ets_fc_df <- cbind("Year" = rownames(as.data.frame(newmexico_ets_fc)), as.data.frame(newmexico_ets_fc))
names(newmexico_ets_fc_df) <- gsub(" ", "_", names(newmexico_ets_fc_df))  
newmexico_ets_fc_df$Date <- as.Date(paste("", newmexico_ets_fc_df$Year, sep = ""), format = "%Y")
newmexico_ets_fc_df$Model <- rep("ets")

newmexico_ets_fc_df %>% filter(Year == "2021") %>% select(Year, "Point_Forecast")

#Filter data for Oklahoma
oklahoma <- filter(dataset, State == 'Oklahoma')
oklahoma2 <- aggregate(Acres ~ year, oklahoma, sum)
oklahoma_ts <- ts(oklahoma2$Acres, start=2016, end=2018, freq=1)
oklahoma_model <- window(x = oklahoma_ts, start = c(2016), end = c(2018))
oklahoma_ets_auto <- ets(oklahoma_model)
oklahoma_ets_fc <- forecast(oklahoma_ets_auto, h=5)

oklahoma_ets_fc_df <- cbind("Year" = rownames(as.data.frame(oklahoma_ets_fc)), as.data.frame(oklahoma_ets_fc))
names(oklahoma_ets_fc_df) <- gsub(" ", "_", names(oklahoma_ets_fc_df))  
oklahoma_ets_fc_df$Date <- as.Date(paste("", oklahoma_ets_fc_df$Year, sep = ""), format = "%Y")
oklahoma_ets_fc_df$Model <- rep("ets")

oklahoma_ets_fc_df %>% filter(Year == "2021") %>% select(Year, "Point_Forecast")

#Filter data for Oregon
oregon <- filter(dataset, State == 'Oregon')
oregon2 <- aggregate(Acres ~ year, oregon, sum)
oregon_ts <- ts(oregon2$Acres, start=2015, end=2018, freq=1)
oregon_model <- window(x = oregon_ts, start = c(2015), end = c(2018))
oregon_ets_auto <- ets(oregon_model)
oregon_ets_fc <- forecast(oregon_ets_auto, h=5)

oregon_ets_fc_df <- cbind("Year" = rownames(as.data.frame(oregon_ets_fc)), as.data.frame(oregon_ets_fc))
names(oregon_ets_fc_df) <- gsub(" ", "_", names(oregon_ets_fc_df))  
oregon_ets_fc_df$Date <- as.Date(paste("", oregon_ets_fc_df$Year, sep = ""), format = "%Y")
oregon_ets_fc_df$Model <- rep("ets")

oregon_ets_fc_df %>% filter(Year == "2021") %>% select(Year, "Point_Forecast")

#Filter data for South Dakota
southdakota <- filter(dataset, State == 'South Dakota')
southdakota2 <- aggregate(Acres ~ year, southdakota, sum)
southdakota_ts <- ts(southdakota2$Acres, start=2016, end=2017, freq=1)
southdakota_model <- window(x = southdakota_ts, start = c(2016), end = c(2017))
southdakota_ets_auto <- ets(southdakota_model)
southdakota_ets_fc <- forecast(southdakota_ets_auto, h=5)

southdakota_ets_fc_df <- cbind("Year" = rownames(as.data.frame(southdakota_ets_fc)), as.data.frame(southdakota_ets_fc))
names(southdakota_ets_fc_df) <- gsub(" ", "_", names(southdakota_ets_fc_df))  
southdakota_ets_fc_df$Date <- as.Date(paste("", southdakota_ets_fc_df$Year, sep = ""), format = "%Y")
southdakota_ets_fc_df$Model <- rep("ets")

southdakota_ets_fc_df %>% filter(Year == "2021") %>% select(Year, "Point_Forecast")

#Filter data for Utah
utah <- filter(dataset, State == 'Utah')
utah2 <- aggregate(Acres ~ year, utah, sum)
utah_ts <- ts(utah2$Acres, start=2017, end=2018, freq=1)
utah_model <- window(x = utah_ts, start = c(2017), end = c(2018))
utah_ets_auto <- ets(utah_model)
utah_ets_fc <- forecast(utah_ets_auto, h=5)

utah_ets_fc_df <- cbind("Year" = rownames(as.data.frame(utah_ets_fc)), as.data.frame(utah_ets_fc))
names(utah_ets_fc_df) <- gsub(" ", "_", names(utah_ets_fc_df))  
utah_ets_fc_df$Date <- as.Date(paste("", utah_ets_fc_df$Year, sep = ""), format = "%Y")
utah_ets_fc_df$Model <- rep("ets")

utah_ets_fc_df %>% filter(Year == "2021") %>% select(Year, "Point_Forecast")

#Filter data for Washington
washington <- filter(dataset, State == 'Washington')
washington2 <- aggregate(Acres ~ year, washington, sum)
washington_ts <- ts(washington2$Acres, start=2015, end=2019, freq=1)
washington_model <- window(x = washington_ts, start = c(2015), end = c(2019))
washington_ets_auto <- ets(washington_model)
washington_ets_fc <- forecast(washington_ets_auto, h=5)

washington_ets_fc_df <- cbind("Year" = rownames(as.data.frame(washington_ets_fc)), as.data.frame(washington_ets_fc))
names(washington_ets_fc_df) <- gsub(" ", "_", names(washington_ets_fc_df))  
washington_ets_fc_df$Date <- as.Date(paste("", washington_ets_fc_df$Year, sep = ""), format = "%Y")
washington_ets_fc_df$Model <- rep("ets")

washington_ets_fc_df %>% filter(Year == "2021") %>% select(Year, "Point_Forecast")

#Filter data for Wyoming
wyoming <- filter(dataset, State == 'Wyoming')
wyoming2 <- aggregate(Acres ~ year, wyoming, sum)
wyoming_ts <- ts(wyoming2$Acres, start=2016, end=2018, freq=1)
wyoming_model <- window(x = wyoming_ts, start = c(2016), end = c(2018))
wyoming_ets_auto <- ets(wyoming_model)
wyoming_ets_fc <- forecast(wyoming_ets_auto, h=5)

wyoming_ets_fc_df <- cbind("Year" = rownames(as.data.frame(wyoming_ets_fc)), as.data.frame(wyoming_ets_fc))
names(wyoming_ets_fc_df) <- gsub(" ", "_", names(wyoming_ets_fc_df))  
wyoming_ets_fc_df$Date <- as.Date(paste("", wyoming_ets_fc_df$Year, sep = ""), format = "%Y")
wyoming_ets_fc_df$Model <- rep("ets")

wyoming_ets_fc_df %>% filter(Year == "2021") %>% select(Year, "Point_Forecast")
