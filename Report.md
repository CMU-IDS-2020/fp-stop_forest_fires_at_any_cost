# Final Project Report
Joshua Vargas | Taylor Sullivan | Sammy Hajomar | Arpit Kumar

**Project URL**: https://share.streamlit.io/cmu-ids-2020/fp-stop_forest_fires_at_any_cost/main/streamlit-visualizations.py

## Abstract
We have noticed that wildfires in the U.S. have been a problem every year and they seem to be increasing in size and frequency as reported by the media and government officials. However, there is a lack of comprehensive analysis done on wildfires to pin point the exact cause and impact, and what the forecast looks like depending on actions we can take to mitigate them in the future. We set to further investigate these wildfires by looking at what caused them, their economic and environmental impact, and what the outlook for them looks like. We utilized datasets from a multitude of different government sources and built visualizations using Altair to communicate our findings. In addition, we created a model to forecast the economic and environmental impact of natural and human caused wildfires and what that impact looks like if we reduced the prevalence of each. We found that while human caused fires had a greater cost per acre impact, the natural caused fires were significantly more severe in their environmental impact. Another observation we made was that despite the drop in the amount of wildfires, each individual wildfire on average was substantially bigger and had a great impact. We did run into constraints with the data provided since certain datasets included some dimensions while others did not. Further work and analysis is required to look at forest preservation and wildfire linkage to global warming.


## Introduction
Our project goal is to analyze the impact of forest fires on the United States' economy and environment and sensitize the audience to the impact we can have by reducing the burn days on the economy and the environment. 

To achieve the goal, we have investigated the primary cause of Forest Fires in the US, i.e., Natural causes or Human related causes. We have looked at the cost per acre burned, suppression cost, and the land loss over the years to understand which reason has a more financial impact. To understand the environmental impact, we have looked into acres burned and burn days.

## Related Work
The project goal and approach have been an inspiration from several online articles that demonstrate similar intentions. Under the forest fire’s economic considerations, several aspects can be looked at, ranging from fire suppression cost, loss of business activity to medical expenses. With the available data on the US government's website, we focused our narrative on analyzing the Fire Suppression and Emergency Response cost. For the environmental aspects, we researched how we can measure the Forest Fire impact. While there are several exciting parameters to look at, such as burned land area, CO2 emissions, change in temperature, loss of flora and fauna, we focused on burned land area and burned days due to data constraints. 

## Methods
### Data Gathering

We looked at several data sources and chose sources with the highest credibility and completeness. We looked into the Federal Government for Wildfires dataset and secured data from 1980 through 2019 at different granularity and variety. The National Interagency Fire Center and all the data for assessing the economic impact of the wildfires. Although the data was in PDFs, we extracted and converted the information from the pdf into an excel file. The Federal Fire Occurrence had information about all scale and fire types from 1980 to 2016 with its geographic locations. Both these sources contributed to almost 95% of the illustration, observations, and analysis. For creating the reforestation clock, we referred to the National Forest Foundation.

### Data Processing and Transformation

**Prediction Models**

The prediction models utilized two different datasets, the dataset used for predicting cost (Significant Fires 2005-2019) was the most incomplete in supporting accuracy. The dataset illustrated the cost incurred from suppressing significant fires, which lent to missing data points for years not represented in the dataset and for fires that were not categorized as significant. The method for addressing the missing values was a k-nearest neighbor (knn) evaluating the three closest neighbors. The imputation method was applied at the state level for assessing future costs. After this, the dataset average cost per acre burned was calculated. At this point, we used the average cost per acre burned alongside the forecasting results from our Acres-Burned ETS Model to calculate an estimate of suppression costs. The Acres-Burned ETS Model uses the Federal Wildland Fire Occurrence Dataset, a limitation listed later in our research. 

**Logis & Reasoning**
The imputation method intended to account for state budgeting trends. In analyzing budget proposals for state land management, the requested budgets were developed by analyzing the previous three years’ trends, which supported the group's decision to utilize the three nearest neighbors.

### Streamlit Visualizations

The methods were simplistic but challenging as the datasets gathered were either incomplete or, across the datasets. The only dataset that captured the primary intent of depicting the correlation between cost and impacted areas (acres by state) was the National Interagency Fire Center’s dataset. This data offered suppression cost insight into significant fires and the acres burned, location, and name of the fires. We attempted to add some robustness for common fire locations and acres burned by supplementing with the Federal Fire Occurrence Website data, which held information over 37 years for sites of fires and acres burned.

### Logic & Reasoning 

The intentions behind using Streamlit visualizations were to understand, explore, and analyze the data we collected from multiple sources. The choice of virtualization helped us put a better narrative for our project. For instance, to assess the impact of wildfires on the economy, we decided to use bar charts with a line for average to understand how the cost per acre changes concerning the change in suppression cost. Because total suppression cost might be huge at the first look, but can make more sense if the area is also increasing. With the cost per acre graph and suppression cost, we were able to deduce that although it's a huge cost on the government, it is well spent to suppress more fires in terms of area.

### Prediction Models

The group’s scope and goals were to develop predictor models capable of forecasting future acres burned and the fire suppression costs. The first model incorporated an Auto-Regressive Moving Average Time Series analysis on the Significant Fires from 2005 to 2019 dataset. Two conclusions were derived from the observations gathered. The first observation was that the ARIMA model’s prediction technique was not representative of irregularity in occurrences due to natural phenomena. The second observation parallels that of the first. The data did not support the approach, and we diverted to an exponential time series analysis to forecast future acres-burned and cost based on historical trends. 
The reason this methodology was selected was two-fold. Primarily as the “Forecasting demand of commodities after natural disasters” study articulates, ARIMA models are not reliable in the case of natural disasters because of their irregularity and non-linearity of the data (Xu, 2019). As an alternative to the study’s hybrid methodology approach, which our sparse data would not support, we selected the Exponential Time Series. This method was also an approved alternative by the textbook, “Forecasting: Principles and Practice,” which states that the Exponential Time Series, in many cases, has improved accuracy over ARIMA and is more generalizable to new data. As a result, we selected the exponential time series method.
This change in modeling provides the user with a more reliable forecast. We forecasted out five years from the end of the dataset to provide the most accurate predictions. With the sparsity of data, predicting more than five years in the future would offer highly inaccurate results. Lastly, we discovered a more robust dataset consisting of over 800,000 rows of fire data spanning 37 years. The only limitation of this dataset is that it did not account for suppression costs. However, using this dataset in conjunction with the ETS model allowed our group to achieve a much more accurate and reliable model. Predicting annually also reduces the issue of seasonality within the dataset, which could’ve been adjusted for if the data were not so irregular and sparse. We selected R as the platform due to its statistical power. 


## Results
### Streamlit Visualizations

There are several results obtained during the analysis. One of the critical results from graphs is that although natural fires are more in terms of area and count than human-caused wildfires, the cost to suppress the human-caused fire per acre is significantly higher than the naturally caused wildfire. 

### Prediction Models
Our model displays predictions that indicate future rises in both human-caused and nature-caused fires, along with increased costs of suppression. The model suggests that nature-caused fires have risen exponentially in recent years (fueling the predictor’s results). Human-caused fires are growing as well, though not nearly at the same rate. Both variables are mutually exclusive in that each acre burned in the future corresponds to rises in the costs incurred for suppression. This model is attempting to display to the user: the need for action and the need to budget for the worst-case scenario. 


## Discussion

### Model Evaluation

We chose to evaluate our predictor model using a train-validate split to analyze the mean squared error, mean absolute percentage error, the root of the mean squared error to determine how well the model generalized to new data. The results demonstrated that the model did generalize well and was selected as our final model choice. 

### Constraints/Limitations

Several factors constrain the level of accuracy our model can achieve. For predicting cost, accuracy is constrained by budget dependencies to local and federal government budget trends. Fire suppression costs are directly influenced by the state’s preparedness levels, both community and organizational. The lag is created in the days spent before the labor is contracted or federal aid is received. The limitations are heightened by the data available for evaluation, given the complexities of combating wildfires with the agencies involved, resources required, and the vast number of fires. It was challenging to find a data source that collected suppression costs; most sources focused on the cost of damage incurred by fires.

In predicting the total area damaged by wildfires (measured in acreage), the forecasting difficulty is best described by wildfires’ classification (natural phenomena). Wildfires are passively influenced by current climate conditions and directly affected by the surrounding areas’ fuel availability (flammable objects). This fact makes a time series analysis less reliable, but with the adjustment for annual numbers, we could account for this limitation. 

Additionally, due to the lack of data, we needed to use the suppression costs of 2019 in the Significant Fires Dataset from NIFC to estimate the corresponding costs of the predicted fires’ suppression costs for our forecasted results. Because of this cross-dataset approach, users should be cautious with the results, and further work is required to draw meaningful conclusions. 

### System overview and application
<img style="float: right;" src="https://github.com/CMU-IDS-2020/fp-stop_forest_fires_at_any_cost/blob/main/RMSE.png">
The application we built is organized into three main sections. The first section contains an introduction designed to captivate the user. This section consists of an animation of human-caused and nature-caused fires over 37 years with illuminating pie charts that depict the proportion of acres-burned and burn-days caused by humans and nature. Below the animation, the user can also manually progress through the time-series at their own pace with a slider. The introduction concludes with an acres-burned clock and reforestation clock for 2020, demonstrating the estimated acres-burned and reforestation efforts so far this year, as well as the rate of both of these processes each second. The user can attempt to “catch-up” to wild-fire deforestation with an input that calculates the reforestation efforts increased by that user input (in millions of acres). The exploration section leads the user through an exploratory data analysis of the environmental and financial impact of wildfires and the added analysis of fire types. The final section displays a predictor model for future acres-burned and suppression costs for the next five years. The user can decrease the fires created by both humans and nature to change the prediction outcomes. 

## Future Work

Extending the applicability of the cost prediction could be best applied to land management budget trends and the allocation of funds. A case study conducted on human-caused wildfires in Spain highlights the direct relationship between socioeconomic trends and wildfires. The vast increase in population and gentrification of rural areas post WWII has had an impact on the severity and regularity of wildfires. A similar trend has been observed when evaluating the recent wildfires the state of California is experiencing. As briefly mentioned above, at-risk states’ strategic focus has been to shift from a reactive response to a proactive preventative approach. The model could best be served by addressing the necessary budget required to combat yearly significant fires and to aid in determining the operational cost for land management. 

As our model currently stands, it does not include monthly predictions to account for the dry seasons associated with wildfires. Adding this functionality would drastically improve the accuracy of our model and offer even more insight into the monthly trends in wildfires. The parsing together of two datasets for this project was a major constraint, and further research should be conducted into the associated costs of fires and the development of more accurate data. Expanding the model from a singular variable forecasting model to a multi variable model could greatly improve the accuracy. Additionally, this model could be better improved through the adaption of a hybrid approach. Implementing a variety of machine learning algorithms has been proven to increase the accuracy of irregular data trends. Because wildfire data is sparse and irregular, providing methods that are both supervised and unsupervised could offer an avenue to more insightful and accurate forecasting.

## References
1. Total fire count and area from 1926 to 2019: https://www.nifc.gov/fireInfo/fireInfo_stats_totalFires.html
2. Federal firefighting costs from 1985 to 2019: https://www.nifc.gov/fireInfo/fireInfo_documents/SuppCosts.pdf
3. Fires >100k area for past 23 years with location https://www.nifc.gov/fireInfo/fireInfo_stats_lgFires.html
4. Overall fire stats link: https://www.nifc.gov/fireInfo/fireInfo_statistics.html
5. Active fire map: https://inciweb.nwcg.gov/incident/article/58587
6. InciWeb Twitter page (Since 2008): https://twitter.com/inciweb?ref_src=twsrc%5Etfw%7Ctwcamp%5Eembeddedtimeline%7Ctwterm%5Eprofile%3Ainciweb&ref_url=http%3A%2F%2Fwww.fs.usda.gov%2Fscience-technology%2Ffire%2Finformation
7. All fires on Map: https://www.fs.usda.gov/science-technology/fire/information
8. How fires affect the economy? https://fireadaptednetwork.org/wp-content/uploads/2014/03/economic_costs_of_wildfires.pdf
9. 1980 through2016 data: https://wildfire.cr.usgs.gov/firehistory/data.html
10. Impact of wildfire on the environment: https://www.nationalforests.org/blog/our-impact-in-2019
11. Model Evaluation: https://otexts.com/fpp2/arima-ets.html
12. Case Study Comparison: http://bs.ustc.edu.cn/bairc/files/links/2014010331964313.pdf

