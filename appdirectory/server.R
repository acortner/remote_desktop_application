function(input, output) {
  
  # Generates info boxes 
  output$rdbox <- renderUI({
    myFunc <- function(dfRow) {
      col <- "green"
      usr = as.numeric(dfRow["users"])
      max = as.numeric(dfRow["cap"])
      if (max == 0) {
        col <- "black"
      }
      else if (max == 100) {
        max <- "∞"
      }
      else if (usr == max | usr > max) {
        col <- "red"
      }
      else if (usr / max > .50) {
        col <- "yellow"
      }
      else {
        col <- "green"
      }
      
      infoBox(
        title = dfRow["server"] ,
        value = paste(usr, "/", max),
        icon = icon('desktop'),
        subtitle = paste(dfRow["server"], "@research.partners.org", sep = ""),
        color = col,
        width = 4
      )
    }
    apply(df, 1, myFunc)
  })
  
  
  
}