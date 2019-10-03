##app.R ##
library(shiny)
library(shinydashboard)
library("rjson")

directory = system(command = "pwd", intern = TRUE,
                   ignore.stdout = FALSE, ignore.stderr = FALSE,
                   wait = TRUE, input = NULL, show.output.on.console = TRUE,
                   minimized = FALSE, invisible = TRUE, timeout = 0)
setwd(directory)

#################### GLOBAL THINGS ##############################
system(command = "./python_scripts/rd_data.py", intern = FALSE,
       ignore.stdout = FALSE, ignore.stderr = FALSE,
       wait = TRUE, input = NULL, show.output.on.console = TRUE,
       minimized = FALSE, invisible = TRUE, timeout = 0)
data <- fromJSON(file = "rd-data.json")
df <- do.call(rbind, data)
df <- data.frame(df)
#Just a test thing for now
capdata <- fromJSON(file = "rd-caps.json")
capdf <- do.call(rbind, capdata)
capdf <- data.frame(capdf)
caps <- capdf$capacity
caps <- unlist(caps)

df["cap"] <- caps
################################################################

# Run the Applications
runApp(appDir="appdirectory")