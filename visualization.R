library(ggplot2)
library(stringr)
library(patchwork)

# =========================================
# Paper-ready helper: consistent formatting
# =========================================
pct_plot_clean <- function(df, title = NULL, facet_var = NULL,
                           show_y_title = FALSE, show_x_title = FALSE) {
  df$pct <- abs(df$pct)
  df$comparison <- str_wrap(df$comparison, 28)
  
  # stable ordering by magnitude (small -> large, displayed top -> bottom after flip)
  df <- df[order(df$pct), ]
  df$comparison <- factor(df$comparison, levels = rev(unique(df$comparison)))
  
  p <- ggplot(df, aes(x = comparison, y = pct)) +
    geom_col(fill = "grey90", color = "black", width = 0.75, linewidth = 0.55) +
    geom_text(aes(label = sprintf("%.2f%%", pct)),
              hjust = -0.08, fontface = "bold", size = 3.1) +
    coord_flip(clip = "off") +
    scale_y_continuous(expand = expansion(mult = c(0.02, 0.30))) +
    theme_classic(base_size = 12) +
    theme(
      # internal title per panel (keep small; overall title will come from patchwork)
      plot.title = element_text(face = "bold", hjust = 0, size = 12),
      axis.text.y = element_text(face = "bold"),
      axis.text.x = element_text(face = "bold"),
      strip.text = element_text(face = "bold"),
      # keep spacing consistent across combined figures
      plot.margin = margin(6, 48, 6, 6)
    )
  
  if (!is.null(title)) p <- p + ggtitle(title)
  if (!is.null(facet_var)) p <- p + facet_wrap(facet_var, ncol = 2)
  
  # Remove titles unless requested (for clean multi-panel stacking)
  if (!show_y_title) p <- p + labs(y = NULL) + theme(axis.title.y = element_blank())
  if (!show_x_title) p <- p + labs(x = NULL) + theme(axis.title.x = element_blank())
  
  p
}

# =========================================
# OPTIONAL: add one shared axis label
# =========================================
shared_y_label <- function(label_text = "Percent Difference (Absolute, %)") {
  ggplot() +
    theme_void() +
    annotate("text", x = 0, y = 0, label = label_text, angle = 90,
             fontface = "bold", size = 4) +
    theme(plot.margin = margin(0, 0, 0, 0))
}

# =========================================
# BUILD your plots (using your existing data)
# (Assumes ripple_10_30_long, ripple_time,
#  tripod_10_30_long, tripod_time, tvr already exist)
# =========================================

# Ripple
p_ripple_10_30_x <- pct_plot_clean(subset(ripple_10_30_long, axis == "x"),
                                   title = "Ripple (X): 10 s vs 30 s",
                                   facet_var = ~ time)

p_ripple_10_30_y <- pct_plot_clean(subset(ripple_10_30_long, axis == "y"),
                                   title = "Ripple (Y): 10 s vs 30 s",
                                   facet_var = ~ time)

p_ripple_time <- pct_plot_clean(ripple_time,
                                title = "Ripple: 30 s vs 10 s",
                                facet_var = ~ axis)

# Tripod
p_tripod_10_30_x <- pct_plot_clean(subset(tripod_10_30_long, axis == "x"),
                                   title = "Tripod (X): 10 s vs 30 s",
                                   facet_var = ~ time)

p_tripod_10_30_y <- pct_plot_clean(subset(tripod_10_30_long, axis == "y"),
                                   title = "Tripod (Y): 10 s vs 30 s",
                                   facet_var = ~ time)

p_tripod_time <- pct_plot_clean(tripod_time,
                                title = "Tripod: 30 s vs 10 s",
                                facet_var = ~ axis)

# Tripod vs Ripple
p_tvr_x <- pct_plot_clean(subset(tvr, axis == "x"),
                          title = "Tripod vs Ripple (X)",
                          facet_var = ~ time)

p_tvr_y <- pct_plot_clean(subset(tvr, axis == "y"),
                          title = "Tripod vs Ripple (Y)",
                          facet_var = ~ time)

# =========================================
# COMBINE into single figures (paper-ready)
# =========================================

ylab <- shared_y_label("Percent Difference (Absolute, %)")

fig_ripple <-
  (ylab | (p_ripple_10_30_x / p_ripple_10_30_y / p_ripple_time)) +
  plot_layout(widths = c(0.06, 0.94), heights = c(1, 1, 1.15)) +
  plot_annotation(
    title = "Ripple: Absolute Percent Differences Summary",
    theme = theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 16))
  )

fig_tripod <-
  (ylab | (p_tripod_10_30_x / p_tripod_10_30_y / p_tripod_time)) +
  plot_layout(widths = c(0.06, 0.94), heights = c(1, 1, 1.15)) +
  plot_annotation(
    title = "Tripod: Absolute Percent Differences Summary",
    theme = theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 16))
  )

fig_tvr <-
  (ylab | (p_tvr_x / p_tvr_y)) +
  plot_layout(widths = c(0.06, 0.94), heights = c(1, 1)) +
  plot_annotation(
    title = "Tripod vs Ripple: Absolute Percent Differences Summary",
    theme = theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 16))
  )

print(fig_ripple)
print(fig_tripod)
print(fig_tvr)

# =========================================
# Export (recommended)
# =========================================
# ggsave("fig_ripple_abs_pct.png", fig_ripple, width = 9, height = 10, dpi = 300)
# ggsave("fig_tripod_abs_pct.png", fig_tripod, width = 9, height = 10, dpi = 300)
# ggsave("fig_tripod_vs_ripple_abs_pct.png", fig_tvr, width = 9, height = 7, dpi = 300)
