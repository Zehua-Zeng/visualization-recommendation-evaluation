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

  differences <- draw_data %>%
    group_by(!!sym(col_to_compare_by), task, dataset, .draw) %>%
    summarize(difference = weighted.mean(as.numeric(!!sym(diff_col)))) %>%
    compare_levels(difference, by = !!sym(col_to_compare_by))

  if(col_to_compare_by=="search"){
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



user_response_expected_diff_in_mean_plot = function(draw_data, col_to_compare_by, metric, xlab, ylab, color_by){
  diff_col = ""
  if(".value" %in% colnames(draw_data)){
    diff_col = ".value"
  } else {
    diff_col = ".prediction"
  }

    # add groupby task
  differences <- draw_data %>%
    group_by(!!sym(col_to_compare_by), task, .draw) %>%
    summarize(difference = weighted.mean(as.numeric(!!sym(diff_col)))) %>%
    compare_levels(difference, by = !!sym(col_to_compare_by))

  differences$metric  = metric

  if(col_to_compare_by=="search"){
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

user_response_combined_mean_diff = function(){

}

