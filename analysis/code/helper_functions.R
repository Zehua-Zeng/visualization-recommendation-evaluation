posterior_draws_plot = function(data, col_to_color_by, facet_by_task, xLab, yLab){

  plot <- data %>% ggplot(aes(
    y = reorder(condition, desc(condition)),
    fill = !!sym(col_to_color_by),
    alpha = 0.5)) +
    stat_halfeye(.width = c(.95, .5)) +
    labs(x = xLab, y = yLab)

  if(".value" %in% colnames(data)){
    plot <- plot + aes(x=.value)
  }
  else{
    plot <- plot + aes(x=.prediction)
  }

  if(facet_by_task){
    plot <- plot + facet_grid(. ~ task)
  }

  return(plot)
}

interaction_posterior_draws_plot = function(data, col_to_color_by){
  plot <- data %>% ggplot(aes(x = dataset, fill = !!sym(col_to_color_by), alpha = 0.5)) +
    stat_eye(.width = c(.95, .5)) +
    theme_minimal() +
    facet_grid(task ~ condition)

  if(".value" %in% colnames(data)){
    plot <- plot + aes(y=.value)
  }
  else{
    plot <- plot + aes(y=.prediction)
  }

  return(plot)
}

user_response_posterior_draws_plot = function(data, model, col_to_color_by, xLab, yLab){
  draw_data <- data %>%
    add_predicted_draws(model,
                        seed = seed,
                        re_formula = NA) %>%
    group_by(search, oracle, .draw) %>%
    mutate(rating = weighted.mean(as.numeric(as.character(.prediction))))

  plot <- draw_data %>%
    ggplot(aes(x = oracle, y = rating)) +
    stat_eye(.width = c(.95, .5)) +
    theme_minimal() +
    coord_cartesian(ylim = c(-2, 2)) +
    labs(x = xLab, y = yLab) +
    facet_grid(. ~ search)

  if(!is.null(col_to_color_by)){
    plot <- plot + aes(fill = !!sym(col_to_color_by), alpha = 0.5)
  }

  intervals <- draw_data %>% group_by(search, oracle) %>% mean_qi(rating, .width = c(.95, .5))

  return(list("plot" = plot, "intervals" = intervals))
}


save_plot = function(plot, filename, path){
  ggsave(
    file = filename,
    plot = plot,
    path = path,
    width = 6,
    height = 4
  )
}


expected_diff_in_mean_plot = function(draw_data, col_to_compare_by, xlab, ylab, color_by){
  diff_col = ""
  if(".value" %in% colnames(draw_data)){
    diff_col = ".value"
  } else {
    diff_col = ".prediction"
  }
  differences <- data.frame()
  if(!is.null(color_by)){
      differences <- draw_data %>%
      group_by(!!sym(col_to_compare_by), task, !!sym(color_by), .draw) %>%
      summarize(difference = weighted.mean(as.numeric(!!sym(diff_col)))) %>%
      compare_levels(difference, by = !!sym(col_to_compare_by))
  }
  else{
      differences <- draw_data %>%
      group_by(!!sym(col_to_compare_by), task, .draw) %>%
      summarize(difference = weighted.mean(as.numeric(!!sym(diff_col)))) %>%
      compare_levels(difference, by = !!sym(col_to_compare_by))
  }

  differences$task = as.factor(differences$task)

  if(col_to_compare_by=="search" || col_to_compare_by == "alg"){
    split = strsplit(differences[[col_to_compare_by]][1], " - ")
    differences[[col_to_compare_by]] = paste0(split[[1]][2], " - ", split[[1]][1])
    differences$difference = -1 * differences$difference
  }

  xlab_formatted = paste0(xlab, " (",differences[[col_to_compare_by]][1],")")

  differences_plot <- differences %>%
    ggplot(aes(x = difference, y = task)) +
    xlab(xlab_formatted) +
    ylab(ylab)+
    stat_halfeye(.width = c(.95, .5)) +
    geom_vline(xintercept = 0, linetype = "longdash") +
    theme_minimal() + scale_y_discrete(limits = rev(levels(differences$task)))

  if(!is.null(color_by)){
    differences_plot <- differences_plot + aes(fill=!!sym(color_by), alpha = 0.5)
    intervals <- differences %>% group_by(!!sym(col_to_compare_by), !!sym(color_by), task) %>% mean_qi(difference, .width = c(.95, .5))
  } else{
    intervals <- differences %>% group_by(!!sym(col_to_compare_by), task) %>% mean_qi(difference, .width = c(.95, .5))
  }

  return(list("plot" = differences_plot, "intervals" = intervals, "differences" = differences))
}



user_response_diff_plot = function(draw_data, col_to_compare_by, metric, xlab, ylab, color_by){
  diff_col = ""
  if(".value" %in% colnames(draw_data)){
    diff_col = ".value"
  } else {
    diff_col = ".prediction"
  }

  differences <- draw_data %>%
    group_by(!!sym(col_to_compare_by), task, .draw) %>%
    summarize(difference = weighted.mean(as.numeric(!!sym(diff_col)))) %>%
    compare_levels(difference, by = !!sym(col_to_compare_by))

  differences$metric  = metric

  if(col_to_compare_by=="search" || col_to_compare_by == "alg"){
    split = strsplit(differences[[col_to_compare_by]][1], " - ")
    differences[[col_to_compare_by]] = paste0(split[[1]][2], " - ", split[[1]][1])
    differences$difference = -1 * differences$difference
  }

  xlab_formatted = paste0(xlab, " (",differences[[col_to_compare_by]][1],")")

  differences_plot <- differences %>%
    ggplot(aes(x = difference, y = task)) +
    xlab(xlab_formatted) +
    ylab(ylab)+
    stat_halfeye(.width = c(.95, .5)) +
    geom_vline(xintercept = 0, linetype = "longdash") +
    theme_minimal() + scale_y_discrete(limits = rev(levels(differences$task)))


  return(list("plot" = differences_plot, "differences" = differences))
}

user_response_diff_summary = function(data, col_to_compare_by){
  analysis_formatted = c('Understanding Data', 'Answer', 'Efficiency', 'Ease of Use', 'Utility', 'Overall')
  confidence_metrics = c('Understanding Data', 'Answer')
  preference_metrics = c('Efficiency', 'Ease of Use', 'Utility', 'Overall')

  data$metric<- gsub('confidence.udata', 'Understanding Data', data$metric)
  data$metric<- gsub('confidence.ans', 'Answer', data$metric)
  data$metric<- gsub('efficiency', 'Efficiency', data$metric)
  data$metric<- gsub('ease.of.use', 'Ease of Use', data$metric)
  data$metric<- gsub('utility', 'Utility', data$metric)
  data$metric<- gsub('overall', 'Overall', data$metric)
  data$metric <- factor(data$metric, levels=rev(analysis_formatted))

  data_confidence <- subset(data, metric %in% confidence_metrics)
  plot_confidence <- user_response_confidence_preference_plot(data_confidence, col_to_compare_by, "Confidence")
  intervals_confidence <- data_confidence %>% group_by(!!sym(col_to_compare_by), metric) %>% mean_qi(difference, .width = c(.95, .5))

  data_preference <- subset(data, metric %in% preference_metrics)
  plot_preference <- user_response_confidence_preference_plot(data_preference, col_to_compare_by, "Preference")
  intervals_preference <- data_preference %>% group_by(!!sym(col_to_compare_by), metric) %>% mean_qi(difference, .width = c(.95, .5))


  return(list("plot_confidence" = plot_confidence, "intervals_confidence" = intervals_confidence,
              "plot_preference" = plot_preference,  "intervals_preference" = intervals_preference
              ))
}

user_response_confidence_preference_plot = function(plot_data, col_to_compare_by, ylab){
  plot <- plot_data %>%
    ggplot(aes(x = difference, y = metric)) +
    ylab(ylab) +
    xlab(paste0("Difference in Rating (",plot_data[[col_to_compare_by]][1],")")) +
    stat_halfeye(.width = c(.95, .5)) +
    geom_vline(xintercept = 0, linetype = "longdash") +
    theme_minimal()

  return(plot)
}

