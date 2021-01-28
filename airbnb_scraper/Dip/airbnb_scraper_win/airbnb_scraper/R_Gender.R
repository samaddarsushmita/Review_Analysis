rm(list = ls())
rm(list = ls(all.names = TRUE))

# PART 1: Select sections to run ----------------------------------------------
PACKAGES             <- 1

# PART 2: Load packages   -----------------------------------------------------
#packages  <- c("readstata13", "foreign",
#               "doBy", "broom", "dplyr",
#               "stargazer", "htmltools",
#               "ggplot2", "plotly", "ggrepel",
#               "RColorBrewer", "RCurl", "XML",
#               "sp", "rgdal", "rgeos",
#               "ggmap", "leaflet",
#               "htmlwidgets", "geosphere",
#               "eeptools", "purrr", "ggforce",
#               "formattable", "tidyr", 
#               "manipulate", "data.table", 
#               "tm", "SnowballC", "wordcloud", 
#               "webshot", "stringr", "devtools")

packages  <- c("readstata13", "dplyr", "ggplot2", "plotly", "tidyr")

# If you selected the option to install packages, install them
if (PACKAGES) {
  
  # Install packages that are not yet installed
  sapply(packages, function(x) {
    if (!(x %in% installed.packages())) {
      install.packages(x, dependencies = TRUE) 
    }
  }
  )
}
# Load all packages -- this is equivalent to using library(package) for each 
# package listed before

invisible(sapply(packages, library, character.only = TRUE))

# PART 3: Set folder folder paths --------------------------------------------
#-------------#
# Root folder #
#-------------#
  projectFolder  <- "/Users/Dip/OneDrive/AirBnb"

#importing the dataset

all_data <- read.csv(file.path(projectFolder, "Combined_Listings_Gendered.csv.gz"),
                                header = TRUE)

#drop <- c(2,3,5:19,21,27:30,32,33,43,49,50,60:62,97:101)
#listing_data <- all_data[-drop]



