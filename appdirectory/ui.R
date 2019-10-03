tagList(
  dashboardPage(
    dashboardHeader(
    title = tags$a(
        href = "https://rc.partners.org/",
        target = "_blank",
        tags$img(height = "45px", alt = "Remote Desktops", src =
                   "SciC_ERIS_Banner_White.png"),
        titleWidth = 400
      )
    ),
    dashboardSidebar(disable = TRUE),
    dashboardBody(
      tags$head(
        tags$link(rel = "stylesheet", type = "text/css", href = "custom.css")
      ),
      sidebarLayout(sidebarPanel =    box(
        title = "Remote Desktops",
        #actionButton("refresh", "Refresh"),
        p("This web applications allows your to view the availability of our NoMachine Remote Desktops."),
        
        
        # h5("Setting Up Connection Details"), 
        # p("1. Start the NoMachine application"),
        # p("2. Click on the 'New' button to add a connection"),
        # p("3. Leave 'Protocol' set to 'NX' and press Continue"),
        # p("4. Enter the server name assigned to you in the 'Host' field and press Continue"),
        # p("5. Select Password on the Authentication panel and press Continue"),
        # p("6. To complete the connection setup, press Done on the Save As panel, changing the connection name if desired"),
        # h5("Connecting to the Virtual Desktop"),
        h4("Knowledge Base Articles", h5(
          a(
            "Remote Linux Desktop in the ERISOne Cluster Environment - Access, and Policies",
            href = "https://rc.partners.org/kb/article/2684",
            target = "_blank", 
            rel="noopener" 
          )
        )),
        h5(
          a(
            'Remote Linux Desktop on ERISOne using the NoMachine Enterprise Client',
            href = "https://rc.partners.org/kb/article/2849",
            target = "_blank",
            rel="noopener" 
          )
        ),
        
        width = 4
      ), mainPanel = uiOutput("rdbox"), fluid = TRUE)
      
      
    )
  ),
  tags$footer(
    tags$div(class = "footer",
      tags$p(tags$a(href = "http://researchlist.partners.org/t/232818/8877776/21043/65/", "Help & FAQ", target = "_blank")),
      tags$p(tags$a(href = "mailto:rcc@partners.org", "Contact Support")),
      tags$p(tags$a(class = "twitter", href = "https://twitter.com/PHSERIS", tags$img(height = "25px", alt = "Follow Us On Twitter!", src =
                                                                                              "Twitter-Logo-White.png"), target = "_blank")),
    align = "center", style = ""),
    
    tags$p("Partners HealthCare, 399 Revolution Drive, Somerville, MA 02145"),
    align = "center",
    style = ""
  )
)