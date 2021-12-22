library(shiny)
library(ggplot2)
library(plyr)
library(rjson)
library(tidyr)

require(mlbench)
data(BostonHousing)
bostonHousingMetaData <- fromJSON(file = "./boston-housing-meta.json")

ui <- fluidPage(
  
  titlePanel("Boston Housing - Painel criado com Shiny"),
  
  sidebarLayout(
    
    sidebarPanel(
      h3("Variáveis"),
      selectInput(inputId = "variavel",
                  label = "Opções",
                  choices = names(BostonHousing),
                  multiple = FALSE),
      plotOutput(outputId = "graficoResumo"),
      h4("Estrutura"),
      verbatimTextOutput(outputId = "estrutura"),
      h4("Sobre"),
      textOutput("sobre"),
      width = 3
    ),
    
    mainPanel(
      h3("Relação com MEDV"),
      plotOutput(outputId = "graficoRegressao"),
      h3("Mapa de Densidade"),
      selectInput(inputId = "variavelMapa",
                  label = "Opções",
                  choices = names(BostonHousing),
                  multiple = FALSE),
      plotOutput(outputId = "mapaDensidade"),
    )

  )
  
)

server <- function(input, output){
  
  output$graficoResumo <- renderPlot({
    if(is.factor(BostonHousing[[input$variavel]])) {
      coluna <- BostonHousing[[input$variavel]]
      data <- data.frame(
        categoria = levels(coluna),
        freq = count(coluna)[2]
      )
      ggplot(data, aes(y=freq, x="", fill=categoria)) +
      geom_bar(stat = "identity", width = 1) +
      coord_polar("y", start=0) +
      labs(title = paste("Contagem de ", input$variavel)) +
      theme_void()
    }
    else {
      ggplot(BostonHousing, aes_string(y=input$variavel)) +
      geom_boxplot() +
      labs(title = paste("Boxplot de ", input$variavel))
    }
  })
  
  output$estrutura <- renderPrint({
    str(BostonHousing[[input$variavel]])
  })
  
  output$sobre <- renderPrint({
    bostonHousingMetaData[[input$variavel]]
  })
  
  output$graficoRegressao <- renderPlot({
    ggplot(BostonHousing, aes_string(y="medv", x=input$variavel)) +
    geom_point() +
    geom_smooth(method=lm)
  })
  
  output$mapaDensidade <- renderPlot({
    ggplot(BostonHousing, aes_string(y=input$variavelMapa, x=input$variavel)) +
    stat_density2d(aes(fill = ..density..), geom = 'tile', contour = F)
  })
  
}

shinyApp(ui = ui, server = server)

