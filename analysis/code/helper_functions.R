posterior_draws_plot = function(data, col_to_color_by, facet_by_task, xLab, yLab){

  plot <- data %>% ggplot(aes(
    x = .value,
    y = reorder(condition, desc(condition)),
    fill = !!sym(col_to_color_by),
    alpha = 0.5)) +
    stat_halfeye(.width = c(.95, .5)) +
    labs(x = xLab, y = yLab)

  if(facet_by_task){
    plot <- plot + facet_grid(. ~ task)
  }

  return(plot)
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


expected_diff_in_mean_plot = function(draw_data, col_to_compare_by, xlab, ylab, reverse_difference, color_by){

  differences <- draw_data %>%
    group_by(!!sym(col_to_compare_by), task, dataset, .draw) %>%
    summarize(diff = weighted.mean(.prediction)) %>%
    compare_levels(diff, by = !!sym(col_to_compare_by))

  if(reverse_difference ||  col_to_compare_by=="search"){
    split = strsplit(differences[[col_to_compare_by]][1], " - ")
    differences[[col_to_compare_by]] = paste0(split[[1]][2], " - ", split[[1]][1])
    differences$diff = -1 * differences$diff
  }

  xlab_formatted = paste0(xlab, " (",differences[[col_to_compare_by]][1],")")
  differences_plot <- differences %>%
    ggplot(aes(x = diff, y = task)) +
    xlab(xlab_formatted) +
    ylab(ylab)+
    stat_halfeye(.width = c(.95, .5)) +
    geom_vline(xintercept = 0, linetype = "longdash") +
    theme_minimal() + scale_y_discrete(limits = rev(levels(differences$task)))


  if(!is.null(color_by)){
    differences_plot <- differences_plot + aes(fill=!!sym(color_by), alpha = 0.5)
    intervals <- differences %>% group_by(!!sym(col_to_compare_by), !!sym(color_by), task) %>% mean_qi(diff, .width = c(.95, .5))
  }
  else{
    intervals <- differences %>% group_by(!!sym(col_to_compare_by), task) %>% mean_qi(diff, .width = c(.95, .5))
  }

  return(list("plot" = differences_plot, "intervals" = intervals))
}





